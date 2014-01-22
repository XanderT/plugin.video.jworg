# -*- coding: UTF-8 -*-

import xbmc
import xbmcgui
import xbmcaddon

import sys
import urlparse
import os

import jw_common

# key is english name, value is the name of the locale IN the locale
# used for first run if no language setted. It takes XBMC language setting
# and convert into "our" locale settings

# <setting id="language" type="labelenum" label="30002" 
# values="Afrikaans|Deutsch|English|Español|Français|Ελληνική|Italiano|Magyar|Nederlands|Polski|Português"  />

# *** IMPORTANT: keep it in the same order of the "language" setting values
locale_2_lang = {
	"Afrikaans"				: "Afrikaans",
	"German"				: "Deutsch",
	"English"				: "English",
	"Spanish"				: "Español",
	"French"				: "Français",
	"Greek"					: "Ελληνική",
	"Italian"				: "Italiano",
	"Hungarian"				: "Magyar",
	"Dutch"					: "Nederlands",
	"Polish"				: "Polski",
	"Portuguese" 			: "Português",
}


main_url = "http://www.jw.org/"
app_url ="http://www.jw.org/apps/"
wol_url = "http://wol.jw.org/wol/"

const = {
	"Italiano" 	: {
		"lang_code"					: "I",
		"url_lang_code"				: "it",
		"video_path" 				: "video",
		
		"bible_index_audio"			: "pubblicazioni/bibbia/nwt/libri/",
		"magazine_index"			: "pubblicazioni/riviste/",
		'has_simplified_edition'	: False,

		"music_index"				: "pubblicazioni/musica-cantici/",
		"dramas_index"				: "pubblicazioni/drammi-biblici-audio/",
		"dramatic_reading_index"	: "pubblicazioni/brani-biblici-recitati/",
		
		'wol'						: "r6/lp-i",
		"date_format"				: "%d/%m/%Y",
		"news_index"				: "news/",
		"activity_index"			: "testimoni-di-geova/attivit%C3%A0/",

		"sign_index"				: "apps/I_QrYQZRQVNFVTr?selLang=ISL",
 	},
 	"Magyar" : {
		"lang_code"					: "H",
		"url_lang_code"				: "hu",
		"video_path" 				: "videok",
		
		"bible_index_audio"			: "kiadvanyok/biblia/nwt/könyvek/",
		"magazine_index"			: "kiadvanyok/folyoiratok/",
		'has_simplified_edition'	: False,

		"music_index"				: "kiadvanyok/zene-enekek/",
		"dramas_index"				: False,
		"dramatic_reading_index"	: "kiadvanyok/bibliai-hangjatekok/",
		
		'wol'						: "r17/lp-h",
		"date_format"				: "%d/%m/%Y",
		"news_index"				: "hirek/",
		"activity_index"			: "jehova-tanui/tevekenysegek/",

		"sign_index"				: "apps/H_QrYQZRQVNFVTr?selLang=HDF",
 	},
 	"Français" : {
		"lang_code"					: "F",
		"url_lang_code"				: "fr",
		"video_path" 				: "videos",
		
		"bible_index_audio"			: "publications/bible/nwt/livres/",
		"magazine_index"			: "publications/revues/",
		'has_simplified_edition'	: True,

		"music_index"				: "publications/musique-cantiques/",
		"dramas_index"				: "publications/representations-dramatiques/",
		"dramatic_reading_index"	: "publications/lectures-bibliques-theatrales/",
		
		'wol'						: "r30/lp-f",
		"date_format"				: "%d/%m/%Y",
		"news_index"				: "actualites/",
		"activity_index"			: "temoins-de-jehovah/activites/",

		"sign_index"				: "apps/F_QrYQZRQVNFVTr?selLang=LSF",
 	},
	"English" 	: {
		"lang_code"					: "E",
		"url_lang_code"				: "en",
		"video_path" 				: "videos",
		
		"bible_index_audio"			: "publications/bible/nwt/books/" ,
		"magazine_index"			: "publications/magazines/",
		'has_simplified_edition'	: True,

		"music_index"				: "publications/music-songs/",
		"dramas_index"				: "publications/audio-bible-dramas/",
		"dramatic_reading_index"	: "publications/dramatic-bible-readings/",

		'wol'						: "r1/lp-e",
		"date_format"				: "%Y-%m-%d",
		"news_index"				: "news/",
		"activity_index"			: "jehovahs-witnesses/activities/",

		"sign_index"				: "apps/E_QrYQZRQVNFVTr?selLang=BSL",
	},
	"Polski" 	: {
		"lang_code"					: "P",
		"url_lang_code"				: "pl",
		"video_path" 				: "filmy",
		
		"bible_index_audio"			: "publikacje/biblia/nwt/ksi%C4%99gi-biblijne/" , 
		"magazine_index"			: "publikacje/czasopisma/",
		'has_simplified_edition'	: False,

		"music_index"				: "publikacje/muzyka-pie%C5%9Bni/",
		"dramas_index"				: "publikacje/s%C5%82uchowiska-biblijne/",
		"dramatic_reading_index"	: "publikacje/adaptacje-d%C5%BAwi%C4%99kowe-biblii/",
		
		'wol'						: "r12/lp-p",
		"date_format"				: "%d-%m-%Y",
		"news_index"				: "wiadomo%C5%9Bci/",
		"activity_index"			: "%C5%9Bwiadkowie-jehowy/dzia%C5%82alno%C5%9B%C4%87/",

		"sign_index"				: "apps/P_QrYQZRQVNFVTr?selLang=PDF",
	},	
	"Nederlands" : {
		"lang_code"					: "O",
		"url_lang_code"				: "nl",
		"video_path" 				: "videos",

		"bible_index_audio"			: "publicaties/bijbel/nwt/boeken/" , 
		"magazine_index"			: "publicaties/tijdschriften/",
		'has_simplified_edition'	: False,

		"music_index"				: "publicaties/muziek-liederen/",
		"dramas_index"				: "publicaties/audio-bijbel-dramas/",
		"dramatic_reading_index"	: "publicaties/bijbelse-hoorspelen/",
		
		'wol'						: "r18/lp-o",
		"date_format"				: "%d-%m-%Y",
		"news_index"				: "nieuws/",
		"activity_index"			: "jehovahs-getuigen/activiteiten/",

		"sign_index"				: "apps/O_QrYQZRQVNFVTr?selLang=NGT",
	},	
	"Español" : {
		"lang_code"					: "S",
		"url_lang_code"				: "es",
		"video_path" 				: "videos",

		"bible_index_audio"			: "publicaciones/biblia/nwt/libros/" , 
		"magazine_index"			: "publicaciones/revistas/",
		'has_simplified_edition'	: True,

		"music_index"				: "publicaciones/m%C3%BAsica-c%C3%A1nticos/",
		"dramas_index"				: "publicaciones/audio-representaciones-dram%C3%A1ticas/",
		"dramatic_reading_index"	: "publicaciones/lecturas-b%C3%ADblicas-dramatizadas/",
		
		'wol'						: "r4/lp-s",
		"date_format"				: "%d-%m-%Y",
		"news_index"				: "noticias/",
		"activity_index"			: "testigos-de-jehov%C3%A1/qui%C3%A9nes-somos-y-qu%C3%A9-hacemos/",

		"sign_index"				: "apps/S_QrYQZRQVNFVTr?selLang=LSE",
	},	
	"Deutsch" : {
		"lang_code"					: "X",
		"url_lang_code"				: "de",
		"video_path" 				: "videos",

		"bible_index_audio"			: "publikationen/bibel/nwt/bibelbuecher/" , 
		"magazine_index"			: "publikationen/zeitschriften/",
		'has_simplified_edition'	: False,

		"music_index"				: "publikationen/musik-lieder/",
		"dramas_index"				: "publikationen/biblische-hoerspiele/",
		"dramatic_reading_index"	: "publikationen/dramatische-bibellesungen/",
		
		'wol'						: "r10/lp-x",
		"date_format"				: "%d-%m-%Y",
		"news_index"				: "aktuelle-meldungen/",
		"activity_index"			: "jehovas-zeugen/aktivitaeten/",

		"sign_index"				:  "apps/X_QrYQZRQVNFVTr?selLang=DGS",
	},		
	"Português" : {
		"lang_code"					: "T",
		"url_lang_code"				: "pt",
		"video_path" 				: "videos",

		"bible_index_audio"			: "publicacoes/biblia/nwt/livros/" , 
		"magazine_index"			: "publicacoes/revistas/",
		'has_simplified_edition'	: True,

		"music_index"				: "publicacoes/musica-canticos/",
		"dramas_index"				: "publicacoes/dramas-biblicos-em-audio/",
		"dramatic_reading_index"	: "publicacoes/leituras-biblicas-dramatizadas/",
		
		'wol'						: "r5/lp-t",
		"date_format"				: "%d-%m-%Y",
		"news_index"				: "noticias/",
		"activity_index"			: "testemunhas-de-jeova/atividades/",

		"sign_index"				: "apps/T_QrYQZRQVNFVTr?selLang=LGP",
	},		
	"Afrikaans" : {
		"lang_code"					: "AF",
		"url_lang_code"				: "af",
		"video_path" 				: "videos",

		"bible_index_audio"			: False, 
		"magazine_index"			: False,
		'has_simplified_edition'	: False,

		"music_index"				: "publikasies/musiek-liedere/",
		"dramas_index"				: "publikasies/bybelse-klankdramas/",
		"dramatic_reading_index"	: "publikasies/gedramatiseerde-bybelvoorlesings/",
		
		'wol'						: "r52/lp-af",
		"date_format"				: "%Y-%m-%d",
		"news_index"				: "nuus/",
		"activity_index"			: "jehovah-se-getuies/bedrywighede/",

		"sign_index"				: False,
	},
	"Ελληνική" : {
		"lang_code"					: "G",
		"url_lang_code"				: "el",
		"video_path" 				: "%CE%B2%CE%AF%CE%BD%CF%84%CE%B5%CE%BF",

		"bible_index_audio"			: False,
		"magazine_index"			: "%CE%B5%CE%BA%CE%B4%CF%8C%CF%83%CE%B5%CE%B9%CF%82/%CF%80%CE%B5%CF%81%CE%B9%CE%BF%CE%B4%CE%B9%CE%BA%CE%AC/",
		'has_simplified_edition'	: False,

		"music_index"				: "%CE%B5%CE%BA%CE%B4%CF%8C%CF%83%CE%B5%CE%B9%CF%82/%CE%BC%CE%BF%CF%85%CF%83%CE%B9%CE%BA%CE%AE-%CF%8D%CE%BC%CE%BD%CE%BF%CE%B9/",
		"dramas_index"				: "%CE%B5%CE%BA%CE%B4%CF%8C%CF%83%CE%B5%CE%B9%CF%82/%CE%B7%CF%87%CE%B7%CF%84%CE%B9%CE%BA%CE%AC-%CE%B2%CE%B9%CE%B2%CE%BB%CE%B9%CE%BA%CE%AC-%CE%B4%CF%81%CE%AC%CE%BC%CE%B1%CF%84%CE%B1/",
		"dramatic_reading_index"	: "%CE%B5%CE%BA%CE%B4%CF%8C%CF%83%CE%B5%CE%B9%CF%82/%CE%B4%CF%81%CE%B1%CE%BC%CE%B1%CF%84%CE%BF%CF%80%CE%BF%CE%B9%CE%B7%CE%BC%CE%AD%CE%BD%CE%B5%CF%82-%CE%B1%CE%BD%CE%B1%CE%B3%CE%BD%CF%8E%CF%83%CE%B5%CE%B9%CF%82-%CE%B1%CE%B3%CE%AF%CE%B1-%CE%B3%CF%81%CE%B1%CF%86%CE%AE/",
		
		'wol'						: "r11/lp-g",
		"date_format"				: "%Y-%m-%d",
		"news_index"				: "%CE%B5%CE%B9%CE%B4%CE%AE%CF%83%CE%B5%CE%B9%CF%82/",
		"activity_index"			: "%CE%BC%CE%AC%CF%81%CF%84%CF%85%CF%81%CE%B5%CF%82-%CF%84%CE%BF%CF%85-%CE%B9%CE%B5%CF%87%CF%89%CE%B2%CE%AC/%CE%B4%CF%81%CE%B1%CF%83%CF%84%CE%B7%CF%81%CE%B9%CF%8C%CF%84%CE%B7%CF%84%CE%B5%CF%82/",

		"sign_index"				: "apps/G_QrYQZRQVNFVTr?selLang=GSL",
	},
}


