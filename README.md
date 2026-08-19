# Ecommerce Store

A basic e-commerce web application built with Django and Bootstrap 5.

## Features

- Product listings with search, category filter and sort
- Product detail page with related products
- Session-based shopping cart with AJAX updates
- Checkout with shipping and payment form
- Order processing and confirmation page
- Order history for logged-in users
- User registration and login
- Admin panel to manage products, categories and orders

## Tech Stack

- **Backend:** Django 6 (Python)
- **Frontend:** HTML, CSS (Bootstrap 5), Vanilla JavaScript
- **Database:** SQLite (development)

## Setup

1. Clone the repo and navigate into the folder:

```
cd ecommerce
```

2. Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Apply migrations:

```
python manage.py migrate
```

5. Load sample data (products + admin user):

```
python manage.py seed_data
```

6. Start the development server:

```
python manage.py runserver
```

Then open http://127.0.0.1:8000/

## Admin

URL: http://127.0.0.1:8000/admin/  
Username: `admin`  
Password: `admin123`

> Change the admin password before deploying to production.

## Project Structure

```
ecommerce/
├── ecommerce/          # Django project settings and urls
├── store/              # Main app (models, views, cart logic)
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── cart.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   └── store/
│       ├── product_list.html
│       ├── product_detail.html
│       ├── cart.html
│       ├── checkout.html
│       ├── order_confirm.html
│       ├── order_list.html
│       ├── login.html
│       └── register.html
├── static/
│   ├── css/main.css
│   └── js/main.js
├── media/              # Uploaded product images
├── manage.py
└── requirements.txt
```
