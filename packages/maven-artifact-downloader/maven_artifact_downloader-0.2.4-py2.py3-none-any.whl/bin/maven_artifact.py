#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, Chris Schmidt <chris.schmidt () contrastsecurity.com>
#
# Built using https://github.com/hamnis/useful-scripts/blob/master/python/download-maven-artifact
# as a reference and starting point.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: maven_artifact
short_description: Downloads an Artifact from a Maven Repository
version_added: "2.0"
description:
    - Downloads an artifact from a maven repository given the maven coordinates provided to the module.
    - Can retrieve snapshots or release versions of the artifact and will resolve the latest available
      version if one is not available.
author: "Chris Schmidt (@chrisisbeef)"
requirements:
    - lxml
    - boto if using a S3 repository (s3://...)
'''

import hashlib
import os
import posixpath
import sys
import shutil
import io

try:
    from lxml import etree
    HAS_LXML_ETREE = True
except ImportError:
    HAS_LXML_ETREE = False

try:
    import boto3
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

try:
    IS_PYTHON2 = False
    from urllib.parse import urlparse
except ImportError:
    IS_PYTHON2 = True
    from urlparse import urlparse

from .request import Requestor,RequestException

class Artifact(object):
    def __init__(self, group_id, artifact_id, version, classifier='', extension='jar'):
        if not group_id:
            raise ValueError("group_id must be set")
        if not artifact_id:
            raise ValueError("artifact_id must be set")

        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.classifier = classifier

        if not extension:
            self.extension = "jar"
        else:
            self.extension = extension

    def is_snapshot(self):
        return self.version and self.version.endswith("SNAPSHOT")

    def path(self, with_version=True):
        base = posixpath.join(self.group_id.replace(".", "/"), self.artifact_id)
        if with_version and self.version:
            base = posixpath.join(base, self.version)
        return base

    def _generate_filename(self):
        filename = self.artifact_id + "-" + self.classifier + "." + self.extension
        if not self.classifier:
            filename = self.artifact_id + "." + self.extension
        return filename

    def get_filename(self, filename=None):
        if not filename:
            return self._generate_filename()

        filename = str(filename) if IS_PYTHON2 else filename
        if os.path.isdir(filename):
            filename = os.path.join(filename, self._generate_filename())
        return filename

    def __str__(self):
        result = "%s:%s:%s" % (self.group_id, self.artifact_id, self.version)
        if self.classifier:
            result = "%s:%s:%s:%s:%s" % (self.group_id, self.artifact_id, self.extension, self.classifier, self.version)
        elif self.extension != "jar":
            result = "%s:%s:%s:%s" % (self.group_id, self.artifact_id, self.extension, self.version)
        return result

    @staticmethod
    def parse(input):
        parts = input.split(":")
        if len(parts) >= 3:
            g = parts[0]
            a = parts[1]
            v = parts[len(parts) - 1]
            t = None
            c = None
            if len(parts) == 4:
                t = parts[2]
            if len(parts) == 5:
                t = parts[2]
                c = parts[3]
            return Artifact(g, a, v, c, t)
        else:
            return None


class MavenDownloader:
    def __init__(self, opts=dict(), base="http://repo1.maven.org/maven2", local=False):
        self.opts = opts
        if base.endswith("/"):
            base = base.rstrip("/")
        self.base = base
        self.local = local
        self.user_agent = "Maven Artifact Downloader/1.0"
        self.requestor = Requestor(opts['username'], opts['password'])
        self.latest_version_found = None
        self.metadata_file_name = "maven-metadata-local.xml" if local else "maven-metadata.xml"

    def find_latest_version_available(self, artifact):
        if self.latest_version_found:
            return self.latest_version_found
        path = "/%s/%s" % (artifact.path(False), self.metadata_file_name)
        content = self._getContent(self.base + path, "Failed to retrieve the maven metadata file: " + path)
        xml = etree.fromstring(content.read())
        v = xml.xpath("/metadata/versioning/versions/version[last()]/text()")
        if v:
            self.latest_version_found = v[0]
            return v[0]

    def find_uri_for_artifact(self, artifact):
        if artifact.version == "latest":
            artifact.version = self.find_latest_version_available(artifact)

        if artifact.is_snapshot():
            if self.local:
                return self._uri_for_artifact(artifact, artifact.version)
            path = "/%s/%s" % (artifact.path(), self.metadata_file_name)
            content = self._getContent(self.base + path, "Failed to retrieve the maven metadata file: " + path)
            xml = etree.fromstring(content.read())

            for snapshotArtifact in xml.xpath("/metadata/versioning/snapshotVersions/snapshotVersion"):
                classifier = snapshotArtifact.xpath("classifier/text()")
                artifact_classifier = classifier[0] if classifier else ''
                extension = snapshotArtifact.xpath("extension/text()")
                artifact_extension = extension[0] if extension else ''
                if artifact_classifier == artifact.classifier and artifact_extension == artifact.extension:
                    return self._uri_for_artifact(artifact, snapshotArtifact.xpath("value/text()")[0])
            timestamp_xmlpath = xml.xpath("/metadata/versioning/snapshot/timestamp/text()")
            if timestamp_xmlpath:
                timestamp = timestamp_xmlpath[0]
                build_number = xml.xpath("/metadata/versioning/snapshot/buildNumber/text()")[0]
                return self._uri_for_artifact(artifact, artifact.version.replace("SNAPSHOT", timestamp + "-" + build_number))

        return self._uri_for_artifact(artifact, artifact.version)

    def _uri_for_artifact(self, artifact, version=None):
        if artifact.is_snapshot() and not version:
            raise ValueError("Expected uniqueversion for snapshot artifact " + str(artifact))
        elif not artifact.is_snapshot():
            version = artifact.version
        if artifact.classifier:
            return posixpath.join(self.base, artifact.path(), artifact.artifact_id + "-" + version + "-" + artifact.classifier + "." + artifact.extension)

        return posixpath.join(self.base, artifact.path(), artifact.artifact_id + "-" + version + "." + artifact.extension)

    # for small files, directly get the full content
    def _getContent(self, url, failmsg, force=True):
        if self.local:
            parsed_url = urlparse(url)
            if os.path.isfile(parsed_url.path):
                with io.open(parsed_url.path, 'rb') as f:
                    return f.read()
            if force:
                raise ValueError(failmsg + " because can not find file: " + url)
            return None
        response = self._request(url, failmsg, force)
        if response:
            return response
        return None

    # only for HTTP request
    def _request(self, url, failmsg, force=True):
        url_to_use = url
        parsed_url = urlparse(url)

        if parsed_url.scheme == 's3':
            parsed_url = urlparse(url)
            bucket_name = parsed_url.netloc
            key_name = parsed_url.path[1:]
            client = boto3.client('s3', aws_access_key_id=self.opts['username'], aws_secret_access_key=self.opts['password'])
            url_to_use = client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': key_name}, ExpiresIn=10)

        req_timeout = self.opts['timeout']

        sys.stdout.write('Downloading from ' + url_to_use + '...\n')
        response = self.requestor.request(url_to_use, lambda r: r)
        if response:
            sys.stdout.write('Downloaded ' + url_to_use + '\n')
            return response
        if force:
            raise ValueError(failmsg + " because of " + response.reason + " for URL " + url_to_use)
        return None

    def download(self, artifact, verify_download, filename=None):
        filename = artifact.get_filename(filename)
        filename = str(filename) if IS_PYTHON2 else filename
        if not artifact.version or artifact.version == "latest":
            artifact = Artifact(artifact.group_id, artifact.artifact_id, self.find_latest_version_available(artifact),
                                artifact.classifier, artifact.extension)
        url = self.find_uri_for_artifact(artifact)
        if self.local:
            parsed_url = urlparse(url)
            if os.path.isfile(parsed_url.path):
                shutil.copy2(parsed_url.path, filename)
            else:
                return "Can not find local file: " + parsed_url.path
        else:
            response = self._request(url, "Failed to download artifact " + str(artifact))
            filename = filename if type(filename) is str else filename.decode('utf-8')
            with io.open(filename, 'wb') as f:
                self._write_chunks(response, f, report_hook=self.chunk_report)
        if verify_download:
            invalid_md5 = self.is_invalid_md5(filename, url)
            if invalid_md5:
                # if verify_change was set, the previous file would be deleted
                os.remove(filename)
                return invalid_md5
        return None

    def chunk_report(self, bytes_so_far, chunk_size, total_size):
        percent = float(bytes_so_far) / total_size
        percent = round(percent * 100, 2)
        sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
                         (bytes_so_far, total_size, percent))
        if bytes_so_far >= total_size:
            sys.stdout.write('\n')

    def _write_chunks(self, response, filehandle, chunk_size=8192, report_hook=None):
        if IS_PYTHON2:
            total_size = response.info().getheader('Content-length').strip()
        else: 
            total_size = response.getheader('Content-Length').strip()
        total_size = int(total_size)
        bytes_so_far = 0

        while 1:
            chunk = response.read(chunk_size)
            bytes_so_far += len(chunk)

            if not chunk:
                break

            filehandle.write(chunk)
            if report_hook:
                report_hook(bytes_so_far, chunk_size, total_size)

        return bytes_so_far

    def is_invalid_md5(self, file, remote_url):
        sys.stdout.write('Checking md5 for file %s\n' % file)
        if os.path.exists(file):
            local_md5 = self._local_md5(file)
            if self.local:
                parsed_url = urlparse(remote_url)
                remote_md5 = self._local_md5(parsed_url.path)
            else:
                remote_md5 = self._getContent(remote_url + '.md5', "Failed to retrieve MD5", False)
                if(not remote_md5):
                    return "Cannot find md5 from " + remote_url
            if local_md5 == remote_md5.read():
                return None
            else:
                return "Checksum does not match: we computed " + str(local_md5) + "but the repository states " + str(remote_md5)

        return "Path does not exist: " + file

    def _local_md5(self, file):
        md5 = hashlib.md5()
        with io.open(file, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), ''):
                md5.update(chunk)
        return md5.hexdigest()
