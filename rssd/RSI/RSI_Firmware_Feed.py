# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Rohde & Scharz Instrument Functions
### Author : Martin C Lim
### Date   : 2019.09.30
###  _____  _____   ____ _______ ____ _________     _______  ______ 
### |  __ \|  __ \ / __ \__   __/ __ \__   __\ \   / /  __ \|  ____|
### | |__) | |__) | |  | | | | | |  | | | |   \ \_/ /| |__) | |__    
### |  ___/|  _  /| |  | | | | | |  | | | |    \   / |  ___/|  __|  
### | |    | | \ \| |__| | | | | |__| | | |     | |  | |    | |____ 
### |_|    |_|  \_\\____/  |_|  \____/  |_|     |_|  |_|    |______|
###############################################################################

def parse_feed_firmware():
    import feedparser

    url = 'https://www.rohde-schwarz.com/us/rss-feeds/firmware-feed_229511.rss'
    feed = feedparser.parse(url)
    print(f'\n{url}')
    for entry in feed.entries:
        entry_title     = entry.title.replace('Firmware for R&S®','')
        entry_link      = entry.link
        entry_published = entry.published           # Unicode string
        # entry_parsed    = entry.published_parsed    # Time object
        # entry_content   = entry.summary

        print (f"{entry_title[0:30]:32}[{entry_link:55}] {entry_published}")

def parse_feed_drivers():
    import feedparser

    url = 'https://www.rohde-schwarz.com/us/rss-feeds/driver-feed_229510.rss'
    feed = feedparser.parse(url)
    print(f'\n{url}')
    for entry in feed.entries:
        entry_title     = entry.title.replace('Drivers for R&S®','')
        entry_link      = entry.link
        entry_published = entry.published           # Unicode string

        print (f"{entry_title[0:30]:32}[{entry_link:55}] {entry_published}")

def parse_feed_appNote():
    import feedparser

    url = 'https://www.rohde-schwarz.com/us/rss-feeds/application-note-feed_229508.rss'
    feed = feedparser.parse(url)
    print(f'\n{url}')
    for entry in feed.entries:
        entry_title     = entry.title.replace('R&S®','')
        entry_link      = entry.link.replace('https://www.rohde-schwarz.com/us/applications','<RSA-Apps>')

        print (f"{entry_title[0:40]:42}[{entry_link:55}]")

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    parse_feed_drivers()
#     parse_feed_firmware()
    parse_feed_appNote()