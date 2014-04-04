# -*- coding: utf-8
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,re,sys, urllib, urllib2,time,datetime,os
import comuns

dbversao=00003
SptveuURL = 'http://www.sporttvhdmi.com/'
TVDezURL = 'http://www.estadiofutebol.com'
TVTugaURL = 'http://www.tvtuga.com'
TugastreamURL = 'http://www.tugastream.com/'
TVPTHDURL = 'http://www.tvportugalhd.eu'
TVPTHDZuukURL = 'http://www.zuuk.pw'
TVCoresURL = 'http://tvfree2.me'
LSHDURL= 'http://livesoccerhq.com'
TVZuneURL = 'http://www.tvzune.tv/'
VBURL= 'http://www.videosbacanas.com/'
ResharetvURL = 'http://resharetv.com/'
DesgrURL = 'http://www.desportogratis.com/'
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

def dbver():
    return dbversao

def info_servidores():
    mensagemprogresso.create('A capturar fontes','A carregar lista de servidores.',pleasewait)
    if selfAddon.getSetting("fontes-desportogratis") == "true":
        try:
            mensagemprogresso.update(6,'',pleasewait + '(Desporto Grátis)')
            if mensagemprogresso.iscanceled(): sys.exit(0)
            desgrlink=comuns.limparcomentarioshtml(comuns.abrir_url(DesgrURL,erro=False),DesgrURL)
            desgrfinal='\n'.join(re.compile('<td>(.+?)</td>').findall(desgrlink))
            comuns.savefile('desgratis', desgrfinal)
        except: comuns.savefile('desgratis', '')
    if selfAddon.getSetting("fontes-livesoccerhd") == "true":
        try:
            mensagemprogresso.update(12,'',pleasewait + '(LivesoccerHD)')
            if mensagemprogresso.iscanceled(): sys.exit(0)
            
            linkinicial=comuns.abrir_url(LSHDURL + '/programacao.php',erro=False)
            urlintermedio=re.compile('<iframe.+?src="(.+?)"').findall(linkinicial)[0]
            ref_data = {'Referer': LSHDURL,'User-Agent':user_agent}
            linkintermedio= comuns.abrir_url_tommy(urlintermedio,ref_data,erro=False)
            lshdfinal='\n'.join(re.compile("<a style='font-size:(.+?)</font></a>").findall(linkintermedio))
            comuns.savefile('livesoccerhd', lshdfinal)
        except: comuns.savefile('livesoccerhd', '')
    #if selfAddon.getSetting("fontes-resharetv") == "true":
    #    try:
    #        mensagemprogresso.update(12,'',pleasewait + '(ReshareTV)')
    #        if mensagemprogresso.iscanceled(): sys.exit(0)
    #        resharetvlink=comuns.limparcomentarioshtml(comuns.abrir_url(ResharetvURL,erro=False),ResharetvURL)
    #        resharefinal='\n'.join(re.compile('<li>(.+?)</li>').findall(resharetvlink))
    #        comuns.savefile('resharetv', resharefinal)
    #    except: comuns.savefile('resharetv', '')
    if selfAddon.getSetting("fontes-thesporttveu") == "true":
        try:
            mensagemprogresso.update(25,'',pleasewait + '(Thesporttv.eu)')
            if mensagemprogresso.iscanceled(): sys.exit(0)
            sptveulink=comuns.abrir_url(SptveuURL,erro=False)
            if re.search('<script>window.location=',sptveulink) or re.search('jdfwkey',sptveulink):
                try:
                    key=re.compile('<script>window.location="/(.+?)";</script>').findall(sptveulink)[0]
                    sptveulink=comuns.abrir_url(SptveuURL + key,erro=False)
                except: pass
            sptvfinal='\n'.join(re.compile('<th scope="col">(.+?)</th>').findall(sptveulink))
            comuns.savefile('thesporttveu', sptvfinal)
        except: comuns.savefile('thesporttveu', '')
    if selfAddon.getSetting("fontes-tugastream") == "true":
        try:
            mensagemprogresso.update(37,'',pleasewait + '(Tugastream)')
            if mensagemprogresso.iscanceled(): sys.exit(0)
            tugastreamlink=comuns.abrir_url(TugastreamURL,erro=False)
            comuns.savefile('tugastream', tugastreamlink)
        except: comuns.savefile('tugastream', '')
    if selfAddon.getSetting("fontes-tvacores") == "true":
        try:
            mensagemprogresso.update(50,'',pleasewait + '(TV a Cores)')
            if mensagemprogresso.iscanceled(): sys.exit(0)
            tvacoreslink=comuns.clean(comuns.abrir_url(TVCoresURL + '/ver?limit=0&filter_order=&filter_order_Dir=&limitstart=',erro=False))
            tvcfinal='\n'.join(re.compile('<strong class="list-title">(.+?)</strong>').findall(tvacoreslink))
            comuns.savefile('tvacores', tvcfinal)
        except: comuns.savefile('tvacores', '')
    if selfAddon.getSetting("fontes-tvdez") == "true":
        try:
            mensagemprogresso.update(62,'',pleasewait + '(TVDez)')
            if mensagemprogresso.iscanceled(): sys.exit(0)
            tvdezlink= comuns.clean(comuns.abrir_url_cookie(TVDezURL,erro=False))
            tvdezfinal='\n'.join(re.compile('<div class="canal">(.+?)</div>').findall(tvdezlink))
            comuns.savefile('tvdez', tvdezfinal)
        except: comuns.savefile('tvdez', '')
    if selfAddon.getSetting("fontes-tvtuga") == "true":
        try:
            mensagemprogresso.update(75,'',pleasewait + '(TVTuga)')
            if mensagemprogresso.iscanceled(): sys.exit(0)
            tvtugalink=comuns.abrir_url_cookie(TVTugaURL + '/category/portugal/',erro=False)
            tvtugafinal='\n'.join(re.compile('<option class="ddpl-form2" (.+?)/option>').findall(tvtugalink))
            comuns.savefile('tvtuga', tvtugafinal)
        except: comuns.savefile('tvtuga', '')
    if selfAddon.getSetting("fontes-tvzune") == "true":
        #try:
        mensagemprogresso.update(87,'',pleasewait + '(TVZune)')
        if mensagemprogresso.iscanceled(): sys.exit(0)
        tvzunelink=comuns.clean(comuns.abrir_url_cookie(TVZuneURL,erro=False))
        tvzunefinal='\n'.join(re.compile('<span>(.+?)">').findall(tvzunelink))
        comuns.savefile('tvzune', tvzunefinal)
        #except: comuns.savefile('tvzune', '')
    if selfAddon.getSetting("fontes-tvpthdorg") == "true":
        try:
            mensagemprogresso.update(95,'',pleasewait + '(TVPortugalHD.org)')
            if mensagemprogresso.iscanceled(): sys.exit(0)
            tvpthdorglink=comuns.clean(comuns.abrir_url(TVPTHDURL,erro=False))
            tvptfinal='\n'.join(re.compile('<li>(.+?)</li>').findall(tvpthdorglink))
            comuns.savefile('tvportugalhd', tvptfinal)
        except: comuns.savefile('tvportugalhd', '')

