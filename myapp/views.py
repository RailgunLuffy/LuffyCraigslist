from cgitb import text
import imp
from urllib import response
import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup

from .models import Search

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.

def home(request):
    return render(request, 'myapp/base.html')

def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://cdn.vox-cdn.com/thumbor/kk92vqQUzmwBCP1kZjG9UR0m8Qc=/1400x1400/filters:format(png)/cdn.vox-cdn.com/uploads/chorus_asset/file/23589997/Screen_Shot_2022_05_26_at_10.49.28_AM.png'

        final_postings.append((post_title, post_url, post_price, post_image_url))
    result = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'myapp/new_search.html', result)
