import fonctions as fn

class TestFonctions:
  
	def test_json_to_dataframe(self):
		df = fn.json_to_dataframe("input_test.json")
		assert df.loc[0,"videos_id"] == "j7vZGMvd4zE"
		assert df.loc[1,"videos_id"] == "k0D9bdBRecU"
		
	
	def test_get_title(self):
		response = fn.requests.get("https://www.youtube.com/watch?v=j7vZGMvd4zE")
		soup = fn.BeautifulSoup(response.text, "html.parser")
		titre_attendu = "Airbus, au coeur du géant de l'aviation"
		assert fn.get_title(soup) == titre_attendu
		
	def test_get_author(self):
		response = fn.requests.get("https://www.youtube.com/watch?v=j7vZGMvd4zE")
		soup = fn.BeautifulSoup(response.text, "html.parser")
		auteur_attendu = "Investigations et Enquêtes"
		assert fn.get_author(soup) == auteur_attendu		
		
	def test_get_likes(self):
		response = fn.requests.get("https://www.youtube.com/watch?v=j7vZGMvd4zE")
		soup = fn.BeautifulSoup(response.text, "html.parser")
		like_attendu = 14864
		
		like_min_attendu = (like_attendu - 1000)
		like_max_attendu = (like_attendu*2)
		
		like_test = int(fn.get_likes(soup))
		
		assert like_min_attendu <= like_test <= like_max_attendu
			
		
