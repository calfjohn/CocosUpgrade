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

patchMap = {
            '3.5': 'cocos35',
            '3.4': 'cocos34',
            '3.3': 'cocos33',
            '3.2': 'cocos32',
            '3.1.1': 'cocos311',
            '3.0': 'cocos30'
            }

def os_is_win32():
    return sys.platform == 'win32'


def os_is_mac():
    return sys.platform == 'darwin'


def get_project_tag(proj_path):
    file_path = os.path.join(proj_path, 'cocos2d/cocos/2d/cocos2d.cpp')
    if not os.path.exists(file_path):
        file_path = os.path.join(proj_path, 'cocos2d/cocos/cocos2d.cpp')
        if not os.path.exists(file_path):
            return None

    file_modifier = modify_file.FileModifier(file_path)
    version = file_modifier.findEngineVesion()
    return get_patch_by_version(version)


def get_patch_by_version(version):
    for key in patchMap:
        result = version.find(key)
        if result > -1:
            return patchMap[key]

    return None

if __name__ == '__main__':
    parser = ArgumentParser(description='Generate prebuilt engine for Cocos Engine.')
    parser.add_argument('-r', dest='repositoryPath', help='Repository in the server')
    parser.add_argument('-d', dest='projPath', help='Your Project path.')
    parser.add_argument('-n', dest='projName', help='New Project name')
    parser.add_argument('-v', dest='upgradeVersion', help='Engine version to be upgrade')
    (args, unknown) = parser.parse_known_args()

    if len(unknown) > 0:
        print('unknown arguments: %s' % unknown)
        sys.exit(1)

    if not os.path.exists(args.repositoryPath) or not os.path.exists(args.projPath):
        cocos.Logging.warning("> Repository or project is not exists.")
        sys.exit(1)

    print('Receive arguments respsitory:%s target:%s name:%s version:%s' % (args.repositoryPath, args.projPath, args.projName, args.upgradeVersion))

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

    diff_path = str.format("%s/diff" % target_project_path)
    if os.path.exists(diff_path):
        shutil.rmtree(diff_path)
    os.mkdir(diff_path)

    patch_tag = get_project_tag(target_project_path)
    upgrade_tag = get_patch_by_version(args.upgradeVersion)
    cmd = str.format("git format-patch %s..%s -o %s" % (patch_tag, upgrade_tag, patch_path))
    ret = subprocess.call(cmd, cwd=args.repositoryPath, shell=True)
    if ret != 0:
        sys.exit(1)

    if 0:
        diff_file = str.format('%s/upgrade.diff' % diff_path)
        cmd = str.format("touch %s" % diff_file)
        ret = subprocess.call(cmd, cwd=diff_path, shell=True)
        if ret != 0:
            sys.exit(1)

        for roots, dirs, files in os.walk(patch_path):
            for f in files:
                cmd = str.format("cat %s >> %s" % (os.path.join(roots, f), diff_file))
                ret = subprocess.call(cmd, cwd=patch_path, shell=True)
                if ret != 0:
                    sys.exit(1)

        cmd = str.format('sed -e \'s/HelloCpp/%s/g\' %s > %s/my.patch' % (args.projName, diff_file, diff_path))
        ret = subprocess.call(cmd, cwd=patch_path, shell=True)
        if ret != 0:
            sys.exit(1)

        # project_rename.replace_string(patch_path + '/0001-35.patch', 'HelloCpp', args.projName)
        cmd = str.format("git apply --reject -p 1 %s/my.patch" % diff_path)
        # cmd = str.format("git am --reject -p 1 %s/0001-34.patch" % patch_path)
        ret = subprocess.call(cmd, cwd=target_project_path, shell=True)
        if ret != 0:
            sys.exit(1)
    else:
        for roots, dirs, files in os.walk(patch_path):
            for f in files:
                cmd = str.format('sed -e \'s/HelloCpp/%s/g\' %s > %s'
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


    # cmd = ""
    # p = subprocess.Popen(cmd, cwd=args.repositoryPath)

