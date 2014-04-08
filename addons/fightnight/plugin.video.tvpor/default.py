# -*- coding: utf-8 -*-

""" TV Portuguesa
    2014 fightnight"""

import xbmc, xbmcgui, xbmcaddon, xbmcplugin,re,sys, urllib, urllib2,time,datetime,os,socket
import zumba,comuns

versao = '0.1.15'
VBURL= 'http://www.videosbacanas.com/'
user_agent = 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'
addon_id = 'plugin.video.tvpor'
art = '/resources/art/'
selfAddon = xbmcaddon.Addon(id=addon_id)
tvporpath = selfAddon.getAddonInfo('path')
mensagemok = xbmcgui.Dialog().ok
menuescolha = xbmcgui.Dialog().select
mensagemprogresso = xbmcgui.DialogProgress()
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
downloadPath = selfAddon.getSetting('pastagravador')
pleasewait='Por favor aguarde. '
socket.setdefaulttimeout(1000)

if selfAddon.getSetting('ga_visitor')=='':
    from random import randint
    selfAddon.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))

def entraraddon():
    #buggalo_fix114()
    if selfAddon.getSetting("mensagemlibrtmp2") == "false": ok = mensagemok('TV Portuguesa','[B][COLOR red]IMPORTANTE! Nova actualização LIBRTMP.[/COLOR][/B]','Visite http://bit.ly/fightnightaddons para mais informacoes.','Mensagem: 23 de Junho')
   
    try:
        req = urllib2.Request('http://google.pt')
        req.add_header('User-Agent', user_agent)
        req.add_header("pragma", "no-cache")
        response = urllib2.urlopen(req)
        print "Com acesso a internet"
        resultado=True
    except:
        print "Sem acesso a internet"
        resultado=False

    if resultado==True:
        try:
            dbverdisp=int(comuns.abrir_url('http://fightnight-xbmc.googlecode.com/svn/tvpor/db_ver.txt'))
            if int(zumba.dbver()) < dbverdisp:
                filecheck=os.path.join(tvporpath, 'zumba.py')
                try:os.remove(filecheck)
                except: pass
                comuns.downloader('http://fightnight-xbmc.googlecode.com/svn/tvpor/zumba.py',filecheck,mensagem="A actualizar módulos...")
        except: xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Não conseguiu actualizar modulos. Verifique situação,'100000'," + tvporpath + art + "icon32-ver1.png)")
        if selfAddon.getSetting("abrirlogolista") == "false": menu_principal()
        else: abrir_lista_canais()
    else:
        opcao= xbmcgui.Dialog().yesno('TV Portuguesa', 'Sem acesso à internet.', "", "",'Voltar a tentar', 'OK')
        if not opcao: entraraddon()
        else:
            addDir("Reconectar Addon",'nada',18,tvporpath + art + 'restart-ver2.png',1,'',True)
            addDir("Definições do addon",'nada',22,tvporpath + art + 'defs-ver2.png',1,'',False)
            xbmc.executebuiltin("Container.SetViewMode(500)")


