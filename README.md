BrightWorks – Household Services Application

A multi-user web application designed to connect customers with home-service professionals. Built as part of the Modern Application Development – I (September 2024 Term) course at IIT Madras.


# # Project Overview

BrightWorks is a role-based household service management platform that allows:

-Customers to browse services, raise service requests, and track status

-Service Professionals to manage requests assigned to them

-Admin to oversee users, services, analytics, and platform activity

-This project demonstrates full-stack development using Flask, SQLite, Jinja2, and Bootstrap, integrating backend logic, a dynamic frontend, and persistent data storage.

 
# # Features

# Role-Based System

# Admin

-Manage customers and service professionals

-Add/modify services

-Monitor service requests

-View analytics dashboards (Chart.js)

# Service Professionals

-View assigned requests

-Update request status

-Manage personal profile

# Customers

-Register and log in

-Raise service requests

-Track request history

# # Core Functionalities

-Secure user login system (role-based)

-CRUD operations for services and requests

-Interactive admin dashboard with charts

-Responsive UI using Bootstrap

-Database-backed architecture with SQLite

# # Technology Stack

# Backend

-Flask

-SQLAlchemy

-SQLite

-Datetime (Python)

# Frontend

-HTML

-CSS

-Bootstrap

-Jinja2

-Chart.js (for admin analytics)

# Project Structure

project/
│── app.py
│── models.py
│── database.db
│── requirements.txt
│── static/
│   ├── css/
│   ├── js/
│   └── images/
│── templates/
│   ├── admin/
│   ├── customer/
│   ├── professional/
│   └── shared/
│── README.md




# # How to Run the Project

1. Clone the repository
git clone https://github.com/yourusername/BrightWorks.git
cd BrightWorks

2. Install dependencies
pip install -r requirements.txt

3. Run the application
python app.py

4. Open in browser
http://127.0.0.1:5000

# # Project Walkthrough Video

You can watch the complete demo here:
🔗 Video URL: https://drive.google.com/file/d/1Q8ui0YS08JsYbsqdjIOHpgSRkj0Fai5X/view?usp=sharing

# # Limitations

-API endpoints were not implemented due to time constraints

-Basic login system (no advanced authentication such as Flask-Login)

-Limited error handling in some flows

# # About the Developer

Name: Aritri Sarkar

Roll No: 23f2004529

Course: Modern Application Development – I

Email: 23f2004529@ds.study.iitm.ac.in

“I’m passionate about solving problems and learning new technologies. BrightWorks helped me understand full-stack development using Flask, SQL, and Bootstrap.”

# # Future Improvements

-Implement REST APIs

-Integrate Flask-Login for secure authentication

-Add payment gateway integration

-Include push notifications for request updates
