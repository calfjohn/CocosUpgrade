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
import modify_file
import shutil
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
    (args, unknown) = parser.parse_known_args()

    if len(unknown) > 0:
        print('unknown arguments: %s' % unknown)
        sys.exit(1)

    if not os.path.exists(args.projPath):
        cocos.Logging.warning("> Project is not exists.")
        sys.exit(1)

    print('Receive arguments target:%s' % args.projPath)

    # Apply rejected patch if it is not applied completely.
    cmd = 'find . -name \'*.rej\''
    ret = subprocess.check_output(cmd, cwd=args.projPath, shell=True)
    files = ret.split('\n')

    for rejectFile in files:
        originFile, extension = os.path.splitext(rejectFile)
        cmd = str.format("wiggle --replace %s %s" % (originFile, rejectFile))
        ret = subprocess.call(cmd, cwd=args.projPath, shell=True)

    cmd = 'find . -name \'*.porig\' | xargs rm -f'
    ret = subprocess.call(cmd, cwd=args.projPath, shell=True)

    cmd = 'find . -name \'*.rej\' | xargs rm -f'
    ret = subprocess.call(cmd, cwd=args.projPath, shell=True)