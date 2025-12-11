# Firebase Google Authentication Setup Guide

## Overview
This guide will help you set up Google authentication using Firebase for the DeepShiva healthcare application.

## Prerequisites
- Google account
- Firebase project (or create a new one)

---

## Part 1: Firebase Console Setup

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or select existing project
3. Follow the setup wizard

### 2. Enable Google Authentication
1. In Firebase Console, go to **Authentication** > **Sign-in method**
2. Click on **Google** provider
3. Toggle **Enable**
4. Set a support email
5. Click **Save**

### 3. Register Web App
1. Go to **Project Settings** (gear icon) > **Your apps**
2. Click the **Web** icon (`</>`)
3. Register app with nickname (e.g., "DeepShiva Web")
4. Copy the Firebase configuration object - you'll need:
   - `apiKey`
   - `authDomain`
   - `projectId`
   - `storageBucket`
   - `messagingSenderId`
   - `appId`

### 4. Download Service Account Key (Backend)
1. Go to **Project Settings** > **Service Accounts**
2. Click **Generate new private key**
3. Download the JSON file
4. Save it as `firebase-service-account.json` in `Pran-Protocol/config/`

---

## Part 2: Frontend Configuration

### 1. Install Firebase SDK
```bash
cd frontend
npm install firebase
```

### 2. Configure Environment Variables
Create/update `frontend/.env.local`:

```env
NEXT_PUBLIC_FIREBASE_API_KEY=your-api-key-from-step-3
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
NEXT_PUBLIC_FIREBASE_APP_ID=your-app-id
```

---

## Part 3: Backend Configuration

### 1. Install Firebase Admin SDK
```bash
cd ..  # back to Pran-Protocol root
pip install firebase-admin
```

### 2. Configure Environment Variables
Update `Pran-Protocol/.env`:

```env
FIREBASE_SERVICE_ACCOUNT_PATH=config/firebase-service-account.json
```

### 3. Update Database
The backend will automatically add the `firebase_uid` column to the User table on restart.

---

## Part 4: Testing

### 1. Start Backend
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend
```bash
cd frontend
npm run dev
```

### 3. Test Google Sign-In
1. Navigate to `http://localhost:3000/login`
2. Click "Sign in with Google" button
3. Select Google account
4. Should redirect to chat interface

### 4. Verify Backend Logs
Check terminal for:
```
✓ Firebase Admin SDK initialized with service account
[FIREBASE_SIGNUP] User registered via Google: user@example.com
```

---

## Security Notes

⚠️ **Important Security Practices:**

1. **Never commit credentials:**
   - Add `firebase-service-account.json` to `.gitignore`
   - Never commit `.env` or `.env.local` files

2. **Restrict API Keys:**
   - In Firebase Console > Project Settings > Your apps
   - Set up App Check for production
   - Restrict API keys to your domain

3. **Production Deployment:**
   - Use environment variables in your hosting platform
   - Enable Firebase App Check
   - Set up proper CORS policies

---

## Troubleshooting

### "Firebase Admin SDK not initialized"
- Check that `firebase-service-account.json` exists in `config/`
- Verify `FIREBASE_SERVICE_ACCOUNT_PATH` in `.env`
- Restart backend server

### "Invalid Firebase token"
- Check frontend `.env.local` has correct Firebase config
- Ensure Firebase project has Google auth enabled
- Clear browser cache and try again

### "Email already registered"
- User exists with email/password login
- They need to use same method or reset password
- Consider implementing account linking

---

## File Structure

```
Pran-Protocol/
├── config/
│   └── firebase-service-account.json  # Backend credential (gitignored)
├── frontend/
│   ├── .env.local                     # Frontend Firebase config
│   └── src/
│       ├── lib/
│       │   └── firebase.ts            # Firebase initialization
│       └── app/
│           ├── login/
│           │   └── page.tsx           # Login with Google button
│           └── api/
│               └── auth/
│                   └── firebase-login/
│                       └── route.ts    # Firebase token proxy
└── src/
    └── auth/
        └── firebase_auth.py           # Token verification
```

---

## What Happens During Google Sign-In?

1. **User clicks "Sign in with Google"** → Firebase popup opens
2. **User selects Google account** → Firebase returns ID token
3. **Frontend sends token to backend** → `/api/auth/firebase-login`
4. **Backend verifies token** → Firebase Admin SDK validates
5. **Backend creates/finds user** → Database lookup by email
6. **Backend returns JWT** → Standard app authentication token
7. **Frontend stores JWT** → Used for all subsequent API calls

---

## Next Steps

- ✅ Google authentication is now enabled
- Consider adding:
  - Profile page with Google avatar
  - Account linking (email/password + Google)
  - Other OAuth providers (GitHub, Microsoft, etc.)
  - Sign-out button that clears Firebase session

---

## Support

If you encounter issues:
1. Check Firebase Console logs
2. Check backend terminal output
3. Check browser console for errors
4. Verify all environment variables are set
