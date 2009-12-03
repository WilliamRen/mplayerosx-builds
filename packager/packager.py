#!/usr/bin/env python
# encoding: utf-8
"""
packager.py

Created by Stefano Pigozzi on 2009-12-03.
Copyright (c) 2009 Stefano Pigozzi. All rights reserved.

This script helps to package up a Mach-O binary of mplayer.git
into an .mpBinaries application bundle. Info.plist is updated
automatically, and a new appcast is created based on the package's
DSA signature.

"""

import sys
import os
from os import path
import subprocess

USERNAME = "stefano"
MPLAYER_EXEC = "/Users/%s/dev/mplayer-build/mplayer/mplayer" % USERNAME
PKG_PRODUCT = "/Users/%s/dev/mplayer-pigoz.mpBinaries" % USERNAME
LIB_DIRS = ["/usr/local","/opt/local"]
BUNDLED_LIBS_DIR = path.join(PKG_PRODUCT, 'Contents/MacOS/lib')
BUNDLED_MPLAYER_EXEC = path.join(PKG_PRODUCT, 'Contents/MacOS/mplayer')

def exec_cmd(command):
	subprocess.call(command, shell=True)

def install_name_tool():
	"""Runs install_name_tool on mplayer with path BUNDLED_MPLAYER_EXEC 
	and on the libraries in the lib/ directory"""
	bundled_libs_dir=os.listdir(BUNDLED_LIBS_DIR)
	for libname in bundled_libs_dir:
		for libdir in LIB_DIRS:
			exec_cmd('install_name_tool -change "%s/lib/%s" "@executable_path/lib/%s" "%s"' % (libdir, libname, libname, BUNDLED_MPLAYER_EXEC))
			exec_cmd('install_name_tool -id "@executable_path/lib/%s" "%s"' % (libname, BUNDLED_LIBS_DIR))
			
			for libname2 in bundled_libs_dir:
				exec_cmd('install_name_tool -change "%s/lib/%s" "@executable_path/lib/%s" "%s"' % (libdir, libname, libname, path.join(BUNDLED_LIBS_DIR, libname2)))
				
def strip():
	"""Strips the mplayer executable and the libraries"""
	exec_cmd('strip -x "%s"' % BUNDLED_MPLAYER_EXEC)
	bundled_libs_dir=os.listdir(BUNDLED_LIBS_DIR)
	for libname in bundled_libs_dir:
		exec_cmd('strip -x "%s"' % path.join(BUNDLED_LIBS_DIR, libname))

def main():
	exec_cmd("cp %s %s" % (MPLAYER_EXEC, \
							path.join(PKG_PRODUCT, 'Contents/MacOS/mplayer')))
	
	install_name_tool()
	strip()

if __name__ == '__main__':
	main()

