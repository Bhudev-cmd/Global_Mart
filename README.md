# Global Mart E-Commerce (Django)

Global Mart is a Django 6 based e-commerce web app with product browsing, cart, wishlist, address management, checkout, and order history.

## Current Project Status

- Active and deployable in cloud and VPS environments.
- Local development works with SQLite.
- Production configuration supports PostgreSQL via `DATABASE_URL`.
- Admin supports management for products, product images, orders, order items, addresses, wishlists, and wishlist items.

## Tech Stack

- Python 3
- Django 6.0.3
- SQLite (local development)
- PostgreSQL (production)
- Gunicorn
- WhiteNoise
- dj-database-url
- psycopg 3

## Core Features

- User signup, login, logout
- Product list with search
- Product detail page with multiple product images support
- Cart management
  - Add item
  - Increase and decrease quantity
  - Remove item
- Wishlist management
  - Add item
  - Remove item
- Address management
- Checkout flow
  - Requires saved address
  - Creates order and order items
  - Clears cart after successful checkout
- Profile page with account details and order history
- Django admin support for operations

## Data Model Overview

### Product Catalog

- `Product`: name, description, price, stock, image_url
- `ProductImage`: product relation, image_url, is_primary, display_order

### Shopping and Orders

- `Cart`: one-to-one with user
- `CartItem`: cart, product, quantity
- `Order`: user, created_at, total_price, status
- `OrderItem`: order, product, frozen price, quantity

### Customer Data

- `UserAddress`: one-to-one with user, full_name, phone, street_address, landmark, city, state, pin_code, country
- `Wishlist`: one-to-one with user
- `WishlistItem`: wishlist, product, added_at

## URL Endpoints

### Public and Authentication

- `/` : Product listing
- `/signup/` : Signup page
- `/accounts/login/` : Login (Django auth)
- `/accounts/logout/` : Logout (Django auth)
- `/product/<int:product_id>/` : Product detail

### Cart and Checkout

- `/cart/`
- `/add-to-cart/<int:product_id>/`
- `/remove-from-cart/<int:item_id>/`
- `/increase-qty/<int:item_id>/`
- `/decrease-qty/<int:item_id>/`
- `/payment/`
- `/order-success/`

### Profile, Address, Wishlist

- `/profile/`
- `/profile/edit/`
- `/profile/add-address/`
- `/profile/update-address/`
- `/wishlist/`
- `/wishlist/add/<int:product_id>/`
- `/wishlist/remove/<int:item_id>/`

### Admin

- `/admin/`

## Project Structure

```text
ecommerce_project/
  manage.py
  requirements.txt
  db.sqlite3
  Procfile
  myshop/
    settings.py
    urls.py
    wsgi.py
  store/
    admin.py
    models.py
    views.py
    urls.py
    templates/
```

## Local Setup (Any Computer)

### 1. Clone or Download the Project

```powershell
git clone <your-repo-url>
cd <your-project-folder>
```

If you already have the project as a zip, extract it and open a terminal in that extracted folder (the folder containing `manage.py`).

### 2. Ensure Python Is Installed and Available in PATH

Check Python and pip:

```powershell
python --version
pip --version
```

If Python is not recognized:

- Reinstall Python from python.org.
- During installation, enable the checkbox: "Add python.exe to PATH".
- Restart the terminal and run the version commands again.

### 3. Create and Activate Virtual Environment

Create environment:

```powershell
python -m venv env
```

Activate on Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

Activate on macOS/Linux:

```bash
source env/bin/activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Apply Database Migrations

```powershell
python manage.py migrate
```

### 6. Create Admin User (Optional but Recommended)

```powershell
python manage.py createsuperuser
```

### 7. Run Development Server

```powershell
python manage.py runserver
```

Open in browser:

- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Useful Commands

```powershell
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
python manage.py test

# System checks
python manage.py check

# Collect static files
python manage.py collectstatic --noinput
```

## Environment Variables

Supported environment variables:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`

Defaults:

- If `DATABASE_URL` is not set, SQLite is used (`db.sqlite3`).
- `DEBUG` defaults to `True` for local development.

## Deployment

This project can be hosted on multiple platforms, not only DigitalOcean.

### Common Production Build and Start Commands

- Build command:
  - `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Start command:
  - `python manage.py migrate && gunicorn myshop.wsgi:application`

### Common Production Environment Variables

- `SECRET_KEY`: secure random string
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: comma-separated domains
- `CSRF_TRUSTED_ORIGINS`: full `https` origins (comma-separated)
- `DATABASE_URL`: managed PostgreSQL connection string

### DigitalOcean App Platform

- You can use app specs for build and run.
- Recommended run command:
  - `python manage.py migrate && gunicorn myshop.wsgi:application --bind 0.0.0.0:$PORT`

### Render

- Build command:
  - `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Start command:
  - `python manage.py migrate && gunicorn myshop.wsgi:application`

### Railway

- Build command:
  - `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Start command:
  - `python manage.py migrate && gunicorn myshop.wsgi:application --bind 0.0.0.0:$PORT`

### Heroku

- `Procfile` is already present and can be used.
- Set required config vars:
  - `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL`

### Fly.io

- Use Gunicorn as the web process.
- Ensure `$PORT` binding is present:
  - `python manage.py migrate && gunicorn myshop.wsgi:application --bind 0.0.0.0:$PORT`

### AWS Elastic Beanstalk

- Use Python platform.
- Configure environment variables.
- Configure startup command to run migrate before Gunicorn.

### Azure App Service

- Linux Python App Service works well for Django.
- Startup command:
  - `python manage.py migrate && gunicorn myshop.wsgi:application --bind 0.0.0.0:$PORT`

### Google Cloud Run

- Containerize app with Gunicorn entrypoint.
- Ensure service listens on `$PORT`.
- Run migrations as part of deploy/release workflow.

### VPS (Ubuntu + Nginx + Gunicorn)

- Deploy Gunicorn behind Nginx.
- Use a process manager (systemd or supervisor).
- Run migrations and collectstatic on each release.
- Use PostgreSQL in production.

## Troubleshooting Notes

- If admin pages return HTTP 500 in production, verify migrations were applied to the same database used by the running app.
- Confirm `DATABASE_URL` points to the expected production PostgreSQL instance.
- Check runtime logs for Python traceback (access logs alone are not enough for root cause).

## Author

- Bhudeb Kumar Munda

## License

This project is submitted as a Final Year Project for academic evaluation and learning purposes.

Copyright (c) 2026 Bhudeb Kumar Munda. All rights reserved.

You may:

- View and reference this project for educational purposes.

You may not:

- Copy and submit this project (or modified versions) as your own academic work.
- Use this project for commercial purposes without written permission from the author.
- Redistribute substantial parts of this code without proper attribution and permission.
