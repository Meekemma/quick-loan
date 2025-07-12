---

# 💰 QuickCheck Loan Management Platform

A Django-powered backend for a fintech loan management platform. Users can register, log in, apply for loans, and track their loan statuses. Admins can approve, reject, or flag suspicious applications using basic fraud detection logic.

---

## ✨ Features

* User registration and login (JWT authentication)
* Submit and track loan applications
* Admin endpoints for:

  * Approving, rejecting, or flagging loans
  * Viewing all flagged loans
* Built-in fraud detection logic for:

  * Rapid loan submissions
  * Excessively large loan amounts
  * Suspicious email domain usage
* Unit tests using `pytest` and `pytest-django`

---

## 🛠️ Tech Stack

* **Language**: Python 3.9+
* **Framework**: Django 4.x
* **API Layer**: Django REST Framework
* **Authentication**: JWT (`djangorestframework-simplejwt`)
* **Testing**: Pytest, Pytest-Django
* **Database**: SQLite (for development)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/quickcheck.git
cd quickcheck
```

### 2. Create and Configure `.env`

Create a `.env` file in the root directory with the following content:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

To generate a `SECRET_KEY`, run the following:

```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

---

## 📦 Install Dependencies

```bash
python -m venv env
source env/bin/activate  # For Windows: env\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Apply Migrations and Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## ▶️ Run the Development Server

```bash
python manage.py runserver
```

---

## 🔗 API Endpoints

### 🔐 Account

| Method | Endpoint                  | Description              |
| ------ | ------------------------- | ------------------------ |
| POST   | `/account/registration/`  | Register a new user      |
| POST   | `/account/login/`         | Obtain JWT tokens        |
| POST   | `/account/token/refresh/` | Refresh access token     |
| POST   | `/account/logout/`        | Logout (blacklist token) |

### 💼 Loan

| Method | Endpoint                                   | Description                       |
| ------ | ------------------------------------------ | --------------------------------- |
| POST   | `/loan/loan-request/<uuid:user_id>/`       | Submit a loan application         |
| GET    | `/loan/retrieve-all-loans/<uuid:user_id>/` | View all user’s loan applications |
| PATCH  | `/loan/admin/loan/<int:loan_id>/`          | Admin updates loan status         |
| GET    | `/loan/admin/flagged-loans/`               | Admin views flagged loans         |

---

## 🧪 Running Tests

```bash
pytest
```

Tests include:

* ✅ Successful loan application submission
* 🚨 Fraud detection logic for high-risk loan behavior

---

## 📌 Assumptions & Design Choices

* **Custom User Model**: Used instead of Django’s default to gain full control over user fields and behavior.
* **Email Uniqueness**: The `email` field is set as unique, ensuring each account is tied to a single user.
* **Email Verification**: Since no email backend is set up to render OTP, users are marked as verified (`is_verified=True`) by default.
* **Fraud Detection**:

  * More than 3 loan applications in 24 hours
  * Loan amount exceeding ₦5,000,000
  * Over 10 users sharing the same email domain

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

