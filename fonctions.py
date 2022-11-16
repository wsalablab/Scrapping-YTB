from bs4 import BeautifulSoup
import requests
import argparse
import pandas as pd
import re
import json

def json_to_dataframe(filename):
	videos_infos = pd.read_json(filename)
	return videos_infos
    
def get_title(soup):
  return (soup.find("meta", itemprop="name")["content"])
    
def get_author(soup):
  return (soup.find('link', itemprop="name")['content'])
    
def get_likes(soup):
	data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
	data_json = json.loads(data) 
	videoPrimaryInfoRendererBuilder = data_json['contents']['twoColumnWatchNextResults']['results']	['results']['contents']

	indice = 0
	if 'videoPrimaryInfoRenderer' in videoPrimaryInfoRendererBuilder[0]:
		indice = 0
	elif 'videoPrimaryInfoRenderer' in videoPrimaryInfoRendererBuilder[1]:
		indice = 1
	elif 'videoPrimaryInfoRenderer' in videoPrimaryInfoRendererBuilder[2]:
		indice = 2
	elif 'videoPrimaryInfoRenderer' in videoPrimaryInfoRendererBuilder[3]:
		indice = 3
	elif 'videoPrimaryInfoRenderer' in videoPrimaryInfoRendererBuilder[4]:
		indice = 4
	else :
		indice = 5
	

	videoPrimaryInfoRenderer = videoPrimaryInfoRendererBuilder[indice]['videoPrimaryInfoRenderer']

	videoSecondaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][(indice + 1)]['videoSecondaryInfoRenderer'] 

	likes = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']

	likes = likes.replace(' clics sur "J\'aime"', '')	
	likes_str = likes.replace(' ', '')
	likes_tab = re.findall(r'\d+', likes_str)
	likes_res = ""
	for e in likes_tab:
		likes_res = (likes_res + e)
	return likes_res
	
def get_description(soup):
	pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
	return pattern.findall(str(soup))[0].replace('\n','\n')
	
def get_urls_description(soup):
	description = get_description(soup)
	return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', description)
	
	
