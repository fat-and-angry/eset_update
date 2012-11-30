import functions
import keytools
import update

import tempfile
import os
import random

dbpath = '../db/'
dbprefix = 'updates'

key = keytools.loadKey()
if not key or not keytools.checkKey(key[0], key[1]):
    print('Searching new keys')
    keys = keytools.findKeys()
    print keys
    for k in keys.keys():
        if keytools.checkKey(k, keys[k]):
            key = [k, keys[k]]
            keytools.saveKey(k, keys[k])
            break
if not key:
    raise Exception, 'Key not found'

print('downloading')
url = 'http://update.eset.com/eset_upd/update.ver'
tmpfhd, tmpfname = tempfile.mkstemp()
functions.downloadToFile(url, tmpfname)

print('unpack')
functions.unrar(tmpfname, dbpath, 'update_new.ver')

os.unlink(tmpfname)

updfile = open(dbpath + 'update_new.ver')
updates = update.parseUpdate(updfile.read())

host = random.choice(updates['HOSTS']['Other'])
print 'Selected host', host

functions.mkpath(dbpath + dbprefix)

for updfile in updates.keys():
    if not 'file' in updates[updfile]:
        continue
    if 'language' in updates[updfile] and not updates[updfile]['language'] in '1033,1049,1058':
        continue
    localfile = dbpath + dbprefix + '/' + os.path.basename(updates[updfile]['file'])
    url = host + updates[updfile]['file']
    if os.path.isfile(localfile):
        ver = update.getFileVer(localfile)
        if ver and ver != updates[updfile]['versionid']:
            print localfile, 'ver mismath'
            print updates[updfile]['versionid'], ver
            functions.downloadToFile(url, localfile, key[0], key[1])
        elif int(updates[updfile]['size']) != os.path.getsize(localfile):
            print localfile, 'size mismath'
            print updates[updfile]['size'], os.path.getsize(localfile)
            functions.downloadToFile(url, localfile, key[0], key[1])
    else:
        functions.downloadToFile(url, localfile, key[0], key[1])
        print localfile, 'downloaded'

verfile = open(dbpath + 'update.ver', 'wt') 
for updfile in updates.keys():
    if updfile == 'HOSTS':
        continue
    if 'language' in updates[updfile] and int(updates[updfile]['language'] in '1033,1049,1058'):
        continue
    verfile.write('[%s]\r\n' % updfile)
    for param in updates[updfile].keys():
        if param == 'file':
            val = dbprefix + '/' + os.path.basename(updates[updfile]['file'])
        else:
            val = updates[updfile][param]
        verfile.write('%s=%s\r\n' % (param, val))
verfile.close()
