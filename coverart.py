from scraper import Page
import urllib

def cover_art_url(artist, album):
    page = Page("http://www.amazon.com/s/ref=nb_sb_noss?rh=n%3A163856011%2Ck%3A{0}&field-keywords={0}".format(
        urllib.quote(artist + " " + album)))
    image = page.xpath('//*[@id="mp3StoreShovelerShvlLink0"]/img/@src')[0].replace("SS110", "AA280")
    return image
