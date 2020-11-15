import requests

url = 'https://maker.ifttt.com/trigger/TurnonOffice1/with/key/bTQ6D-WnYUA6ZpK2vQ_95m'
#myobj = {'somekey': 'somevalue'}

x = requests.post(url)

print(x.text)