def request_servidores(url,name):
    #if name=='[B]Eventos[/B] (Cesarix/Rominhos)':
    #    obter_lista(name,url)
    #    return
    name=name.replace('[','-')
    nome=re.compile('B](.+?)/B]').findall(name)[0]
    nomega=nome.replace('-','')
    comuns.GA("listacanais",nomega)
    titles=[]; ligacao=[]

    if nome=='-COLOR white]Zapping-/COLOR]-': zapping(nome)
    else:


        ########################################DESPORTOGRATIS############################
        if selfAddon.getSetting("fontes-desportogratis") == "true":
            try:
                desgrref=int(0)
                desgrlink=comuns.openfile('desgratis')
                nomedesgr=nome.replace('SPORTTV 1-','1.html').replace('SPORTTV 2-','2.html').replace('SPORTTV 3-','3.html').replace('SPORTTV LIVE-','4.html').replace('Benfica TV-','5.html')
                desgr=re.compile('<a href="http://www.desportogratis.com/'+nomedesgr+'" target="iframe"><form>').findall(desgrlink)
                if desgr:
                    for resto in desgr:
                        desgrref=int(desgrref + 1)
                        if len(desgr)==1:
                            desgr2=str('')
                        else:
                            desgr2=' #' + str(desgrref)
                        titles.append('Desporto Grátis' + desgr2)
                        ligacao.append('http://www.desportogratis.com/' + nomedesgr)
                        
            except: pass


        ########################################LIVESOCCERHD############################
        if selfAddon.getSetting("fontes-livesoccerhd") == "true":
            try:
                lshdref=int(0)
                lshdlink=comuns.openfile('livesoccerhd')
                nomelshd=nome.replace('SPORTTV 1-','SPTV 1').replace('SPORTTV 2-','SPTV 2').replace('SPORTTV 3-','SPTV 3').replace('SPORTTV LIVE-','SPTV LIVE').replace('Benfica TV-','BENFICA TV')
                lshd=re.compile("href='(.+?)'>.+?</span>"+nomelshd+".+?/span>").findall(lshdlink)
                if lshd:
                    for resto in lshd:
                        lshdref=int(lshdref + 1)
                        if len(lshd)==1:
                            lshd2=str('')
                        else:
                            lshd2=' #' + str(lshdref)
                        titles.append('LivesoccerHD' + lshd2)
                        ligacao.append(resto)
                        
            except: pass

        ########################################RESHARETV############################
        if selfAddon.getSetting("fontes-resharetv") == "true":
            try:
                resharetv=False
                resharetvref=int(0)
                resharetvlink=comuns.openfile('resharetv')
                nomeresharetv=nome.replace('SPORTTV 1-','Sport Tv1').replace('SPORTTV 2-','Sport Tv2').replace('SPORTTV 3-','Sport Tv3').replace('SPORTTV LIVE-','Sport Tv Live').replace('RTP 1-','Rtp 1').replace('RTP 2-','Rtp 2').replace('SIC-','Sic').replace('TVI-','Tvi').replace('Big Brother VIP-','Tvi Direct').replace('SIC Noticias-','Sic Not&iacute;cias').replace('MTV-','Mtv').replace('RTP Informação-','Rtp Informa&ccedil;&atilde;o').replace('VH1-','Vh1').replace('Fashion TV-','FashionTV').replace('Benfica TV-','Benfica TV')
                resharetv=re.compile('<a href="/(.+?)".+?>'+nomeresharetv+'</a>').findall(resharetvlink)
                if not resharetv:
                    resharetvlink=comuns.clean(resharetvlink)
                    resharetv=re.compile('<a href="/(.+?)" target="box" >'+nomeresharetv+'</a>.+?</ul>').findall(resharetvlink)
                    extralinks=re.compile('<a href="/.+?" target="box" >'+nomeresharetv+'</a>(.+?)</ul>').findall(resharetvlink)[0]
                    blabla=re.compile('<a href="/(.+?)" target="box" >').findall(extralinks)
                    for links in blabla:
                        resharetv.append(links)
                if resharetv:
                    for codigo in resharetv:
                        resharetvref=int(resharetvref + 1)
                        if len(resharetv)==1: resharetv2=str('')
                        else: resharetv2=' #' + str(resharetvref)
                        titles.append('ReshareTV' + resharetv2)
                        ligacao.append(ResharetvURL + codigo)
            except: pass


        ########################################THESPORTTVEU############################
        if selfAddon.getSetting("fontes-thesporttveu") == "true":
            try:
                sptveuref=int(0)
                sptveulink=comuns.openfile('thesporttveu')
                nomesptveu=nome.replace('SPORTTV 1-','Sporttv1').replace('SPORTTV 1 HD-','Sporttv1-v').replace('SPORTTV 2-','Sporttv2').replace('SPORTTV 3-','Sporttv3').replace('SPORTTV LIVE-','Sporttv-live').replace('Benfica TV-','Benficatv').replace('TVI-','Tvi')
                sptveu=re.compile('<a href="' + nomesptveu + '(.+?)" target="_blank"><img src=').findall(sptveulink)
                if sptveu:
                    for resto in sptveu:
                        sptveuref=int(sptveuref + 1)
                        if len(sptveu)==1:
                            sptveu2=str('')
                        else:
                            sptveu2=' #' + str(sptveuref)
                        titles.append('Thesporttv.eu' + sptveu2)
                        ligacao.append(SptveuURL + nomesptveu + resto)
                        
            except: pass


        ########################################TV A CORES############################
        if selfAddon.getSetting("fontes-tvacores") == "true":
            try:
                tvacoresref=int(0)
                tvacoreslink=comuns.openfile('tvacores')
                nometvacores=nome.replace('RTP 1-','RTP 1 Online').replace('RTP 2-','RTP 2 Online').replace('SIC-','SIC Online').replace('TVI-','TVI Online').replace('SPORTTV 1-','Sporttv Direto').replace('Big Brother VIP-','BB VIP').replace('SIC K-','SIC K Online').replace('SIC Radical-','SIC Radical Online').replace('SIC Mulher-','SIC Mulher Online').replace('SIC Noticias-','SIC Noticias Online').replace('TVI24-','TVI24 online').replace('Hollywood-','Canal Hollywood').replace('MOV-','Canal MOV').replace('AXN-','AXN Portugal').replace('AXN Black-','AXN Black Online').replace('AXN White-','AXN White online').replace('FOX-','Fox Online PT').replace('FOX Crime-','FOX Crime Online').replace('FOX Life-','FOX Life Online').replace('FOX Movies-','FOX Movies Portugal').replace('Canal Panda-','Canal Panda').replace('Discovery Channel-','Discovery Channel PT').replace('Eurosport-','Eurosport Portugal').replace('Benfica TV-','Benfica TV Online').replace('Porto Canal-','Porto Canal - Emissão Online').replace('Syfy-','SYFY Channel Portugal').replace('Odisseia-','Canal Odisseia').replace('História-','Canal Historia Portugal').replace('National Geographic Channel-','National Geographic PT').replace('MTV-','MTV Portugal').replace('RTP Açores-','RTP Açores Online').replace('RTP Africa-','RTP África Online').replace('RTP Informação-','RTP Informação - Emissão Online').replace('RTP Madeira-','RTP Madeira Online').replace('RTP Memória-','RTP Memória').replace('Disney Channel-','Disney Portugal').replace('Disney Junior-','Disney Junior').replace('Panda Biggs-','Panda Biggs').replace('Motors TV-','Motors TV Online').replace('ESPN-','ESPN USA').replace('ESPN America-','ESPN Online BR').replace('A Bola TV-','A Bola TV').replace('RTP Africa-','RTP Africa').replace('RTP Madeira-','RTP Madeira').replace('RTP Internacional-','RTP Internacional').replace('RTP Açores-','RTP Açores').replace('A Bola TV-','A Bola TV').replace('Casa dos Segredos 4-','Secret Story 4 em Direto').replace('CM TV-','CMTV em direto').replace('TVI Ficção-','TVI Ficção online')
                tvacores=re.compile('<a href="(.*?)">'+nometvacores+'</a>').findall(tvacoreslink)
                if tvacores:
                    for codigo in tvacores:
                        tvacoresref=int(tvacoresref + 1)
                        if len(tvacores)==1: tvacores2=str('')
                        else: tvacores2=' #' + str(tvacoresref)
                        titles.append('TV a Cores' + tvacores2)
                        ligacao.append(TVCoresURL + codigo)
            except: pass
                  
        ########################################TUGASTREAM############################
        if selfAddon.getSetting("fontes-tugastream") == "true":
            try:
                tugastreamref=int(0)
                tugastreamlink=comuns.openfile('tugastream')
                nometugastream=nome.replace('RTP 1-','rtp1').replace('RTP 2-','rtp2').replace('TVI-','tvi').replace('FOX-','fox').replace('AXN-','axn').replace('SIC-','sic').replace('AXN Black-','axnblack').replace('AXN White-','axnwhite').replace('FOX Life-','foxlife').replace('FOX Crime-','foxcrime').replace('FOX Movies-','foxmovies').replace('SPORTTV 1-','sporttv1').replace('SPORTTV 2-','sporttv2').replace('SPORTTV 3-','sporttv3').replace('SPORTTV LIVE-','sporttvlive').replace('Canal Panda-','panda').replace('Hollywood-','hollywood').replace('Eurosport-','eurosport').replace('MOV-','mov').replace('VH1-','vh1').replace('Porto Canal-','portocanal').replace('SIC Noticias-','sicnoticias').replace('SIC Radical-','sicradical').replace('SIC Mulher-','sicmulher').replace('SIC K-','sick').replace('Big Brother VIP-','bigbrothervip').replace('TVI Ficção-','tvificcao').replace('Syfy-','syfy').replace('Benfica TV-','benficatv').replace('CM TV-','cmtv').replace('RTP Africa-','rtpafrica').replace('RTP Informação-','rtpinformacao').replace('Fashion TV-','fashiontv').replace('ESPN-','espn').replace('RTP Africa-','rtpafrica').replace('RTP Madeira-','rtpmadeira').replace('RTP Internacional-','rtpinternacional').replace('Casa dos Segredos 4-','secretstory')
                tugastream=re.compile('<a href="'+nometugastream + '(.+?)php">').findall(tugastreamlink)
                if tugastream:
                    for codigo in tugastream:
                        tugastreamref=int(tugastreamref + 1)
                        if len(tugastream)==1: tugastream2=str('')
                        else: tugastream2=' #' + str(tugastreamref)
                        titles.append('Tugastream' + tugastream2)
                        ligacao.append(TugastreamURL + nometugastream + codigo + 'php?altura=432&largura=768')
            except: pass

        ########################################TVTUGA############################
        if selfAddon.getSetting("fontes-tvtuga") == "true":
            try:
                tvtugaref=int(0)
                tvtugalink=comuns.openfile('tvtuga')
                
                nometvtuga=nome.replace('RTP 1-','rtp-1').replace('RTP 2-','rtp-2').replace('TVI-','tvi').replace('FOX-','fox').replace('AXN-','axn').replace('SIC-','sic').replace('AXN Black-','axnblack').replace('AXN White-','axn-white').replace('FOX Life-','fox-life').replace('FOX Crime-','fox-crime').replace('FOX Movies-','fox-movies').replace('SPORTTV 1-','sporttv1').replace('SPORTTV 2-','sporttv2').replace('SPORTTV 3-','sporttv3').replace('SPORTTV LIVE-','sporttvlive').replace('Canal Panda-','canal-panda').replace('Hollywood-','canal-hollywood').replace('Eurosport-','eurosport').replace('MOV-','mov').replace('VH1-','vh1').replace('Porto Canal-','portocanal').replace('SIC Noticias-','sic-noticias').replace('SIC Radical-','sicradical').replace('SIC Mulher-','sicmulher').replace('SIC K-','sick').replace('Big Brother VIP-','bigbrothervip').replace('TVI Ficção-','tvi-ficcao').replace('Syfy-','syfy').replace('Benfica TV-','benfica-tv').replace('CM TV-','cm-tv').replace('RTP Africa-','rtp-africa').replace('RTP Informação-','rtp-informacao').replace('Fashion TV-','fashiontv').replace('ESPN-','espn').replace('A Bola TV-','abola-tv').replace('Casa dos Segredos 4-','secret-story-4-casa-dos-segredos').replace('RTP Açores-','rtp-acores').replace('RTP Internacional-','rtp-internacional').replace('RTP Madeira-','rtp-madeira').replace('RTP Memória-','rtp-memoria').replace('TVI24-','tvi-24')

                tvtuga=re.compile('value="http://www.tvtuga.com/'+nometvtuga+'(.+?)">').findall(tvtugalink)
                if tvtuga:
                    for codigo in tvtuga:
                        tvtugaref=int(tvtugaref + 1)
                        if len(tvtuga)==1: tvtuga2=str('')
                        else: tvtuga2=' #' + str(tvtugaref)
                        titles.append('TVTuga' + tvtuga2)
                        ligacao.append(TVTugaURL + '/' + nometvtuga + codigo)
            except: pass

                
        ########################################TVDEZ############################
        if selfAddon.getSetting("fontes-tvdez") == "true":
            try:
                tvdezref=int(0)
                tvdezlink=comuns.openfile('tvdez')
                tvdezlink=tvdezlink.replace('+ TVI','Mais TVI')
                nometvdez=nome.replace('RTP 1-','RTP').replace('RTP 2-','RTP 2').replace('FOX-','FOX').replace('AXN-','AXN').replace('AXN Black-','AXN Black').replace('AXN White-','AXN White').replace('FOX Life-','FOX Life').replace('FOX Crime-','FOX Crime').replace('FOX Movies-','FOX Movies').replace('SPORTTV 3-','Sport TV 3').replace('SPORTTV LIVE-','Sporttv Live').replace('Canal Panda-','Canal Panda').replace('Hollywood-','Hollywood').replace('Eurosport-','Eurosport').replace('MOV-','Canal MOV').replace('VH1-','VH1 Hits').replace('Porto Canal-','Porto Canal').replace('SIC Radical-','SIC Radical').replace('SIC Mulher-','SIC Mulher').replace('SIC K-','SIC K').replace('TVI Ficção-','TVI Fic&ccedil;&atilde;o').replace('Benfica TV-','Benfica TV').replace('Discovery Channel-','Discovery Channel').replace('TVI24-','TVI 24').replace('Mais TVI-','Mais TVI').replace('Syfy-','Syfy').replace('Odisseia-','Odisseia').replace('História-','Hist&oacute;ria').replace('National Geographic Channel-','National Geographic').replace('MTV-','MTV').replace('CM TV-','Correio da Manh&atilde; TV').replace('RTP Açores-','RTP A&ccedil;ores').replace('RTP Informação-','RTP Informa&ccedil;&atilde;o').replace('RTP Madeira-','RTP Madeira').replace('RTP Memória-','RTP Mem&oacute;ria').replace('Disney Channel-','Disney Channel').replace('Fashion TV-','Fashion TV').replace('Disney Junior-','Disney Junior').replace('Panda Biggs-','Panda Biggs').replace('Motors TV-','Motors TV').replace('ESPN-','ESPN').replace('ESPN America-','ESPN').replace('A Bola TV-','A Bola TV').replace('RTP Africa-','RTP Africa').replace('RTP Madeira-','RTP Madeira').replace('RTP Internacional-','RTP Internacional').replace('RTP Memória-','RTP Mem&oacute;ria').replace('RTP Açores-','RTP A&ccedil;ores').replace('Casa dos Segredos 4-','Casa dos segredos 4')
                tvdez=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                if not tvdez:
                    nometvdez=nome.replace('SPORTTV 1-','Sport TV 1').replace('SPORTTV 2-','Sport TV 2').replace('SIC-','SIC').replace('TVI-','TVI').replace('SIC Noticias-','SIC Not&iacute;cias').replace('Big Brother VIP-','Big Brother VIP 2013').replace('Benfica TV-','Benfica-TV').replace('Casa dos Segredos 4-','Casa dos segredos 4')
                    tvdez=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                    nometvdez=nome.replace('SPORTTV 1-','Sporttv em Directo').replace('SPORTTV 2-','Sporttv 2').replace('SIC-','SIC Online - Stream 2').replace('TVI-','TVI Online - Stream 2').replace('SIC Noticias-','SIC Not&iacute;cias Online').replace('Big Brother VIP-','Big Brother Portugal').replace('Benfica TV-','Benfica-TV')
                    tvdez+=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                    nometvdez=nome.replace('SPORTTV 1-','Sporttv HD')
                    tvdez+=re.compile('<a href="(.+?)" title="'+nometvdez+'">').findall(tvdezlink)
                if tvdez:
                    for codigo in tvdez:
                        tvdezref=int(tvdezref + 1)
                        if len(tvdez)==1: tvdez2=str('')
                        else: tvdez2=' #' + str(tvdezref)
                        titles.append('TVDez' + tvdez2)
                        ligacao.append(TVDezURL + codigo)
            except: pass


        ########################################TVZUNE############################
        if selfAddon.getSetting("fontes-tvzune") == "true":
            try:
                tvzuneref=int(0)
                tvzunelink=comuns.openfile('tvzune')
                nometvzune=nome.replace('RTP 1-','RTP 1').replace('RTP 2-','RTP 2').replace('SIC-','SIC').replace('SPORTTV 1-','SPORT TV 1').replace('SPORTTV 2-','SPORT TV 2').replace('SPORTTV 3-','SPORT TV 3').replace('TVI-','TVI').replace('FOX-','FOX').replace('AXN-','AXN').replace('Discovery Channel-','discovery').replace('AXN Black','axnblack').replace('AXN White-','axnwhite').replace('FOX Life-','foxlife').replace('FOX Crime-','foxcrime').replace('FOX Movies-','foxmovies').replace('Canal Panda-','panda').replace('Hollywood-','hollywood').replace('Eurosport-','eurosport').replace('MOV-','mov').replace('VH1-','vh1').replace('TVI24-','tvi24').replace('SIC Noticias-','sicnoticias').replace('SIC Radical-','sicradical').replace('SIC Mulher-','sicmulher').replace('SIC K-','sick').replace('Big Brother VIP-','bigbrothervip').replace('TVI Ficção-','tvificcao')
                tvzune=re.compile(nometvzune + "</span>.+?iframe/channel.php.+?ch=(.+?)'" ).findall(tvzunelink)
                if tvzune:
                    for resto in tvzune:
                        tvzuneref=int(tvzuneref + 1)
                        if len(tvzune)==1: tvzune2=str('')
                        else: tvzune2=' #' + str(tvzuneref)
                        titles.append('TVZune' + tvzune2)
                        ligacao.append(TVZuneURL + 'iframe/channel.php?ch=' + nometvzune)
            except: pass  

        ######################################TVPORTUGALHD.ORG########################
        if selfAddon.getSetting("fontes-tvpthdorg") == "true":
            try:
                nometvpthdorg=nome.replace('RTP 1-','RTP').replace('RTP 2-','RTP 2').replace('SIC-','SIC').replace('SPORTTV 1-','SPORTTV 1').replace('SPORTTV 2-','SPORTTV 2').replace('SPORTTV 3-','SPORTTV 3').replace('SPORTTV LIVE-','SPORTTV Live').replace('SIC-','SIC').replace('TVI-','TVI').replace('FOX-','FOX').replace('AXN-','AXN').replace('Discovery Channel-','Discovery Channel').replace('AXN Black-','AXN Black').replace('AXN White-','AXN White').replace('FOX Life-','FOX Life').replace('FOX Crime-','FOX Crime').replace('FOX Movies-','FOX Movies').replace('Canal Panda-','Canal Panda').replace('Hollywood-','Hollywood').replace('Eurosport-','Eurosport').replace('MOV-','MOV').replace('VH1-','VH1').replace('Benfica TV-','Benfica TV').replace('Porto Canal-','Porto Canal').replace('TVI24-','TVI24').replace('SIC Noticias-','SIC Noticias').replace('SIC Radical-','SIC Radical').replace('SIC Mulher-','SIC Mulher').replace('SIC K-','SIC K').replace('Big Brother VIP-','Big Brother Vip1').replace('TVI Ficção-','TVI Ficção').replace('Syfy-','Syfy').replace('Odisseia-','Odisseia').replace('História-','Historia').replace('National Geographic Channel-','National Geographic').replace('MTV-','MTV').replace('RTP Africa-','RTP Africa').replace('RTP Informação-','RTP Informação').replace('RTP Madeira-','RTP Madeira').replace('Disney Channel-','Disney Channel').replace('Panda Biggs-','Panda Biggs').replace('A Bola TV-','A Bola TV').replace('RTP Açores-','RTP Açores').replace('RTP Informação-','RTP Informa&ccedil;&atilde;o').replace('RTP Madeira-','RTP Madeira').replace('Disney Channel-','Disney Channel').replace('Fashion TV-','Fashion TV').replace('Disney Junior-','Disney Junior').replace('Panda Biggs-','Panda Biggs').replace('Motors TV-','Motors TV').replace('ESPN-','ESPN').replace('ESPN America-','ESPN America').replace('A Bola TV-','A Bola TV').replace('RTP Africa-','RTP Africa').replace('RTP Madeira-','RTP Madeira').replace('RTP Internacional-','RTP Internacional').replace('RTP Memória-','RTP Memoria').replace('Casa dos Segredos 4-','Secret Story 4').replace('CM TV-','CMTV')
                tvpthdorglink=comuns.openfile('tvportugalhd')
                tvpthdorgref=int(0)
                nometvpthdorg=urllib.quote(nometvpthdorg)
                tvpthdorg=re.compile("<a dir='ltr' href='http://www.tvportugalhd.eu/search/label/" + nometvpthdorg + "'>.+?</a>").findall(tvpthdorglink)
                reftvpth=1
                if not tvpthdorg:
                    tvpthdorg=re.compile("<a dir='ltr' href='http://www.tvportugalhd.eu/search/label/" + nometvpthdorg + "(.+?)>.+?</a>").findall(tvpthdorglink)
                    reftvpth=0
                if tvpthdorg:
                    for codigotv in tvpthdorg:
                        tvpthdorgref=int(tvpthdorgref + 1)
                        if len(tvpthdorg)==1: tvpthdorg2=str('')
                        else:
                            if tvpthdorgref==1: tvpthdorg2=' #' + str(tvpthdorgref)
                            else: tvpthdorg2=' #' + str(tvpthdorgref)# + '[COLOR red] (indisponivel)[/COLOR]'
                        codigotv=codigotv.replace("'",'')
                        titles.append('TVPortugal HD.org' + tvpthdorg2)
                        if reftvpth==1: ligacao.append('http://www.tvportugalhd.eu/search/label/' + nometvpthdorg)
                        else: ligacao.append('http://www.tvportugalhd.eu/search/label/' + nometvpthdorg + codigotv)
            except: pass

        if len(ligacao)==1: index=0
        elif len(ligacao)==0: ok=mensagemok('TV Portuguesa', 'Nenhum stream disponivel.'); return     
        else: index = xbmcgui.Dialog().select('Escolha o servidor', titles)
        if index > -1:
            mensagemprogresso.create('TV Portuguesa', 'A carregar stream. (' + titles[index] + ')','Por favor aguarde...')
            mensagemprogresso.update(0)
            if mensagemprogresso.iscanceled(): mensagemprogresso.close()
            pre_resolvers(titles,ligacao,index,nome)

