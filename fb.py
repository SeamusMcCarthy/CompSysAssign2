#!/usr/bin/python3


# pip install git+https://github.com/ozgur/python-firebase

from firebase import firebase
firebase = firebase.FirebaseApplication('https://compsys2020-154671.firebaseio.com/', None)
#result = firebase.post('/scheduled', 23)
data = {
   'Date' : '2020-11-30',
   'Name' : 'Seamus',
   'Start' : '08:00:00',
   'End' : '08:15:00'
}
result = firebase.post('/scheduled', data)
print(result)

#result = firebase.delete('compsys2020-154671/users', 'Test@test.com')

#result = firebase.get('/compsys2020-154671/users', None)
#print(result)


