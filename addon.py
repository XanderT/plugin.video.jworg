# -*- coding: UTF-8 -*-

# for utf-8 see http://www.python.org/dev/peps/pep-0263/

import xbmcplugin

import jw_config

from video import jw_video

from audio import jw_audio
from audio import jw_audio_bible
from audio import jw_audio_music
from audio import jw_audio_drama
from audio import jw_audio_dramatic_reading
from audio import jw_audio_magazine

from program import jw_exec_index
from program import jw_exec_daily_text

"""
START
"""
# call arguments
params 		 = jw_config.plugin_params

content_type = params["content_type"][0]

mode = None
try: 	
	mode = params["mode"][0]
except:
	pass


"""
Call router
"""
if content_type == "video" :
	if mode is None :
		jw_video.showVideoFilter()

	if mode == "open_video_index":
		start = params["start"][0]        
		video_filter = params["video_filter"][0]	#Note: video_filter can be 'none', and it's a valid filter for jw.org !
		jw_video.showVideoIndex(start, video_filter)

	if mode == "open_json_video":
		json_url 	= params["json_url"][0]
		thumb 		= params["thumb"][0]
		jw_video.showVideoJsonUrl(json_url, thumb)


if content_type == "audio" :
	if mode is None :
		jw_audio.showAudioIndex()

	if mode == "open_bible_index" :
		jw_audio_bible.showAudioBibleIndex()

	if mode == "open_bible_book_index"  :
		book_num = params["book_num"][0]
		jw_audio_bible.showAudioBibleBookJson(book_num)

	if mode == "open_music_index" :
		start = params["start"][0]
		jw_audio_music.showMusicIndex( start);

	if mode == "open_music_json" : 
		json_url = params["json_url"][0]
		jw_audio.showAudioJson(json_url);

	if mode == "open_drama_index" :
		start = params["start"][0]
		jw_audio_drama.showDramaIndex( start);

	if mode == "open_drama_json" : 
		json_url = params["json_url"][0]
		jw_audio.showAudioJson(json_url);

	if mode == "open_dramatic_reading_index": 
		start = params["start"][0]
		jw_audio_dramatic_reading.showDramaticReadingIndex( start);

	if mode == "open_dramatic_reading_json" : 
		json_url = params["json_url"][0]
		jw_audio.showAudioJson(json_url);

	if mode == "open_magazine_index" :
		try: pub_filter = params["pub_filter"][0]
		except : pub_filter = None
		try: year_filter = params["year_filter"][0]
		except : year_filter = None
		jw_audio_magazine.showMagazineIndex(pub_filter, year_filter);

if content_type == "executable" :
	if mode is None : 
		jw_exec_index.showExecIndex();

	if mode == "open_daily_text" : 
		date = params["date"][0]
		jw_exec_daily_text.showDailyText(date);	