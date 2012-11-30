

def parseUpdate(verfileData):
    sections = verfileData.split('[')

    params = []
    for data in sections:
        if not data:
            continue
        params.append(data.split(']'))

    update = {}
    for data in params:
        strings = data[1].split('\r\n')
        update[data[0]] = {}
        for string in strings:
            if string:
                vals = string.split('=')            
                update[data[0]][vals[0]] = vals[1][:]
    ''' Filtering hosts lists ''' 
    for data in update['HOSTS']:
        hosts = update['HOSTS'][data].split(', ')
        filteredHosts = []
        for host in hosts:
            filteredHosts.append(host[4:host[11:].index('/')+11])
        update['HOSTS'][data] = filteredHosts
    return update

def getFileVer(filename):
    f = open(filename)
    verid = ''
    while True:
        s = f.readline()
        s = s.rstrip()
        if not s:
            break
        if 'versionid=' in s:
            p, verid = s.split('=')
            break
    return verid
