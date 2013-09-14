# -*- coding: UTF-8 -*-

# for utf-8 see http://www.python.org/dev/peps/pep-0263/

import xbmc
import xbmcplugin
import xbmcgui
import sys
import re

import urllib
import urllib2
import urlparse
import json

"""
FUNCTION PRINCIPALI
"""

# elenca le pagine disponibili
def showVideoIndex(start):
	global pluginPid

	url = "http://www.jw.org/it/video/?start=" + str(start)
	print "JWORG VIDEO url: " + url

	html = loadUrl (url)

	# Recupero link delle pagine

	regexp_video_pages = '<a href="[^"]+=([0-9]+)" class="pageNum">([0-9]+)</a>'
	other_pages = re.findall(regexp_video_pages, html)
	
	# print other_pages
	"""
	grazie a set() forzo l'univocità 
	[i link di cambio pagina sono presenti sia in cima che sotto la pagina]
	riguardo a set see comments here: http://www.peterbe.com/plog/uniqifiers-benchmark
	
	ottengo una lista di coppie start index, page num
	 [('10', '2'), ('20', '3'), ('30', '4'), ('40', '5'), ('50', '6')]
	grazie a come è fatto il sito della società, la pagina corrente è automaticamente esclusa
	il link non matcha
	"""
	other_pages =  list(set(other_pages))
	other_pages.sort()

	# Recupero titoli dei video
	# C'è una sola regexp quindi è una semplice lista, un array non associativo
	regexp_video_title = 'data-onpagetitle="([^"]+)"'
	videos = re.findall(regexp_video_title, html) 

	# Recupero immagine "locandina" del video
	regexp_video_poster = '<img src=["\'](assets[^"\']+)["\']'
	posters = re.findall(regexp_video_poster, html)

	regexp_video_json = 'data-jsonurl="([^"]+)"';
	video_json = re.findall(regexp_video_json, html)

	print "JWORG video_json: " 
	print video_json

	count = 0
	for title in videos:
		# print "JWORG title n. " + str(count) + ": " + title + " image at: " + posters[count]
		listItem = xbmcgui.ListItem(
			label=title, 
			thumbnailImage= "http://www.jw.org/" + posters[count]
		)
		# TODO: link termporaneo
		params = {"content_type" : "video", "mode" : "open_json_video", "json_url": video_json[count]} 
		url = sys.argv[0] + '?' + urllib.urlencode(params)
		xbmcplugin.addDirectoryItem(
			handle=pluginPid, 
			url=url, 
			listitem=listItem, 
			isFolder=True 
		)  
		count = count + 1

	# Link alle pagine
	for page in other_pages:
		next_start =  page[0] 
		pagina = page[1] 
		title = "Vai a pagina " + str(page[1])
		print "JWORG title " + title
		listItem = xbmcgui.ListItem(title)
		params = {"content_type" : "video", "start" : next_start} 
		url = sys.argv[0] + '?' + urllib.urlencode(params)
		print "JWORG list url " + url
		xbmcplugin.addDirectoryItem(handle=pluginPid, url=url, listitem=listItem, isFolder=True )  
		

	xbmcplugin.endOfDirectory(handle=pluginPid)
	
	
def showVideoJsonUrl(json_url):
	# print "JWORG video json url: " + json_url
	#  /apps/I_TRGCHlZRQVNYVrXF?fileformat=mp4&output=json&pub=ivfe&langwritten=I&alllangs=1
	json = loadJsonFromUrl("http://www.jw.org" + json_url)

	language_code = None;
	for language in  json["languages"]:
		locale =  json["languages"][language]["locale"]
		if locale == "it":
			language_code = language
			break

	#adesso ho in locale una lettera tipo 'I' per l'italiano per accedere all'url del file
	if language_code == None:
		xbmcgui.Dialog().ok("jworg browser", "Sembra che il file non sia disponibile nella tua lingua")
		return

	options = []
	mp4_to_play = []
	for mp4 in json["files"][language_code]["MP4"]:
		url = mp4["file"]["url"]
		res = mp4["label"]
		title = mp4["title"]
		title = "[" + res + "] - " + title
		# print mp4
		print url
		mp4_to_play.append(url);
		options.append(title.encode('utf8'))
		print title.encode('utf8')
	
	dia = xbmcgui.Dialog()
	selected = dia.select("Scegli cosa guardare", options)
	
	print "JWOORG Hai scelto " + str(selected)
	print "JWORG I'll play " + mp4_to_play[selected]
	xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(mp4_to_play[selected])
	

"""
UTILITY
"""
def loadUrl (url):
	response = urllib2.urlopen(url)
	html = response.read()
	return html	


def loadJsonFromUrl (url):
	response = urllib2.urlopen(url)
	data = json.load(response)
	return data

"""
START
"""


# Usato in tutte le chiamate ad addDirectory
pluginPid    = int(sys.argv[1])
print "JWORG pluginPid " + str(pluginPid)


# Stampo per debug gli argomenti della chiamata
params 		 = urlparse.parse_qs((sys.argv[2])[1:])
print "JWORG argomenti lancio: " 
print sys.argv
print params

content_type = "video"
try:
	content_type = params["content_type"][0]
except:
	pass

mode = None
try:	
	mode = params["mode"][0]
except:
	pass

start = 0
try:
	start = params["start"][0]        
except:
    pass

if content_type == "video" and mode is None:
	showVideoIndex(start);

if content_type == "video" and mode == "open_json_video":
	json_url = params["json_url"][0]
	showVideoJsonUrl(json_url);


