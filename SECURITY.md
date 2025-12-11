# 🔒 Security & Setup Instructions

## ⚠️ IMPORTANT - Single .env File Setup

After cloning this repository, you only need to create **ONE** file with your credentials:

### Setup Instructions

**1. Copy the example file:**
```bash
cp .env.example .env
```

**2. Edit `.env` and add your API keys:**
- OpenAI API Key
- Tavily API Key  
- YouTube API Key
- Firebase Configuration (all 6 values from Firebase Console)

**3. Download Firebase Service Account:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to Project Settings > Service Accounts
4. Click "Generate new private key"
5. Save the JSON file as `config/firebase-service-account.json`

**4. Install dependencies:**
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install dotenv
npm install
```

**5. Run the application:**
```bash
# Backend (from root directory)
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Frontend (from root directory)
cd frontend
npm run dev
```

---

## 🎯 That's It!

The single `.env` file in the root directory now contains:
- ✅ Backend API keys
- ✅ Firebase frontend configuration
- ✅ Firebase backend service account path
- ✅ All other settings

No need for `frontend/.env.local` - everything is centralized!

---

## 🚨 NEVER COMMIT THESE FILES:
- `.env` (has all your secrets!)
- `config/firebase-service-account.json`
- `healthcare.db`

These are already in `.gitignore` for your protection!
