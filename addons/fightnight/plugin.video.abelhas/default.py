# -*- coding: utf-8 -*-

""" abelhas.pt
    2013 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime

####################################################### CONSTANTES #####################################################

versao = '0.0.01'
addon_id = 'plugin.video.abelhas'
MainURL = 'http://abelhas.pt/'
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
iconpequeno=wtpath + art + 'iconpq.jpg'
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
downloadPath = selfAddon.getSetting('download-folder').decode('utf-8')
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
cookies = os.path.join(pastaperfil, "cookies.lwp")
username = urllib.quote(selfAddon.getSetting('abelhas-username'))
password = urllib.quote(selfAddon.getSetting('abelhas-password'))
PATH = ""            
UATRACK=""

#################################################### LOGIN WAREZTUGA #####################################################

def login_abelhas():
      print "Sem cookie. A iniciar login"
      try:
            link=abrir_url(MainURL)
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(link)[0]
            from t0mm0.common.net import Net
            net=Net()
            form_d = {'RedirectUrl':'','Redirect':'True','FileId':0,'Login':username,'Password':password,'RememberMe':'true','__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://abelhas.pt', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://abelhas.pt/','User-Agent':user_agent}
            endlogin=MainURL + 'action/login/login'
            try:
                  logintest= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: logintest='Erro'
      except:
            link='Erro'
            logintest='Erro'
      if selfAddon.getSetting('abelhas-username')== '':
            ok = mensagemok('Abelhas.pt','Necessitas de criar uma conta no abelhas.','Vai a www.abelhas.pt.')
            entrarnovamente(1)
      else:    
            if re.search(username,logintest):
                  xbmc.executebuiltin("XBMC.Notification(abelhas.pt,Sessão iniciada com sucesso.,'500000',"+iconpequeno.encode('utf-8')+")")
                  net.save_cookies(cookies)
                  menu_principal(1)
            elif re.search('Erro',logintest) or link=='Erro':
                  opcao= xbmcgui.Dialog().yesno('abelhas.pt', "Sem ligação à internet.", "", "","Tentar novamente", 'OK')
                  if opcao: menu_principal(0)
                  else: login_abelhas()
                
################################################### MENUS PLUGIN ######################################################

def menu_principal(ligacao):
      if ligacao==1:
            conteudo=clean(abrir_url_cookie('http://abelhas.pt/action/Help'))
            pontos=re.compile('href="/Points.aspx" title="Pontos" rel="nofollow".+?</a><strong>(.+?)</strong>').findall(conteudo)[0]
            mensagens=re.compile('href="/action/PrivateMessage" id="topbarMessage".+?</a><strong>(.+?)</strong>').findall(conteudo)[0]
            transf=re.compile('Transfe.+?ncia.+?<strong>(.+?)</strong>').findall(conteudo)[0]
            addDir("Top Coleccionadores",MainURL,1,wtpath + art + 'filmes.png',1,True)
            addDir("Abelhas Mais Recentes",MainURL,2,wtpath + art + 'series.png',2,True)
            addDir("A Minha Abelha",MainURL + username,3,wtpath + art + 'series.png',2,True)
            addDir("Ir para uma Abelha",'pastas',5,wtpath + art + 'series.png',2,True)
            addDir("Pesquisar Conteúdo",'pesquisa',7,wtpath + art + 'pesquisa.png',3,True)
            addLink("",'',wtpath + art + 'nothingx.png')
            addLink("[COLOR blue][B]Mensagens:[/B][/COLOR] " + mensagens,'',wtpath + art + 'nothingx.png')
            addLink("[COLOR blue][B]Transferência:[/B][/COLOR] " + transf,'',wtpath + art + 'nothingx.png')
            addLink("[COLOR blue][B]Pontos:[/B][/COLOR] " + pontos,'',wtpath + art + 'nothingx.png')
      elif ligacao==0:
            addDir('Reconectar Addon',MainURL,6,wtpath + art + 'refresh.png',1,True)
            addLink("",'',wtpath + art + 'nothingx.png')
      if ligacao==1:
            disponivel=versao_disponivel()
            if disponivel==versao: addLink("Última versão instalada (" + versao+ ')','',wtpath + art + 'versao_disp.png')
            else: addDir("Instalada: " + versao + ' | Actualização: ' + disponivel,MainURL,13,wtpath + art + 'versao_disp.png',1,False)
      else: addLink("Versão instalada:" + versao,'',wtpath + art + 'versao_disp.png')
      addDir("Definições | [COLOR gold][B]abelhas.pt[/B][/COLOR]",MainURL,8,wtpath + art + 'defs.png',6,False)
      xbmc.executebuiltin("Container.SetViewMode(50)")

def entrarnovamente(opcoes):
      if opcoes==1: selfAddon.openSettings()
      addDir('Entrar no addon',MainURL,None,wtpath + art + 'refresh.png',1,True)
      addDir('Alterar definições',MainURL,8,wtpath + art + 'defs.png',1,False)

def topcolecionadores():
      conteudo=clean(abrir_url_cookie('http://abelhas.pt/' + username))
      users=re.compile('<li><div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" /><span></span></a></div>.+?<i>(.+?)</i></li>').findall(conteudo)
      for urluser,nomeuser,thumbuser,nruser in users:
            addDir('[B][COLOR blue]' + nruser + 'º[/B][/COLOR] ' + nomeuser,MainURL + urluser,3,thumbuser,len(users),True)
      xbmc.executebuiltin("Container.SetViewMode(500)")
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def abelhasmaisrecentes():
      conteudo=clean(abrir_url_cookie('http://abelhas.pt/action/LastAccounts/MoreAccounts'))
      users=re.compile('<div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" /><span>').findall(conteudo)
      for urluser,nomeuser,thumbuser in users:
            addDir(nomeuser,MainURL + urluser,3,thumbuser,len(users),True)
      xbmc.executebuiltin("Container.SetViewMode(500)")
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def pesquisa():
      conteudo=clean(abrir_url_cookie('http://abelhas.pt/action/Help'))
      lista=re.compile('<select name="FileType">(.+?)</select>').findall(conteudo)[0]
      opcoeslabel=re.compile('<option value=".+?">(.+?)</option>').findall(conteudo)
      opcoesvalue=re.compile('<option value="(.+?)">.+?</option>').findall(conteudo)
      index = xbmcgui.Dialog().select("Seleccione o filtro", opcoeslabel)
      if index > -1:
            caixadetexto('pesquisa',ftype=opcoesvalue[index])
      else:sys.exit(0)

def pastas(url):
      if re.search('action/SearchFiles',url): extra= '&IsGallery=False'
      else: extra='?requestedFolderMode=filesList'
      conteudo=clean(abrir_url_cookie(url + extra))
      if re.search('ProtectedFolderChomikLogin',conteudo):
            chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            from t0mm0.common.net import Net
            net=Net()
            
            form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'abelhas.pt','Origin':'http://abelhas.pt','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/Files/LoginToFolder'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('IsSuccess":false',teste):
                  mensagemok('Abelhas.pt','Password errada.')
                  sys.exit(0)
            else:
                  pastas_ref(url)
      else:
            try:
                  conta=re.compile('<h3>(.+?)<span>(.+?)</span></h3>').findall(conteudo)[0]
                  nomeconta=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  addLink('[COLOR blue][B]Conta de ' + nomeconta + '[/B][/COLOR]: ' + conta[0] + conta[1],'',wtpath + art + 'star2.png')
            except: pass
            try:
                  pastas=re.compile('<div id="foldersList">(.+?)</table>').findall(conteudo)[0]
                  seleccionados=re.compile('<a href="/(.+?)".+?title="(.+?)">(.+?)</a>').findall(pastas)
                  for urlpasta,nomepasta,password in seleccionados:
                        if re.search('<span class="pass">',password): displock=' (bloqueado)'
                        else:displock=''
                        addDir(nomepasta + displock,MainURL + urlpasta,3,wtpath + art + 'pasta.png',len(seleccionados),True)
            except: pass
            items=re.compile('<ul class="borderRadius tabGradientBg"><li><span>(.+?)</span></li><li><span class="date">(.+?)</span></li></ul></div>.+?<ul>            <li><a href="/(.+?)" class="downloadAction".+?<li class="fileActionsFacebookSend" data-url=".+?" data-title="(.+?)">.+?<span class="bold">.+?</span>(.+?)</a>').findall(conteudo)
            for tamanhoficheiro,dataficheiro,urlficheiro, tituloficheiro,extensao in items:
                  extensao=extensao.replace(' ','')
                  if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.RAR' or extensao=='.7z' or extensao=='.7Z': thumb=wtpath + art + 'rar.png'
                  elif extensao=='.mp3' or extensao=='.MP3' or extensao == '.wma' or extensao=='.WMA' or extensao=='.m3u' or extensao=='.M3U' or extensao=='.flac' or extensao=='.FLAC': thumb=wtpath + art + 'musica.png'
                  elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=wtpath + art + 'foto.png'
                  elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV': thumb=wtpath + art + 'video.png'
                  else:thumb=wtpath + art + 'file.png'
                  addDir('[B]' + tituloficheiro + extensao + '[/B] (' + tamanhoficheiro + ')',MainURL + urlficheiro,4,thumb,len(items),False)
            paginas(conteudo)            
            
      xbmc.executebuiltin("Container.SetViewMode(51)")            

def pastas_ref(url):
      pastas(url)

def paginas(link):
      try:
            conteudo=re.compile('<div id="listView".+?>(.+?)<div class="filerow fileItemContainer">').findall(link)[0]
            pagina=re.compile('anterior.+?<a href="/(.+?)" class="right" rel="(.+?)"').findall(conteudo)[0]
            addDir('[COLOR blue]Página ' + pagina[1] + ' >>>[/COLOR]',MainURL + pagina[0],3,wtpath + art + 'seta.png',1,True)
      except:
            pass


########################################################### PLAYER ################################################

def analyzer():
      mensagemprogresso.create('Abelhas.pt', 'A carregar...')
      from t0mm0.common.net import Net
      net=Net()
      conteudo=abrir_url_cookie(url)
      fileid=re.compile('<input type="hidden" name="FileId" value="(.+?)"/>').findall(conteudo)[0]
      token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
      form_d = {'fileId':fileid,'__RequestVerificationToken':token}
      ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://abelhas.pt', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://abelhas.pt/','User-Agent':user_agent}
      endlogin=MainURL + 'action/License/Download'
      final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
      try:
            linkfinal=re.compile('"redirectUrl":"(.+?)"').findall(final)[0]
            linkfinal=linkfinal.replace('\u0026','&')
      except:
            if re.search('Por favor tenta baixar este ficheiro mais tarde.',final):
                  mensagemok('Abelhas.pt','Ficheiro não está disponivel. Tente mais tarde')
                  return

      mensagemprogresso.close()
      if re.search('.jpg',url) or re.search('.png',url) or re.search('.gif',url) or re.search('.bmp',url):
            xbmc.executebuiltin("ActivateWindow(Pictures,"+linkfinal+")")
            xbmc.executebuiltin("Action(Play)")
      if re.search('.mkv',url) or re.search('.avi',url) or re.search('.mp3',url) or re.search('.wmv',url):
            comecarvideo(name,linkfinal)
      else:
            comecarvideo(name,linkfinal)

def comecarvideo(name,url):
        thumbnail=''
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        listitem.setInfo("Video", {"Title":name})
        listitem.setInfo("Music", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        dialogWait = xbmcgui.DialogProgress()
        dialogWait.create('Video', 'A carregar')
        playlist.add(url, listitem)
        dialogWait.close()
        del dialogWait
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

           
######################################################## DOWNLOAD ###############################################
### THANKS ELDORADO (ICEFILMS) ###
def fazerdownload(name,url):
      vidname=name.replace('[B]','').replace('[/B]','').replace('\\','')
      vidname = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  vidname)
      if os.path.exists(downloadPath):
            if re.search('subs/',url): vidname = vidname+'.srt'; url=MainURL + url
            else: vidname = vidname+'.mp4'
            mypath=os.path.join(downloadPath,vidname)
      else: mypath= '0'           
      if mypath == '0':
            ok = mensagemok('Abelhas.pt','Não escolheste a pasta de download dos ficheiros.','Introduz nas definições do addon.','')
            selfAddon.openSettings()
            return False
      else:
            if os.path.isfile(mypath) is True:
                  ok = mensagemok('Abelhas.pt','Esse vídeo já existe no teu disco.','','')
                  return False
            else:              
                  try:
                        dp = xbmcgui.DialogProgress()
                        dp.create('Abelhas.pt - A Transferir', '', name)
                        start_time = time.time()
                        try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
                        except:
                              while os.path.exists(mypath): 
                                    try: os.remove(mypath); break 
                                    except: pass 
                              if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): return False 
                              else: raise 
                              return False
                        return True
                  except: ok=mensagemok('Abelhas.pt','Download Falhou'); print 'download failed'; return False

def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB de %.02f MB' % (currently_downloaded, total) 
            #e = 'Velocidade: (%.0f Kb/s) ' % kbps_speed
            e = ' (%.0f Kb/s) ' % kbps_speed 
            tempo = 'Tempo restante: %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs + e,tempo)
            #if percent=xbmc.executebuiltin("XBMC.Notification(Abelhas.pt,"+ mbs + e + ",'500000',"+iconpequeno+")")
      except: 
            percent = 100 
            dp.update(percent) 
      if dp.iscanceled(): 
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)

######################################################## OUTRAS FUNCOES ###############################################

def savefile(filename, contents):
    try:
        destination = os.path.join(pastaperfil, filename)
        fh = open(destination, 'wb')
        fh.write(contents)  
        fh.close()
    except: print "Nao gravou o marcador de: %s" % filename

def openfile(filename):
    try:
        destination = os.path.join(pastaperfil, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu o marcador de: %s" % filename
        return None

def format_time(seconds):
	minutes,seconds = divmod(seconds, 60)
	if minutes > 60:
		hours,minutes = divmod(minutes, 60)
		return "%02d:%02d:%02d" % (hours, minutes, seconds)
	else:
		return "%02d:%02d" % (minutes, seconds)

def caixadetexto(url,ftype=''):
      if url=='pastas': title="Ir para abelha - Abelhas.pt"
      elif url=='password': title="Password - Abelhas.pt"
      elif url=='pesquisa': title="Pesquisa - Abelhas.pt"
      else: title="Abelhas.pt"
      keyb = xbmc.Keyboard(selfAddon.getSetting('ultima-pesquisa'), title)
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            encode=urllib.quote_plus(search)
            if url=='pastas': pastas(MainURL + search)
            elif url=='password': return search
            elif url=='pesquisa': pastas(MainURL + 'action/SearchFiles?FileName=' + encode + '&submitSearchFiles=Procurar&FileType=' + ftype)
            
      else: sys.exit(0)
            
def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def abrir_url_cookie(url):
      from t0mm0.common.net import Net
      net=Net()
      net.set_cookies(cookies)
      try:
            ref_data = {'Host': 'abelhas.pt', 'Connection': 'keep-alive', 'Referer': 'http://abelhas.pt/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://abelhas.pt/'}
            link=net.http_GET(url,ref_data).content.encode('latin-1','ignore')
            return link
      except urllib2.HTTPError, e:
            mensagemok('Abelhas.pt',str(urllib2.HTTPError(e.url, e.code, "Erro na página.", e.hdrs, e.fp)),'Tente novamente.')
            sys.exit(0)
      except urllib2.URLError, e:
            mensagemok('Abelhas.pt','Erro na página. Tente novamente.')
            sys.exit(0)
            
def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.abelhas/addon.xml')
            match=re.compile('name="Abelhas.pt"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
      except:
            ok = mensagemok('Abelhas.pt','Addon não conseguiu conectar ao servidor','de actualização. Verifique a situação.','')
            match='Erro. Verificar origem do erro.'
      return match

def handle_wait(time_to_wait,title,text):
      ret = mensagemprogresso.create(' '+title)
      secs=0
      percent=0
      increment = int(100 / time_to_wait)
      cancelled = False
      while secs < time_to_wait:
            secs = secs + 1
            percent = increment*secs
            secs_left = str((time_to_wait - secs))
            remaining_display = 'Aguarda '+secs_left+' segundos para terminar.'
            mensagemprogresso.update(percent,' '+text,remaining_display)
            xbmc.sleep(1000)
            if (mensagemprogresso.iscanceled()):
                  cancelled = True
                  break
      if cancelled == True:
            return False
      else:
            return True

def redirect(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      gurl=response.geturl()
      return gurl

def millis():
      import time as time_
      return int(round(time_.time() * 1000))

def load_json(data):
      def to_utf8(dct):
            rdct = {}
            for k, v in dct.items() :
                  if isinstance(v, (str, unicode)) :
                        rdct[k] = v.encode('utf8', 'ignore')
                  else :
                        rdct[k] = v
            return rdct
      try :        
            from lib import simplejson
            json_data = simplejson.loads(data, object_hook=to_utf8)
            return json_data
      except:
            try:
                  import json
                  json_data = json.loads(data, object_hook=to_utf8)
                  return json_data
            except:
                  import sys
                  for line in sys.exc_info():
                        print "%s" % line
      return None

def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                  params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]                 
      return param

def clean(text):
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&#039;':'','&#39;':"'",'&#227;':'ã','&170;':'ª','&#233;':'é','&#231;':'ç','&#243;':'ó','&#226;':'â','&ntilde;':'ñ','&#225;':'á','&#237;':'í','&#245;':'õ','&#201;':'É','&#250;':'ú','&amp;':'&','&#193;':'Á','&#195;':'Ã','&#202;':'Ê','&#199;':'Ç','&#211;':'Ó','&#213;':'Õ','&#212;':'Ó','&#218;':'Ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)

def parseDate(dateString):
      try: return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
      except: return datetime.datetime.today() - datetime.timedelta(days = 1) #force update

def checkGA():
      secsInHour = 60 * 60
      threshold  = 2 * secsInHour
      now   = datetime.datetime.today()
      prev  = parseDate(selfAddon.getSetting('ga_time2'))
      delta = now - prev
      nDays = delta.days
      nSecs = delta.seconds
      doUpdate = (nDays > 0) or (nSecs > threshold)
      if not doUpdate: return
      selfAddon.setSetting('ga_time2', str(now).split('.')[0])
      APP_LAUNCH() 
                    
def send_request_to_google_analytics(utm_url):
      try:
            req = urllib2.Request(utm_url, None, {'User-Agent':user_agent})
            response = urllib2.urlopen(req).read()
      except: print ("GA fail: %s" % utm_url)         
      return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            #VISITOR = ADDON.getSetting('ga_visitor')
            VISITOR = environ.get("GA_VISITOR", username)
            VISITOR = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]
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
            
        except: print "================  CANNOT POST TO ANALYTICS  ================" 
            
def APP_LAUNCH():
        print '==========================   '+PATH+' '+versao+'   =========================='
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            import platform
            VISITOR = environ.get("GA_VISITOR", username)
            VISITOR = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]
            if re.search('12.0',xbmc.getInfoLabel( "System.BuildVersion"),re.IGNORECASE) or re.search('12.1',xbmc.getInfoLabel( "System.BuildVersion"),re.IGNORECASE): build="Frodo" 
            if re.search('11.0',xbmc.getInfoLabel( "System.BuildVersion"),re.IGNORECASE): build="Eden" 
            if re.search('13.0',xbmc.getInfoLabel( "System.BuildVersion"),re.IGNORECASE): build="Gotham"
            try: PLATFORM=platform.system()+' '+platform.release()
            except: PLATFORM=platform.system()
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + versao + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+PATH+"-"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except: print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
        except: print "================  CANNOT POST TO ANALYTICS  ================"
checkGA()
            
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
      print "Versao Instalada: v" + versao
      login_abelhas()
elif mode==1: topcolecionadores()
elif mode==2: abelhasmaisrecentes()
elif mode==3: pastas(url)
elif mode==4: analyzer()
elif mode==5: caixadetexto(url)
elif mode==6: login_abelhas()
elif mode==7: pesquisa()
elif mode==8: selfAddon.openSettings()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