plugin_name 	= sys.argv[0]   # plugin://plugin.video.jworg/
plugin_pid   	= int(sys.argv[1])
plugin_params 	= urlparse.parse_qs((sys.argv[2])[1:])
skin_used 		= xbmc.getSkinDir()
dir_media		= os.path.dirname(__file__) + os.sep + "resources" + os.sep + "media" + os.sep
addon 			= xbmcaddon.Addon("plugin.video.jworg")

try: 
	emulating = xbmcgui.Emulating
except: 
	emulating = False

try:
	import StorageServer
except:
	from resources.lib import storageserverdummy as StorageServer
	 
cache 			= StorageServer.StorageServer(plugin_name, 24)  # 2 hour cache
audio_sorting 	= str(int(addon.getSetting("audio_sorting")) + 1)
video_sorting 	= str(int(addon.getSetting("video_sorting")) + 1)

# if language is set, it used a localized language name, like "Italiano" or "Polski"
language		= addon.getSetting("language")

# AUTODETECT LANGUAGE IF MISSING
# if not set, language will be read from system, where it uses english language name
# if it's one of supported language, I got localized name to adhere to addon language setting 
# availables values ( Italiano, English, Polski, ... )

if language == "":
	actual_locale = xbmc.getLanguage()
	if actual_locale in locale_2_lang :
		language = locale_2_lang[actual_locale]
		addon.setSetting("language", language)
	else :
		language = "English"

