# pip install git+https://github.com/ozgur/python-firebase
import json
from firebase import firebase
firebase = firebase.FirebaseApplication('https://compsys2020-154671.firebaseio.com/', None)
#result = firebase.post('/scheduled', 23)
data = {
   'Name' : 'Seamus',
   'Start' : '08:15:00',
   'End' : '08:30:00'
}

result = firebase.post('/users', data)
print(result)

result = firebase.get('/users', None)
print(result)

for hashkey in result:
   print(hashkey)

for item, value in result.items():
   print(value['Start'])



#result = firebase.delete('compsys2020-154671/users', 'Test@test.com')

#result = firebase.get('/compsys2020-154671/users', None)
#print(result)


