#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  Copyright 2020 LINE Corporation
# 
#  LINE Corporation licenses this file to you under the GNU License,
#  version 3.0 (the "License"); you may not use this file except in compliance
#  with the License.

import argparse
import os
import posixpath

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

from maven_artifact import MavenDownloader, Artifact

def split_pre_existing_dir(dirname):
    '''
    Return the first pre-existing directory and a list of the new directories that will be created.
    '''
    head, tail = os.path.split(dirname)
    b_head = bytearray(head, 'utf-8', 'strict')
    if not os.path.exists(b_head):
        (pre_existing_dir, new_directory_list) = split_pre_existing_dir(head)
    else:
        return head, [tail]
    new_directory_list.append(tail)
    return pre_existing_dir, new_directory_list


def adjust_recursive_directory_permissions(pre_existing_dir, new_directory_list, module, directory_args, changed):
    '''
    Walk the new directories list and make sure that permissions are as we would expect
    '''
    if new_directory_list:
        working_dir = os.path.join(pre_existing_dir, new_directory_list.pop(0))
        directory_args['path'] = working_dir
        changed = module.set_fs_attributes_if_different(directory_args, changed)
        changed = adjust_recursive_directory_permissions(working_dir, new_directory_list, module, directory_args, changed)
    return changed

def main():
    # get arguments
    psr = argparse.ArgumentParser()
    psr.add_argument('--repository_url', default='https://repo1.maven.org/maven2')
    psr.add_argument('--group_id', required=True)
    psr.add_argument('--artifact_id', required=True)
    psr.add_argument('--version', default='latest')
    psr.add_argument('--classifier', default='')
    psr.add_argument('--extension', default='jar')
    psr.add_argument('--username', default='')
    psr.add_argument('--password', default='')
    psr.add_argument('--user_agent', default=None)
    psr.add_argument('--state', choices=["present", "absent"], default='present')
    psr.add_argument('--timeout', default=10)
    psr.add_argument('--dest', default='')
    psr.add_argument('--validate_certs', default=True)
    psr.add_argument('--keep_name', default=False)
    psr.add_argument('--verify_checksum', default='download', choices=['never', 'download', 'change', 'always'])
    args = psr.parse_args()

    if not HAS_LXML_ETREE:
        raise ValueError('module requires the lxml python library installed on the managed machine')

    try:
        parsed_url = urlparse(args.repository_url)
    except AttributeError as e:
        raise ValueError('url parsing went wrong %s' % e)

    is_local = parsed_url.scheme == "file"

    if parsed_url.scheme == 's3' and not HAS_BOTO:
        raise ValueError('boto3 required for this module, when using s3:// repository URLs')

    repository_url = args.repository_url
    group_id = args.group_id
    artifact_id = args.artifact_id
    version = args.version
    classifier = args.classifier
    extension = args.extension
    state = args.state
    dest = args.dest
    b_dest = bytearray(dest, 'utf-8', 'strict')
    keep_name = args.keep_name
    verify_checksum = args.verify_checksum
    verify_download = verify_checksum in ['download', 'always']
    verify_change = verify_checksum in ['change', 'always']

    downloader = MavenDownloader(
        dict(username=args.username, password=args.password, user_agent=args.user_agent, timeout=args.timeout), 
        repository_url, 
        is_local
    )

    try:
        artifact = Artifact(group_id, artifact_id, version, classifier, extension)
    except ValueError as e:
        raise ValueError(e.args[0])

    changed = False
    prev_state = "absent"

    if dest.endswith(os.sep):
        b_dest = bytearray(dest, 'utf-8', 'strict')
        if not os.path.exists(b_dest):
            (pre_existing_dir, new_directory_list) = split_pre_existing_dir(dest)
            os.makedirs(b_dest)
            directory_args = module.load_file_common_arguments(module.params)
            directory_mode = module.params["directory_mode"]
            if directory_mode is not None:
                directory_args['mode'] = directory_mode
            else:
                directory_args['mode'] = None
            changed = adjust_recursive_directory_permissions(pre_existing_dir, new_directory_list, module, directory_args, changed)

    dir = dest if IS_PYTHON2 else b_dest
    if os.path.isdir(dir):
        version_part = version
        if keep_name and version == 'latest':
            version_part = downloader.find_latest_version_available(artifact)

        if classifier:
            dest = posixpath.join(dest, "%s-%s-%s.%s" % (artifact_id, version_part, classifier, extension))
        else:
            dest = posixpath.join(dest, "%s-%s.%s" % (artifact_id, version_part, extension))
        b_dest = to_bytes(dest, errors='strict')

    if os.path.lexists(dir) and ((not verify_change) or not downloader.is_invalid_md5(dest, downloader.find_uri_for_artifact(artifact))):
        prev_state = "present"

    if prev_state == "absent":
        download_error = downloader.download(artifact, verify_download, b_dest)
        if download_error is None:
            changed = True
        else:
            raise ValueError("Cannot retrieve the artifact to destination: " + download_error)



if __name__ == '__main__':
    main()