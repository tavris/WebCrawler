class log:
	path = './data/logs/';

	def __init__(self, subType):
		self.path = self.path + subType;
		pass;

	def writeNewLog(self, url, msg):
		f = open(self.path + '/' + url + '.logs', mode='wt', encoding='utf-8');
		f.write(msg + '\n');
		f.close();

	def writeAppendLog(self, url, msg):
		try:
			f = open(self.path + '/' + url + '.logs', mode='a+', encoding='utf-8');
			f.write(msg + '\n');
			f.close();
		except:
			self.writeNewLog(url, msg);
	
	def log(self, url, msg):
		url = url.replace('http://', '');
		url = url.replace('https://', '');
		fname = url.split('/')[0].replace('.', '_');
		self.writeAppendLog(fname, msg);