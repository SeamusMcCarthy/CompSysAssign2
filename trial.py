import requests

url = 'https://maker.ifttt.com/trigger/ToggleOffice1/with/key/bTQ6D-WnYUA6ZpK2vQ_95m'
x = requests.post(url)
print(x.text)
url = 'https://maker.ifttt.com/trigger/ToggleOffice3/with/key/bTQ6D-WnYUA6ZpK2vQ_95m'
x = requests.post(url)
print(x.text)
url = 'https://maker.ifttt.com/trigger/ToggleLight/with/key/bTQ6D-WnYUA6ZpK2vQ_95m'
x = requests.post(url)
print(x.text)
