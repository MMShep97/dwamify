import { apiKey } from './keys.js'
import * as firebase from 'firebase'

  // Your web app's Firebase configuration
  var firebaseConfig = {
    apiKey: apiKey,
    authDomain: "wheredwami.firebaseapp.com",
    databaseURL: "https://wheredwami.firebaseio.com",
    projectId: "wheredwami",
    storageBucket: "wheredwami.appspot.com",
    messagingSenderId: "696688358809",
    appId: "1:696688358809:web:e0438259f46f52e4dd4f08"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);

  var database = firebase.database();

  export { database }