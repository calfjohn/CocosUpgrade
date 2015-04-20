#
# ----------------------------------------------------------------------------
# Upgrade the cocos2d engine to the specified version.
#
# Copyright 2015 (C) lijun
#
# License: MIT
# ----------------------------------------------------------------------------

import os
import sys
import cocos
import excopy
import subprocess
import modify_file
import shutil
from argparse import ArgumentParser

UPGRADE_PATH = 'Upgrade'

#'3.0', '3.1.1', '3.2', '3.3',
patchList = ['3.3rc2', '3.4', '3.5']
# patchMap = {
#             '3.4': '0005-35.patch',
#             '3.3': '0004-34.patch',
#             '3.2': '0003-33.patch',
#             '3.1.1': '0002-32.patch',
#             '3.0': '0001-311.patch'
#             }

patchMap = {
            '3.5': '2lua35-36.diff',
            '3.4': '1lua34-35.diff',
            '3.3rc2': '0lua33rc2-34.diff',
            '3.3': '0004-34.patch',
            '3.2': '0003-33.patch',
            '3.1.1': '0002-32.patch',
            '3.0': '0001-311.patch'
            }

def os_is_win32():
    return sys.platform == 'win32'


def os_is_mac():
    return sys.platform == 'darwin'

def get_project_version(proj_path):
    file_path = os.path.join(proj_path, 'cocos2d/cocos/2d/cocos2d.cpp')
    if not os.path.exists(file_path):
        file_path = os.path.join(proj_path, 'cocos2d/cocos/cocos2d.cpp')
        if not os.path.exists(file_path):
            file_path = os.path.join(proj_path, 'frameworks/cocos2d-x/cocos/2d/cocos2d.cpp')
            if not os.path.exists(file_path):
                file_path = os.path.join(proj_path, 'frameworks/cocos2d-x/cocos/cocos2d.cpp')
                if not os.path.exists(file_path):
                    return None

    file_modifier = modify_file.FileModifier(file_path)
    version = file_modifier.findEngineVesion()
    return get_key_by_version(version)


def get_key_by_version(version):
    for key in patchMap:
        result = version.find(key)
        if result > -1:
            return key

    return None

if __name__ == '__main__':
    parser = ArgumentParser(description='Generate prebuilt engine for Cocos Engine.')
    parser.add_argument('-d', dest='projPath', help='Your Project path.')
    parser.add_argument('-n', dest='projName', help='Your Project name.')
    parser.add_argument('-v', dest='upgradeVersion', help='Engine version to be upgrade.')
    (args, unknown) = parser.parse_known_args()

    if len(unknown) > 0:
        print('unknown arguments: %s' % unknown)
        sys.exit(1)

    if not os.path.exists(args.projPath):
        cocos.Logging.warning("> Project is not exists.")
        sys.exit(1)

    print('Receive arguments target:%s name:%s version:%s' % (args.projPath, args.projName, args.upgradeVersion))

    target_project_path = args.projPath + UPGRADE_PATH
    if not os.path.exists(target_project_path):
        cocos.Logging.info("> Copy your project into %s ..." % target_project_path)
        excopy.copy_directory(args.projPath, target_project_path)

    # Creat a git repository if there is not a repository
    cmd = "git init \n git add -A \n git commit -m \'Init project for cocos upgrade.\'"
    ret = subprocess.call(cmd, cwd=target_project_path, shell=True)
    # if ret != 0:
    #     sys.exit(1)

    patch_path = str.format("%s/patch" % target_project_path)
    if os.path.exists(patch_path):
        shutil.rmtree(patch_path)
    os.mkdir(patch_path)

    diff_path = str.format("%s/diff" % target_project_path)
    if os.path.exists(diff_path):
        shutil.rmtree(diff_path)
    os.mkdir(diff_path)

    temp_find = False
    patch_tag = get_project_version(target_project_path)
    for i in patchList:
        if patch_tag == i:
            temp_find = True
        if args.upgradeVersion == i:
            break
        if temp_find:
            patch_file = os.path.join(os.getcwd(), 'patch', patchMap[i])
            shutil.copy(patch_file, patch_path)

    for roots, dirs, files in os.walk(patch_path):
        for f in files:
            cmd = str.format('sed -e \'s/HelloLua/%s/g\' %s > %s'
                             % (args.projName, os.path.join(roots, f), os.path.join(diff_path, f)))
            ret = subprocess.call(cmd, cwd=patch_path, shell=True)
            if ret != 0:
                sys.exit(1)

    for roots, dirs, files in os.walk(diff_path):
        for f in files:
            cmd = str.format("git apply --reject -p 1 %s" % os.path.join(roots, f))
            ret = subprocess.call(cmd, cwd=target_project_path, shell=True)

            cmd = str.format("git add -A \n git commit -m \'%s\'" % f)
            ret = subprocess.call(cmd, cwd=target_project_path, shell=True)
            if ret != 0:
                sys.exit(1)
