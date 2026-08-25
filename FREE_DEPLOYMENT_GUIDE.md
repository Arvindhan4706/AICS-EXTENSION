# Free Cloud Deployment Guide (Vercel + Render)

Follow these steps to host CyberShield AI 100% for free in the cloud so it runs 24/7.

## Step 1: Push Your Code to GitHub
Both Vercel and Render require your code to be on GitHub.
1. Go to [GitHub](https://github.com/) and create a new **private** repository called `cybershield-ai`.
2. Open your terminal in the project root (`D:\Class 12\AICS REVIEW`) and run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/cybershield-ai.git
   git push -u origin main
   ```

## Step 2: Deploy the Backend to Render (Free)
1. Go to [Render.com](https://render.com/) and sign up with GitHub.
2. Click **New +** and select **Web Service**.
3. Connect your `cybershield-ai` repository.
4. Fill in the following settings:
   - **Name**: cybershield-backend
   - **Environment**: Python
   - **Build Command**: `pip install -r apps/backend/requirements.txt && pip install pandas scipy scikit-learn`
   - **Start Command**: `uvicorn apps.backend.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free
5. Click **Create Web Service**. 
6. Wait for it to deploy. Once it's live, copy the URL (e.g., `https://cybershield-backend.onrender.com`).

## Step 3: Deploy the Dashboard to Vercel (Free)
1. Go to [Vercel.com](https://vercel.com/) and sign up with GitHub.
2. Click **Add New** -> **Project**.
3. Import your `cybershield-ai` repository.
4. Before clicking Deploy, configure these settings:
   - **Framework Preset**: Next.js
   - **Root Directory**: `apps/web`
   - **Environment Variables**: Add a new variable called `NEXT_PUBLIC_API_URL` and set its value to your Render backend URL from Step 2 + `/api/v1` (e.g., `https://cybershield-backend.onrender.com/api/v1`).
5. Click **Deploy**. Vercel will give you a free live link for your dashboard!

## Step 4: Update the Chrome Extension
Now that your backend is running in the cloud, you must update the extension to talk to it instead of your local PC.

1. Open `apps/extension/popup.js` and change `const API_BASE = "http://localhost:8000/api/v1";` to your new Render URL:
   `const API_BASE = "https://cybershield-backend.onrender.com/api/v1";`
2. Do the exact same thing in `apps/extension/background.js`.
3. In Chrome, go to `chrome://extensions`, hit the **Refresh** icon on your CyberShield extension, or remove it and reload the unpacked folder.

You're done! The ML model, Dashboard, and Extension are now online permanently for free!
