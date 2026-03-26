# Global Mart E-Commerce (Django)

Global Mart is a Django 6 based e-commerce web app with product browsing, cart, wishlist, address management, checkout, and order history.

## Current Project Status

- Active and deployable on DigitalOcean App Platform.
- Local development works with SQLite.
- Production-ready configuration supports PostgreSQL via DATABASE_URL.
- Admin includes management for products, product images, orders, order items, addresses, wishlists, and wishlist items.

## Tech Stack

- Python 3
- Django 6.0.3
- SQLite for local development
- PostgreSQL for production (via DATABASE_URL)
- Gunicorn
- WhiteNoise
- dj-database-url
- psycopg 3

## Core Features

- User signup, login, logout
- Product list with search
- Product detail page with multiple product images support
- Cart management:
  - Add to cart
  - Increase and decrease quantity
  - Remove item
- Wishlist management:
  - Add to wishlist
  - Remove from wishlist
- Address management (India-focused fields)
- Checkout flow:
  - Requires saved address
  - Creates order and order items
  - Clears cart after successful checkout
- Profile page with account information and order history
- Django admin support for operational management

## Data Model Overview

### Product Catalog

- Product: name, description, price, stock, image_url
- ProductImage: product relation, image_url, is_primary, display_order

### Shopping and Orders

- Cart: one-to-one with user
- CartItem: cart, product, quantity
- Order: user, created_at, total_price, status
- OrderItem: order, product, frozen price, quantity

### Customer Data

- UserAddress: one-to-one with user, full_name, phone, street_address, landmark, city, state, pin_code, country
- Wishlist: one-to-one with user
- WishlistItem: wishlist, product, added_at

## URL Endpoints

### Public and Authentication

- / : Product listing
- /signup/ : Signup page
- /accounts/login/ : Login (Django auth)
- /accounts/logout/ : Logout (Django auth)
- /product/<int:product_id>/ : Product detail

### Cart and Checkout

- /cart/
- /add-to-cart/<int:product_id>/
- /remove-from-cart/<int:item_id>/
- /increase-qty/<int:item_id>/
- /decrease-qty/<int:item_id>/
- /payment/
- /order-success/

### Profile, Address, Wishlist

- /profile/
- /profile/edit/
- /profile/add-address/
- /profile/update-address/
- /wishlist/
- /wishlist/add/<int:product_id>/
- /wishlist/remove/<int:item_id>/

### Admin

- /admin/

## Project Structure

```text
ecommerce_project/
  manage.py
  requirements.txt
  db.sqlite3
  Procfile
  .do/app.yaml
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

## Local Setup (Windows PowerShell)

```powershell
cd c:\Users\iamre\Desktop\ecommerce_project

# Activate virtual environment
.\env\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (optional but recommended)
python manage.py createsuperuser

# Run development server
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

These are supported by current settings:

- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- CSRF_TRUSTED_ORIGINS
- DATABASE_URL

Defaults:

- If DATABASE_URL is not set, SQLite is used (db.sqlite3).
- DEBUG defaults to True for local development.

## Deployment

### DigitalOcean App Platform (Current Recommended Path)

Use the included app spec in .do/app.yaml.

Current commands in app spec:

- Build command:
  - pip install -r requirements.txt && python manage.py collectstatic --noinput
- Run command:
  - python manage.py migrate && gunicorn myshop.wsgi:application --bind 0.0.0.0:$PORT

Why this matters:

- Migrations run at runtime against the live production database, reducing schema mismatch issues.

Important env setup in DigitalOcean:

- Set SECRET_KEY to a secure random value.
- Set DEBUG=False.
- Set ALLOWED_HOSTS with your app domain(s).
- Set CSRF_TRUSTED_ORIGINS with full https origins.
- Set DATABASE_URL from managed PostgreSQL.

### Render (Alternative)

Suggested setup:

- Build command:
  - pip install -r requirements.txt && python manage.py collectstatic --noinput
- Start command:
  - python manage.py migrate && gunicorn myshop.wsgi:application

## Troubleshooting Notes

- If admin pages return HTTP 500 in production, verify migrations were applied to the same database used by the running app.
- Confirm DATABASE_URL points to the expected managed PostgreSQL instance.
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
