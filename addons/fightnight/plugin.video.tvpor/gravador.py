# -*- coding: utf-8 -*-
import xbmc,xbmcaddon,xbmcgui,re,datetime, time,os,sys

user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
selfAddon = xbmcaddon.Addon(id='plugin.video.tvpor')
tvporpath = selfAddon.getAddonInfo('path')
downloadPath = selfAddon.getSetting('pastagravador')
gravadorpath = os.path.join(selfAddon.getAddonInfo('path'),'resources','gravador')

def verifica_so(args,nomecanal,siglacanal,directo):
    #correrdump(args,nomecanal,'windows',siglacanal,directo)
    if selfAddon.getSetting('rtmpdumpalternativo')=='':
        if xbmc.getCondVisibility('system.platform.windows'): correrdump(args,nomecanal,'windows',siglacanal,directo)
        elif xbmc.getCondVisibility('system.platform.osx'): correrdump(args,nomecanal,'osx',siglacanal,directo)
        elif xbmc.getCondVisibility('system.platform.linux'): correrdump(args,nomecanal,'linux',siglacanal,directo)
    else: correrdump(args,nomecanal,'alternativo',siglacanal,directo)
        
    
def correrdump(args,nomecanal,pathso,siglacanal,directo):
    import subprocess
    from datetime import timedelta
    info=infocanal(siglacanal)
    escolha=0 #### inicializador
    if info!=False and directo!='listas': escolha=listadeprogramas(info) #### se ha programacao, mostra lista
    if escolha==0:
        if info!=False and directo!='listas': #### ha programacao
            fimprograma=calculafinalprograma(info)
            minutosrestantes=fimprograma / 60
            opcao= xbmcgui.Dialog().yesno("TV Portuguesa", 'Faltam ' + str(minutosrestantes) + ' minutos para o fim do programa', "Deseja gravar o resto do programa ou", "definir um tempo de gravação?",'Definir tempo', 'Gravar restante')
            if opcao==1:
                if selfAddon.getSetting("acrescentogravacao") == "0": segundos=fimprograma
                elif selfAddon.getSetting("acrescentogravacao") == "1": segundos=fimprograma+120
                elif selfAddon.getSetting("acrescentogravacao") == "2": segundos=fimprograma+300
                elif selfAddon.getSetting("acrescentogravacao") == "3": segundos=fimprograma+600
                else: segundos=fimprograma + 120
                minutos=segundos/60
            else:
                minutos = -1
                while minutos < 1: minutos = int(xbmcgui.Dialog().numeric(0,"Num de minutos de gravacao"))
                segundos=minutos*60
        else:
            minutos = -1
            while minutos < 1: minutos = int(xbmcgui.Dialog().numeric(0,"Num de minutos de gravacao"))
            segundos=minutos*60
        nomecanal = limpar(re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  nomecanal))
        horaactual=horaportuguesa(False)
        print downloadPath
        if pathso=='alternativo': caminhodump=selfAddon.getSetting("localizacaortmpdump")
        else: caminhodump=os.path.join(gravadorpath,pathso,'rtmpdump')
        argumentos=args + ' -o "' + downloadPath + horaactual + ' - ' + nomecanal + '.flv" -B ' + str(segundos)
        print caminhodump
        print argumentos
        try:
            #proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if xbmc.getCondVisibility('system.platform.windows'):
                proc = subprocess.Popen(argumentos, executable=caminhodump + '.exe', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                cmd = '"%s" %s' % (caminhodump, argumentos)
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print "RTMPDump comecou a funcionar"
            xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Gravação de "+str(minutos)+" minutos iniciou,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
            (stdout, stderr) = proc.communicate()
            print "RTMPDump parou de funcionar"
            stderr = normalize(stderr)
            if u'Download complete' in stderr:
                print 'stdout: ' + str(stdout)
                print 'stderr: ' + str(stderr)
                print "Download Completo!"
                xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Gravação efectuada com sucesso,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
            else:
                print 'stdout: ' + str(stdout)
                print 'stderr: ' + str(stderr)
                print "Download Falhou!"
                xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Gravação falhou,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
        except Exception:
            print ("Nao conseguiu abrir o programa")
            xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Erro ao abrir programa de gravação,'10000'," + tvporpath + "/resources/art/icon32-ver1.png)")
            (etype, value, traceback) = sys.exc_info()
            print "Erro etype: " + str(etype)
            print "Erro valor: " + str(value)
            print "Erro traceback: " + str(traceback)