def menu_principal():
    comuns.GA("None","menuprincipal")
    addDir("Ver Canais",'nada',13,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    if xbmc.getCondVisibility('system.platform.linux') or xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.osx'):
        addDir('Ver Gravações','nada',12,tvporpath + art + 'gravador-ver1.png',1,'Aceda à lista das gravações já efectuadas',False)
    disponivel=versao_disponivel()
    if disponivel==versao: addLink('Última versao (' + versao+ ')','',tvporpath + art + 'versao-ver2.png')
    else: addDir('Instalada v' + versao + ' | Actualização v' + disponivel,'nada',15,tvporpath + art + 'versao-ver2.png',1,'',False)
    addDir("Definições do addon",'nada',22,tvporpath + art + 'defs-ver2.png',1,'',False)
    addDir("[COLOR red][B]LER AVISO[/B][/COLOR]",'nada',23,tvporpath + art + 'aviso-ver2.png',1,'',False)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def versao_disponivel():            
    try:
        link=comuns.abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.tvpor/addon.xml')
        match=re.compile('name="TV Portuguesa"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
    except:
        ok = mensagemok('TV Portuguesa','Addon não conseguiu conectar ao servidor','de actualização. Verifique a situação.','')
        match='Erro. Verificar origem do erro.'
    return match

def listascanais():
    addDir("[B]Desporto[/B]",'http://dl.dropbox.com/u/74834278/Desporto.xml',5,tvporpath + art + 'ces-desp-ver1.png',1,'',True)
    addDir("[B]Música[/B]",'http://dl.dropboxusercontent.com/u/74834278/Musica.xml',5,tvporpath + art + 'ces-mus-ver1.png',1,'',True)
    addDir("[B]Ciências[/B]",'http://dl.dropbox.com/u/74834278/Tv%20Ciencia.xml',5,tvporpath + art + 'ces-ciencia-ver1.png',1,'',True)
    addDir("[B]Alemanha[/B]",'http://dl.dropboxusercontent.com/u/74834278/Tv%20Alema.xml',5,tvporpath + art + 'ces-alem-ver1.png',1,'',True)
    addDir("[B]Espanha[/B]",'http://dl.dropboxusercontent.com/u/74834278/Tv%20Espanhola.xml',5,tvporpath + art + 'ces-espa-ver1.png',1,'',True)
    addDir("[B]UK[/B]",'http://dl.dropboxusercontent.com/u/74834278/Tv%20UK.xml',5,tvporpath + art + 'ces-uk-ver1.png',1,'',True)
    addDir("[B]USA[/B]",'http://dl.dropboxusercontent.com/u/74834278/Tv%20USA.xml',5,tvporpath + art + 'ces-usa-ver1.png',1,'',True)
    addDir("[B]Global[/B]",'http://dl.dropbox.com/u/88295111/pissos13.xml',5,tvporpath + art + 'pissos-ver1.png',1,'',True)
    addDir("[B]Portugal[/B]",'http://dl.dropboxusercontent.com/s/h9s0oiop70tjwe8/TV%20PORTUGUESA.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    addDir("[B]Filmes[/B]",'http://dl.dropboxusercontent.com/s/kk79s083x208zug/xml%20pt%20tv%20-%20nova.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    addDir("[B]Infantil[/B]",'http://dl.dropboxusercontent.com/s/kbly079op7kwaz2/INFANTIL%20TV%20POR.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    addDir("[B]Brasil[/B]",'http://dl.dropboxusercontent.com/s/9ilbiv4d83dlcrr/TV%20BRASILEIRA%20POR.txt',5,tvporpath + art + 'vercanais-ver2.png',1,'',True)
    #addLink("",'',tvporpath + art + 'listas-ver2.png')
    
    addDir("[B][COLOR white]A tua lista aqui?[/COLOR][/B]",'nada',14,tvporpath + art + 'versao-ver2.png',1,'',False)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def obter_lista(name,url):
    comuns.GA("None",name)
    titles = []; ligacao = []; thumb=[]
    link=comuns.abrir_url(url)
    link2=comuns.clean(link)
    listas=re.compile('<title>(.+?)</title>(.+?)<thumbnail>(.+?)</thumbnail>').findall(link2)
    for nomecanal,streams,thumbcanal in listas:
        streams2=re.compile('<link>(.+?)</link>').findall(streams)
        for rtmp in streams2:
#            if re.search('$doregex',rtmp):
#                #parametros=re.compile('<regex></regex>').findall(rtmp)
#                doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(rtmp)
#                    for k in doRegexs:
#                    
#                        if k in regexs:
#                            m = regexs[k]
#                            #if m['page'] in cachedPages:
#                            #    link = cachedPages[m['page']]
#                            #else:
#                            page=re.compile('<page>(.+?)</page>').findall(streams2)[0]
#                            req = urllib2.Request(page)
#                            req.add_header('User-Agent', user_agent)
#                            if re.search('<referer>',streams2):
#                                referer=re.compile('<referer>(.+?)</referer>').findall(streams2)[0]
#                                req.add_header('Referer', referer)
#                            response = urllib2.urlopen(req)
#                            link = response.read()
#                            response.close()
#                            expres=re.compile("""<expres>'file':'([^']*)<expres>""").findall(streams2)[0]
#                            reg = re.compile(expres).search(link)
#                            rtmp = url.replace("$doregex[" + k + "]", reg.group(1).strip())
                        

            if name=='[B]Eventos[/B] (Cesarix/Rominhos)':
                titles.append(nomecanal)
                ligacao.append(rtmp)
                thumb.append(thumbcanal)
            else:
                addCanal(nomecanal,rtmp,17,thumbcanal,len(listas),'')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

                    
    if name=='[B]Eventos[/B] (Cesarix/Rominhos)':
        if len(ligacao)==1: index=0
        elif len(ligacao)==0: ok=mensagemok('TV Portuguesa', 'Sem eventos disponiveis.'); return     
        else:
            index = xbmcgui.Dialog().select('Escolha o servidor', titles)
            if index > -1:
                urlescolha=ligacao[index]
                nomecanal=titles[index]
                #thumb123=thumbcanal[index]
                #print thumb123
                zumba.comecarvideo(urlescolha,nomecanal,'listas',False,thumb=tvporpath + art + 'vercanais-ver2.png')

def abrir_lista_canais():
    zumba.info_servidores()
    canais()

#################### CAPTURA SERVERS ###############

def canais():
    nrcanais=49
    canaison=[]
    empty='nada'
    comuns.GA("None","listacanais")
    if selfAddon.getSetting("prog-lista3") == "true":
        mensagemprogresso.create('TV Portuguesa', '')
        mensagemprogresso.update(100,'A carregar listas de programação.',pleasewait)
        if mensagemprogresso.iscanceled(): sys.exit(0)
        programas=p_todos()
    else: programas=[]
    
    mensagemprogresso.close()
    
    #### GRAVADOR #####
    #if selfAddon.getSetting("gravadoractivar") == "true": colorgravador='[COLOR green]ON[/COLOR]'
    #else: colorgravador='[COLOR red]OFF[/COLOR]'
    #
    ##### PREVENCAO OUTROS OS NAO SUPORTADOS:
    #if xbmc.getCondVisibility('system.platform.linux') or xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.osx'):
    #    if selfAddon.getSetting("gravacoes") == "true": addDir('[B][COLOR white]Gravador[/COLOR] '+colorgravador+'[/B]','nada',12,tvporpath + art + 'gravador-ver1.png',1,'Aceda à lista das gravações já efectuadas',False)
    #else: selfAddon.setSetting('gravadoractivar',value='false')
    ##### FIM GRAVADOR #####
    if selfAddon.getSetting("abrirlogolista") == "true":
        if selfAddon.getSetting("abrirlogolista-botao") == "true": addDir("[B][COLOR white]Menu Principal[/COLOR][/B]",'nada',1,tvporpath + art + 'defs-ver2.png',1,'Clique aqui para voltar ao menu principal.',True)
    #if selfAddon.getSetting("restarttv") == "true": addDir("[B][COLOR white]Restart TV[/COLOR][/B]",'nada',2,tvporpath + art + 'restart-ver2.png',1,'Veja ou reveja os programas que já passaram na TV Portuguesa.',True)
    if selfAddon.getSetting("listas-pessoais") == "true": addDir("[B][COLOR white]Listas Pessoais[/COLOR][/B]",'nada',6,tvporpath + art + 'listas-ver2.png',1,'Outras listas de canais criadas pela comunidade.',True)
    #addDir("[B][COLOR white]Zapping[/COLOR][/B]",empty,16,tvporpath + art + 'zapp-ver1.png',nrcanais,'Com esta funcionalidade, pode utilizar a tecla » do seu comando e correr a lista de todos os canais comodamente.',False)
    if selfAddon.getSetting("alterarvista") == "true": addDir("[B][COLOR white]Alterar Vista[/COLOR][/B]",'nada',9,tvporpath + art + 'aviso-ver2.png',1,'Opção para alterar a vista da lista de canais.',False)
    #addDir("[B][COLOR red]TESTE[/COLOR][/B]",'nada',2013,'',1,'Para testes',False)

    if selfAddon.getSetting("eventos") == "true": canaison.append('[B]Eventos[/B]'); addCanal("[B]Eventos[/B] (Cesarix/Rominhos)",'http://dl.dropboxusercontent.com/u/266138381/Eventos.xml',11,tvporpath + art + 'vercanais-ver2.png',nrcanais,'')
    if selfAddon.getSetting("canais-rtp1") == "true": canaison.append('[B]RTP 1[/B]'); addCanal("[B]RTP 1[/B] " + p_umcanal(programas,'RTP1','nomeprog'),empty,16,tvporpath + art + 'rtp1-ver2.png',nrcanais,p_umcanal(programas,'RTP1','descprog'))
    if selfAddon.getSetting("canais-rtp2") == "true":  canaison.append('[B]RTP 2[/B]'); addCanal("[B]RTP 2[/B] " + p_umcanal(programas,'RTP2','nomeprog'),empty,16,tvporpath + art + 'rtp2-ver2.png',nrcanais,p_umcanal(programas,'RTP2','descprog'))
    if selfAddon.getSetting("canais-sic") == "true":  canaison.append('[B]SIC[/B]'); addCanal("[B]SIC[/B] " + p_umcanal(programas,'SIC','nomeprog'),empty,16,tvporpath + art + 'sic-ver3.png',nrcanais,p_umcanal(programas,'SIC','descprog'))
    if selfAddon.getSetting("canais-tvi") == "true":  canaison.append('[B]TVI[/B]'); addCanal("[B]TVI[/B] " + p_umcanal(programas,'TVI','nomeprog'),empty,16,tvporpath + art + 'tvi-ver2.png',nrcanais,p_umcanal(programas,'TVI','descprog'))
    if selfAddon.getSetting("canais-sporttv1") == "true":
        canaison.append('[B]SPORTTV 1[/B]'); addCanal("[B]SPORTTV 1[/B] " + p_umcanal(programas,'SPTV1','nomeprog'),empty,16,tvporpath + art + 'sptv1-ver2.png',nrcanais,p_umcanal(programas,'SPTV1','descprog'))
        canaison.append('[B]SPORTTV 1 HD[/B]'); addCanal("[B]SPORTTV 1 HD[/B] " + p_umcanal(programas,'SPTV1','nomeprog'),empty,16,tvporpath + art + 'sptvhd-ver2.png',nrcanais,p_umcanal(programas,'SPTV1','descprog'))
    if selfAddon.getSetting("canais-sporttv2") == "true": canaison.append('[B]SPORTTV 2[/B]'); addCanal("[B]SPORTTV 2[/B] " + p_umcanal(programas,'SPTV2','nomeprog'),empty,16,tvporpath + art + 'sptv2-ver2.png',nrcanais,p_umcanal(programas,'SPTV2','descprog'))
    if selfAddon.getSetting("canais-sporttv3") == "true": canaison.append('[B]SPORTTV 3[/B]'); addCanal("[B]SPORTTV 3[/B] " + p_umcanal(programas,'SPTV3','nomeprog'),empty,16,tvporpath + art + 'sptv3-ver2.png',nrcanais,p_umcanal(programas,'SPTV3','descprog'))
    if selfAddon.getSetting("canais-sporttvlive") == "true": canaison.append('[B]SPORTTV LIVE[/B]'); addCanal("[B]SPORTTV LIVE[/B] " + p_umcanal(programas,'SPTVL','nomeprog'),empty,16,tvporpath + art + 'sptvlive-ver1.png',nrcanais,p_umcanal(programas,'SPTVL','descprog'))
    if selfAddon.getSetting("canais-benficatv") == "true": canaison.append('[B]Benfica TV[/B]'); addCanal("[B]Benfica TV[/B] " + p_umcanal(programas,'SLB','nomeprog'),empty,16,tvporpath + art + 'bentv-ver2.png',nrcanais,p_umcanal(programas,'SLB','descprog'))
    if selfAddon.getSetting("canais-portocanal") == "true": canaison.append('[B]Porto Canal[/B]'); addCanal("[B]Porto Canal[/B] " + p_umcanal(programas,'PORTO','nomeprog'),empty,16,tvporpath + art + 'pcanal-ver2.png',nrcanais,p_umcanal(programas,'PORTO','descprog'))
    if selfAddon.getSetting("canais-abolatv") == "true": canaison.append('[B]A Bola TV[/B]'); addCanal("[B]A Bola TV[/B] " + p_umcanal(programas,'ABOLA','nomeprog'),empty,16,tvporpath + art + 'abola-ver1.png',nrcanais,p_umcanal(programas,'ABOLA','descprog'))
    if selfAddon.getSetting("canais-cmtv") == "true": canaison.append('[B]CM TV[/B]'); addCanal("[B]CM TV[/B] " + p_umcanal(programas,'CMTV','nomeprog'),empty,16,tvporpath + art + 'cmtv-ver1.png',nrcanais,p_umcanal(programas,'CMTV','descprog'))    
    if selfAddon.getSetting("canais-rtpac") == "true": canaison.append('[B]RTP Açores[/B]'); addCanal("[B]RTP Açores[/B] " + p_umcanal(programas,'RTPAC','nomeprog'),empty,16,tvporpath + art + 'rtpac-ver1.png',nrcanais,p_umcanal(programas,'RTPAC','descprog'))
    if selfAddon.getSetting("canais-rtpaf") == "true": canaison.append('[B]RTP Africa[/B]'); addCanal("[B]RTP Africa[/B] " + p_umcanal(programas,'RTPA','nomeprog'),empty,16,tvporpath + art + 'rtpaf-ver1.png',nrcanais,p_umcanal(programas,'RTPA','descprog'))
    if selfAddon.getSetting("canais-rtpi") == "true": canaison.append('[B]RTP Informação[/B]'); addCanal("[B]RTP Informação[/B] " + p_umcanal(programas,'RTPIN','nomeprog'),empty,16,tvporpath + art + 'rtpi-ver1.png',nrcanais,p_umcanal(programas,'RTPIN','descprog'))
    if selfAddon.getSetting("canais-rtpint") == "true": canaison.append('[B]RTP Internacional[/B]'); addCanal("[B]RTP Internacional[/B] " + p_umcanal(programas,'RTPINT','nomeprog'),empty,16,tvporpath + art + 'rtpint-ver1.png',nrcanais,p_umcanal(programas,'RTPINT','descprog'))
    if selfAddon.getSetting("canais-rtpmad") == "true": canaison.append('[B]RTP Madeira[/B]'); addCanal("[B]RTP Madeira[/B] " + p_umcanal(programas,'RTPMD','nomeprog'),empty,16,tvporpath + art + 'rtpmad-ver1.png',nrcanais,p_umcanal(programas,'RTPMD','descprog'))
    if selfAddon.getSetting("canais-rtpmem") == "true": canaison.append('[B]RTP Memória[/B]'); addCanal("[B]RTP Memória[/B] " + p_umcanal(programas,'RTPM','nomeprog'),empty,16,tvporpath + art + 'rtpmem-ver1.png',nrcanais,p_umcanal(programas,'RTPM','descprog'))   
    if selfAddon.getSetting("canais-sick") == "true": canaison.append('[B]SIC K[/B]'); addCanal("[B]SIC K[/B] " + p_umcanal(programas,'SICK','nomeprog'),empty,16,tvporpath + art + 'sick-ver2.png',nrcanais,p_umcanal(programas,'SICK','descprog'))
    if selfAddon.getSetting("canais-sicmulher") == "true": canaison.append('[B]SIC Mulher[/B]'); addCanal("[B]SIC Mulher[/B] " + p_umcanal(programas,'SICM','nomeprog'),empty,16,tvporpath + art + 'sicm-ver3.png',nrcanais,p_umcanal(programas,'SICM','descprog'))
    if selfAddon.getSetting("canais-sicnoticias") == "true": canaison.append('[B]SIC Noticias[/B]'); addCanal("[B]SIC Noticias[/B] " + p_umcanal(programas,'SICN','nomeprog'),empty,16,tvporpath + art + 'sicn-ver2.png',nrcanais,p_umcanal(programas,'SICN','descprog'))
    if selfAddon.getSetting("canais-sicradical") == "true": canaison.append('[B]SIC Radical[/B]'); addCanal("[B]SIC Radical[/B] " + p_umcanal(programas,'SICR','nomeprog'),empty,16,tvporpath + art + 'sicrad-ver2.png',nrcanais,p_umcanal(programas,'SICR','descprog'))
    if selfAddon.getSetting("canais-tvi24") == "true": canaison.append('[B]TVI24[/B]'); addCanal("[B]TVI24[/B] " + p_umcanal(programas,'TVI24','nomeprog'),empty,16,tvporpath + art + 'tvi24-ver2.png',nrcanais,p_umcanal(programas,'TVI24','descprog'))
    if selfAddon.getSetting("canais-tvificcao") == "true": canaison.append('[B]TVI Ficção[/B]'); addCanal("[B]TVI Ficção[/B] " + p_umcanal(programas,'TVIFIC','nomeprog'),empty,16,tvporpath + art + 'tvif-ver2.png',nrcanais,p_umcanal(programas,'TVIFIC','descprog'))
    if selfAddon.getSetting("canais-maistvi") == "true": canaison.append('[B]Mais TVI[/B]'); addCanal("[B]Mais TVI[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'maistvi-ver2.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    if selfAddon.getSetting("canais-hollywood") == "true": canaison.append('[B]Hollywood[/B]'); addCanal("[B]Hollywood[/B] " + p_umcanal(programas,'HOLLW','nomeprog'),empty,16,tvporpath + art + 'hwd-ver2.png',nrcanais,p_umcanal(programas,'HOLLW','descprog'))
    if selfAddon.getSetting("canais-mov") == "true": canaison.append('[B]MOV[/B]'); addCanal("[B]MOV[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'mov-ver2.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    if selfAddon.getSetting("canais-axn") == "true": canaison.append('[B]AXN[/B]'); addCanal("[B]AXN[/B] " + p_umcanal(programas,'AXN','nomeprog'),empty,16,tvporpath + art + 'axn-ver2.png',nrcanais,p_umcanal(programas,'AXN','descprog'))
    if selfAddon.getSetting("canais-axnblack") == "true": canaison.append('[B]AXN Black[/B]'); addCanal("[B]AXN Black[/B] " + p_umcanal(programas,'AXNBL','nomeprog'),empty,16,tvporpath + art + 'axnb-ver2.png',nrcanais,p_umcanal(programas,'AXNBL','descprog'))
    if selfAddon.getSetting("canais-axnwhite") == "true": canaison.append('[B]AXN White[/B]'); addCanal("[B]AXN White[/B] " + p_umcanal(programas,'AXNWH','nomeprog'),empty,16,tvporpath + art + 'axnw-ver2.png',nrcanais,p_umcanal(programas,'AXNWH','descprog'))
    if selfAddon.getSetting("canais-fox") == "true": canaison.append('[B]FOX[/B]'); addCanal("[B]FOX[/B] " + p_umcanal(programas,'FOX','nomeprog'),empty,16,tvporpath + art + 'fox-ver2.png',nrcanais,p_umcanal(programas,'FOX','descprog'))
    if selfAddon.getSetting("canais-foxcrime") == "true": canaison.append('[B]FOX Crime[/B]'); addCanal("[B]FOX Crime[/B] " + p_umcanal(programas,'FOXCR','nomeprog'),empty,16,tvporpath + art + 'foxc-ver2.png',nrcanais,p_umcanal(programas,'FOXCR','descprog'))
    if selfAddon.getSetting("canais-foxlife") == "true": canaison.append('[B]FOX Life[/B]'); addCanal("[B]FOX Life[/B] " + p_umcanal(programas,'FLIFE','nomeprog'),empty,16,tvporpath + art + 'foxl-ver3.png',nrcanais,p_umcanal(programas,'FLIFE','descprog'))
    if selfAddon.getSetting("canais-foxmovies") == "true": canaison.append('[B]FOX Movies[/B]'); addCanal("[B]FOX Movies[/B] " + p_umcanal(programas,'FOXM','nomeprog'),empty,16,tvporpath + art + 'foxm-ver2.png',nrcanais,p_umcanal(programas,'FOXM','descprog'))
    if selfAddon.getSetting("canais-syfy") == "true": canaison.append('[B]Syfy[/B]'); addCanal("[B]Syfy[/B] " + p_umcanal(programas,'SYFY','nomeprog'),empty,16,tvporpath + art + 'syfy-ver1.png',nrcanais,p_umcanal(programas,'SYFY','descprog'))
    if selfAddon.getSetting("canais-disney") == "true": canaison.append('[B]Disney Channel[/B]'); addCanal("[B]Disney Channel[/B] " + p_umcanal(programas,'DISNY','nomeprog'),empty,16,tvporpath + art + 'disney-ver1.png',nrcanais,p_umcanal(programas,'DISNY','descprog'))
    if selfAddon.getSetting("canais-cpanda") == "true": canaison.append('[B]Canal Panda[/B]'); addCanal("[B]Canal Panda[/B] " + p_umcanal(programas,'PANDA','nomeprog'),empty,16,tvporpath + art + 'panda-ver2.png',nrcanais,p_umcanal(programas,'PANDA','descprog'))
    if selfAddon.getSetting("canais-pbiggs") == "true": canaison.append('[B]Panda Biggs[/B]'); addCanal("[B]Panda Biggs[/B] " + p_umcanal(programas,'BIGGS','nomeprog'),empty,16,tvporpath + art + 'pbiggs-ver1.png',nrcanais,p_umcanal(programas,'BIGGS','descprog'))
    if selfAddon.getSetting("canais-motors") == "true": canaison.append('[B]Motors TV[/B]'); addCanal("[B]Motors TV[/B] " + p_umcanal(programas,'MOTOR','nomeprog'),empty,16,tvporpath + art + 'motors-ver1.png',nrcanais,p_umcanal(programas,'MOTOR','descprog'))
    if selfAddon.getSetting("canais-discovery") == "true": canaison.append('[B]Discovery Channel[/B]'); addCanal("[B]Discovery Channel[/B] " + p_umcanal(programas,'DISCV','nomeprog'),empty,16,tvporpath + art + 'disc-ver2.png',nrcanais,p_umcanal(programas,'DISCV','descprog'))
    if selfAddon.getSetting("canais-odisseia") == "true": canaison.append('[B]Odisseia[/B]'); addCanal("[B]Odisseia[/B] " + p_umcanal(programas,'ODISS','nomeprog'),empty,16,tvporpath + art + 'odisseia-ver1.png',nrcanais,p_umcanal(programas,'ODISS','descprog'))
    if selfAddon.getSetting("canais-historia") == "true": canaison.append('[B]História[/B]'); addCanal("[B]História[/B] " + p_umcanal(programas,'HIST','nomeprog'),empty,16,tvporpath + art + 'historia-ver1.png',nrcanais,p_umcanal(programas,'HIST','descprog'))
    if selfAddon.getSetting("canais-ngc") == "true": canaison.append('[B]National Geographic Channel[/B]'); addCanal("[B]National Geographic Channel[/B] " + p_umcanal(programas,'NGC','nomeprog'),empty,16,tvporpath + art + 'natgeo-ver1.png',nrcanais,p_umcanal(programas,'NGC','descprog'))
    if selfAddon.getSetting("canais-eurosport") == "true": canaison.append('[B]Eurosport[/B]'); addCanal("[B]Eurosport[/B] " + p_umcanal(programas,'EURSP','nomeprog'),empty,16,tvporpath + art + 'eusp-ver2.png',nrcanais,p_umcanal(programas,'EURSP','descprog'))
    if selfAddon.getSetting("canais-espna") == "true": canaison.append('[B]ESPN America[/B]'); addCanal("[B]ESPN America[/B] " + p_umcanal(programas,'SEM','nomeprog'),empty,16,tvporpath + art + 'espna-ver1.png',nrcanais,p_umcanal(programas,'SEM','descprog'))
    if selfAddon.getSetting("canais-fashion") == "true": canaison.append('[B]Fashion TV[/B]'); addCanal("[B]Fashion TV[/B] " + p_umcanal(programas,'FASH','nomeprog'),empty,16,tvporpath + art + 'fash-ver1.png',nrcanais,p_umcanal(programas,'FASH','descprog'))
    if selfAddon.getSetting("canais-vh1") == "true": canaison.append('[B]VH1[/B]'); addCanal("[B]VH1[/B] " + p_umcanal(programas,'VH1','nomeprog'),empty,16,tvporpath + art + 'vh1-ver2.png',nrcanais,p_umcanal(programas,'VH1','descprog'))
    if selfAddon.getSetting("canais-mtv") == "true": canaison.append('[B]MTV[/B]'); addCanal("[B]MTV[/B] " + p_umcanal(programas,'MTV','nomeprog'),empty,16,tvporpath + art + 'mtv-ver1.png',nrcanais,p_umcanal(programas,'MTV','descprog'))
    try:
        canaison=''.join(canaison)      
        comuns.savefile(('canaison', canaison))
    except: pass
    xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

    #### KILL ####
    #xbmcplugin.endOfDirectory(int(sys.argv[1]))
    #sys.exit(0)
    ##############



    #xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    #xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )

'''
    #addCanal("[B]Disney Junior[/B] " + p_umcanal(programas,'DISNJ','nomeprog'),empty,16,tvporpath + art + 'djun-ver1.png',nrcanais,False)
    #addCanal("[B]ESPN[/B] " + p_umcanal(programas,'ESPN','nomeprog'),empty,16,tvporpath + art + 'espn-ver1.png',nrcanais,False)
    
    addCanal("[B]Chelsea TV[/B] " + p_umcanal(programas,'CHELS','nomeprog'),empty,16,'',nrcanais,False)
    addCanal("[B]Discovery Turbo[/B] " + p_umcanal(programas,'DISCT','nomeprog'),empty,16,'',nrcanais,False)
    addCanal("[B]Económico TV[/B] " + p_umcanal(programas,'ECONO','nomeprog'),empty,16,'',nrcanais,False)
    addCanal("[B]Eurosport 2[/B] " + p_umcanal(programas,'EURS2','nomeprog'),empty,16,'',nrcanais,False)
    addCanal("[B]Fuel TV[/B] " + p_umcanal(programas,'FUEL','nomeprog'),empty,16,'',nrcanais,False)
    addCanal("[B]Nickelodeon[/B] " + p_umcanal(programas,'NICK','nomeprog'),empty,16,'',nrcanais,False)
    addCanal("[B]SBT[/B] " + p_umcanal(programas,'SBT','nomeprog'),empty,16,'',nrcanais,False)
    addCanal("[B]TLC[/B] " + p_umcanal(programas,'TLC','nomeprog'),empty,16,'',nrcanais,False)
    addCanal("[B]TV Globo[/B] " + p_umcanal(programas,'GLOBO','nomeprog'),empty,16,'',nrcanais,False)
    addCanal("[B]TV Record[/B] " + p_umcanal(programas,'TVrec','nomeprog'),empty,16,'',nrcanais,False)
    #addCanal("[COLOR blue][B]Nr. de canais:[/B][/COLOR]" + nrcanais,'',16,'',nrcanais,False)
'''      

#################################### RESTART TV ##################
def restarttv():
    nrcanais=5
    comuns.GA("None","Restart TV")
    if selfAddon.getSetting("mensagemrestart") == "true":
            ok = mensagemok('TV Portuguesa','Serviço disponibilizado por Vídeos Bacanas.','Visita o site oficial.','http://www.videosbacanas.com/')
            selfAddon.setSetting('mensagemrestart',value='false')
    #addDir("[B]RTP[/B]","RTP",3,tvporpath + art + 'rtp1-ver2.png',nrcanais,'',True)
    #addDir("[B]SIC[/B]","SIC",3,tvporpath + art + 'sic-ver3.png',nrcanais,'',True)
    #addDir("[B]SIC Noticias[/B]","SIC Notícias",3,tvporpath + art + 'sicn-ver2.png',nrcanais,'',True)
    #addDir("[B]TVI[/B]","TVI",3,tvporpath + art + 'tvi-ver2.png',nrcanais,'',True)
    #addDir("[B]Outros[/B]","Entretenimento",3,tvporpath + art + 'listas-ver2.png',nrcanais,'',True)
    #addDir("[B]TVI24[/B]","TVI 24",3,tvporpath + art + 'tvi24-ver2.png',nrcanais,'',True)
    addDir("[B]Pesquisa[/B]","Pesquisa",10,tvporpath + art + 'pesquisa-ver2.png',nrcanais,'',True)
    restarttv_progs('',VBURL)
    #restarttv_dailymotionfix()
    #xbmc.executebuiltin("Container.SetViewMode(500)")

def restarttv_lista(name,url):
    comuns.GA("Restart TV",url)
    link=comuns.abrir_url(VBURL)
    link=comuns.clean(link)
    if url=="Entretenimento":
        restarttv_progs('Entretenimento',VBURL + 'category/entretenimento/')
    else:
        infocanal=re.compile('<a href="#">'+url+'</a><ul class="sub-menu">(.+?)</ul>').findall(link)[0]
        programas=re.compile('<li><a title=".+?" href="(.+?)">(.+?)</a></li>').findall(infocanal)
        for endereco,nomeprog in programas:
            addDir(nomeprog,endereco,4,tvporpath + art + 'restart-ver2.png',len(programas),'',True)

def restarttv_progs(name,url):
    link=comuns.clean(comuns.abrir_url(url))
    link=link.replace('&#8211;','-').replace('&#8216;','').replace('&#8217;','')
    progs=re.compile('src="(.+?)".+?<h2><a href="(.+?)" title="(.+?)">').findall(link)
    for thumb,endereco,nomeprog in progs:
        addDir(nomeprog,endereco,8,thumb,len(progs),'',False)
    restarttv_paginas(link)

def restarttv_dailymotionfix():
    if selfAddon.getSetting("dailymotionfix") == "true":
        try:
            print "A actualizar dailymotion"
            path = xbmc.translatePath(os.path.join('special://home/addons/script.module.urlresolver/lib/urlresolver/plugins',''))
            lib=os.path.join(path, 'dailymotion.py')
            os.remove(lib)
            urldaily = 'http://raw.github.com/the-one-/script.module.urlresolver/master/lib/urlresolver/plugins/dailymotion.py'
            comuns.downloader(urldaily,lib)
            selfAddon.setSetting('dailymotionfix',value='false')
        except: print "Erro ao actualizar dailymotion"

def buggalo_fix114():
    if selfAddon.getSetting("buggalofix") == "true":
        try:
            urlfusion='http://fightnight-xbmc.googlecode.com/svn/buggalo/script.module.buggalo.zip' #v1.1.4
            path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
            lib=os.path.join(path, 'script.module.buggalo.zip')
            comuns.downloader(urlfusion,lib)
            addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
            xbmc.sleep(2000)
            dp = xbmcgui.DialogProgress()
            dp.create("TV Portuguesa", "A instalar...")
            try:
                print "A extrair buggalo"
                import extract
                extract.all(lib,addonfolder,dp)
            except: print "Nao conseguiu extrair buggalo"
            selfAddon.setSetting('buggalofix',value='false')
        except: print "Erro ao actualizar buggalo"

def restarttv_sapo(name,link):
    dp = xbmcgui.DialogProgress()
    dp.create("A criar lista de vídeos",'Criando...')
    dp.update(0)
    playlist = xbmc.PlayList(1)
    playlist.clear()
    videoindividual=re.compile('<iframe src="http://videos.sapo.pt/playhtml.+?file=(.+?)"').findall(link)
    dp.create("TV Portuguesa",'Criando...')
    dp.update(0)
    for endvideo in videoindividual:
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage='')
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(endvideo,listitem)
        progress = len(playlist) / float(len(videoindividual)) * 100               
        dp.update(int(progress), 'A adicionar à playlist.')
    dp.close()
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist)


def restarttv_play(name,url):
    mensagemprogresso.create('TV Portuguesa', 'A carregar...')
    if mensagemprogresso.iscanceled(): 
        raise Exception("Canceled")                
        mensagemprogresso.close()
    mensagemprogresso.update(50)
    import urlresolver
    link=comuns.abrir_url(url)
    if re.search('dailymotion',link):
        daily=re.compile('<iframe frameborder="0" width=".+?" height=".+?" src="http://www.dailymotion.com/embed/video/(.+?)"></iframe>').findall(link)[0]
        embedvideo='http://www.dailymotion.com/video/' + daily
    elif re.search('youtube',link):
        youtube=re.compile('<iframe.+?src=".+?/embed/(.+?)".+?></iframe>').findall(link)[0]
        embedvideo='http://www.youtube.com/watch?v=' + youtube
    elif re.search('videos.sapo.pt',link):
        restarttv_sapo(name,link)
        return
    else: ok=mensagemok("TV Portuguesa", "Nenhum servidor compativel"); return
    mensagemprogresso.update(100)
    mensagemprogresso.close()
    sources=[]
    hosted_media = urlresolver.HostedMediaFile(url=embedvideo)
    sources.append(hosted_media)
    source = urlresolver.choose_source(sources)
    if source:
        linkescolha=source.resolve()
        if linkescolha==False:
            mensagemok('TV Portuguesa','Conteudo não disponível (removido).')
            return
        zumba.comecarvideo(linkescolha,name,False,zapping)

def restarttv_pesquisa():
      keyb = xbmc.Keyboard('', 'TV Portuguesa - Restart TV')
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            encode=urllib.quote_plus(search)
            if encode=='': pass
            else: restarttv_progs('',VBURL + '?s=' + encode)

def restarttv_paginas(link):
    try:
        paginas=re.compile('<span class="current">.+?</span>' + "<a href='(.+?)'" + ' class="inactive">(.+?)</a>').findall(link)
        for endereco, nrseg in paginas:
            addDir('[B][COLOR blue]Próxima pagina ('+nrseg+') >>[/COLOR][/B]',endereco,4,'',len(paginas),'',True)
    except: pass

def p_todos():
    if selfAddon.getSetting("prog-lista3") == "false": return ''
    else:
        try:
            dia=comuns.horaportuguesa()
            listacanais='RTP1,RTP2,SIC,TVI,SPTV1,SPTV2,SPTV3,SPTVL,SLB,PORTO,CMTV,BBV,RTPIN,SICK,SICM,SICN,SICR,TVI24,TVIFIC,HOLLW,AXN,AXNBL,AXNWH,FOX,FOXCR,FLIFE,FOXM,SYFY,DISNY,PANDA,MOTOR,DISCV,ODISS,HIST,NGC,EURSP,FASH,VH1,MTV,ABOLA,RTPAC,RTPA,RTPM,RTPMD,BIGGS'
            url='http://services.sapo.pt/EPG/GetChannelListByDateInterval?channelSiglas='+listacanais+'&startDate=' + dia +':01&endDate='+ dia + ':02'
            link=comuns.clean(comuns.abrir_url(url,erro=False))
            listas=re.compile('<Sigla>(.+?)</Sigla>.+?<Title>(.+?)</Title>.+?<Description>(.+?)</Description>').findall(link)
            canais={}
            for nomecanal, nomeprog, descricao in listas:
                canais[nomecanal]={'nomeprog':'(' + nomeprog + ')','descprog':descricao}
            return canais
        except: pass

def p_umcanal(listas,desejado,desc):
    try: return listas[desejado][desc]
    except: return ''

def mensagemaviso():
    try:
        xbmc.executebuiltin("ActivateWindow(10147)")
        window = xbmcgui.Window(10147)
        xbmc.sleep(100)
        window.getControl(1).setLabel( "%s - %s" % ('AVISO','TV Portuguesa',))
        window.getControl(5).setText("[COLOR red][B]Termos:[/B][/COLOR]\nEste addon não aloja quaisquer conteúdos. O conteúdo apresentado é da responsabilidade dos servidores e em nada está relacionado com este addon.\n\nEste plugin não pretende substituir o acesso aos serviços de televisão pagos. Apenas funciona como extra a esses serviços.\n\nEste plugin apenas indexa links de outros sites, não alojando quaisquer conteúdos.\n\nEste plugin não pretende substituir o acesso aos sites de streaming, mas sim facilitar o acesso a estes via plataformas móveis (RPi, android, etc.)\n\nVisitem os sites oficiais e suportem os sites clicando na publicidade.\n\nUm obrigado a todos eles. (www.livesoccerhq.com, www.reshare.net, www.thesporttv.eu, www.tugastream.com, www.tvdez.com, www.tvfree4.me, www.tvportugalhd.org, www.tvzune.tv).\n\nRestart TV (www.videosbacanas.com), Eventos (Cesarix/Rominhos), Listas (Cesarix, Pissos13, Benfiquista), Grafismo (Rukanito), Veetle (TvM) \n\n[COLOR red][B]É necessário actualizar o libRTMP do XBMC para alguns streams funcionarem a 100%.\nMais informações em: [/B][/COLOR] http://bit.ly/fightnightaddons\n\n[B]Data de actualização do aviso: [/B] 13 de Fevereiro de 2014")
    except: pass

def zapping(name):
    dp = xbmcgui.DialogProgress()
    #if dp.iscanceled(): dp.close()
    dp.create("A criar lista de canais",'Criando...')
    dp.update(0)
    playlist = xbmc.PlayList(1)
    playlist.clear()

    comuns.savefile(('zapping', ''))
    dp.update(25)
    #descobrirresolver('http://tugastream.com/bigbrothervip.php','Big Brother VIP-',False,True)
    dp.update(50)
    descobrirresolver('http://tugastream.com/sporttv1.php','SPORTTV 1-',False,True)
    dp.update(75)
    descobrirresolver('http://tugastream.com/rtp1.php','RTP 1-',False,True)
    dp.update(100)
    dp.close()
    conteudozapping=comuns.openfile(('zapping'))
    canalindividual=re.compile('_comeca_(.+?)_nomecanal_(.+?)_thumb_(.+?)_acaba_').findall(conteudozapping)
    dp.create("TV Portuguesa",'Criando...')
    dp.update(0)
    print canalindividual
    for nomecanal, rtmp,thumb in canalindividual:
        listitem = xbmcgui.ListItem(nomecanal, iconImage="DefaultVideo.png", thumbnailImage=tvporpath + art + thumb)
        listitem.setInfo("Video", {"Title":nomecanal})
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(rtmp,listitem)
        progress = len(playlist) / float(len(canalindividual)) * 100               
        print rtmp
        print nomecanal
        dp.update(int(progress), 'A adicionar à playlist.')
    dp.close()
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist)

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

def menugravador():
    if downloadPath=='':
        xbmcgui.Dialog().ok('TV Portuguesa','Necessitas de introduzir a pasta onde vão ficar','as gravações. Escolhe uma pasta com algum espaço','livre disponível.')
        dialog = xbmcgui.Dialog()
        pastafinal = dialog.browse(int(3), "Escolha pasta para as gravações", 'files')
        selfAddon.setSetting('pastagravador',value=pastafinal)
        return
    xbmc.executebuiltin("ReplaceWindow(VideoFiles," + downloadPath + ")")

def libalternativo(finalurl):
    if xbmc.getCondVisibility('system.platform.windows'):
        import newrtmp
        finalurl,spsc=newrtmp.start_stream(rtmp=finalurl)
    else: spsc=''
    return finalurl,spsc


def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
    try:
        if re.search('HD',name) or re.search('1080P',name) or re.search('720P',name):liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 1280, 'height': 720 } )
        else: liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
    except: pass    
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addCanal(name,url,mode,iconimage,total,descricao):
    cm=[]
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
    liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
    try:
        if re.search('HD',name) or re.search('1080P',name) or re.search('720P',name):liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 1280, 'height': 720 } )
        else: liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
    except: pass
    #cm.append(('Adicionar stream preferencial', "XBMC.RunPlugin(%s?mode=%s&name=%s&url=%s)")%(sys.argv[0],)
    liz.addContextMenuItems(cm, replaceItems=False)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=total)

