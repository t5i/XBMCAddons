# -*- coding: utf-8 -*-

"""
    Plugin for streaming video content from Hidabroot
"""
import urllib, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import HTMLParser
import BeautifulSoup
import urlparse
import json
from xml.sax import saxutils as su



##General vars
### http://www.hidabroot.org/he/vod_categories/10/all/all/all/0?SupplierID=1&page=0%2C99
__plugin__ = "addons://sources/video/Zamir"
__author__ = "t5i"

base_domain="www.hidabroot.org"
baseVOD_url = "http://rabbizamircohen.org/Webservices/GetAllVideo.php"
baseVOD_urlGlobl="http://www.hidabroot.org"
base_url = sys.argv[0]

__settings__ = xbmcaddon.Addon(id='plugin.video.Zamir')

__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
__DEBUG__       = __settings__.getSetting('DEBUG') == 'true'

LIB_PATH = xbmc.translatePath( os.path.join( __PLUGIN_PATH__, 'resources', 'appCaster' ) )

import CommonFunctions
common = CommonFunctions
common.plugin = "plugin.video.Zamir"

def build_XBMCurl(query):
	return base_url + '?' + urllib.urlencode(query)


def playMovie(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36')
	#req.add_header('Cookie', 'visid_incap_172050=p38EPb70SDKdiG5ET58Q1Y1qv1QAAAAAQUIPAAAAAAAZe7rcEcv5x02MxQ2ETK0o; incap_ses_264_172050=oTvpMEi/eBHltm1z3eqpA3tvGVUAAAAAO2gzlNYBuURCjCKde3pqqQ==; _gat=1; has_js=1; _ga=GA1.2.1227030176.1421830788')
	#req.add_header('referer','http://www.hidabroot.org/he/video/70494')
	print req
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()    
	media=re.compile('<a href="(.*?)"<span style').findall(link)
	print ("the vk link is "+  str(media))
	addFinalLink(media[0],str(name))

def get_params():
        param=[]
        paramstring=sys.argv[2]
        hndl=sys.argv[1]
        print "sys.argv[1] ->"+hndl
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

def GetPageNLink(uri):
	print "req URL = " + uri
	req = urllib2.Request(uri)
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link


def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url) +"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	#u= build_XBMCurl({'mode': 'folder', 'foldername': name,'httplink': url})#sys.argv[0]+ url 
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDirNextPage(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url) +"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	#u= build_XBMCurl({'mode': 'folder', 'foldername': name,'httplink': url})#sys.argv[0]+ url 
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="folder", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
    
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
#
#http://rabbizamircohen.org/Images/10072008_????_????_-_???_?`_10102011140129605.jpg
#http://rabbizamircohen.org/Videos/Pirke-Avot-part-A.mp4

def GetLinksPage (uri):

	links=GetPageNLink(uri)
	jsonObject = json.loads(links)
	
	#match=re.compile('(<div class="views-field views-field-title">.*?</div>)').findall(links) # Videos
	#print "uri ------------------------------------------------------------------------------------ views-field views-field-title  "
	#print links
	print "next pageeeepageeeepageeeepageeeepageeeepageeeepageeeepageeeepageeee" 
	parent =  jsonObject["Video"]
	json_string = json.dumps(jsonObject,sort_keys=True,indent=2)
	for item in parent:
		sFile = item["videoFile"].encode('utf-8').strip()
		sName = item["name"].encode('utf-8').strip()
		sCat = item["category"].encode('utf-8').strip()
		sImg = item["imgThumb"].encode('utf-8').strip()
		addLink(sName,"http://rabbizamircohen.org/Videos/" + sFile, "http://rabbizamircohen.org/Images/" + sImg)#addDir(sName,sFile,"1","")
		#print sName, "  --  "  , sCat
	##addDirNextPage("..הבא..",baseVOD_url+str(iPage),2,"")
	xbmcplugin.endOfDirectory(int(sys.argv[1]))	

	 
	##print "-------------------"
	##sPage=uri.split("=")[2].split("C")[1]
	##iPage=int(sPage)+1
	##print iPage
	##for url in match:
	##	matchVidURL=re.compile('<a href="(/he/video/.*?)">(.*?)</a>').findall(url)
	##	for name,uri in matchVidURL:
	##		addDir(uri,name,"1","")
	##		#addLink(uri,name,"")
	##addDirNextPage("..הבא..",baseVOD_url+str(iPage),2,"")
	##xbmcplugin.endOfDirectory(int(sys.argv[1]))


def GetLinkVideo(uri,name,iconimage):
	html=""
	html=GetPageNLink(uri)
	matchVid=re.compile('<source src="(.*?)" />').findall(html)
	print matchVid[0]
	addLink("",matchVid[0],"")
	playMovie(matchVid[0],"")


def playMovie(uri,title):	
	li = xbmcgui.ListItem('Hrav Zamir')
	xbmc.Player().play(item=uri, listitem=li)
	 

params=get_params()
print "test"

args = urlparse.parse_qs(sys.argv[2][1:])
print args
mode = args.get('mode', None)
urll=args.get('url')
FolderMode='1'
NextPage='2'
print urll

###links=GetPageNLink(baseVOD_url)
#GetLinksPage(baseVOD_url)

print "mode="+str(mode) + "   url=" + str(urll) + "    len=" + str(len(str(urll)))


if mode==None or urll==None or len(urll)<1:
	GetLinksPage(baseVOD_url)
else:
	if mode[0]==FolderMode:
		print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
		GetLinkVideo(baseVOD_urlGlobl+urll[0],"","")
	else:
		if mode[0] == NextPage:
			print "222"
			GetLinksPage(urll[0])


xbmcplugin.setPluginFanart(int(sys.argv[1]),xbmc.translatePath( os.path.join( __PLUGIN_PATH__, "fanart.png") ))
xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
