# Deployment Guide — Render

## Build Command

```
pip install -r requirements.txt
```

## Start Command

```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `ACCOUNT_SID` | Twilio Account SID |
| `AUTH_TOKEN` | Twilio Auth Token |
| `TWILIO_NUMBER` | Twilio phone number (e.g. `+1...`) |
| `TWILIO_WHATSAPP_NUMBER` | Twilio WhatsApp sender (e.g. `whatsapp:+14155238886`) |
| `FRONTEND_URL` | Deployed frontend URL for CORS (e.g. `https://your-app.vercel.app`) |

## Render Deployment Steps

1. Push the repository to GitHub.

2. Go to [Render Dashboard](https://dashboard.render.com/) and create a **New Web Service**.

3. Connect your GitHub repository.

4. Configure:
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. Add environment variables listed above in the Render **Environment** tab.

6. Deploy.

## Notes

- SQLite database (`fieldhub.db`) is created automatically on first startup and seeded with demo data.
- `storage/images/` and `storage/documents/` directories are created automatically on startup.
- Uploaded files are served via the `/storage` route (FastAPI StaticFiles).
- On Render's free tier, the filesystem is ephemeral — data resets on each deploy. For persistent storage, upgrade to a Render Disk or switch to PostgreSQL.
- The `FRONTEND_URL` environment variable controls which deployed frontend origin is allowed by CORS. Set it to your Vercel/Netlify URL once deployed.
