# Frontend Deployment Guide

## Development

1. Copy the environment template:

```bash
cd frontend
cp .env.example .env
```

2. Set the local backend URL in `.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

3. Start the backend (from `backend/`):

```bash
python run.py
```

4. Start the frontend:

```bash
pnpm install
pnpm dev
```

5. Open `http://localhost:3000`

The dashboard polls the backend every 5 seconds.

## Production

Set the deployed backend URL:

```
VITE_API_BASE_URL=https://twilio-poc-fp9p.onrender.com
```

All API requests use:

```
${VITE_API_BASE_URL}/api/...
```

Image and document URLs use:

```
${VITE_API_BASE_URL}/storage/...
```

## Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend base URL (no trailing slash) | `https://twilio-poc-fp9p.onrender.com` |

## Vercel Deployment Steps

1. Push the repository to GitHub.

2. Go to [Vercel Dashboard](https://vercel.com/dashboard) and create a **New Project**.

3. Import your GitHub repository.

4. Configure:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite
   - **Build Command:** `pnpm build`
   - **Output Directory:** `dist`
   - **Install Command:** `pnpm install`

5. Add environment variable:
   - `VITE_API_BASE_URL` = `https://twilio-poc-fp9p.onrender.com`

6. Deploy.

7. On Render, set the backend `FRONTEND_URL` to your Vercel URL (e.g. `https://your-app.vercel.app`) so CORS allows the frontend.

## Notes

- Do not commit `.env` — only `.env.example` is tracked.
- Vercel rebuilds are required after changing environment variables.
- The frontend is read-only; all data comes from WhatsApp via the backend.
