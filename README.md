# Flight Route System

## Overview

The **Flight Route System** is a Django-based web application with **role-based authentication** that manages airport connections and routes. The project includes separate dashboards, registration, and restricted views for **Admin** and **User** roles.

* **Admin Dashboard:** Admins can add, edit, delete airports, and manage airport connections.
* **User Dashboard:** Users can view airport lists and find the shortest route between airports.
* **Role-Based Access:** Admin and User have separate access permissions — users cannot access admin functions.

---

## Setup Instructions

### 1. Clone or Download the Project

```bash
git clone https://github.com/albertthomas2205/flights_routes_system
cd flight_route_system
```

---

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

Install all required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 4. Database Setup

Run the following commands to create and apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Then open your browser and go to:

```
http://127.0.0.1:8000/
```

---

## Features

### 👨‍💼 Admin Features

* Register as an Admin.
* Log in to the Admin Dashboard.
* Add new airports.
* Edit or delete existing airports.
* Create and manage connections between airports (with left and right direction distances).
* Full CRUD access to airport data.

### 🧑‍✈️ User Features

* Register as a User.
* Log in to the User Dashboard.
* View available airports.
* Find the **shortest path** between two airports based on connection distances.
* Users have **restricted access** — cannot view or modify admin-only pages or data.

### 🔐 Role-Based Authentication

* Each user has a defined role (Admin/User) assigned at registration.
* Access to views and dashboard pages is restricted based on user role.
* Unauthorized access redirects to the appropriate dashboard or login page.

---

## File Summary

* **`manage.py`** — Django project management file.
* **`requirements.txt`** — Lists all dependencies needed to run the project.
* **`flight_route_system/`** — Main Django project folder containing settings, URLs, and configurations.
* **`airports/`** — Django app managing airport models, routes, and business logic.

---

## Example Workflow

1. **Registration:** User or Admin registers through their respective registration page.
2. **Login:** System authenticates based on role (Admin/User).
3. **Admin Workflow:**

   * Logs into admin dashboard.
   * Adds or edits airports.
   * Creates connections (with left/right distance values).
4. **User Workflow:**

   * Logs into user dashboard.
   * Views airport list.
   * Selects start and destination airports.
   * System calculates and displays the **shortest route**.
5. **Access Control:**

   * Admin-only routes (add/edit/delete airports) are protected.
   * Users can only view data and find routes.

---

## Notes

* Uses Django’s authentication system for role-based login and access control.
* Ensure your virtual environment is activated before running any commands.
* All dependencies are listed in `requirements.txt`.
* The project uses `db.sqlite3` by default; you can change the database in `settings.py` if needed.

---

## Author

**Albert Thomas**
Python Full Stack Developer
📧 Email: [albertjohny000@gmail.com](mailto:albertjohny000@gmail.com)
