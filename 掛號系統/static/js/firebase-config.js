// firebase-config.js (fixed for 400 issues)
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { initializeFirestore } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

export const firebaseConfig = {
  apiKey: "AIzaSyB3Ca7tChq0aHo04D333fnAbJgCKWx_u_8",
  authDomain: "project1-1faee.firebaseapp.com",
  projectId: "project1-1faee",
  storageBucket: "project1-1faee.firebasestorage.app",
  messagingSenderId: "1042374295064",
  appId: "1:1042374295064:web:9f53ce52fb9fdf12f54d6d",
  measurementId: "G-RL8HVRNR46"
};

export const app = initializeApp(firebaseConfig);


export const db = initializeFirestore(app, {
  experimentalAutoDetectLongPolling: true,
  useFetchStreams: false
});
