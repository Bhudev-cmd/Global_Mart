# Environment Setup Guide

This file explains how to configure environment variables for Global Mart.

## 1. Create Your `.env` File

From the project root (same folder as `manage.py`):

```powershell
Copy-Item .env.example .env
```

If `.env` already exists, edit it directly.

## 2. Required Variables

Set these values in `.env`:

```env
# Django
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,::1
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000,http://[::1]:8000

# Database
DATABASE_URL=

# Razorpay
RAZORPAY_MODE=mock
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=
```

## 3. Razorpay Modes

### Mock Mode (College Project / Demo)

Use this for presentations and evaluation without real transactions:

```env
RAZORPAY_MODE=mock
```

Behavior:
- Razorpay button is available.
- Payment is simulated.
- No real charge happens.

### Live Mode (Real Payments Later)

When launching real payments:

```env
RAZORPAY_MODE=live
RAZORPAY_KEY_ID=your_live_key_id
RAZORPAY_KEY_SECRET=your_live_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
```

Behavior:
- Server creates real Razorpay orders.
- Razorpay Checkout popup handles card/UPI/netbanking.
- Backend verifies payment signature.

## 4. Local Development Recommended Values

For local development:

- `DEBUG=True`
- `DATABASE_URL=` (empty to use SQLite)
- `RAZORPAY_MODE=mock`

## 5. Production Recommended Values

For production deployment:

- `DEBUG=False`
- `ALLOWED_HOSTS` set to your real domain(s)
- `CSRF_TRUSTED_ORIGINS` set to your `https://` domain(s)
- `DATABASE_URL` set to managed PostgreSQL URL
- `RAZORPAY_MODE=live` with live keys

## 6. Apply Changes

After editing `.env`, restart the Django server:

```powershell
env\Scripts\python.exe manage.py runserver
```

## 7. Quick Validation

Run system checks:

```powershell
env\Scripts\python.exe manage.py check
```

If there are no errors, environment configuration is loaded correctly.

## 8. Security Notes

- Never commit `.env` to git.
- Keep `SECRET_KEY`, `RAZORPAY_KEY_SECRET`, and webhook secrets private.
- Use HTTPS before enabling live payments.