def pre_resolvers(titles,ligacao,index,nome):
    import buggalo
    buggalo.SUBMIT_URL = 'http://fightnight.pusku.com/exceptions/submit.php'
    try:
        sys.argv[2]=sys.argv[2]+ titles[index]

        linkescolha=ligacao[index]
        if linkescolha:
            if re.search('estadiofutebol',linkescolha):
                link=comuns.abrir_url_cookie(linkescolha)
                if re.search('televisaofutebol',link):
                    codigo=re.compile('<iframe src="http://www.televisaofutebol.com/(.+?)"').findall(link)[0]
                    embed='http://www.televisaofutebol.com/' + codigo
                    ref_data = {'Referer': 'http://www.estadiofutebol.com','User-Agent':user_agent}
                    html= comuns.abrir_url_tommy(embed,ref_data)
                    descobrirresolver(embed,nome,html,False)
                else:descobrirresolver(linkescolha, nome,False,False)
            elif re.search('tvfree2',linkescolha):
                link=comuns.abrir_url(linkescolha)
                if re.search('antena.tvfree',link) or re.search('iframe id="player"',link):
                    frame=re.compile('<iframe id="player".+?src="(.+?)"').findall(link)[0]
                    if not re.search('antena.tvfree',frame): frame= TVCoresURL + frame
                    ref_data = {'Referer': linkescolha,'User-Agent':user_agent}
                    link= comuns.abrir_url_tommy(frame,ref_data)
                    descobrirresolver(frame, nome,link,False)
                else: descobrirresolver(linkescolha, nome,False,False)
            elif re.search('sporttvhd',linkescolha):
                link=comuns.clean(comuns.abrir_url(linkescolha))
                try:
                    linkcod=re.compile("id='(.+?)'.+?</script><script type='text/javascript' src='"+SptveuURL +"/teste/").findall(link)[0]
                    descobrirresolver(SptveuURL+ '/teste/c0d3r.php?id=' + linkcod,nome,'hdm1.tv',False)
                except:
                    frame=re.compile('</p>          <iframe allowtransparency="true" frameborder="0" scrolling=".+?" src="(.+?)"').findall(link)[0]
                    link=comuns.clean(comuns.abrir_url(frame))
                    if re.search('var urls = new Array',link):
                        framedupla=re.compile('new Array.+?"(.+?)".+?"(.+?)"').findall(link)[0]
                        if framedupla[0]==framedupla[1]: frame=framedupla[0]
                        else:
                            opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Escolha um stream da lista dos disponiveis.", "", "","Stream Extra", 'Stream Principal')
                            if opcao: frame=framedupla[0]
                            else: frame=framedupla[1]
              
                    descobrirresolver(frame, nome,False,False)
            elif re.search('lvshd',linkescolha):
                link=comuns.abrir_url(linkescolha)
                linkfinal=comuns.limparcomentarioshtml(link,linkescolha)
                endereco=re.compile('<iframe.+?src="(.+?)".+?</iframe></div>').findall(link)[0]
                descobrirresolver(endereco, nome,False,False)
            elif re.search('tvzune',linkescolha):
                ref_data = {'Referer': 'http://www.tvzune.tv','User-Agent':user_agent}
                html= comuns.abrir_url_tommy(linkescolha,ref_data)
                print html
                descobrirresolver(linkescolha, nome,html,False)
            else: descobrirresolver(linkescolha, nome,False,False)
    except Exception:
        mensagemprogresso.close()
        mensagemok('TV Portuguesa','Servidor não suportado.')
        #buggalo.onExceptionRaised()

def descobrirresolver(url_frame,nomecanal,linkrecebido,zapping):
    if zapping==False:mensagemprogresso.update(50)
    try:
        import buggalo
        buggalo.SUBMIT_URL = 'http://fightnight.pusku.com/exceptions/submit.php'
        yoyo265='type:"flash".+?"'
        yoyo115='file:'

        if linkrecebido==False:
            print "Resolver: O url da frame e " + url_frame
            url_frame=url_frame.replace(' ','%20')
            link=comuns.abrir_url_cookie(url_frame)
            try:link=comuns.limparcomentarioshtml(link,url_frame)
            except: pass
            link=link.replace('cdn.zuuk.net\/boi.php','').replace('cdn.zuuk.net\/stats.php','').replace('cdn.zuuk.net/boi.php','').replace('cdn.zuuk.net/stats.php','')
        else:
            print "Resolver: O produto final no descobrirresolver"
            link=comuns.limparcomentarioshtml(linkrecebido,url_frame)
            link=link.replace('<title>Zuuk.net</title>','').replace('http://s.zuuk.net/300x250.html','').replace('www.zuuk.net\/test.php?ch=','').replace('cdn.zuuk.net\/boi.php','').replace('cdn.zuuk.net\/stats.php','').replace('cdn.zuuk.net/boi.php','').replace('cdn.zuuk.net/stats.php','')
            
        if re.search("<iframe src='http://www.zuuk.pw",link):
            name=re.compile("<iframe src='http://www.zuuk.pw(.+?)'").findall(link)[0]
            descobrirresolver('http://www.zuuk.pw' + name,nomecanal,False,zapping)
        
        elif re.search("zuuk.net",link):
            try:
                print "Catcher: zuuk"
                l
