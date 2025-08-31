# Deploy Nia Bot to Render

## Step 1: Prepare Your Repository
1. Make sure all files are committed to your Git repository
2. Push to GitHub/GitLab if not already done

## Step 2: Create Render Web Service
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub/GitLab repository
4. Select this repository

## Step 3: Configure the Service
**Basic Settings:**
- Name: `nia-bot`
- Environment: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`

**Environment Variables:**
- `GEMINI_API_KEY`: Your Gemini API key (from .env file)
- `FLASK_ENV`: `production`

## Step 4: Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Note your app URL (e.g., https://nia-bot-xyz.onrender.com)

## Step 5: Update n8n Workflow
Update your n8n HTTP Request node URL from:
`http://localhost:5000/n8n/webhook`

To:
`https://YOUR-RENDER-URL.onrender.com/n8n/webhook`

## Step 6: Test
1. Trigger your n8n workflow
2. Check Render logs to see if the webhook is received
3. Your bot should now receive meeting notifications in the cloud!

## Important Notes:
- The cloud version logs meetings but doesn't join them (no GUI in cloud)
- For actual meeting joining, you'd need a more complex setup with virtual displays
- This deployment is perfect for receiving and processing meeting webhooks