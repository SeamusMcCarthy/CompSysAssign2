from firebase import firebase
firebase = firebase.FirebaseApplication('https://compsys2020-154671.firebaseio.com/', None)
result = firebase.get('/users', None)


