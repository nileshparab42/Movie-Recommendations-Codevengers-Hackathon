import requests

url = "https://imdb146.p.rapidapi.com/v1/find/"

querystring = {"query":"Conjuring"}

headers = {
	"X-RapidAPI-Key": "c3d046ca4dmsh278a376fcb52f38p19229cjsn1c727078f7ac",
	"X-RapidAPI-Host": "imdb146.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
# print(response.json())
res = response.json()
# Assuming res contains the JSON data

# Get the URL of the poster for the first movie
first_movie_poster_url = res['titleResults']['results'][0]['titlePosterImageModel']['url']

print(first_movie_poster_url)

