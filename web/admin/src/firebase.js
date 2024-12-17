// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyByvGeX4gmNfOUARtkusNe-YbzvpZS6g9Q",
  authDomain: "ds-project-6b231.firebaseapp.com",
  projectId: "ds-project-6b231",
  storageBucket: "ds-project-6b231.firebasestorage.app",
  messagingSenderId: "273156791301",
  appId: "1:273156791301:web:957a4428e7d6df2b20d06c",
  measurementId: "G-QDDHF4RKVC"
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);

// Nếu sử dụng Firestore
const db = getFirestore(firebaseApp);

export { firebaseApp, db };