def infocanal(siglacanal):
    if siglacanal=='SEM':
        print "Canal sem programacao."
        return False
    try:
        dia=horaportuguesa(True)
        diaseguinte=horaportuguesa('diaseguinte')
        url='http://services.sapo.pt/EPG/GetChannelListByDateInterval?channelSiglas='+siglacanal+'&startDate=' + dia +':01&endDate='+ diaseguinte + ':02'
        link=clean(abrir_url(url))
        return link
    except:
        print "Nao conseguiu capturar programacao."
        return False

def listadeprogramas(link):
    titles=[]
    ligacao=[]
    ref=int(0)
    programas=re.compile('<Title>(.+?)</Title>.+?<StartTime>.+?-.+?-(.+?) (.+?):(.+?):.+?</StartTime>').findall(link)
    for nomeprog,dia, horas,minutos in programas:
        ref=ref+1
        if dia==datetime.datetime.now().strftime('%d'): dia='Hoje'
        else: dia='Amanhã'
        if ref!=1: pass# titles.append('[COLOR red]' + dia + ' ' + horas + ':' + minutos + ' - ' +nomeprog + '[/COLOR]')
        else: titles.append(dia + ' ' + horas + ':' + minutos + ' - ' +nomeprog)
        ligacao.append('')
    index = xbmcgui.Dialog().select('Escolha o programa a gravar', titles)
    return index
        
        
    

def calculafinalprograma(link):
    fim=re.compile('<EndTime>(.+?)-(.+?)-(.+?) (.+?):(.+?):.+?</EndTime>').findall(link)[0]
    agora=horaportuguesa(False)
    inicio=re.compile('(.+?)-(.+?)-(.+?) (.+?)-(.+?)-').findall(agora)[0]
    start = datetime.datetime(year=int(inicio[0]), month=int(inicio[1]), day=int(inicio[2]), hour=int(inicio[3]), minute=int(inicio[4]))
    end = datetime.datetime(year=int(fim[0]), month=int(fim[1]), day=int(fim[2]), hour=int(fim[3]), minute=int(fim[4]))
    diff = end - start
    segundos= (diff.microseconds + (diff.seconds + diff.days * 24 * 3600) * 10**6) / 10**6
    return segundos

def normalize(text):
    if isinstance(text, str):
        try:
            text = text.decode('utf8')
        except:
            try:
                text = text.decode('latin1')
            except:
                text = text.decode('utf8', 'ignore')
    import unicodedata
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')

def horaportuguesa(sapo):
    dt  = datetime.datetime.now()
    if sapo==True:dts = dt.strftime('%Y-%m-%d%%20%H:%M')
    elif sapo=='diaseguinte': dts = dt.strftime('%Y-%m-') + str(int(dt.strftime('%d')) + 1) +dt.strftime('%%20%H:%M')
    else: dts = dt.strftime('%Y-%m-%d %H-%M-%S')
    return dts

def limpar(text):
    command={'(':'- ',')':''}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)

def abrir_url(url):
    print "A fazer request de: " + url
    import urllib2
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def clean(text):
    command={'\r':'','\n':'','\t':'','&nbsp;':''}
    regex = re.compile("|".join(map(re.escape, command.keys())))
    return regex.sub(lambda mo: command[mo.group(0)], text)
