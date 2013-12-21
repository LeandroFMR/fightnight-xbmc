# -*- coding: utf-8 -*-

""" Gato Fedorento
    2013 fightnight"""

import xbmc, xbmcgui, xbmcaddon, xbmcplugin,re,sys, urllib, urllib2,time,datetime

versao = '0.0.03'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
addon_id = 'plugin.video.gatofedorento'
art = '/resources/art/'
selfAddon = xbmcaddon.Addon(id=addon_id)
tvporpath = selfAddon.getAddonInfo('path')
mensagemok = xbmcgui.Dialog().ok
menuescolha = xbmcgui.Dialog().select
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
#PATH = "XBMC_G"
#UATRACK="UA-39199007-1"

if selfAddon.getSetting('ga_visitor')=='':
    from random import randint
    selfAddon.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))

def menu_principal():
#    GA("None","menuprincipal")
    if selfAddon.getSetting("mensagemfb") == "true":
            ok = mensagemok('wareztuga.tv','Faz like na pagina do facebook para','obteres todas as novidades.','http://fb.com/fightnightxbmc')
            selfAddon.setSetting('mensagemfb',value='false')
    addDir("Séries Completas",'nada',2,tvporpath + art + '',1,True)
    addDir("Sketchs Soltos",'nada',4,tvporpath + art + '',1,False)
    addDir("Procurar Vídeos",'nada',4,tvporpath + art + '',1,False)
    addDir("Quem são os Gato Fedorento?",'nada',4,tvporpath + art + '',1,False)
    addDir("",'',22,tvporpath + art + 'defs.png',1,False)
    disponivel=versao_disponivel()
    if disponivel==versao: addLink('Última versao (' + versao+ ')','',tvporpath + art + 'versao.png')
    else: addDir('Instalada v' + versao + ' | Actualização v' + disponivel,'nada',15,tvporpath + art + 'versao.png',1,False)
    addDir("Definições do addon",'',22,tvporpath + art + 'defs.png',1,False)

def abrir_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def versao_disponivel():
    try:
        link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.gatofedorento/addon.xml')
        match=re.compile('name="Gato Fedorento"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
    except:
        ok = mensagemok('Gato Fedorento','Addon não conseguiu conectar ao servidor','de actualização. Verifique a situação.','')
        match='Erro. Verificar origem do erro.'
    return match

def seriescompletas():
    nrcanais=30
    #GA("None","listacanais")
    addDir("Gato Fedorento: Série Fonseca (2003)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_fonseca.txt',3,tvporpath + art + '',1,False)
    addDir("Gato Fedorento: Série Meireles (2004)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_meireles.txt',3,tvporpath + art + '',1,False)
    addDir("Gato Fedorento: Série Barbosa (2005)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_barbosa.txt',3,tvporpath + art + '',1,False)    
    addDir("Gato Fedorento: Série Lopes da Silva (2006)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_lopesdasilva.txt',3,tvporpath + art + '',1,False)    
    addDir("Gato Fedorento: Diz que é uma Espécie de Magazine (2006)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_magazine.txt',3,tvporpath + art + '',1,False)
    addDir("Gato Fedorento: Zé Carlos (2008)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_zecarlos.txt',3,tvporpath + art + '',1,False)
    addDir("Gato Fedorento: Esmiúça os Sufrágios (2009)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_sufragios.txt',3,tvporpath + art + '',1,False)
    addDir("Gato Fedorento: MEO - Fora da Box (2011)",'http://fightnight-xbmc.googlecode.com/svn/gatofedorento/completas_foradabox.txt',3,tvporpath + art + '',1,False)
    
def request_servidores(url,name):
    titles=[]; ligacao=[]
    link=abrir_url(url)
    recolha=re.compile('----- (.+?) ---- (.+?) ---').findall(link)
    for titulo, endereco in recolha:
        titles.append(titulo)
        ligacao.append(endereco)
    print len(ligacao)
    if len(ligacao)==1: index=0
    elif len(ligacao)==0: ok=mensagemok('Gato Fedorento', 'Nenhum stream disponivel.'); return     
    else: index = menuescolha('Escolha a parte', titles)
    if index > -1:
        linkescolha=ligacao[index]
        if linkescolha:
            import urlresolver
            sources=[]
            hosted_media = urlresolver.HostedMediaFile(url=linkescolha)
            sources.append(hosted_media)
            source = urlresolver.choose_source(sources)
            if source:
                linkescolha=source.resolve()
                if linkescolha==False:
                    okcheck = xbmcgui.Dialog().ok
                    okcheck(traducao(40000),traducao(40019))
                    return
                comecarvideo(linkescolha,name)


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]                         
    return param

def comecarvideo(finalurl,name):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage='')
    listitem.setInfo("Video", {"Title":name})
    listitem.setProperty('IsPlayable', 'true')
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create('Gato Fedorento', 'A carregar')
    playlist.add(finalurl, listitem)
    dialogWait.close()
    del dialogWait
    if selfAddon.getSetting("playertype") == "0": player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    elif selfAddon.getSetting("playertype") == "1": player = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
    elif selfAddon.getSetting("playertype") == "2": player = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
    elif selfAddon.getSetting("playertype") == "3": player = xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER)
    else: player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    #GA("player",name)
    player.play(playlist)

def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 } )
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def clean(text):
    command={'\r':'','\n':'','\t':'','&nbsp;':''}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)

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
#checkGA()

params=get_params()
url=None
name=None
mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
    menu_principal()
elif mode==1: menu_principal()
elif mode==2: seriescompletas()
elif mode==3: request_servidores(url,name)
elif mode==4: ok = mensagemok('Gato Fedorento','Em actualização.')
elif mode==15: ok = mensagemok('Gato Fedorento','A actualizacao é automática. Caso nao actualize va ao','repositorio fightnight e prima c ou durante 2seg','e force a actualizacao. De seguida, reinicie o XBMC.')
elif mode==22: selfAddon.openSettings()
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
