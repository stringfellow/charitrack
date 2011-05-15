import chardet
import sys
import requests
import re

from BeautifulSoup import BeautifulSoup

from django.utils.html import strip_tags



def _get_links(soup):

    twitter_name = None
    twit_links = soup(href=re.compile("http://.*?twitter\.com.*"))
    if len(twit_links) > 0:
        for link in twit_links:
            m = re.search(r"http://.*?twitter\.com/([\w_]+)", str(link))
            if m:
                if not m.group(1) in ['share']:
                    twitter_name = m.group(1)
                    break

    facebook_page = None
    face_links = soup(href=re.compile("http://.*facebook\.com.*"))
    if len(face_links) > 0:
        for link in face_links:
            m = re.search(r"http://.*?facebook\.com/([^\"']*)", str(link))
            if m:
                facebook_page = m.group(0)
                break



    return {
        'twitter': twitter_name,
        'facebook': facebook_page,
    }


def _get_logo(soup):
    logo = None
    logos = soup(src=re.compile(r"(?i).*?logo([^\"']*)"))
    print logos
    logos = filter(lambda x: 'facebook' not in str(x), logos)
    logos = filter(lambda x: 'twitter' not in str(x), logos)
    logos = filter(lambda x: 'tube' not in str(x), logos)
    logos = filter(lambda x: 'myspace' not in str(x), logos)
    print logos
    if len(logos) > 0:

        logo = logos[0]

        m = re.search(r"(i?)src\s*=\s*['\"]{1}([^'\"]+)['\"]{1}", str(logo))
        if m:
            logo = m.group(2)

    return logo


def _link_sharpen(url, link):
    _link = link
    if _link and not _link.lower().startswith('http'):
        if not _link.startswith('/'):
            _link = '/'+_link

        url_parts = url.split('/')
        if "." in url_parts[-1]:
            url_parts = url_parts[:-1]

        _url = "/".join(url_parts)
        if _url.endswith('/'):
            _url = _url[:-1]

        _link = _url + _link

    return _link


def _get_number(content):
    text = strip_tags(content)
    m = re.search(r"(?i)registered(.*?)([0-9]{6}[0-9]*)", text)
    if m:
        return m.group(2)

    return None

def find_info(url, text=None):
    try:
        if not text:
            r = requests.get(url)
            assert r.status_code == 200, "Got status code: %s" % (r.status_code)
            text = r.content
            encoding = chardet.detect(text)
            text.decode(encoding['encoding'], 'ignore').encode("utf-8")

        soup = BeautifulSoup(text)
        try:
            links = _get_links(soup)
        except:
            links = {'facebook':None, 'twitter':None}
            print "links error"

        try:
            number = _get_number(text)
        except:
            number = None
            print "num error"

        try:
            logo = _link_sharpen(url, _get_logo(soup))
        except Exception,e:
            logo = None
            print "logo error",e

        return links, number, logo
    except Exception, e:
        print e


