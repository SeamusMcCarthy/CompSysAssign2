// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAAInu1OfiJTtnsHdE48lppG-iDHVSOCJc",
    authDomain: "sensepi-e9029.firebaseapp.com",
    databaseURL: "https://sensepi-e9029.firebaseio.com",
    projectId: "sensepi-e9029",
    storageBucket: "sensepi-e9029.appspot.com",
    messagingSenderId: "773384483699",
    appId: "1:773384483699:web:8f3c008cbfc6b715544b06"
};

firebase.initializeApp(firebaseConfig);

// Get a reference to the file storage service
const storage = firebase.storage();
// Get a reference to the database service
const database = firebase.database();

// Create camera database reference
const camRef = database.ref("file");

// Sync on any updates to the DB. THIS CODE RUNS EVERY TIME AN UPDATE OCCURS ON THE DB.
camRef.limitToLast(1).on("value", function(snapshot) {
  snapshot.forEach(function(childSnapshot) {
    const image = childSnapshot.val()["image"];
    const time = childSnapshot.val()["timestamp"];
    const storageRef = storage.ref(image);

    storageRef
      .getDownloadURL()
      .then(function(url) {
        console.log(url);
        document.getElementById("photo").src = url;
        document.getElementById("time").innerText = time;
      })
      .catch(function(error) {
        console.log(error);
      });
  });
});
