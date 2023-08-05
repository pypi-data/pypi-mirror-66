from bs4 import BeautifulSoup as bs
import urllib.request
from random import choice as rc
import os
import requests

def randImg():
    r= requests.get("https://www.shitpostbot.com/api/randsource")
    img_url = "https://www.shitpostbot.com/"
    content = str(r.content)[2:-1:]
    content = content.replace('null', '0')
    img_url += eval(content)['sub']['img']['full'].replace('\\', '')
    return img_url

def getLink(query,sort = 'random', order='total_rating',direction="DESC"):
    url = f"https://www.shitpostbot.com/gallery/sourceimages?review_state=accepted&query={query}&order={order}&direction={direction}"
    response = urllib.request.urlopen(url)
    soup = bs(response,'html.parser')
    result = []
    for div in soup.findAll('div', attrs={'class':'img'}):
        result.append(div.find('a')['href'])
    if len(result) == 0:
        raise ResultError('Image with the given query does not exist')
    else:
        if sort == 'random':
            fin = rc(result)
        elif sort == 'top':
            fin = result[0]
        elif sort == 'bottom':
            fin = result[-1]
        return 'https://www.shitpostbot.com' + fin

def getImg(query,sort='random', order='total_rating',direction="DESC"):
    url = getLink(query,sort,order,direction)
    response = urllib.request.urlopen(url)
    soup = bs(response,'html.parser')
    for div in soup.findAll('div', attrs={'style':'padding-top: 15px'}):
        return 'https://www.shitpostbot.com' + (div.find('a')['href'])
