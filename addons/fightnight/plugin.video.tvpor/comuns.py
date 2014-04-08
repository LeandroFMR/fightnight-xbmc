# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon, re,sys, urllib, urllib2,time,datetime,os

versao = '0.1.15'
user_agent = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'
addon_id = 'plugin.video.tvpor'
selfAddon = xbmcaddon.Addon(id=addon_id)
tvporpath = selfAddon.getAddonInfo('path')
mensagemok = xbmcgui.Dialog().ok
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
PATH = "XBMC_TVPOR"
UATRACK="UA-39199007-1"

def savefile(filename, contents):
    try:
        destination = os.path.join(pastaperfil,filename)
        fh = open(destination, 'wb')
        fh.write(contents)  
        fh.close()
    except: print "Nao gravou os temporarios de: %s" % filename

def openfile(filename):
    try:
        destination = os.path.join(pastaperfil, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu os temporarios de: %s" % filename
        return None

def abrir_url(url,erro=True):
    print "A fazer request normal de: " + url
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
    except urllib2.HTTPError, e:
        if erro==True:
            mensagemok('TV Portuguesa',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)))
            sys.exit(0)
    except urllib2.URLError, e:
        if erro==True:
            mensagemok('TV Portuguesa',"Erro na página.")
            sys.exit(0)

def abrir_url_cookie(url,erro=True):

    print "A fazer request com cookie de: " + url
    try:
        hdr = {'User-Agent': user_agent, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        req = urllib2.Request(url, headers=hdr)
        page = urllib2.urlopen(req)
        content = page.read()
        return content
    except urllib2.HTTPError, e:
        if erro==True:
            mensagemok('TV Portuguesa',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)))
            sys.exit(0)
    except urllib2.URLError, e:
        if erro==True:
            mensagemok('TV Portuguesa',"Erro na página.")
            sys.exit(0)

def abrir_url_tommy(url,referencia,form_data=None,erro=True):
    print "A fazer request tommy de: " + url
    from t0mm0.common.net import Net
    net = Net()
    try:
        if form_data==None:link = net.http_GET(url,referencia).content
        else:link= net.http_POST(url,form_data=form_data,headers=referencia).content.encode('latin-1','ignore')
        return link

    except urllib2.HTTPError, e:
        if erro==True:
            mensagemok('TV Portuguesa',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)))
            sys.exit(0)
    except urllib2.URLError, e:
        if erro==True:
            mensagemok('TV Portuguesa',"Erro na página.")
            sys.exit(0)

def limparcomentarioshtml(link,url_frame):
    print "A limpar: " + url_frame
    if re.search('Sporttv1-veetle-iframe',url_frame) or re.search('Sporttv2-veetle-iframe',url_frame):
        return link
    else:
        link=clean(link)
        htmlcomments=re.compile('<!--(?!<!)[^\[>].*?-->').findall(link)
        for comentario in htmlcomments:
            link=link.replace(comentario,'oioioioi')
        return link

def clean(text):
    command={'\r':'','\n':'','\t':'','&nbsp;':''}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)

def redirect(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    gurl=response.geturl()
    return gurl

def downloader(url,dest, mensagem="A fazer download...",useReq = False):
    dp = xbmcgui.DialogProgress()
    dp.create("TV Portuguesa",mensagem,'')

    if useReq:
        import urllib2
        req = urllib2.Request(url)
        req.add_header('Referer', 'http://wallpaperswide.com/')
        f       = open(dest, mode='wb')
        resp    = urllib2.urlopen(req)
        content = int(resp.headers['Content-Length'])
        size    = content / 100
        total   = 0
        while True:
            if dp.iscanceled(): 
                raise Exception("Canceled")                
                dp.close()

            chunk = resp.read(size)
            if not chunk:            
                f.close()
                break

            f.write(chunk)
            total += len(chunk)
            percent = min(100 * total / content, 100)
            dp.update(percent)       
    else:
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))

def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()

def horaportuguesa():
    dt  = datetime.datetime.now()
    dts = dt.strftime('%Y-%m-%d%%20%H:%M')
    return dts

def millis():
      import time as time_
      return int(round(time_.time() * 1000))

#################### GA #####################
    
def parseDate(dateString):
    try: return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except: return datetime.datetime.today() - datetime.timedelta(days = 1) #force update

def checkGA():
    secsInHour = 60 * 60
    threshold  = 2 * secsInHour
    now   = datetime.datetime.today()
    prev  = parseDate(selfAddon.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds
    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return
    selfAddon.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    
    
                    
def send_request_to_google_analytics(utm_url):
    try:
        req = urllib2.Request(utm_url, None,{'User-Agent':user_agent})
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = selfAddon.getSetting('ga_visitor')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + versao + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + versao + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + versao + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + versao + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
        if versionNumber < 12:
            if xbmc.getCondVisibility('system.platform.osx'):
                if xbmc.getCondVisibility('system.platform.atv2'):
                    log_path = '/var/mobile/Library/Preferences'
                else:
                    log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
            elif xbmc.getCondVisibility('system.platform.ios'):
                log_path = '/var/mobile/Library/Preferences'
            elif xbmc.getCondVisibility('system.platform.windows'):
                log_path = xbmc.translatePath('special://home')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+versao+'  =========================='
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = selfAddon.getSetting('ga_visitor')
        for build, PLATFORM in match:
            if re.search('12',build[0:2],re.IGNORECASE): 
                build="Frodo" 
            if re.search('11',build[0:2],re.IGNORECASE): 
                build="Eden" 
            if re.search('13',build[0:2],re.IGNORECASE): 
                build="Gotham" 
            print build
            print PLATFORM
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + versao + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
