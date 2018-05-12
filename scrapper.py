import urllib.request, json 
with urllib.request.urlopen("https://api.cafci.org.ar/estadisticas/informacion/diaria/2/2018-04-26") as url:
    data = json.loads(url.read().decode())
    print(data)