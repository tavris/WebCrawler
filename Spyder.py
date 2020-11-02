import urllib.request, queue, Log, re;
from bs4 import BeautifulSoup;

class spyder:
	log = None;
	url = None;
	html2bs4 = None;

	maxDeep = 10;

	denyLinkList = [];
	visitdLinkList = [];
	taskQueue = queue.Queue();

	def __init__(self):
		self.log = Log.log('spyder');
		self.getDenyLink();
#		self.getVisitLink();
		pass;

	def Log(self, msg):
		self.log.log(self.url, msg);

	def getDenyLink(self, path = 'data/info/denyList.url'):
		try:
			f = open(path, mode='r', encoding='utf-8');
			for line in f.readline():	self.denyLinkList.append(line);
			f.close();
		except Exception as e:
			print(e);
			pass;

	def setURL(self, url):
		cleanURL = re.sub('(http:|https:|\/\/)', '', url);
		if(url[0] == '/'):
			self.url = self.url.split('/')[0] + cleanURL;
		else:
			self.url = 'http://' + cleanURL;

	def setMaxDeep(self, deep):	self.maxDeep = deep;

	def getWeb(self):
		req = None;
		try:
			with urllib.request.urlopen(self.url) as f:
				req = f.read().decode(''+f.headers.get_content_charset());
			self.html2bs4 = BeautifulSoup(req, 'html.parser');
			self.visitdLinkList.append(self.url);
		except Exception as e:
			return False;
		return True;

	def searchLink(self):
		self.Log("* Search Link.");
		for link in self.html2bs4.find_all("a"):
			if('href' in link.attrs):
				linkURL = re.sub('(http:|https:|\/\/)', '', link.attrs['href']);
				if( self.isVisitedLink(linkURL) and self.isDenyLink(linkURL) and self.notLink(linkURL) ):	# 방문한 주소와 방문 금지한 주소를 확인하고 작업큐에 저장
					self.Log("- Append Link Queue : %s" % linkURL);
					self.taskQueue.put(linkURL);
				else:	self.Log("- Deny/Visited Link : %s" % linkURL);

	def isVisitedLink(self, url):
		if(url in self.visitdLinkList):	return False;
		else:	return True;

	def isDenyLink(self, url):
		if(url in self.denyLinkList):	return False;
		else:	return True;

	def notLink(self, url):
		if(len(url) > 0):
			if(re.match('(#|javascript)', url) != None):	return False;
			elif(url[0] == '\\' or url[0] == ''):	return False;
			elif(url[0] == '/' and len(url) == 1):	return False;
			else:	return True;
		else:	return False;

	def run(self):
		self.getWeb();
		self.searchLink();

		while(not self.taskQueue.empty()):
			self.setURL(self.taskQueue.get());
			self.getWeb();
			self.searchLink();

def main():
	sp = spyder();
	sp.setURL("http://news.kbs.co.kr/common/main.html");
	sp.run();
	pass;

if __name__ == '__main__':
	main();