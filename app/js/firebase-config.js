/**
 * Neural Observatory — Firebase Configuration
 *
 * This module initializes Firebase and exports the Firestore instance.
 * Config values are filled in after `firebase_get_sdk_config` returns.
 *
 * To run against the local emulator (no GCP auth needed):
 *   firebase emulators:start
 *   → Firestore emulator on port 8080, Hosting on port 5000
 */

import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.7.1/firebase-app.js';
import {
  getFirestore,
  connectFirestoreEmulator,
} from 'https://www.gstatic.com/firebasejs/11.7.1/firebase-firestore.js';

// ── Firebase project config ─────────────────────────────────────────
// TODO: Replace with actual values from firebase_get_sdk_config
const firebaseConfig = {
  apiKey: 'AIzaSyDzUrhgqUHedNXYlGSqq2sFISBVrc2-Bbg',
  authDomain: 'skill-library-prod.firebaseapp.com',
  projectId: 'skill-library-prod',
  storageBucket: 'skill-library-prod.firebasestorage.app',
  messagingSenderId: '792932882875',
  appId: '1:792932882875:web:838c3d1c33afdfd5298c9e',
};

// ── Initialize ──────────────────────────────────────────────────────
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Connect to emulator when running locally
if (
  location.hostname === 'localhost' ||
  location.hostname === '127.0.0.1'
) {
  try {
    connectFirestoreEmulator(db, 'localhost', 8080);
    console.log('[NO] Connected to Firestore emulator on :8080');
  } catch (e) {
    // Already connected — ignore
  }
}

export { db };
