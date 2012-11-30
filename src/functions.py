import rarfile
import urllib2
import os

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def remove_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def unrar(rarFileName, path, filename=''):
    if (rarfile.is_rarfile(rarFileName)):
        rarFile = rarfile.RarFile(rarFileName)
        for f in rarFile.infolist():
            if not filename:
                filename = f.filename
            targetFile = open(path + filename, 'wb')
            targetFile.write(rarFile.read(f))
            targetFile.close()
    else:
        raise ValueError("File %s is not RAR file" % rarFileName)

def download(url, username='', password=''):
    if username != '':
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, username, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0')
    u = urllib2.urlopen(req)
    blockSize = 8192
    gbuffer = ''
    while True:
        buffer = u.read(blockSize)
        if not buffer:
            break
        gbuffer += buffer
    return gbuffer

def downloadToFile(url, filename, username = '', password = ''):
    f = open(filename, 'w')
    f.write(download(url, username, password))
    f.close()

def mkpath(path):
    dirs = os.path.abspath(path).split('/')
    fdir = ''
    for dir in dirs:
        if dir:
            fdir += '/' + dir
            if os.path.exists(fdir):
                continue
            else:
                os.mkdir(fdir)
                
