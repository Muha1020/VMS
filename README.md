# Visitor Management System (VMS)

A web-based Visitor Management System built with Django, developed as a final year project for Al-Hikmah University. The system replaces manual paper-based visitor logbooks with a secure, role-based digital solution.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [User Roles](#user-roles)
- [URL Routes](#url-routes)
- [Setup & Installation](#setup--installation)
- [Deployment](#deployment)
- [Security Notes](#security-notes)

---

## Overview

The VMS allows Security Unit personnel at Al-hikmah University to register visitors at the gate, track who is currently on campus, check visitors out when they leave, and blacklist individuals who should be denied entry. All other staff can view reports and the dashboard.

---

## Features

- **User Authentication** — Register, login, logout, and password reset via email
- **User Profiles** — Department assignment, profile picture upload
- **Visitor Check-In** — Security Unit staff register visitors with full details
- **Visitor Check-Out** — Mark visitors as checked out with a timestamp
- **Dashboard** — Live count of active visitors, today's total, and recent activity
- **Reports** — Full paginated log of all visitors with status indicators
- **Blacklisting** — Block individuals by phone number; blocked visitors cannot be checked in
- **Print Report** — Browser print functionality on the report page
- **Role-Based Access** — Security Unit staff can register, check out, and blacklist; all other staff are read-only
- **Django Admin** — Full CRUD access for superusers

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Django 5.2 |
| Database | PostgreSQL (Neon cloud-hosted) |
| Frontend | HTML5, Bootstrap 5.3, custom CSS |
| Icons | Phosphor Icons |
| Font | Plus Jakarta Sans (Google Fonts) |
| Static Files | WhiteNoise |
| Production Server | Gunicorn |
| Image Handling | Pillow |

---

## Project Structure

```
visitor_system/
├── visitor_system/          # Django project configuration
│   ├── settings.py          # App settings, database, static files
│   ├── urls.py              # Root URL dispatcher
│   ├── wsgi.py              # WSGI entry point (production)
│   └── asgi.py              # ASGI entry point (async)
│
├── users/                   # User authentication & profiles app
│   ├── models.py            # Profile model (extends Django User)
│   ├── views.py             # Register, profile update, password reset
│   ├── forms.py             # UserRegisterForm, UserUpdateForm, ProfileUpdateForm
│   ├── signals.py           # Auto-creates Profile on User creation
│   ├── urls.py
│   └── admin.py
│
├── visitor/                 # Visitor tracking app
│   ├── models.py            # Visitor model, Blacklist model
│   ├── views.py             # Dashboard, register, report, checkout, blacklist
│   ├── urls.py
│   └── admin.py
│
├── templates/
│   ├── base.html            # Base layout: sidebar, top nav, messages
│   ├── user/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   ├── welcome.html
│   │   ├── password_reset.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_confirm.html
│   │   ├── password_reset_complete.html
│   │   └── password_reset_email.txt
│   └── visitor/
│       ├── index.html           # Dashboard
│       ├── visitor.html         # Visitor registration form
│       ├── report.html          # Full visitor log
│       ├── blacklist.html       # Blacklist management page
│       └── blacklist_confirm.html  # Blacklist confirmation form
│
├── static/
│   ├── css/premium.css      # Custom UI: dark sidebar, card layout, animations
│   └── js/actions.js        # Sidebar toggle, mobile responsive behaviour
│
├── manage.py
├── requirements.txt
├── Procfile                 # Heroku/Render deployment command
└── create_test_user.py      # Script to seed an admin/Security Unit user
```

---

## Database Models

### `users.Profile`

Extends Django's built-in `User` model via a OneToOne relationship.

| Field | Type | Description |
|---|---|---|
| `user` | OneToOneField | Links to Django auth User |
| `image` | ImageField | Profile picture (default: `default.jpg`) |
| `dept` | CharField(100) | Department name, e.g. `Security Unit` |

A Django signal automatically creates and saves a `Profile` whenever a `User` is created or saved.

---

### `visitor.Visitor`

Records every visitor check-in event.

| Field | Type | Description |
|---|---|---|
| `first_name` | CharField(50) | Visitor's first name |
| `last_name` | CharField(50) | Visitor's last name |
| `phone` | CharField(20) | Contact phone number |
| `email` | EmailField | Optional email address |
| `address` | TextField | Optional home address |
| `purpose_of_visit` | CharField(200) | Reason for visiting |
| `host_name` | CharField(100) | Name of the person being visited |
| `check_in_time` | DateTimeField | Auto-set to current time on creation |
| `check_out_time` | DateTimeField | Set when visitor is checked out (nullable) |
| `status` | CharField | `Checked In` or `Checked Out` |
| `recorded_by` | ForeignKey(User) | Security personnel who logged the entry |

---

### `visitor.Blacklist`

Stores individuals who are denied entry. Keyed on phone number.

| Field | Type | Description |
|---|---|---|
| `phone` | CharField(20) | Unique identifier used to block at check-in |
| `first_name` | CharField(50) | Visitor's first name |
| `last_name` | CharField(50) | Visitor's last name |
| `reason` | TextField | Reason for blacklisting |
| `blacklisted_by` | ForeignKey(User) | Staff member who added the entry |
| `blacklisted_at` | DateTimeField | Timestamp of when they were blacklisted |

When a visitor is being registered, their phone number is checked against this table. If a match is found, check-in is blocked and the reason is shown to the security officer.

---

## User Roles

Access is determined by the `dept` field on a user's profile.

| Role | How to Set | Permissions |
|---|---|---|
| **Security Unit** | Set `dept = Security Unit` in profile or admin | Register visitors, check out visitors, blacklist visitors, view all pages |
| **Regular Staff** | Any other department value | View dashboard and reports only |
| **Superuser** | Django `is_superuser = True` | All of the above + Django admin panel |

---

## URL Routes

### Users App

| URL | View | Access |
|---|---|---|
| `/` or `/Welcome/` | Welcome / landing page | Public |
| `/register/` | User registration | Public |
| `/login/` | Login | Public |
| `/logout/` | Logout (POST) | Authenticated |
| `/profile/` | Profile update | Authenticated |
| `/password-reset/` | Request password reset email | Public |
| `/password-reset/done/` | Reset email sent confirmation | Public |
| `/password-reset-confirm/<uidb64>/<token>/` | Set new password | Public (via email link) |
| `/password-reset-complete/` | Reset success page | Public |

### Visitor App

| URL | View | Access |
|---|---|---|
| `/index/` | Dashboard | Authenticated |
| `/visitor/` | Register a new visitor | Security Unit only |
| `/report/` | Full visitor log | Authenticated |
| `/checkout/<id>/` | Check out a visitor | Security Unit only |
| `/blacklist/` | View blacklist | Security Unit only |
| `/blacklist/<visitor_id>/` | Blacklist a visitor (confirmation form) | Security Unit only |
| `/blacklist/remove/<entry_id>/` | Remove from blacklist | Security Unit only |

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- pip
- A PostgreSQL database (or use the existing Neon connection string)

### Steps

```bash
# 1. Clone or copy the project
cd visitor_system

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your database
# Open visitor_system/settings.py and update the DATABASES connection string,
# or set it as an environment variable (recommended for production).

# 5. Apply migrations
python manage.py migrate

# 6. Create a superuser / test Security Unit account
python create_test_user.py
# Creates: username=admin, password=admin123, dept=Security Unit

# 7. Collect static files (for production / WhiteNoise)
python manage.py collectstatic --noinput

# 8. Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/login/` to log in.

---

## Deployment

The project is configured for deployment on Render or Heroku.

- **`Procfile`** — `web: gunicorn visitor_system.wsgi` starts the production server
- **WhiteNoise** — serves static files without a separate web server
- **`dj-database-url`** — parses the `DATABASE_URL` environment variable
- **`DEBUG = False`** — already set for production

### Recommended Environment Variables

Store these as environment variables rather than hardcoding them in `settings.py`:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | Full PostgreSQL connection string |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |

---

## Security Notes

The following items should be addressed before treating this as a hardened production deployment:

1. **`SECRET_KEY` is hardcoded** in `settings.py` — move it to an environment variable
2. **Database credentials are hardcoded** — use `DATABASE_URL` env var via `dj-database-url`
3. **`ALLOWED_HOSTS = ['*']`** — restrict to your actual domain in production
4. **`MEDIA_ROOT` / `MEDIA_URL`** are not configured — profile image uploads may not persist correctly on cloud platforms; consider using object storage (e.g. AWS S3)
5. **Role check is a string comparison** — if a user's `dept` value is mistyped it silently falls back to read-only; consider using a dedicated boolean or choices field for the Security Unit role

---

## Author

**Abubakar Usman Malami** — 20222031
Department of Computer Science, Faculty of Computing
Nile University of Nigeria

Supervisor: Mr. Ahmed Adeniyii
Submitted: 20/01/2025
