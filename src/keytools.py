import urllib2
import re
import functions


def findKeys():
    url = 'http://www.google.com/search?num=100&q=nod32+EAV-*+OR+AV-*&hl=en&safe=off&as_qdr=w'
    
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0')
    req.add_header('Accept', 'text/html')
    
    u = urllib2.urlopen(req)
    page = u.read()
    
    
    # Bug in HTMLParser on server
    #===========================================================================
    # page = functions.remove_tags(page)
    #===========================================================================

    keys = {}
    
    result = re.finditer(r'(eav-|av-)(\d+)', page, flags=re.IGNORECASE)
    for match in result:
        match_pass = re.search(match.group() + r'.{0,10}password:* *([a-z0-9]{10})', page, flags=re.IGNORECASE)
        if match_pass == None:
            continue
        password = re.search(r'password:* *([a-z0-9]{10})', match_pass.group(), flags=re.IGNORECASE)
        keys[match.group()] = password.group()[-10:]
    return keys


def checkKey(username, password):
    url = 'http://update.eset.com/v3-rel-stop/mod_000_loader/em000_32_l0.nup'
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'ESS Update (Windows; U; 32bit; VDB 12606; BPC 4.2.40.10; OS: 5.1.2600 SP 3.0 NT; TDB 12606; CH 1.0; LNG 1049; x32c; UPD http://nod.malbi.dp.ua; APP eavbe; BEO 1; CPU 1356; ASP 0.10; FW 0.0; PX 0; PUA 1)')
    try:
        u = urllib2.urlopen(req)
        u.read()
        return True
    except IOError, e:
        if e.code == 401:
            return False
        else:
            raise EnvironmentError('Undefined problem! Error %i' % e.code)

def saveKey(username, password):
    f = open('keys', 'wt')
    f.write('%s %s' % (username, password))
    f.close()

def loadKey():
    try:
        f = open('keys', 'rt')
        s = f.readline()
    except IOError:
        s = ''
    return s.split()
