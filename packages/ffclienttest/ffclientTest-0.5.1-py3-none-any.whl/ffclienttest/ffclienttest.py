import requests 

URL = "https://api.featureflag.tech"
apikey = {"fft-api-key": "38312f60-557a-11ea-8dfc-5976faa419b4"}

r = requests.get(url = URL, headers = apikey) 

print(r.json())
