from bs4 import BeautifulSoup
import requests
import argparse
import pandas as pd
import re
import json
import fonctions as fn

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("--input", action="store", dest="input_file", help="input file argument", 	required=True)
	parser.add_argument("--output", action="store", dest="output_file", help="output argument", required=True)
	args = parser.parse_args()

	
	videos_infos = fn.json_to_dataframe(args.input_file)
	videos_infos['title'] = 0
	videos_infos['author'] = 0
	videos_infos['likes'] = 0
	videos_infos['description'] = 0
	videos_infos['urls_descr'] = 0
	videos_infos['id'] = 0
  
	for i in range(len(videos_infos)):
		
		id = videos_infos.loc[i,"videos_id"]

		url = "https://www.youtube.com/watch?v="+id
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		
		#titre
		titre = fn.get_title(soup)
		videos_infos.loc[i,"title"] = titre
		
		#auteur
		auteur = fn.get_author(soup)
		videos_infos.loc[i,"author"] = auteur

		#likes
		likes = fn.get_likes(soup)
		videos_infos.loc[i,"likes"] = likes

		#description
		description = fn.get_description(soup)
		videos_infos.loc[i,"description"] = description 

		#urls description
		urls = fn.get_urls_description(soup)
		links = ""
		for v in urls:
			links += (v + ", ")
		videos_infos.loc[i,"urls_descr"] = links
    
		#id
		videos_infos.loc[i,"id"] = id 
		

	videos_infos.to_json(args.output_file)	
	

main()


