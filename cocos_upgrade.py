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
import modify_file
import modify_template
import dowload_engine
from argparse import ArgumentParser

UPGRADE_PATH = 'Upgrade'

def os_is_win32():
    return sys.platform == 'win32'


def os_is_mac():
    return sys.platform == 'darwin'

if __name__ == '__main__':
    parser = ArgumentParser(description='Generate prebuilt engine for Cocos Engine.')
    parser.add_argument('-s', dest='projPath', help='Your Project path.')
    parser.add_argument('-d', dest='cocosPath', help='Latest cocos engine paths')
    (args, unknown) = parser.parse_known_args()

    if len(unknown) > 0:
        print('unknown arguments: %s' % unknown)
        sys.exit(1)

    print('Receive arguments src:%s dst:%s' % (args.projPath, args.cocosPath))

    if not os.path.exists(args.projPath) or not os.path.exists(args.cocosPath):
        cocos.Logging.warning("> src or dst is not exists.")
        sys.exit(1)

    target_path = args.projPath + UPGRADE_PATH
    target_project_path = os.path.join(target_path, 'Target')
    if not os.path.exists(target_project_path):
        cocos.Logging.info("> Copy your project into %s ..." % target_path)
        excopy.copy_directory(args.projPath, target_project_path)

    cocos.Logging.info("> Copying cocos2d from engine directory ...")
    des_cocos2d_path = os.path.join(target_project_path, 'cocos2d')
    excopy.remove_directory(des_cocos2d_path)
    excopy.append_x_engine(args.cocosPath, des_cocos2d_path)

    tempPath, filename = os.path.split(args.projPath)
    proj_file_path = os.path.join(target_project_path, 'proj.win32/%s.vcxproj' % filename)
    cocos.Logging.info("> Modifing visual studio project for win32 ... ")
    modify_template.modify_win32(proj_file_path)

    if os_is_mac():
        tempPath, filename = os.path.split(args.projPath)
        proj_file_path = os.path.join(target_project_path, 'proj.ios_mac/%s.xcodeproj/project.pbxproj' % filename)
        cocos.Logging.info("> Modifing xcode project for iOS&Mac ... ")
        modify_template.modify_mac_ios(proj_file_path)

    mk_file_path = os.path.join(target_project_path, 'proj.android/jni/Android.mk')
    cocos.Logging.info("> Modifing mk file for Android ...")
    modify_template.modify_android(mk_file_path)

    modify_file_path = os.path.join(target_project_path, 'proj.android/project.properties')
    fileModifier = modify_file.FileModifier(modify_file_path)
    fileModifier.replaceString('../cocos2d/cocos/platform/android/java', '../cocos2d/cocos/2d/platform/android/java')
    fileModifier.save()

    if os_is_mac():
        modify_file_path = os.path.join(target_project_path, 'proj.ios_mac/ios/AppController.mm')
        fileModifier = modify_file.FileModifier(modify_file_path)
        fileModifier.replaceString('platform/ios/CCEAGLView-ios.h', 'CCEAGLView.h')
        fileModifier.replaceString('GLViewImpl::create', 'GLView::create')
        fileModifier.save()

        modify_file_path = os.path.join(target_project_path, 'proj.ios_mac/ios/RootViewController.mm')
        fileModifier = modify_file.FileModifier(modify_file_path)
        fileModifier.replaceString('platform/ios/CCEAGLView-ios.h', 'CCEAGLView.h')
        fileModifier.save()

    modify_file_path = os.path.join(target_project_path, 'Classes/AppDelegate.cpp')
    fileModifier = modify_file.FileModifier(modify_file_path)
    fileModifier.replaceString('GLViewImpl::create', 'GLView::create')
    fileModifier.save()

    manifest_file_path = os.path.join(target_project_path, 'proj.android/AndroidManifest.xml')
    modify_template.modify_manifest(manifest_file_path)