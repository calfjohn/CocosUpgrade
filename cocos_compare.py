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
import excopy
import cocos
import compare_diff
from argparse import ArgumentParser

UPGRADE_PATH = 'Upgrade'

def os_is_win32():
    return sys.platform == 'win32'


def os_is_mac():
    return sys.platform == 'darwin'

if __name__ == '__main__':
    parser = ArgumentParser(description='Generate prebuilt engine for Cocos Engine.')
    parser.add_argument('-s', dest='projPath', help='Your Project path')
    parser.add_argument('-d', dest='cocosPath', help='Origin source path of cocos2d-x your project based.')
    (args, unknown) = parser.parse_known_args()

    if len(unknown) > 0:
        print('unknown arguments: %s' % unknown)
        sys.exit(1)

    if not os.path.exists(args.projPath) or not os.path.exists(args.cocosPath):
        cocos.Logging.warning("> src or dst is not exists.")
        sys.exit(1)

    print('Receive arguments src:%s dst:%s' % (args.projPath, args.cocosPath))

    target_path = args.projPath + UPGRADE_PATH
    user_cocos_path = os.path.join(target_path, 'UserCocos2d')
    origin_cocos_path = os.path.join(target_path, 'OriginCocos2d')
    target_project_path = os.path.join(target_path, 'Target')

    if not os.path.exists(target_project_path):
        cocos.Logging.info("> Copy your project into %s ..." % target_path)
        excopy.copy_directory(args.projPath, target_project_path)
    
    src_cocos2d_path = os.path.join(args.projPath, 'cocos2d')
    if not os.path.exists(user_cocos_path):
        cocos.Logging.info("> Copy your cocos2d from %s into %s ..." % (src_cocos2d_path, user_cocos_path))
        excopy.copy_directory(src_cocos2d_path, user_cocos_path)

    if not os.path.exists(origin_cocos_path):
        cocos.Logging.info("> Copy origin cocos2d into %s ..." % user_cocos_path)
        excopy.append_x_engine(args.cocosPath, origin_cocos_path)

    diff_file = os.path.join(os.getcwd(), 'diff')
    if os.path.exists(diff_file):
        os.remove(diff_file)

    if os_is_mac():
        diff_tool = 'diffmerge.sh'
    else:
        diff_tool = 'sgdm'

    cocos.Logging.info("> Preparing difference file %s ..." % diff_file)
    cmd = str.format('%s -diff %s %s %s' % (diff_tool, diff_file, user_cocos_path, origin_cocos_path))
    os.system(cmd)

    cocos.Logging.info("> Compare every single difference ...")
    compareFiles = compare_diff.CompareFiles(diff_file)
    compareFiles.compare(os.path.join(target_project_path, 'cocos2d'))