def addDir(name,url,mode,iconimage,total,descricao,pasta):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
    liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

comuns.checkGA()

params=get_params()
url=None
thumb=None
name=None
mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: thumb=urllib.unquote_plus(params["thumb"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

def testejanela():
    d = menulateral("menulateral.xml" , tvporpath, "Default")
    d.doModal()
    del d

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(url)

if mode==None or url==None or len(url)<1:
    print "Versao Instalada: v" + versao
    if selfAddon.getSetting('termos') == 'true':
        mensagemaviso()
        selfAddon.setSetting('termos',value='false')
    entraraddon()
elif mode==1: menu_principal()
elif mode==2: restarttv()
elif mode==3: restarttv_lista(name,url)
elif mode==4: restarttv_progs(name,url)
elif mode==5: obter_lista(name,url)
elif mode==6: listascanais()
elif mode==7: descobrirresolver(url,nomecanal,linkrecebido,zapping)
elif mode==8: restarttv_play(name,url)
elif mode==9: xbmc.executebuiltin("Container.NextViewMode")
elif mode==10: restarttv_pesquisa()
elif mode==11: obter_lista(name,url)
elif mode==12: menugravador()
elif mode==13: abrir_lista_canais()
elif mode==14: ok = mensagemok('TV Portuguesa','[B][COLOR white]Queres adicionar a tua lista (XML)?[/COLOR][/B]','Visita [B]http://bit.ly/fightnightaddons[/B]','ou contacta "fightnight.addons@gmail.com')
elif mode==15: ok = mensagemok('TV Portuguesa','A actualizacao é automática. Caso nao actualize va ao','repositorio fightnight e prima c ou durante 2seg','e force a actualizacao. De seguida, reinicie o XBMC.')
elif mode==16: zumba.request_servidores(url,name)
elif mode==17: zumba.comecarvideo(url,name,'listas',False,thumb=thumb)
elif mode==18: entraraddon()
elif mode==22: selfAddon.openSettings()
elif mode==23: mensagemaviso()
elif mode==2013: testejanela()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
