#!/usr/bin/python

import getopt
import libxml2
import os
import sys
import urllib2

def download(url, output):
	resp = urllib2.urlopen(url)
	out = open(output, 'wb')
	out.write(resp.read())
	out.close()

def get_url(channel):
	api = 'http://dl.bukkit.org/api/1.0/downloads/projects/bukkit/view/latest-%s/?_accept=application/xml' % (channel)

	resp = urllib2.urlopen(api)
	xml = resp.read()

	doc = libxml2.parseDoc(xml.encode('UTF-8'))
	ctxt = doc.xpathNewContext()

	dlr = ctxt.xpathEval("/root/file/url")
	bnr = ctxt.xpathEval("/root/build_number")
	cnr = ctxt.xpathEval("/root/channel/name")

	dl = None
	bn = None
	cn = None

	if (len(dlr) > 0):
		dl = dlr[0].content
	if (len(bnr) > 0):
		bn = bnr[0].content
	if (len(cnr) > 0):
		cn = cnr[0].content

	doc.freeDoc()
	ctxt.xpathFreeContext()

	return (dl, bn, cn)

def main():
	channel = 'rb'
	output = None

	try:
		opts, args = getopt.getopt(sys.argv[1:], "c:h", ["channel=", "help"])
	except getopt.GetoptError:
		usage()

	if len(args) != 1:
		usage()

	output = args[0]

	for o, a in opts:
		if o in ("-c", "--channel"):
			channel = a
		if o in ("-h", "--help"):
			usage()

	print 'Downloading latest BUKKIT from [%s] channel to [%s]' % (channel, output)
	dl, bn, cn = get_url(channel)

	if not dl or not bn or not cn:
		print 'ERROR: unable to find artifact information'
		sys.exit(' ')

	print 'Found BUKKIT build [%s] from channel [%s]' % (bn, cn)
	print 'Downloading from [%s]' % (dl)

	download(dl, output)

	print 'COMPLETE'

def usage():
	print 'Get latest Bukkit JAR'
	print ''
	print 'Downloads the latest Bukkit artifact JAR.'
	print 'Usage:'
	print '  get-bukkit.py [-c|--channel <channel>] <output>'
	print '  get-bukkit.py [-h|--help]'
	sys.exit(' ')

if __name__ == "__main__":
	main();
