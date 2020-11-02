import os, argparse;
import urllib.request;
from bs4 import BeautifulSoup;

import spider;

global args;

def url2get(url, target='soup'):
	with urllib.request.urlopen(url) as f:
		req = f.read().decode(''+f.headers.get_content_charset());
	
	if(target == 'text'):	return req.text;
	elif(target == 'soup'):	return BeautifulSoup(req.text, 'html.parser');
	else:  return req.text;
	
def fingerPrint ():
	robots_text = url2get(url=args.site + "/robots.txt", target='text');
	print(robot_text);

def main():
    fingerPrint();

if __name__ == '__main__':
	parser = argparse.ArgumentParser();
	parser.add_argument("-site", "--site", dest="site", help="Base target site.", required=True);
	parser.add_argument("-ir", "--ignore_robots", dest="site", help="Base target site.");
	args = parser.parse_args();

	main();
