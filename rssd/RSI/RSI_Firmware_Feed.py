""" Rohde & Scharz Instrument Functions"""
import feedparser

def parse_feed_firmware():
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
    url = 'https://www.rohde-schwarz.com/us/rss-feeds/driver-feed_229510.rss'
    feed = feedparser.parse(url)
    print(f'\n{url}')
    for entry in feed.entries:
        entry_title     = entry.title.replace('Drivers for R&S®','')
        entry_link      = entry.link
        entry_published = entry.published           # Unicode string

        print (f"{entry_title[0:30]:32}[{entry_link:55}] {entry_published}")

def parse_feed_appNote():
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
