import functions
import keytools
import update

import tempfile
import os
import random
import logging

dbpath = '/tmp/db/'
dbprefix = 'updates'
logfile = '/tmp/esetupd.log'

logging.basicConfig(
    filename = logfile,
    format = "%(asctime)s [%(levelname)s]: %(message)s",
    level = logging.DEBUG)


log = logging.getLogger()

log.warning('Start working.')
log.info('Loading keys.')
key = keytools.loadKey()
if not key or not keytools.checkKey(key[0], key[1]):
    log.warning('Walid key not found. Start searching new key.')
    keys = keytools.findKeys()
    for k in keys.keys():
        if keytools.checkKey(k, keys[k]):
            key = [k, keys[k]]
            keytools.saveKey(k, keys[k])
            log.info('New key found.')
            break
if not key:
    log.error('No walid key found. Terminating')
    raise Exception, 'Key not found'

functions.mkpath(dbpath + dbprefix)

log.info('Downloading VER file')
url = 'http://update.eset.com/eset_upd/update.ver'
tmpfhd, tmpfname = tempfile.mkstemp()
functions.downloadToFile(url, tmpfname)

log.debug('Unpacking VER file')
functions.unrar(tmpfname, dbpath, 'update_new.ver')
os.unlink(tmpfname)

updfile = open(dbpath + 'update_new.ver')
updates = update.parseUpdate(updfile.read())

host = random.choice(updates['HOSTS']['Other'])
log.debug('Selected host %s', host )

log.info('Start update checking and downloading')
for updfile in updates.keys():
    if not 'file' in updates[updfile]:
        continue
    if 'language' in updates[updfile] and not updates[updfile]['language'] in '1033,1049,1058':
        continue
    needdownload = False
    localfile = dbpath + dbprefix + '/' + os.path.basename(updates[updfile]['file'])
    url = host + updates[updfile]['file']
    if os.path.isfile(localfile):
        ver = update.getFileVer(localfile)
        if ver and ver != updates[updfile]['versionid']:
            needdownload = True
        elif int(updates[updfile]['size']) != os.path.getsize(localfile):
            needdownload = True
    else:
        needdownload = True
    if needdownload:
        functions.downloadToFile(url, localfile, key[0], key[1])
        log.warning('File %s downloaded', localfile)

os.unlink(dbpath + 'update_new.ver')

log.info('Saving VER file.')
verfile = open(dbpath + 'update.ver', 'wt') 
for updfile in updates.keys():
    if updfile == 'HOSTS':
        continue
    if 'language' in updates[updfile] and not updates[updfile]['language'] in '1033,1049,1058':
        continue
    verfile.write('[%s]\r\n' % updfile)
    for param in updates[updfile].keys():
        if param == 'file':
            val = dbprefix + '/' + os.path.basename(updates[updfile]['file'])
        else:
            val = updates[updfile][param]
        verfile.write('%s=%s\r\n' % (param, val))
verfile.close()
log.warning('Finished.')
