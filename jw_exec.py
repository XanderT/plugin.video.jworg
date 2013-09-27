"""
EXECUTABLE RELATED FUNCTION
"""
import xbmc
import xbmcgui
import xbmcplugin

import os
import jw_config
import jw_load
import re
import urllib
import datetime

now = datetime.datetime.now()

# List of available executable  services
def showExecIndex(language):

    # 1. Dailiy Text
    now 			= datetime.datetime.now()
    date_for_json 	= str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    date_format 	= jw_config.const[language]["date_format"]
    title 			= jw_config.t(30012)  + " - " + now.strftime(date_format)
    listItem 		= xbmcgui.ListItem( title )
    params  		= {
        "content_type"  : "executable", 
        "mode" 			: "open_daily_text",
        "date"			: date_for_json
    } 
    url = jw_config.plugin_name + '?' + urllib.urlencode(params)
    xbmcplugin.addDirectoryItem(
        handle		= jw_config.pluginPid, 
        url			= url, 
        listitem	= listItem, 
        isFolder	= True 
    )  

    xbmcplugin.endOfDirectory(handle=jw_config.pluginPid)


# Show daily text 
def showDailyText(language, date):

    json_url = jw_config.const[language]["daily_text_json"] + "/" + date
    json = jw_load.loadJsonFromUrl(json_url)
    text = json["items"][0]["content"]

    dialog = DailiyText()
    dialog.customInit(text);
    dialog.doModal();
    del dialog
    xbmc.executebuiltin('Action("back")')


# Window showing daily text
class DailiyText(xbmcgui.WindowDialog):

    def __init__(self):
        if jw_config.emulating: xbmcgui.Window.__init__(self)

    def customInit(self, text):
        
        width = self.getWidth()
        height = self.getHeight()
        border = 50; # px relative to 1280/720 fixed grid resolution

        # width is always 1280, height is always 720.
        # getWidth() and getHeight() instead read the REAL screen resolution
        self.ctrlDate= xbmcgui.ControlTextBox(
            border, 0, 
            1280 - border *2, 60, 
            'font35_title', "0xFF0000FF"
        )
        self.ctrlScripture= xbmcgui.ControlTextBox(
            border, 60, 
            1280 - border *2, 100, 
            'font35_title', "0xFF000000"
        )
        self.ctrlComment= xbmcgui.ControlTextBox(
            border, 200, 
            1280 - border *2, 720 - 200, 
            'font30', "0xFF000000"
        )
        bg_image = jw_config.dir_media + "blank.png"

        self.ctrlBackgound = xbmcgui.ControlImage(0,0, 1280, 720, bg_image)
        
        self.addControl (self.ctrlBackgound)
        self.addControl (self.ctrlDate)
        self.addControl (self.ctrlScripture)
        self.addControl (self.ctrlComment)

        self.ctrlDate.setText( self.getDateLine(text) );
        self.ctrlScripture.setText( self.getScriptureLine(text) );
        self.ctrlComment.setText( self.getComment(text) );

    def onAction(self, action):
        self.close()

    # Grep today's textual date
    def getDateLine(self, text):

        regexp_date = "'ss'>([^<].*)</p>"
        date_list = re.findall(regexp_date, text)    
        date = date_list[0] + " [" + str(self.getWidth()) + " x " + str(self.getHeight()) + "] "
        return date.encode("utf8")

    # Grep holy scripture ref
    def getScriptureLine(self, text):
       
        regexp_scripture = "'sa'>(.*)</div>"
        scripture_list = re.findall(regexp_scripture, text)    
        if scripture_list == []:
            return ""

        scripture = scripture_list[0]
        scripture = re.sub("<([^>]*)>", "", scripture)    

        return scripture.encode("utf8") 

    # Grep comment 
    def getComment(self, text):

        regexp_full_comment = "'sb'>(.*)"
        full_comment_list = re.findall(regexp_full_comment, text)
        if full_comment_list == []:
            return ""

        full_comment = full_comment_list[0]
        full_comment = re.sub("<([^>]*)>", "", full_comment)

        return  full_comment.encode("utf8")