# Global Mart E-Commerce (Django)

A Django-based e-commerce web application with product browsing, cart, wishlist, checkout, order history, user profile, and address management.

## Tech Stack

- Python
- Django 6.0.3
- SQLite (default, `db.sqlite3`)

## Features

- User authentication (signup, login, logout)
- Product listing with search
- Product detail pages
- Shopping cart management
  - Add to cart
  - Increase/decrease quantity
  - Remove item
- Wishlist management
- Checkout flow with payment page (basic flow)
- Order creation and order history
- User profile and profile edit
- User address management (India-focused fields)
- Django Admin with enhanced product/order/address admin views
- Multiple product image support via `ProductImage`

## Project Structure

```text
ecommerce_project/
  manage.py
  requirements.txt
  db.sqlite3
  myshop/
    settings.py
    urls.py
  store/
    models.py
    views.py
    urls.py
    templates/
```

## Installation and Setup

1. Clone or open the project folder.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Run migrations.
5. Create an admin user.
6. Start the development server.

### Windows PowerShell Commands

```powershell
cd c:\Users\iamre\Desktop\College Project\ecommerce_project

# Activate existing venv (if already present)
.\env\Scripts\Activate.ps1

# Alternative (if you stay in parent folder):
# .\ecommerce_project\env\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Open:

- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Main URL Endpoints

### Public / Auth

- `/` - Product list
- `/signup/` - User signup
- `/accounts/login/` - Login (provided by Django auth)
- `/accounts/logout/` - Logout (provided by Django auth)
- `/product/<id>/` - Product details

### Cart and Checkout

- `/cart/` - Cart detail
- `/add-to-cart/<product_id>/`
- `/remove-from-cart/<item_id>/`
- `/increase-qty/<item_id>/`
- `/decrease-qty/<item_id>/`
- `/payment/` - Checkout/payment page
- `/order-success/` - Order success page

### Profile, Address, Wishlist

- `/profile/` - User profile and order summary
- `/profile/edit/`
- `/profile/add-address/`
- `/profile/update-address/`
- `/wishlist/`
- `/wishlist/add/<product_id>/`
- `/wishlist/remove/<item_id>/`

## Data Models (Store App)

- `Product`
- `ProductImage`
- `Cart`, `CartItem`
- `Order`, `OrderItem`
- `UserAddress`
- `Wishlist`, `WishlistItem`

## Useful Development Commands

```powershell
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
python manage.py test

# Django system checks
python manage.py check
```

## Notes

- Default DB is SQLite (`db.sqlite3`).
- This setup is suitable for development and learning; production deployment requires additional hardening.
- In `myshop/settings.py`, `DEBUG=True` is enabled for local development.

## Deployment Guide (Student Pack Friendly)

This project is now prepared for cloud deployment using:

- `gunicorn` as production server
- `whitenoise` for static files
- `DATABASE_URL` for managed PostgreSQL

### 1) Push Project to GitHub

```powershell
git add .
git commit -m "Prepare Django app for production deployment"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 2) Deploy to a Free Host (Render Example)

1. Sign in to Render and create a new **Web Service** from your GitHub repo.
2. Set:
  - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
  - Start command: `gunicorn myshop.wsgi:application`
3. Add environment variables from `.env.example`:
  - `SECRET_KEY`
  - `DEBUG=False`
  - `ALLOWED_HOSTS=your-render-service.onrender.com,yourdomain.com,www.yourdomain.com`
  - `CSRF_TRUSTED_ORIGINS=https://your-render-service.onrender.com,https://yourdomain.com,https://www.yourdomain.com`
4. Create a managed PostgreSQL database and set `DATABASE_URL` in your web service.

### 3) Connect Free Domain from Student Pack

If your free domain is from Namecheap/Name.com:

1. In Render web service settings, add custom domains:
  - `yourdomain.com`
  - `www.yourdomain.com`
2. In your domain DNS panel:
  - Add `CNAME` record: `www` -> `<your-render-service>.onrender.com`
  - Add root/apex record as instructed by Render (ANAME/ALIAS/A)
3. Wait for DNS propagation (usually a few minutes to 24 hours).
4. Verify HTTPS certificate is issued (automatic on Render).

### 4) Create Admin User on Production

Use host shell/console:

```bash
python manage.py createsuperuser
```

### 5) Post-Deploy Checklist

- `DEBUG=False`
- Secret key is not hardcoded in host settings
- PostgreSQL is used in production
- Static files load correctly
- Login, cart, checkout, and order flows are tested

## DigitalOcean Deployment (Recommended for Your Student Pack)

If you want to use DigitalOcean credits from GitHub Student Pack, use **App Platform**.

### 1) Push this repository to GitHub

```powershell
git add .
git commit -m "Add DigitalOcean deployment config"
git push origin main
```

### 2) Use included App Spec

This project includes a ready App Platform spec at `.do/app.yaml`.

Before importing, update these placeholders in `.do/app.yaml`:

- `YOUR_GITHUB_USERNAME/YOUR_REPO_NAME`
- `your-app.ondigitalocean.app`
- `yourdomain.com`

### 3) Create app from spec (App Platform)

1. Open DigitalOcean -> App Platform -> **Create App**.
2. Choose **GitHub** and select this repository.
3. Choose **Edit App Spec** and paste/import `.do/app.yaml`.
4. Review plan and launch app.

The spec already defines:

- Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Run command: `python manage.py migrate && gunicorn myshop.wsgi:application --bind 0.0.0.0:$PORT`
- Managed PostgreSQL (`DATABASE_URL` linked from DigitalOcean DB)

### 4) Set secure runtime values

In App Settings -> Environment Variables, replace:

- `SECRET_KEY` with a long random secret
- host/domain values for `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`

### 5) Attach your free domain

1. In App Platform -> Settings -> Domains, add:
  - `yourdomain.com`
  - `www.yourdomain.com`
2. In domain DNS panel (Namecheap/Name.com), add required records shown by DigitalOcean.
3. Wait for propagation and confirm SSL becomes active.

### 6) Initialize production admin

Use the App Console:

```bash
python manage.py createsuperuser
```

## Author

- Bhudeb Kumar Munda

## License

This project is submitted as a Final Year Project and is intended for academic evaluation and learning purposes.

Copyright (c) 2026 Bhudeb Kumar Munda. All rights reserved.

You may:

- View and reference this project for educational purposes.

You may not:

- Copy and submit this project (or modified versions) as your own academic work.
- Use this project for commercial purposes without written permission from the author.
- Redistribute substantial parts of this code without proper attribution and permission.
