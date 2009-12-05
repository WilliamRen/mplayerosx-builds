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
import os
from os import path
import sys
import re

import datetime
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

USERNAME = "stefano"
MPLAYER_EXEC = "/Users/%s/dev/mplayer-build/mplayer/mplayer" % USERNAME
LIB_DIRS = ["/usr/local","/opt/local"]
PKG_DIR = "/Users/%s/dev" % USERNAME
PKG_NAME = "mplayer-pigoz.mpBinaries"
DSA_PRIV = "/Users/%s/dsa_priv.pem" % USERNAME

PKG_PRODUCT = path.join(PKG_DIR, PKG_NAME)
BUNDLED_LIBS_DIR = path.join(PKG_PRODUCT, 'Contents/MacOS/lib')
BUNDLED_MPLAYER_EXEC = path.join(PKG_PRODUCT, 'Contents/MacOS/mplayer')
BUNDLED_PLIST_FILE = path.join(PKG_PRODUCT, 'Contents/Info.plist')

def exec_cmd(command):
	subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def exec_cmd_with_result(command):
	result = subprocess.Popen( ["-c", command ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
	return re.sub("\n$", "", result.communicate()[0])

def install_name_tool():
	"""Runs install_name_tool on mplayer with path BUNDLED_MPLAYER_EXEC 
	and on the libraries in the lib/ directory"""
	bundled_libs_dir=os.listdir(BUNDLED_LIBS_DIR)
	for libname in bundled_libs_dir:
		for libdir in LIB_DIRS:
			exec_cmd('install_name_tool -change "%s/lib/%s" "@executable_path/lib/%s" "%s"' % (libdir, libname, libname, BUNDLED_MPLAYER_EXEC))
			exec_cmd('install_name_tool -id "@executable_path/lib/%s" "%s"' % (libname, path.join(BUNDLED_LIBS_DIR, libname)))
			
			for libname2 in bundled_libs_dir:
				exec_cmd('install_name_tool -change "%s/lib/%s" "@executable_path/lib/%s" "%s"' % (libdir, libname, libname, path.join(BUNDLED_LIBS_DIR, libname2)))
				
def strip():
	"""Strips the mplayer executable and the libraries"""
	exec_cmd('strip -x "%s"' % BUNDLED_MPLAYER_EXEC)
	bundled_libs_dir=os.listdir(BUNDLED_LIBS_DIR)
	for libname in bundled_libs_dir:
		exec_cmd('strip -x "%s"' % path.join(BUNDLED_LIBS_DIR, libname))
		
def time_to_version(time):
	return time.strftime("%Y%m%d")

def time_to_strversion(time):
	return time.strftime("%Y-%m-%d")

def time_to_filename(time):
	return 'mplayer-%s.zip' % time_to_strversion(time)

def plist(time):
	return """<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
		<key>CFBundleName</key>
		<string>mplayer.git</string>
		<key>MPEBinaryDescription</key>
		<string>Bleeding edge version of the mplayer binary compiled with ffmpeg-mt, newest libass available and ordered chapters support. x86_64 and Snow Leopard only.</string>
		<key>MPEBinaryMaintainer</key>
		<string>Stefano Pigozzi</string>
		<key>MPEBinaryHomepage</key>
		<string>http://code.google.com/p/mplayerosx-builds/</string>
		<key>MPEBinarySVNRevisionEquivalent</key>
		<string>29971</string>
		<key>CFBundleVersion</key>
		<string>%s</string>
		<key>CFBundleShortVersionString</key>
		<string>%s</string>
		<key>CFBundleIdentifier</key>
		<string>com.google.code.mplayerosx-builds.git</string>
		<key>CFBundleExecutable</key>
		<string>mplayer</string>
		<key>CFBundleInfoDictionaryVersion</key>
		<string>6.0</string>
		<key>SUFeedURL</key>
		<string>http://mplayerosx-builds.googlecode.com/hg/sparkle/appcast.xml</string>
		<key>SUPublicDSAKeyFile</key>
		<string>dsa_pub.pem</string>
		<key>LSBackgroundOnly</key>
		<integer>1</integer>
	</dict>
	</plist>""" % (time.strftime("%Y%m%d"), time.strftime("%Y-%m-%d"))
	
def write_plist(time):
	f = open(BUNDLED_PLIST_FILE, 'w')
	f.write(plist(time))
	f.close()

def appcast(time, dsa, length):
	return """<?xml version="1.0" encoding="utf-8"?>
	<rss version="2.0" xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle"  xmlns:dc="http://purl.org/dc/elements/1.1/">
	   <channel>
	      <title>mplayer.git Binary Distribution Changelog</title>
	      <link>http://mplayerosx-builds.googlecode.com/hg/sparkle/appcast.xml</link>
	      <description>Most recent changes with links to updates.</description>
	      <language>en</language>
	         <item>
	           <title>Version %s</title>
							<sparkle:releaseNotesLink>
								http://mplayerosx-builds.googlecode.com/hg/sparkle/rnotes/%s.html
							</sparkle:releaseNotesLink>
	           <pubDate>%s</pubDate>
	           <enclosure url="http://mplayerosx-builds.googlecode.com/files/%s" sparkle:version="%s" sparkle:shortVersionString="%s" sparkle:dsaSignature="%s" length="%s" type="application/octet-stream" />
	        </item>
	   </channel>
	</rss>""" % (time_to_strversion(time), time_to_strversion(time), time.strftime("%a, %d %b %Y %H:%M:%S +0000"), time_to_filename(time), time_to_version(time), time_to_strversion(time), dsa, length)

def main():
	print("Copying mplayer binary to the package directory...")
	exec_cmd("cp %s %s" % (MPLAYER_EXEC, \
		path.join(PKG_PRODUCT, 'Contents/MacOS/mplayer')))
	
	print("Changing libraries linking path...")
	install_name_tool()
	print("Stripping mplayer binary and libraries...")
	strip()
	
	now = datetime.datetime.utcnow()
	
	print("Writing new version number to Info.plist...")
	write_plist(now)
	print("Zipping %s to %s..." % (PKG_NAME, time_to_filename(now)))
	exec_cmd("cd %s && rm %s" % (PKG_DIR, time_to_filename(now)))
	exec_cmd("cd %s && zip -rq %s %s" % (PKG_DIR, time_to_filename(now), PKG_NAME+"/"))

	print("Preparing appcast.xml...")
	dsa = exec_cmd_with_result("openssl dgst -sha1 -binary < %s | openssl dgst -dss1 -sign %s | openssl enc -base64" % (path.join(PKG_DIR, time_to_filename(now)), DSA_PRIV))
	length = os.stat(path.join(PKG_DIR, time_to_filename(now))).st_size
	print appcast(now, dsa, length)

if __name__ == '__main__':
	main()

