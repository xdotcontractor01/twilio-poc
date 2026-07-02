# Twilio POC Backend

A proof-of-concept FastAPI backend demonstrating communication between a user's phone and a server using Twilio. This project is intentionally modular and self-contained so it can be copied into other projects later.

## Folder Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── config.py        # Environment variable configuration
│   ├── routers/
│   │   └── twilio.py    # Twilio webhook and status endpoints
│   ├── services/
│   │   ├── downloader.py  # Media download (placeholder)
│   │   └── messaging.py   # Twilio messaging (placeholder)
│   └── utils/
│       └── logger.py    # Logging utility
├── uploads/             # Local storage for downloaded media
├── .env.example         # Environment variable template
├── requirements.txt
├── run.py               # Development server launcher
└── README.md
```

## Install

Requires Python 3.11+.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in your Twilio credentials in `.env` when ready.

## Run

```bash
python run.py
```

The server starts at `http://localhost:8000`.

- `GET /` — health check, returns `{"message": "Twilio POC Running"}`
- `POST /twilio/webhook` — placeholder webhook endpoint

API docs are available at `http://localhost:8000/docs`.

## Future Roadmap

- [ ] Parse incoming Twilio webhook payloads (SMS, MMS)
- [ ] Implement messaging service for outbound messages
- [ ] Download and store media attachments from Twilio
- [ ] Add webhook signature validation
- [ ] Expose endpoints for triggering outbound communication
- [ ] Integrate with xDOT (separate project)
