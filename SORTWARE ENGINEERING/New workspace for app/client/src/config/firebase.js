import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

// Your web app's Firebase configuration
// Replace these with your actual Firebase config values
const firebaseConfig = {
  apiKey: "your-api-key-here",
  authDomain: "your-auth-domain-here",
  projectId: "your-project-id-here",
  storageBucket: "your-storage-bucket-here",
  messagingSenderId: "your-messaging-sender-id-here",
  appId: "your-app-id-here"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);

export default app;