#                try:chname=re.compile("file='(.+?)'.+?</script>").findall(link)[0]
#                except:chname=False
#                if not chname:
#                    chname=re.compile('src=.+?http://www.zuuk.net/el.php.+?ch=(.+?)&').findall(link)[0]
#                    link=comuns.abrir_url_cookie('http://www.zuuk.net/el.php?ch='+chname)
#                streamurl='rtmp://198.7.58.79/edge playPath='+ chname +' swfUrl=http://cdn.zuuk.net/ply.swf live=true timeout=15 swfVfy=1 pageUrl=http://www.zuuk.net/'
#                comecarvideo(streamurl,nomecanal,True,zapping)
            except:
                print "Catcher: zuuk outro"
                if re.search('<script type="text/javascript">var urls = new Array',link): url_final=re.compile('new Array.+?"(.+?)",').findall(link)[0]
                ##derbie##
                else:
                    try:name=re.compile('<iframe.+?src="http://.+?zuuk.net/(.+?)"').findall(link)[0]
                    except:name=re.compile("<iframe.+?src='http://.+?zuuk.net/(.+?)'").findall(link)[0]
                    url_final="http://cdn.zuuk.net/" + name
                link=comuns.abrir_url_cookie(url_final)
                link=comuns.limparcomentarioshtml(link,url_frame)
                try:
                    info=re.compile("<div id='mediaspace'>"+'<script language="javascript".+?' + "document.write.+?unescape.+?'(.+?)'").findall(link)[0]
                    if info=="' ) );</script> <script type=": info=False
                except:info=False
                if info: infotratada=urllib.unquote(info)
                else: infotratada=link
                descobrirresolver(url_final,nomecanal,infotratada,zapping)

        #### ALIVE REMOVER DEPOIS ####

        elif re.search('file=myStream.sdp',link) or re.search('ec21.rtp.pt',link):
            print "Catcher: RTP Proprio"
            #link=comuns.abrir_url_cookie(url_frame)
            #urlalive=re.compile('<iframe src="(.+?)".+?></iframe>').findall(link)[0]
            #import cookielib
            #cookie = cookielib.CookieJar()
            #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            #opener.addheaders = [('Host','www.rtp.pt'), ('User-Agent', user_agent), ('Referer',url_frame)]
            #linkfinal = opener.open(urlalive).read()
            rtmpendereco=re.compile('streamer=(.+?)&').findall(link)[0]
            filepath=re.compile('file=(.+?)&').findall(link)[0]
            filepath=filepath.replace('.flv','')
            swf="http://player.longtailvideo.com/player.swf"
            streamurl=rtmpendereco + ' playPath=' + filepath + ' swfUrl=' + swf + ' live=1 timeout=15 pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('720Cast',link) or re.search('ilive',link):
            print "Catcher: ilive"
            setecast=re.compile("fid='(.+?)';.+?></script>").findall(link)
            if not setecast: setecast=re.compile('file: ".+?/app/(.+?)/.+?",').findall(link)
            if not setecast: setecast=re.compile('flashvars="file=(.+?)&').findall(link)
            if not setecast: setecast=re.compile('src="/ilive.tv.php.+?id=(.+?)" id="innerIframe"').findall(link)
            if not setecast: setecast=re.compile('http://www.ilive.to/embed/(.+?)&').findall(link)
            if not setecast: setecast=re.compile('http://www.ilive.to/embedplayer.php.+?&channel=(.+?)&').findall(link)
            if not setecast: setecast=re.compile('http://www.ilive.to/embed/(.+?)&').findall(link)
            for chname in setecast:
                embed='http://www.ilive.to/embedplayer.php?width=640&height=400&channel=' + chname + '&autoplay=true'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                tempomili=str(comuns.millis())
                urltoken=re.compile(""".*getJSON\("([^'"]+)".*""").findall(html)[0] + '&_='+ tempomili
                urltoken2= comuns.abrir_url_tommy(urltoken,ref_data)
                print urltoken2
                print html
                token=re.compile('"token":"(.+?)"').findall(urltoken2)[0]
                rtmp=re.compile('streamer: "(.+?)",').findall(html)[0]
                filelocation='noti'
                #filelocation=re.compile('file: "(.+?).flv",').findall(html)[0]
                swf=re.compile("type: 'flash', src: '(.+?)'").findall(html)[0]
                streamurl=rtmp + ' playPath=' + filelocation + ' swfUrl=' + swf + ' token='+ token +' swfVfy=1 live=1 timeout=15 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('aliez',link):
            print "Catcher: aliez"
            aliez=re.compile('src="http://emb.aliez.tv/player/live.php.+?id=(.+?)&').findall(link)
            for chid in aliez:
                embed='http://emb.aliez.tv/player/live.php?id=' + chid + '&w=700&h=420'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                swf=re.compile('swfobject.embedSWF\("([^"]+)"').findall(html)[0]
                rtmp=urllib.unquote(re.compile('"file":\s."([^"]+)"').findall(html)[0])
                streamurl=rtmp + ' live=true swfVfy=1 swfUrl=' + swf + ' pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('castalba', link):
            print "Catcher: castalba"
            castalba=re.compile('<script type="text/javascript"> id="(.+?)";.+?></script>').findall(link)
            for chname in castalba:
                embed='http://castalba.tv/embed.php?cid=' + chname + '&wh=640&ht=385&r=cdn.thesporttv.eu'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                swf=re.compile("""flashplayer': "(.+?)",""").findall(html)[0]
                filelocation=re.compile("'file': '(.+?)',").findall(html)[0]
                rtmpendereco=re.compile("'streamer': '(.+?)',").findall(html)[0]
                streamurl=rtmpendereco + ' playPath=' + filelocation + '?id=' + ' swfUrl=http://www.udemy.com/static/flash/player5.9.swf live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('castamp',link):
            print "Catcher: castamp"
            castamp=re.compile('channel="(.+?)".+?</script>').findall(link)
            for chname in castamp:
                embed='http://castamp.com/embed.php?c='+chname
                ref_data = {'Referer': 'http://www.zuuk.net','User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                swf=re.compile("""flashplayer': "(.+?)",""").findall(html)[0]
                filelocation=re.compile("'file': '(.+?)',").findall(html)[0]
                rtmpendereco=re.compile("'streamer': '(.+?)',").findall(html)[0]
                streamurl=rtmpendereco + ' playPath=' + filelocation + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)
                
        elif re.search('cast3d', link): ##nao esta
            print "Catcher: cast3d"
            cast3d=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in cast3d:
                embed='http://www.cast3d.tv/embed.php?channel=' + '&vw=640&vh=385&domain=lsh.lshunter.tv'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                swf=re.compile("""flashplayer': "(.+?)",""").findall(html)
                filelocation=re.compile("'file': '(.+?)',").findall(html)
                rtmpendereco=re.compile("'streamer': '(.+?)',").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + '?id=' + ' swfUrl=' + swf[0] + ' live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('castto.me',link):
            print "Catcher: castto.me"
            castamp=re.compile('fid="(.+?)".+?</script>').findall(link)
            for chname in castamp:
                embed='http://static.castto.me/embed.php?channel='+chname+'&vw=650&vh=500&domain='+url_frame
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                if re.search('Channel does not exist',html):
                    mensagemok('TV Portuguesa','Stream está offline.')
                    return
                swf=re.compile("SWFObject.+?'(.+?)'").findall(html)[0]
                filelocation=re.compile("so.addVariable.+?file.+?'(.+?)'").findall(html)[0]
                rtmpendereco=re.compile("so.addVariable.+?streamer.+?'(.+?)'").findall(html)[0]
                streamurl=rtmpendereco + ' playPath=' + filelocation + ' swfUrl=' + swf + ' live=true timeout=15 swfVfy=1 token=#ed%h0#w@1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('ChelTV',link) or re.search('visionip',link):
            print "Catcher: cheltv"
            chelsea=re.compile("file=(.+?).flv&streamer=(.+?)&").findall(link)
            swf=re.compile('src="(.+?)" type="application/x-shockwave-flash">').findall(link)[0]
            streamurl=chelsea[0][1] + ' playPath=' + chelsea[0][0] + ' swfUrl=' + swf + ' live=true pageUrl=http://www.casadossegredos.tv'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('ezcast', link):
            print "Catcher: ezcast"
            ezcast=re.compile("channel='(.+?)',.+?</script>").findall(link)
            if not ezcast: ezcast=re.compile('src="/ezcast.tv.php.+?id=(.+?)" id="innerIframe"').findall(link)
            if not ezcast: ezcast=re.compile('channel="(.+?)",.+?</script>').findall(link)
            for chname in ezcast:
                embed='http://www.ezcast.tv/embedded/' + chname + '/1/555/435'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                link=comuns.abrir_url('http://www.ezcast.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                idnum=re.compile("'FlashVars'.+?id=(.+?)&s=.+?&").findall(html)[0]
                chnum=re.compile("'FlashVars'.+?id=.+?&s=(.+?)&").findall(html)[0]
                streamurl='rtmp://' + rtmpendereco + '/live playPath=' + chnum + '?id=' + idnum + ' swfUrl=http://www.ezcast.tv/static/scripts/eplayer.swf live=true conn=S:OK swfVfy=1 timeout=14 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('fcast', link):
            print "Catcher: fcast"
            fcast=re.compile("fid='(.+?)';.+?></script>").findall(link)
            if not fcast: fcast=re.compile("e-fcast.tv.php.+?fid=(.+?).flv").findall(link)
            for chname in fcast:
                embed='http://www.fcast.tv/embed.php?live=' + chname + '&vw=600&vh=400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                swf=re.compile("SWFObject.+?'(.+?)'").findall(html)
                filelocation=re.compile("so.addVariable.+?file.+?'(.+?)'").findall(html)
                rtmpendereco=re.compile("so.addVariable.+?streamer.+?'(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + ' swfUrl=' + swf[0] + ' live=true timeout=14 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('flashi', link):
            print "Catcher: flashi"
            flashi=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in flashi:
                embed='http://www.flashi.tv/embed.php?v=' + chname +'&vw=640&vh=490&typeplayer=0&domain=f1-tv.info'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                if re.search('This Channel is not Existed !',html):
                    ok=mensagemok('TV Portuguesa','Stream indisponivel')
                    return
                swf=re.compile("new SWFObject.+?'(.+?)'").findall(html)[0]
                filename=re.compile("so.addVariable.+?'file'.+?'(.+?)'").findall(html)
                #rtmpendereco=re.compile("so.addVariable.+?'streamer'.+?'(.+?)'").findall(link)
                streamurl='rtmp://flashi.tv:1935/lb' + ' playPath=' + filename[0] + ' swfUrl=http://www.flashi.tv/' + swf + ' live=true timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hdcast.tv',link):
            chid=re.compile('fid=(.+?)"').findall(link)[0]
            chid=chid.replace('.flv','')
            streamurl='rtmp://origin.hdcast.tv:1935/redirect/ playPath='+chid+' swfUrl=http://www.udemy.com/static/flash/player5.9.swf live=true timeout=15 swfVfy=1 pageUrl=http://www.hdcast.tv'
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hdcaster.net', link):
            print "Catcher: hdcaster"
            hdcaster=re.compile("<script type='text/javascript'>id='(.+?)'").findall(link)
            for chid in hdcaster:
                urltemp='rtmp://188.138.121.99/hdcaster playPath=' + chid + ' swfUrl=http://hdcaster.net/player.swf pageUrl=http://hdcaster.net/player.php?channel_id=101634&width=600&height=430'
                token = '%Xr8e(nKa@#.'
                streamurl=urltemp + ' token=' + token
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('icasthd', link):
            print "Catcher: icastHD"
            icast=re.compile('fid="(.+?)";.+?></script>').findall(link)
            for chname in icast:
                embed='http://www.icasthd.tv/embed.php?v='+chname+'&vw=575&vh=390&domain=www.ihdsports.com'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                if re.search('This Channel is not Existed !',html):
                    ok=mensagemok('TV Portuguesa','Stream indisponivel')
                    return
                swf=re.compile("'flashplayer': 'http://www.icasthd.tv//(.+?)'").findall(html)[0]
                filename=re.compile("'file': '(.+?)'").findall(html)[0]
                rtmpendereco=re.compile("'streamer': '(.+?)redirect3").findall(html)[0]
                app=re.compile("Ticket=(.+?)'").findall(html)[0]
                streamurl=rtmpendereco+ 'live app=live?f=' + app + ' playPath=' + filename + ' swfUrl=http://www.icasthd.tv/' + swf + ' live=1 timeout=15 swfVfy=1 pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('janjua',link):
            print "Catcher: janjua"
            janj=re.compile("channel='(.+?)',.+?</script>").findall(link)
            if not janj: janj=re.compile('channel="(.+?)",.+?</script>').findall(link)
            for chname in janj:
                embed='http://www.janjua.tv/embedplayer/'+chname+'/1/650/500'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                if re.search('Channel is domain protected.',html):
                    url_frame='http://www.janjua.tv/' + chname
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    html= comuns.abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=comuns.abrir_url('http://www.janjua.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)
                streamurl='rtmp://' + rtmpendereco[0] + '/live/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true swfUrl=http://www.janjua.tv' + swf[0] + ' pageUrl=' + embed
                #print streamurl
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('longtail', link):
            print "Catcher: longtail"
            longtail=re.compile("src='http://player.longtailvideo.com/player.swf' flashvars='file=(.+?)&streamer=(.+?)&").findall(link)
            if not longtail: longtail=re.compile('flashvars="file=(.+?)&streamer=(.+?)&').findall(link)
            for chname,rtmp in longtail:
                chname=chname.replace('.flv','')
                streamurl=rtmp + ' playPath=' + chname + ' live=true swfUrl=http://player.longtailvideo.com/player.swf pageUrl=http://longtailvideo.com/'
                comecarvideo(streamurl,nomecanal,True,zapping)
            if not longtail:
                streamurl=re.compile('file: "(.+?)"').findall(link)[0]
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('hdm1.tv',link):
            print "Catcher: hdm1.tv"
            hdmi=re.compile("fid='(.+?)';.+?></script>").findall(link)
            for chid in hdmi:
                embed='http://hdm1.tv/embed.php?live='+ chid +'&vw=600&vh=470'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                swf=re.compile("new SWFObject.+?'(.+?)'").findall(html)[0]
                filelocation=re.compile("so.addVariable.+?'file'.+?'(.+?)'").findall(html)
                rtmpendereco=re.compile("so.addVariable.+?'streamer'.+?'(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)
            if not hdmi:
                hdmi=re.compile("src='(.+?).swf.+?file=(.+?)&streamer=(.+?)&autostart=true").findall(link)
                for swf,chid,rtmp in hdmi:
                    embed='http://hdm1.tv/embed.php?live='+ chid +'&vw=600&vh=470'
                    streamurl=rtmp + ' playPath=' + chid + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + embed
                    comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('jimey',link):
            print "Catcher: jimey"
            chname=re.compile("file='(.+?)';.+?</script>").findall(link)[0]
            embed= 'http://jimey.tv/player/embedplayer.php?channel=' + chname + '&width=640&height=490'
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            html= comuns.abrir_url_tommy(embed,ref_data)
            rtmp=re.compile('&streamer=(.+?)/redirect').findall(html)[0]
            streamurl= rtmp + ' playPath='+chname + " token=zyklPSak>3';CyUt%)'ONp" + ' swfUrl=http://jimey.tv/player/fresh.swf live=true timeout=15 swfVfy=1 pageUrl=' + embed
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('jwlive',link) or re.search('jw-play',link):
            print "Catcher: jwlive"
            endereco=TVCoresURL + re.compile('<iframe src="(.+?)" id="innerIframe".+?>').findall(link)[0]
            if re.search('tvfree2.me/jw-player.html',endereco):
                streamurl=endereco.replace('http://tvfree2.me/jw-player.html?cid=','')
            else:
                link=comuns.abrir_url(endereco)
                streamurl=re.compile('file: "(.+?)"').findall(link)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('liveflash', link):
            print "Catcher: liveflash"
            flashtv=re.compile("channel='(.+?)',.+?></script>").findall(link)
            if not flashtv: flashtv=re.compile('channel="(.+?)".+?</script>').findall(link)
            if not flashtv: flashtv=re.compile('iframe src="/cc-liveflash.php.+?channel=(.+?)"').findall(link)
            if not flashtv: flashtv=re.compile("window.open.+?'/e-liveflash.tv.php.+?channel=(.+?)'").findall(link)
            if not flashtv: flashtv=re.compile("http://tvph.googlecode.com/svn/players/liveflash.html.+?ver=(.+?)'").findall(link)
            if not flashtv: flashtv=re.compile("pop-liveflash.php.+?get=(.+?)'").findall(link)
            for chname in flashtv:
                embed='http://www.liveflash.tv/embedplayer/' + chname + '/1/640/460'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                if re.search('Channel is domain protected.',html):
                    url_frame='http://www.liveflash.tv/' + chname
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    html= comuns.abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=comuns.abrir_url('http://www.liveflash.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)
                streamurl='rtmp://' + rtmpendereco[0] + '/stream/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true swfUrl=http://www.liveflash.tv' + swf[0] + ' pageUrl=' + embed
                #print streamurl
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('livestream', link):
            print "Catcher: livestream"
            livestream=re.compile("videoborda.+?channel=(.+?)&").findall(link)
            for chname in livestream:
                streamurl='rtmp://extondemand.livestream.com/ondemand playPath=trans/dv04/mogulus-user-files/ch'+chname+'/2009/07/21/1beb397f-f555-4380-a8ce-c68189008b89 live=true swfVfy=1 swfUrl=http://cdn.livestream.com/chromelessPlayer/v21/playerapi.swf pageUrl=http://cdn.livestream.com/embed/' + chname + '?layout=4&amp;autoplay=true'
                comecarvideo(streamurl,nomecanal,True,zapping)



        elif re.search('megom', link):
            print "Catcher: megom.tv"
            megom=re.compile('HEIGHT=432 SRC="http://distro.megom.tv/player-inside.php.+?id=(.+?)&width=768&height=432"></IFRAME>').findall(link)
            for chname in megom:
                embed='http://distro.megom.tv/player-inside.php?id='+chname+'&width=768&height=432'
                link=comuns.abrir_url(embed)
                swf=re.compile(".*'flashplayer':\s*'([^']+)'.*").findall(link)[0]
                streamer=re.compile("'streamer': '(.+?)',").findall(link)[0]
                streamer=streamer.replace('live.megom.tv','37.221.172.85')
                streamurl=streamer + ' playPath=' + chname + ' swfVfy=1 swfUrl=' + swf + ' live=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('micast', link):
            print "Catcher: micast"
            micast=re.compile('micast.tv:1935/live/(.+?)/').findall(link)
            if not micast: micast=re.compile('ca="(.+?)".+?></script>').findall(link)
            if not micast: micast=re.compile('setTimeout.+?"window.open.+?' + "'http://micast.tv/gen.php.+?ch=(.+?)',").findall(link)
            if not micast: micast=re.compile('src="http://micast.tv/gen5.php.+?ch=(.+?)&amp;"').findall(link)
            if not micast: micast=re.compile('src="http://micast.tv/chn.php.+?ch=(.+?)"').findall(link)
            for chname in micast:
                embed=comuns.redirect('http://micast.tv/chn.php?ch='+chname)
                link=comuns.abrir_url(embed)
                if re.search('refresh',link):
                    chname=re.compile('refresh" content="0; url=http://micast.tv/gen.php.+?ch=(.+?)"').findall(link)[0]                
                    link=comuns.abrir_url('http://micast.tv/gen5.php?ch='+chname)
                try:
                    final=re.compile('file=(.+?)&amp;streamer=(.+?)&amp').findall(link)[0]
                    streamurl=final[1] + ' playPath=' + final[0] + ' swfUrl=http://files.mica.st/player.swf live=true timeout=15 swfVfy=1 pageUrl=http://micast.tv/gen.php?ch='+final[0]
                except:
                    rtmp=re.compile('file: "(.+?),').findall(link)[0]
                    chid=re.compile('/liveedge/(.+?)"').findall(rtmp)[0]
                    chidplay=chid.replace('.flv','')
                    rtmp=rtmp.replace(chid+'"','')
                    #rtmp://89.248.168.21/liveedge/<playpath>live5 <swfUrl>http://micast.tv/jwplayer/jwplayer.flash.swf <pageUrl>http://micast.tv/gens2.php?ch=live5
                    streamurl=rtmp + ' playPath=' + chidplay + ' swfUrl=http://micast.tv/jwplayer/jwplayer.flash.swf live=true pageUrl=' + embed

                comecarvideo(streamurl,nomecanal,True,zapping)
            if not micast:
                try:
                    micast=re.compile('<iframe src="(.+?)" id="innerIframe"').findall(link)[0]
                    link=comuns.abrir_url(TVCoresURL + micast)
                    if re.search('privatecdn',link):
                        descobrirresolver(url_frame,nomecanal,link,zapping)
                    else:
                        micast=re.compile('//(.+?).micast.tv/').findall(link)[0]
                        linkfinal='http://' + micast+  '.micast.tv'
                        link=comuns.abrir_url(linkfinal)
                        final=re.compile('file=(.+?)&amp;streamer=(.+?)&amp').findall(link)[0]
                        #if not final: final=re.compile("file=(.+?)&streamer=(.+?)'").findall(link)[0]
                        streamurl=final[1] + ' playPath=' + final[0] + ' swfUrl=http://files.mica.st/player.swf live=true timeout=15 swfVfy=1 pageUrl=http://micast.tv/gen.php?ch='+final[0]
                        comecarvideo(streamurl,nomecanal,True,zapping)
                except: pass
                
        elif re.search('mips', link):
            print "Catcher: mips"
            mips=re.compile("channel='(.+?)',.+?></script>").findall(link)
            if not mips: mips=re.compile('channel="(.+?)",.+?></script>').findall(link)
            if not mips: mips=re.compile('<iframe src="/mips.tv.php.+?fid=(.+?)" id="innerIframe"').findall(link)
            for chname in mips:
                embed='http://www.mips.tv/embedplayer/' + chname + '/1/500/400'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                swf=re.compile('SWFObject.+?"(.+?)",').findall(html)[0]
                flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                flashvars=flashvars.replace("')","&nada").split('l=&')
                if flashvars[1]=='nada':
                    nocanal=re.compile("&s=(.+?)&e=").findall(flashvars[0])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[0]
                else:
                    nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                    chid=re.compile("id=(.+?)&s=").findall(html)[1]
                nocanal=nocanal.replace('&','')
                link=comuns.abrir_url('http://www.mips.tv:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                streamurl='rtmp://' + rtmpendereco + '/live/ playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 live=true timeout=15 conn=S:OK swfUrl=http://www.mips.tv' + swf + ' pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('privatecdn',link):
            print "Catcher: privatecdn"
            privatecdn=re.compile('<script type="text/javascript">id="(.+?)"').findall(link)
            for chid in privatecdn:
                embed='http://privatecdn.tv/ch.php?id='+chid
                link=comuns.abrir_url(embed)
                rtmp=re.compile('file: "(.+?)"').findall(link)[0]
                rtmp=rtmp.replace('/'+chid,'')
                streamurl=rtmp + ' playPath='+chid + ' live=true swfUrl=http://player.longtailvideo.com/player.swf pageUrl='+embed
                comecarvideo(streamurl,nomecanal,True,zapping)
                
        elif re.search('putlive', link):
            print "Catcher: putlive"
            putlivein=re.compile("<iframe.+?src='.+?.swf.+?file=(.+?)&.+?'.+?></iframe>").findall(link)
            if not putlivein: putlivein=re.compile("file='(.+?)'.+?</script>").findall(link)
            if not putlivein: putlivein=re.compile('src="http://www.putlive.in/e/(.+?)"></iframe>').findall(link)
            for chname in putlivein:
                streamurl='rtmpe://199.195.199.172:443/liveedge2/ playPath=' + chname + ' swfUrl=http://www.megacast.io/player59.swf live=true timeout=15 swfVfy=1 pageUrl=http://putlive.in/'
                comecarvideo(streamurl,nomecanal,True,zapping)

        ##livesoccerhd
        elif re.search('src="http://cdn.sporttvhdmi.com',link):
            print "Catcher: livesoccerhd stolen sptvhd"
            ups=re.compile('<iframe.+?src="(.+?)"').findall(link)[0]
            descobrirresolver(ups,nomecanal,False,zapping)
        
        elif re.search('ptcanal', link):
            print "Catcher: ptcanal"
            ptcanal=re.compile('<p><a href="(.+?)" onclick="window.open').findall(link)[0]
            descobrirresolver(ptcanal,nomecanal,False,zapping)

        elif re.search('rtps',link):
            print "Catcher: rtps"
            ficheiro=re.compile("file='(.+?).flv'.+?</script>").findall(link)[0]
            streamurl='rtmp://ec21.rtp.pt/livetv/ playPath=' + ficheiro + ' swfUrl=http://museu.rtp.pt/app/templates/templates/swf/pluginplayer.swf live=true timeout=15 pageUrl=http://www.rtp.pt/'
            comecarvideo(streamurl, nomecanal,True,zapping)

        elif re.search('h2e.rtp.pt',link) or re.search('h2g2.rtp.pt',link) or re.search('.rtp.pt',link):
            link=link.replace('\\','').replace('">',"'>")
            try:streamurl=re.compile("cid=(.+?).m3u8").findall(link)[0]
            except:streamurl=re.compile("file=(.+?).m3u8").findall(link)[0]
            #streamurl='rtmp://ec21.rtp.pt/livetv/ playPath=' + ficheiro + ' swfUrl=http://museu.rtp.pt/app/templates/templates/swf/pluginplayer.swf live=true timeout=15 pageUrl=http://www.rtp.pt/'
            comecarvideo(streamurl + '.m3u8', nomecanal,True,zapping)

        elif re.search('resharetv',link): #reshare tv
            ref_data = {'Referer': 'http://resharetv.com','User-Agent':user_agent}
            html= comuns.abrir_url_tommy(url_frame,ref_data)
            html=comuns.clean(html)
            try:
                try: streamurl=re.compile(',  file: "(.+?)"').findall(html)[0]
                except: streamurl=re.compile('file: "(.+?)"').findall(html)[0]
            except:
                try:
                    swf=re.compile('<param name="movie" value="/(.+?)"></param>').findall(html)[0]
                    rtmp=re.compile('<param name="flashvars" value="src=http%3A%2F%2F(.+?)%2F_definst_%2F.+?%2Fmanifest.f4m&loop=true.+?">').findall(html)[0]
                    play=re.compile('_definst_%2F(.+?)%2Fmanifest.f4m&loop=true.+?">').findall(html)[0]
                except:
                    try:
                        swf=re.compile('src="(.+?)" type="application/x-shockwave-flash"').findall(html)[0]
                        rtmp=re.compile('streamer=(.+?)&amp').findall(html)[0]
                        play=re.compile('flashvars="file=(.+?).flv&').findall(html)[0]
                        streamurl='rtmp://' + urllib.unquote(rtmp) + ' playPath=' + play + ' live=true timeout=15 swfVfy=1 swfUrl=' + ResharetvURL + swf + ' pageUrl=' + ResharetvURL
                    except:
                        try:
                            frame=re.compile('<iframe.+?src="(.+?)">').findall(html)[0]
                            descobrirresolver(frame,nomecanal,False,zapping)
                            return
                        except:
                            ok = mensagemok('TV Portuguesa','Não e possível carregar stream.')
                            return
            comecarvideo(streamurl, nomecanal,True,zapping)
        elif re.search('sharecast',link):
            print "Catcher: sharecast"
            share=re.compile('src="http://sharecast.to/embed/(.+?)"></iframe>').findall(link)
            if not share: share=re.compile('src="http://sharecast.to/embed.php.+?ch=(.+?)"').findall(link)
            for chname in share:
                embed= 'http://sharecast.to/embed/' + chname
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                if re.search('Channel not found',html):
                    ok = mensagemok('TV Portuguesa','Stream offline.')
                    return
                try:
                    playpath= re.compile('file: "(.+?)",').findall(html)[0]
                    rtmp= re.compile('streamer: "(.+?)",').findall(html)[0]
                    conteudo=rtmp + ' playPath=' + playpath
                except:
                    rtmp= re.compile('file: "(.+?)",').findall(html)[0]
                    conteudo=rtmp
                
                streamurl= conteudo + ' live=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)


        elif re.search('p,a,c,k,e,r',link):
            print "Catcher: zuuk ruu.php"
            link=link.replace('|','')
            tuga=re.compile('ruuphpnr(.+?)style').findall(link)[0]
            descobrirresolver("http://www.zuuk.net/ruu.php?nr=" + tuga,nomecanal,False,zapping)

        elif re.search('sapo.pt',link):
            print "Catcher: sapo.pt"
            try:
                chname=re.compile('live/(.+?)&').findall(link)[0]
                filepath=re.compile('file=(.+?)&amp').findall(link)[0]
                l
            except:
                chname=re.compile('http://videos.sapo.pt/(.+?)"').findall(link)[0]
                info=comuns.abrir_url('http://videos.sapo.pt/'+chname)
                filepath=re.compile('/live/(.+?)",').findall(info)[0]
            host=comuns.abrir_url('http://videos.sapo.pt/hosts_stream.html')
            hostip=re.compile('<host>(.+?)</host>').findall(host)[0]
            streamurl='rtmp://' + hostip + '/live' + ' playPath=' + filepath  + ' swfUrl=http://imgs.sapo.pt/sapovideo/swf/flvplayer-sapo.swf?v11 live=true pageUrl=http://videos.sapo.pt/'+chname
            #ok=mensagemok('TV Portuguesa','Servidor não suportado')
            comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('telewizja',link):
            codigo=re.compile('<iframe src="(.+?)" id="innerIframe".+?>').findall(link)[0]
            ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            embed=TVCoresURL + codigo
            html= comuns.abrir_url_tommy(embed,ref_data)
            descobrirresolver(embed,nomecanal,html,zapping)

        elif re.search('televisaofutebol',link):
            print "Catcher: televisaofutebol"
            link=link.replace('\\','')
            tuga=re.compile('src="http://www.televisaofutebol.com/(.+?)".+?/iframe>').findall(link)[0]
            embed='http://www.televisaofutebol.com/' + tuga
            ref_data = {'Referer': 'http://www.estadiofutebol.com','User-Agent':user_agent}
            html= comuns.abrir_url_tommy(embed,ref_data)
            descobrirresolver(embed,nomecanal,html,zapping)

        elif re.search('tugastream',link):
            print "Catcher: tugastream"
            tuga=re.compile('src=".+?tugastream.com/(.+?)".+?/iframe>').findall(link)[0]
            descobrirresolver('http://www.tugastream.com/' + tuga,nomecanal,False,zapping)

        elif re.search('secretstory4_s.php',link):
            descobrirresolver('http://cdn.zuuk.net/secretstory4_s.php',nomecanal,False,zapping)

        elif re.search('tv-msn',link):
            print "Catcher: tv-msn"
            idcanal= 'http://tv-msn.com/' + re.compile('<iframe src="http://tv-msn.com/(.+?)" marginheight="0" marginwidth="0"').findall(link)[0]
            link=comuns.abrir_url(idcanal)
            frame=re.compile('<iframe.+?src="(.+?)".+?></iframe>').findall(link)[0]
            conteudo=comuns.abrir_url_cookie(frame)
            variaveis=re.compile("flashvars='file=(.+?)&streamer=(.+?)&autostart=true").findall(conteudo)[0]
            streamurl=variaveis[1] + ' playPath=' + variaveis[0]  + ' swfUrl=http://www.cdnbr.biz/swf/player.swf live=true pageUrl='+frame


        elif re.search("<iframe style='position:relative; overflow:hidden; width:508px; height:408px; top:-8px; left:-8px;' src='http://tvzune.tv",link):
            print "Catcher: tvzune em tvpthd"
            streamurl=re.compile("<iframe.+?src='(.+?)'").findall(link)[0]
            descobrirresolver(streamurl,nomecanal,False,zapping)

        elif re.search('sicnoticias_sp.php',link):
            print "Catcher: sicnoticias"
            descobrirresolver('http://www.tugastream.com/sicnoticias_sp.php',nomecanal,False,zapping)
        
        elif re.search('tvph.googlecode.com',link):
            print "Catcher: tvph google code"
            if re.search('playeer.html',link):
                info=re.compile("cid=file=(.+?)&streamer=(.+?)'").findall(link)[0]
                rtmp=info[1]
                streamurl=rtmp + ' playPath='+info[0]+' swfUrl=http://www.tvzune.tv/jwplayer/jwplayer.flash.swf live=true pageUrl=' + url_frame
            else:
                streamurl=re.compile("cid=(.+?)'").findall(link)[0]
            comecarvideo(streamurl,nomecanal,True,zapping)
            

        elif re.search('player_tvzune',link):
            print "Catcher: player tvzune"
            yoyo412=re.compile(yoyo115 + ' "(.+?)"').findall(link)[0]
            yoyo721='/'.join((yoyo412.split('/'))[:-1])
            yoyo428=re.compile('src="(.+?)"').findall(link)[0]
            yoyo683=re.compile(yoyo265 + '(.+?)"').findall(comuns.abrir_url(yoyo428))[0]
            yoyo378='/'.join((yoyo428.split('/'))[:-1]) + '/' + yoyo683
            streamurl=yoyo721 + ' playPath=' + yoyo412.split('/')[-1] + ' swfUrl=' +yoyo378 +' live=true pageUrl=' + url_frame
            comecarvideo(streamurl,nomecanal,True,zapping)
            

        elif re.search('veetle',url_frame) or re.search("src='http://veetle",link):
            print "Catcher: veetle"
            if selfAddon.getSetting("verif-veetle3") == "false":
                ok = mensagemok('TV Portuguesa','Necessita de instalar o addon veetle.','Este irá ser instalado já de seguida.')
                import extract
                urlfusion='http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.veetle/plugin.video.veetle-0.3.1.zip' #v2.3
                path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
                lib=os.path.join(path, 'plugin.video.veetle.zip')
                comuns.downloader(urlfusion,lib)
                addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
                xbmc.sleep(2000)
                dp = xbmcgui.DialogProgress()
                #if dp.iscanceled(): dp.close()
                dp.create("TV Portuguesa", "A instalar...")
                try:
                    extract.all(lib,addonfolder,dp)
                    ok = mensagemok('TV Portuguesa','Veetle instalado / actualizado.','Necessita de reiniciar o XBMC.')
                    selfAddon.setSetting('verif-veetle3',value='true')
                except:
                    ok = mensagemok('TV Portuguesa','Sem acesso para instalar Veetle. Instale o veetle','do repositório fightnight.','De seguida, active o Veetle nas definições do addon.')
            else:
                ## PATCH SPTHD IN LSHD
                if re.search('var urls = new Array',link):
                        framedupla=re.compile('new Array.+?"(.+?)".+?"(.+?)"').findall(link)[0]
                        if framedupla[0]==framedupla[1]: frame=framedupla[0]
                        else:
                            opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Escolha um stream da lista dos disponiveis.", "", "","Stream Extra", 'Stream Principal')
                            if opcao: frame=framedupla[0]
                            else: frame=framedupla[1]
                        descobrirresolver(frame, nomecanal,False,False)
                        return
                try:idembed=re.compile('/index.php/widget/index/(.+?)/').findall(link)[0]
                except: idembed=re.compile('/index.php/widget#(.+?)/true/16:9').findall(link)[0]
                print "ID embed: " + idembed
                try:
                    chname=comuns.abrir_url('http://fightnightaddons.x10.mx/tools/veet.php?id=' + idembed)
                    chname=chname.replace(' ','')
                    if re.search('DOCTYPE HTML PUBLIC',chname):
                        ok = mensagemok('TV Portuguesa','Erro a obter link do stream. Tenta novamente.')
                        return
                    print "ID final obtido pelo TvM."
                except:
                    chname=comuns.abrir_url('http://fightnight-xbmc.googlecode.com/svn/veetle/sporttvhdid.txt')
                    print "ID final obtido pelo txt."
                print "ID final: " + chname
                link=comuns.abrir_url('http://veetle.com/index.php/channel/ajaxStreamLocation/'+chname+'/flash')
                if re.search('"success":false',link): ok = mensagemok('TV Portuguesa','O stream está offline.')
                else:
                    streamfile='plugin://plugin.video.veetle/?channel=' + chname
                    comecarvideo(streamfile,nomecanal,True,zapping)

        elif re.search('wcast', link):
            print "Catcher: wcast"
            wcast=re.compile("fid='(.+?)';.+?></script>").findall(link)
            for chid in wcast:
                embed='http://www.wcast.tv/embed.php?u=' + chid+ '&vw=600&vh=470'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                swf='http://www.wcast.tv/player/player.swf'
                filelocation=re.compile("so.addVariable.+?'file'.+?'(.+?)'").findall(html)
                rtmpendereco=re.compile("so.addVariable.+?'streamer'.+?'(.+?)'").findall(html)
                streamurl=rtmpendereco[0] + ' playPath=' + filelocation[0] + ' swfUrl=' + swf + ' live=true swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('ucaster', link):
            print "Catcher: ucaster"
            ucaster=re.compile("channel='(.+?)',.+?></script>").findall(link)
            if not ucaster: ucaster=re.compile('flashvars="id=.+?&s=(.+?)&g=1&a=1&l=').findall(link)
            if not ucaster: ucaster=re.compile('src="/ucaster.eu.php.+?fid=(.+?)" id="innerIframe"').findall(link)
            if not ucaster: ucaster=re.compile('flashvars="id=.+?&amp;s=(.+?)&amp;g=1').findall(link)
            if not ucaster: ucaster=re.compile("flashvars='id=.+?&s=(.+?)&").findall(link)
            if not ucaster: ucaster=re.compile('flashvars="id=.+?id=.+?&amp;s=(.+?)&amp;g=1').findall(link)
            if not ucaster: ucaster=re.compile('channel="(.+?)".+?g="1"').findall(link)
            #if not ucaster:
                #mensagemok('TV Portuguesa','Stream não é o do site responsável','logo não é possível visualizar.')
            for chname in ucaster:
                embed='http://www.ucaster.eu/embedded/' + chname + '/1/600/430'
                try:
                    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                    html= comuns.abrir_url_tommy(embed,ref_data)
                    swf=re.compile('SWFObject.+?"(.+?)",').findall(html)[0]
                    flashvars=re.compile("so.addParam.+?'FlashVars'.+?'(.+?);").findall(html)[0]
                    flashvars=flashvars.replace("')","&nada").split('l=&')
                    if flashvars[1]=='nada':
                        nocanal=re.compile("&s=(.+?)&").findall(flashvars[0])[0]
                        chid=re.compile("id=(.+?)&s=").findall(html)[0]
                    else:
                        nocanal=re.compile("&s=(.+?)&nada").findall(flashvars[1])[0]
                        chid=re.compile("id=(.+?)&s=").findall(html)[1]
                    nocanal=nocanal.replace('&','')
                except:
                    nocanal=chname
                    chid=re.compile("flashvars='id=(.+?)&s").findall(link)[0]
                    swf=re.compile("true' src='http://www.ucaster.eu(.+?)'").findall(link)[0]
                link=comuns.abrir_url('http://www.ucaster.eu:1935/loadbalancer')
                rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
                streamurl='rtmp://' + rtmpendereco + '/live playPath=' + nocanal + '?id=' + chid + ' swfVfy=1 conn=S:OK live=true swfUrl=http://www.ucaster.eu' + swf + ' pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('xuuby',link): ##proteccao tvdez
            print "Catcher: xuuby"
            xuuby=re.compile('chname="(.+?)".+?</script>').findall(link)
            if not xuuby: xuuby=re.compile('chname=(.+?)&').findall(link)
            for chname in xuuby:
                embed='http://www.xuuby.com/show2.php?chname='+chname+'&width=555&height=555&a=1'
                ref_data = {'Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                html=urllib.unquote(html)
                streamurl=re.compile('file: "(.+?)"').findall(html)[0]
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('youtube.com/v',link):
            idvideo=re.compile('type="application/x-shockwave-flash" src="http://www.youtube.com/v/(.+?)&.+?"></object>').findall(link)[0]
            sources=[]
            import urlresolver
            embedvideo='http://www.youtube.com/watch?v=' + idvideo
            hosted_media = urlresolver.HostedMediaFile(url=embedvideo)
            sources.append(hosted_media)
            source = urlresolver.choose_source(sources)
            if source:
                streamurl=source.resolve()
                comecarvideo(streamurl,nomecanal,True,zapping)
                    

        elif re.search('yukons', link):
            print "Catcher: yukons"
            yukons=re.compile('kuyo&file=(.+?)&').findall(link)
            if not yukons: yukons=re.compile("file='(.+?)'.+?</script>").findall(link)
            if not yukons: yukons=re.compile('channel="(.+?)".+?</script>').findall(link)
            if not yukons: yukons=re.compile('file=(.+?)&').findall(link)
            for chname in yukons:
                idnumb='36353636373337303331363936433646'
                ref_data = {'Host': 'yukons.net','Connection': 'keep-alive','Accept': '*/*','Referer': url_frame,'User-Agent':user_agent}
                link= comuns.abrir_url_tommy('http://yukons.net/yaem/' + idnumb,ref_data)

                idfinal=re.compile("return '(.+?)'").findall(link)[0]
                embed='http://yukons.net/embed/'+idnumb+'/'+idfinal+'/650/500'
                ref_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': url_frame,'User-Agent':user_agent}
                html= comuns.abrir_url_tommy(embed,ref_data)
                
                idrtmp=re.compile('FlashVars\|id\|(.+?)\|').findall(html)[0]
                pidrtmp=re.compile('\|pid\|\|(.+?)\|').findall(html)[0]
                swfrtmp=re.compile('SWFObject\|.+?\|\|\|(.+?)\|swf\|eplayer').findall(html)[0]
                ref_data = {'Referer': 'http://yukons.net/' + swfrtmp + '.swf','User-Agent':user_agent}
                servertmp= comuns.abrir_url_tommy('http://yukons.net/srvload/'+ idrtmp,ref_data).replace('srv=','')

                streamurl='rtmp://' + servertmp + ':443/kuyo playPath=' + chname + '?id=' + idrtmp + '&pid=' + pidrtmp + ' swfUrl=http://yukons.net/'+swfrtmp + '.swf live=true conn=S:OK timeout=15 swfVfy=true pageUrl=' + embed
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('yycast', link): ##requires librtmp 14-9-2013
            print "Catcher: yycast"
            mensagemok("TV Portuguesa","Servidor incompativel.")
            #yycast=re.compile('fid="(.+?)";.+?</script><script type="text/javascript" src="http://www.yycast.com/javascript/embedPlayer.js"></script>').findall(link)
            #if not yycast: yycast=re.compile("file='(.+?).flv'.+?</script>").findall(link)
            #if not yycast: yycast=re.compile('fid="(.+?)".+?</script>').findall(link)
            #if not yycast: yycast=re.compile('channel="(.+?)".+?</script>').findall(link)
            #for chname in yycast:
            #    embed='http://yycast.com/embedded/'+ chname + '/1/555/435'
            #    ref_data = {'Referer': url_frame,'User-Agent':user_agent}
            #    html= comuns.abrir_url_tommy(embed,ref_data)
            #    #print html
            #    link=comuns.abrir_url('http://yycast.com:1935/loadbalancer')
            #    rtmpendereco=re.compile(".*redirect=([\.\d]+).*").findall(link)[0]
            #    print rtmpendereco                
            #    #so.addParam('FlashVars', 'id=1516&s=sic880809&g=1&a=1&l=');
            #    swf=re.compile('SWFObject.+?"(.+?)"').findall(html)[0]
            #    idnum=re.compile("'FlashVars', 'id=(.+?)&s=.+?'").findall(html)[0]
            #    chnum=re.compile("'FlashVars', 'id=.+?&s=(.+?)&").findall(html)[0]
            #    #streamurl='rtmp://yycast.com:1935/live/_definst_/sicasdf. app=live playPath=' + chnum + '?id=' + idnum + ' swfVfy=1 timeout=15 conn=S:OK live=true swfUrl=http://yycast.com' + swf + ' pageUrl=' + embed
            #    streamurl='rtmp://' + rtmpendereco + '/live/ playPath=' + chnum + '?id=' + idnum + ' swfVfy=1 timeout=15 conn=S:OK live=true swfUrl=http://yycast.com' + swf + ' pageUrl=' + embed
            #    #print html
            #    #streamurl='rtmp://live.yycast.com/lb playPath=' + chname + ' live=true timeout=15 swfUrl=http://cdn.yycast.com/player/player.swf pageUrl=http://www.yycast.com/embed.php?fileid='+chname+'&vw=768&vh=432'
            #    comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('zcast.us', link):
            print "Catcher: zcast"
            zcast=re.compile('channel="(.+?)";.+?></script>').findall(link)
            for chname in zcast:
                embed='http://zcast.us/gen.php?ch=' + chname + '&width=700&height=480'
                streamurl='rtmp://gabon.zcast.us/liveedge' + ' playPath=' + url_frame + ' live=true timeout=15 swfVfy=1 swfUrl=http://player.zcast.us/player58.swf pageUrl=http://www.xuuby.com/'
                comecarvideo(streamurl,nomecanal,True,zapping)

        elif re.search('<p><script language="JavaScript">setTimeout', link):
            print "Catcher: tvtuga zuuk"
            ptcanal=comuns.redirect(re.compile('setTimeout.+?"window.open.+?' + "'(.+?)',").findall(link)[0])
            html=urllib.unquote(comuns.abrir_url(ptcanal))
            descobrirresolver(ptcanal,nomecanal,html,zapping)

        else:
            print "Catcher: noserver" 
            ok=mensagemok('TV Portuguesa','Servidor não suportado')
            mensagemprogresso.close()
    except Exception:
        mensagemprogresso.close()
        mensagemok('TV Portuguesa','Servidor não suportado.')
        (etype, value, traceback) = sys.exc_info()
        print etype
        print value
        print traceback
        #buggalo.onExceptionRaised()

def iniciagravador(finalurl,siglacanal,name,directo):
    if downloadPath=='':
        xbmcgui.Dialog().ok('TV Portuguesa','Necessitas de introduzir a pasta onde vão ficar','as gravações. Escolhe uma pasta com algum espaço','livre disponível.')
        dialog = xbmcgui.Dialog()
        pastafinal = dialog.browse(int(3), "Escolha pasta para as gravações", 'files')
        selfAddon.setSetting('pastagravador',value=pastafinal)
        return
    if directo==True:
        if re.search('rtmp://',finalurl):
            finalurl=finalurl.replace('playPath=','-y ').replace('swfVfy=1','').replace('conn=','-C ').replace('live=true','-v').replace('swfUrl=','-W ').replace('pageUrl=','-p ').replace('token=','-T ').replace('app=','-a ')
            import gravador
            gravador.verifica_so(' -r ' + finalurl,name,siglacanal,directo)
        else: xbmc.executebuiltin("XBMC.Notification(TV Portuguesa, Stream não gravável. Escolha outro.,'100000'," + tvporpath + art + "icon32-ver1.png)")


def comecarvideo(finalurl,name,directo,zapping,thumb=''):
    listacanaison=selfAddon.getSetting("listacanais")
    siglacanal=''
    namega=name.replace('-','')
    comuns.GA("player",namega)
    if directo==True:
        thumb=name.replace('Mais TVI-','maistvi-ver2.png').replace('AXN-','axn-ver2.png').replace('FOX-','fox-ver2.png').replace('RTP 1-','rtp1-ver2.png').replace('RTP 2-','rtp2-ver2.png').replace('SIC-','sic-ver3.png').replace('SPORTTV 1-','sptv1-ver2.png').replace('SPORTTV 1 HD-','sptv1-ver2.png').replace('SPORTTV 2-','sptv2-ver2.png').replace('SPORTTV 3-','sptv3-ver2.png').replace('SPORTTV LIVE-','sptvlive-ver1.png').replace('TVI-','tvi-ver2.png').replace('Discovery Channel-','disc-ver2.png').replace('AXN Black-','axnb-ver2.png').replace('AXN White-','axnw-ver2.png').replace('FOX Crime-','foxc-ver2.png').replace('FOX Life-','foxl-ver3.png').replace('FOX Movies-','foxm-ver2.png').replace('Eurosport-','eusp-ver2.png').replace('Hollywood-','hwd-ver2.png').replace('MOV-','mov-ver2.png').replace('Canal Panda-','panda-ver2.png').replace('VH1-','vh1-ver2.png').replace('Benfica TV-','bentv-ver2.png').replace('Porto Canal-','pcanal-ver2.png').replace('Big Brother VIP-','bbvip-ver2.png').replace('SIC K-','sick-ver2.png').replace('SIC Mulher-','sicm-ver3.png').replace('SIC Noticias-','sicn-ver2.png').replace('SIC Radical-','sicrad-ver2.png').replace('TVI24-','tvi24-ver2.png').replace('TVI Ficção-','tvif-ver2.png').replace('Syfy-','syfy-ver1.png').replace('Odisseia-','odisseia-ver1.png').replace('História-','historia-ver1.png').replace('National Geographic Channel-','natgeo-ver1.png').replace('MTV-','mtv-ver1.png').replace('CM TV-','cmtv-ver1.png').replace('RTP Informação-','rtpi-ver1.png').replace('Disney Channel-','disney-ver1.png').replace('Motors TV-','motors-ver1.png').replace('ESPN America-','espna-ver1.png').replace('Fashion TV-','fash-ver1.png').replace('A Bola TV-','abola-ver1.png').replace('Casa dos Segredos 4-','casadseg-ver1.png').replace('RTP Açores-','rtpac-ver1.png').replace('RTP Internacional-','rtpint-ver1.png').replace('RTP Madeira-','rtpmad-ver1.png').replace('RTP Memória-','rtpmem-ver1.png').replace('RTP Africa-','rtpaf-ver1.png')
        name=name.replace('-','')
        progname=name
        if selfAddon.getSetting("prog-player3") == "true":
            try:
                siglacanal=name.replace('SPORTTV 1','SPTV1').replace('SPORTTV 2','SPTV2').replace('SPORTTV 3','SPTV3').replace('SPORTTV LIVE','SPTVL').replace('Discovery Channel','DISCV').replace('AXN Black','AXNBL').replace('AXN White','AXNWH').replace('FOX Crime','FOXCR').replace('FOX Life','FLIFE').replace('FOX Movies','FOXM').replace('Eurosport','EURSP').replace('Hollywood','HOLLW').replace('Canal Panda','PANDA').replace('Benfica TV','SLB').replace('Porto Canal','PORTO').replace('Big Brother VIP','BBV').replace('SIC K','SICK').replace('SIC Mulher','SICM').replace('SIC Noticias','SICN').replace('SIC Radical','SICR').replace('TVI24','TVI24').replace('TVI Ficção','TVIFIC').replace('Mais TVI','SEM').replace('Syfy-','SYFY').replace('Odisseia','ODISS').replace('História','HIST').replace('National Geographic Channel','NGC').replace('MTV','MTV').replace('CM TV','CMTV').replace('RTP Informação','RTPIN').replace('Disney Channel','DISNY').replace('Motors TV','MOTOR').replace('ESPN America','SEM').replace('Fashion TV','FASH').replace('MOV','SEM').replace('A Bola TV','ABOLA')
                progname=p_umcanal(p_todos(),siglacanal,'nomeprog')
                if progname=='':pass
                else: name=name + ' ' + progname
            except: pass
        listitem = xbmcgui.ListItem(progname, iconImage="DefaultVideo.png", thumbnailImage=tvporpath + art + thumb)
    else: listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
    if zapping==True:
        conteudoficheiro=comuns.openfile(('zapping'))
        comuns.savefile(('zapping', conteudoficheiro + '_comeca_' + name + '_nomecanal_' + finalurl + '_thumb_' + thumb + '_acaba_'))
    else:

        #finalurl,spscpid=libalternativo(finalurl)
        spscpid='nada'
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(finalurl, listitem)
        mensagemprogresso.close()
        dialogWait = xbmcgui.DialogProgress()
        dialogWait.create('TV Portuguesa', 'A carregar...')
        dialogWait.close()
        del dialogWait
        lat123 = menulateral("menulateral.xml" , tvporpath, "Default",finalurl=finalurl,name=name,siglacanal=siglacanal,directo=directo)
        
        player = Player(finalurl=finalurl,name=name,siglacanal=siglacanal,directo=directo,spscpid=spscpid)
        if "RunPlugin" in finalurl:
            xbmc.executebuiltin(finalurl)
        else:

            player.play(playlist)
            while player.is_active:
                if listacanaison == "true":
                    if xbmc.getCondVisibility('Window.IsActive(videoosd)') and directo==True:
                        xbmc.executebuiltin('XBMC.Control.Move(videoosd,9999)')
                        lat123.doModal()
                        while xbmc.getCondVisibility('Window.IsActive(videoosd)'): pass
                player.sleep(1000)
            #if not player.is_active:
            #    print "Parou. Saiu do ciclo."
            #    sys.exit(0)
                
                #player.sleep(10000)
            #print "ERRO"

class Player(xbmc.Player):
      def __init__(self,finalurl,name,siglacanal,directo,spscpid):
            if selfAddon.getSetting("playertype") == "0": player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            elif selfAddon.getSetting("playertype") == "1": player = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
            elif selfAddon.getSetting("playertype") == "2": player = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
            elif selfAddon.getSetting("playertype") == "3": player = xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER)
            else: player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            self.is_active = True
            self._refInfo = True
            self._totalTime = 999999
            self._finalurl=finalurl
            self._name=name
            self._siglacanal=siglacanal
            self._directo=directo
            self._spscpid=spscpid
            print "Criou o player"
            #player.stop()

      def onPlayBackStarted(self):
            print "Comecou o player"
                              
      def onPlayBackStopped(self):
            print "Parou o player"
            self.is_active = False
            #import newrtmp
            #newrtmp.stop_stream(self._spscpid)
            #opcao= xbmcgui.Dialog().yesno("TV Portuguesa", "Este stream funciona? ", "(exemplificação / ainda não funciona)", "",'Sim', 'Não')
            ###### PERGUNTAR SE O STREAM E BOM #####            

      def onPlayBackEnded(self):              
            self.onPlayBackStopped()
            print 'Chegou ao fim. Playback terminou.'


      def sleep(self, s): xbmc.sleep(s) 

class PlaybackFailed(Exception):
      '''XBMC falhou a carregar o stream'''

MODE_EPG = 'EPG'
MODE_TV = 'TV'
MODE_OSD = 'OSD'

ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_UP = 3
ACTION_DOWN = 4
ACTION_PAGE_UP = 5
ACTION_PAGE_DOWN = 6
ACTION_SELECT_ITEM = 7
ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10
ACTION_SHOW_INFO = 11
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15

ACTION_MOUSE_WHEEL_UP = 104
ACTION_MOUSE_WHEEL_DOWN = 105
ACTION_MOUSE_MOVE = 107

KEY_NAV_BACK = 92
KEY_CONTEXT_MENU = 117
KEY_HOME = 159
C_CHANNELS_LIST=6000

##################################MENU LATERAL######################
class menulateral(xbmcgui.WindowXMLDialog):

    def __init__( self, *args, **kwargs ):
            xbmcgui.WindowXML.__init__(self)
            self.finalurl = kwargs[ "finalurl" ]
            self.siglacanal = kwargs[ "siglacanal" ]
            self.name = kwargs[ "name" ]
            self.directo = kwargs[ "directo" ]

    def onInit(self):
        self.updateChannelList()

    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK, KEY_CONTEXT_MENU]:
            self.close()
            return

    def onClick(self, controlId):
        if controlId == 4001:
            self.close()
            request_servidores('','[B]%s[/B]' %(self.name))

        elif controlId == 40010:
            self.close()
            iniciagravador(self.finalurl,self.siglacanal,self.name,self.directo)

        elif controlId == 203:
            #xbmc.executebuiltin("XBMC.PlayerControl(stop)")
            self.close()

        elif controlId == 6000:
            listControl = self.getControl(C_CHANNELS_LIST)
            item = listControl.getSelectedItem()
            nomecanal=item.getProperty('chname')
            self.close()
            request_servidores('',nomecanal)

        
        #else:
        #    self.buttonClicked = controlId
        #    self.close()

    def onFocus(self, controlId):
        pass

    def updateChannelList(self):
        idx=-1
        listControl = self.getControl(C_CHANNELS_LIST)
        listControl.reset()
        canaison=comuns.openfile(('canaison'))
        canaison=canaison.replace('[','')
        lista=re.compile('B](.+?)/B]').findall(canaison)
        for nomecanal in lista:
            idx=int(idx+1)
            if idx==0: idxaux=' '
            else:
                idxaux='%4s.' % (idx)
                item = xbmcgui.ListItem(idxaux + ' %s' % (nomecanal), iconImage = '')
                item.setProperty('idx', str(idx))
                item.setProperty('chname', '[B]' + nomecanal + '[/B]')
                listControl.addItem(item)
        
    def updateListItem(self, idx, item):
        channel = self.channelList[idx]
        item.setLabel('%3d. %s' % (idx+1, channel.title))
        item.setProperty('idx', str(idx))

    def swapChannels(self, fromIdx, toIdx):
        if self.swapInProgress: return
        self.swapInProgress = True

        c = self.channelList[fromIdx]
        self.channelList[fromIdx] = self.channelList[toIdx]
        self.channelList[toIdx] = c

        # recalculate weight
        for idx, channel in enumerate(self.channelList):
            channel.weight = idx

        listControl = self.getControl(C_CHANNELS_LIST)
        self.updateListItem(fromIdx, listControl.getListItem(fromIdx))
        self.updateListItem(toIdx, listControl.getListItem(toIdx))

        listControl.selectItem(toIdx)
        xbmc.sleep(50)
        self.swapInProgress = False
