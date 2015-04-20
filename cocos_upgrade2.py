#
# ----------------------------------------------------------------------------
# Upgrade the cocos2d engine to the specified version by a specified patch file
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
from argparse import ArgumentParser

UPGRADE_PATH = 'Upgrade'
REPLACE_NAME = 'HelloJs'

def os_is_win32():
    return sys.platform == 'win32'


def os_is_mac():
    return sys.platform == 'darwin'

if __name__ == '__main__':
    parser = ArgumentParser(description='Generate prebuilt engine for Cocos Engine.')
    parser.add_argument('-d', dest='projPath', help='Your Project path.')
    parser.add_argument('-n', dest='projName', help='Your Project name.')
    parser.add_argument('-p', dest='patchFile', help='The patch file path.')
    (args, unknown) = parser.parse_known_args()

    if len(unknown) > 0:
        print('unknown arguments: %s' % unknown)
        sys.exit(1)

    if not os.path.exists(args.projPath) or not os.path.exists(args.patchFile):
        cocos.Logging.warning("> Project is not exists.")
        sys.exit(1)

    print('Receive arguments target:%s name:%s patch:%s' % (args.projPath, args.projName, args.patchFile))

    target_project_path = args.projPath + UPGRADE_PATH
    if not os.path.exists(target_project_path):
        cocos.Logging.info("> Copy your project into %s ..." % target_project_path)
        excopy.copy_directory(args.projPath, target_project_path)

    diff_path = os.path.join(os.getcwd(), 'temp.diff')
    if os.path.exists(diff_path):
        os.remove(diff_path)

    # Creat a git repository if there is not a repository.
    cmd = "git init \n git add -A \n git commit -m \'Init project for cocos upgrade.\'"
    ret = subprocess.call(cmd, cwd=target_project_path, shell=True)
    # if ret != 0:
    #     sys.exit(1)

    cmd = str.format('sed -e \'s/%s/%s/g\' %s > %s'
                     % (REPLACE_NAME, args.projName, args.patchFile, diff_path))
    ret = subprocess.call(cmd, shell=True)
    if ret != 0:
        sys.exit(1)

    # Apply patch.
    cmd = str.format("git apply --reject -p 1 %s" % diff_path)
    ret = subprocess.call(cmd, cwd=target_project_path, shell=True)

    # Apply rejected patch if it is not applied completely.
    cmd = 'find . -name \'*.rej\''
    ret = subprocess.check_output(cmd, cwd=target_project_path, shell=True)
    files = ret.split('\n')

    for rejectFile in files:
        originFile, extension = os.path.splitext(rejectFile)
        cmd = str.format("wiggle --replace %s %s" % (originFile, rejectFile))
        ret = subprocess.call(cmd, cwd=target_project_path, shell=True)

    # Remove .porig file created by wiggle
    cmd = 'find . -name \'*.porig\' | xargs rm -f'
    ret = subprocess.call(cmd, cwd=target_project_path, shell=True)

    # Compare reject file with orgine
    cmd = 'find . -name \'*.rej\' | xargs rm -f'
    ret = subprocess.call(cmd, cwd=target_project_path, shell=True)

    # Commit all changes.
    cmd = str.format("git add -A \n git commit -m \'cocos upgrade\'")
    ret = subprocess.call(cmd, cwd=target_project_path, shell=True)
    if ret != 0:
        sys.exit(1)