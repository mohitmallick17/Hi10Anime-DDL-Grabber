import hashlib
import random
import re
import string

import requests

from exceptions import InvalidSessionException


def generateJToken():
    length = random.randint(7, 10)
    ranString = (''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length)))[:8]
    jtoken = hashlib.md5(ranString.encode('utf-8')).hexdigest()[:5]
    id = hashlib.md5(jtoken.encode('utf-8')).hexdigest()[:5]
    return f'?jtoken={jtoken}{id}'


def formattedTitle(title):
    newTitle = ''
    for ch in title:
        if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or '0' <= ch <= '9' or ch == ' ':
            newTitle += ch
        if len(newTitle) > 20:
            break
    newTitle = newTitle.strip()
    if newTitle == '':
        return 'output'
    return newTitle


def FetchAnimeData(URL, left, right):
    session = requests.session()
    session.headers.update(
        {'User-Agent': 'Mozilla/5.0 (Windows NT '
                       '10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, '
                       'like Gecko) '
                       'Chrome/90.0.4430.93 '
                       'Safari/537.36',
         }
    )
    session.cookies.update({
        'wordpress_test_cookie': 'WP%20Cookie%20check',
        left: right,
    })
    page = session.get(URL)
    if '<title>Not allowed' in page.text:
        raise InvalidSessionException("Your session is either expired or is invalid. Please generate a new one")
    title = 'output'
    result = re.search('<\W*title\W*(.*)</title', page.text, re.IGNORECASE)
    if result:
        title = result.group(1)
    return formattedTitle(title), findAnimeDataInPage(page.text)


def findAnimeDataInPage(pageData):
    animeList = []
    urlRegex = 'https://ouo\.io/s/QgcGSmNw\?s=(.*?)\"'
    for line in iter(pageData.splitlines()):
        match = re.search(urlRegex, line)
        if match is not None:
            animeList.append(match.group(1) + generateJToken())
    return animeList
