import xbmc,xbmcaddon,subprocess,os,re

selfAddon = xbmcaddon.Addon(id='plugin.video.tvpor')
addonPath= selfAddon.getAddonInfo("path")
if xbmc.getCondVisibility('system.platform.windows'):
    libpath=os.path.join(addonPath,'resources','rtmpgw','rtmp-windows.exe')
if xbmc.getCondVisibility('system.platform.linux'):
    if os.uname()[4] == "armv6l": libpath=os.path.join(addonPath,'resources','rtmpgw','rtmp-rpi')

print libpath

def start_stream(rtmp=''):
    if rtmp=='':
        print "EMPTY RTMP"
        return
    if re.search('rtmp://',rtmp) or re.search('rtmpe://',rtmp):
        cmd = [libpath, '-D', '127.0.0.1', '-g','9000']
        spsc = subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None)
        print spsc
        temp=rtmp.replace('playPath=','&y=').replace('swfVfy=1','').replace('conn=','&C=').replace('live=true','').replace('swfUrl=','&W=').replace('pageUrl=','&p=').replace('token=','&T=').replace('app=','&a=').replace('timeout=','&m=').replace(' ','')
        final='http://127.0.0.1:9000/?r=%s' % (temp)
        return final,spsc
    else:
        return rtmp,''

def stop_stream(spsc):
    if xbmc.getCondVisibility('system.platform.windows'):
        subprocess.Popen('taskkill /F /IM rtmp-windows.exe /T',shell=True)
    else:
        try:spsc.kill()
        except:pass
        xbmc.sleep(100)
        try:spsc.wait()
        except:pass
        xbmc.sleep(100)         
