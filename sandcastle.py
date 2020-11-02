#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, commands, requests
from argparse import ArgumentParser

print """
   ____             __             __  __   
  / __/__ ____  ___/ /______ ____ / /_/ /__ 
 _\ \/ _ `/ _ \/ _  / __/ _ `(_-</ __/ / -_)
/___/\_,_/_//_/\_,_/\__/\_,_/___/\__/_/\__/ 
                                            
S3 bucket enumeration // release v1.2.4 // ysx

"""
targetStem = ""
inputFile = ""

parser = ArgumentParser()
parser.add_argument("-t", "--target", dest="targetStem",
                    help="Select a target stem name (e.g. 'shopify')", metavar="targetStem", required="True")
parser.add_argument("-v", dest="verbose", action='count', default=0,
                    help="Scanning verbosity")
parser.add_argument("-f", "--file", dest="inputFile",
                    help="Select a bucket permutation file (default: bucket-names.txt)", default="bucket-names.txt", metavar="inputFile")
args = parser.parse_args()

with open(args.inputFile, 'r') as f: 
    bucketNames = [line.strip() for line in f] 
    lineCount = len(bucketNames)

print "[*] Commencing enumeration of '%s', reading %i lines from '%s'." % (args.targetStem, lineCount, f.name)

for name in bucketNames:
	r = requests.head("http://%s%s.s3.amazonaws.com" % (args.targetStem, name))
	if args.verbose > 0:
		print "[.] {} Test bucket: {:>25} \"http://{}{}.s3.amazonaws.com\"".format(r.status_code, name, args.targetStem, name)

	if r.status_code != 404:
                # macOS, coming soon: os.system("notify Potential match found! %s%s: %s" % (args.targetStem, name, r.status_code))
		if args.verbose > 0:
			print "[+] Checking potential match: %s%s --> %s" % (args.targetStem, name, r.status_code)
			print "[.] Execute: /usr/bin/aws s3 ls s3://%s%s" % (args.targetStem, name)
		
		check = commands.getoutput("/usr/bin/aws s3 ls s3://%s%s" % (args.targetStem, name))
		print "[+] Found {}: {}".format(args.targetStem, check)
	else:
		sys.stdout.write('')

print "[*] Enumeration of '%s' buckets complete." % (args.targetStem)
# macOS, coming soon: os.system("notify Enumeration of %s buckets complete." % (args.targetStem))
