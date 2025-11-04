# 🗑️ SMARTRASH - Smart Waste Management System

A comprehensive IoT-based waste management system that connects municipalities, customers, collection agents, and recyclers through an intelligent platform with smart bin monitoring.

![Django](https://img.shields.io/badge/Django-3.2-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![IoT](https://img.shields.io/badge/IoT-Enabled-orange)

## 🌟 Features

### 🤖 Smart Bin Monitoring
- **Real-time Level Detection**: Ultrasonic sensors monitor waste levels
- **Automatic Notifications**: Alerts when bins reach 75% capacity
- **IoT Integration**: NodeMCU with WiFi connectivity
- **LED Status Indicators**: Visual feedback for bin status

### 💰 Digital Payment System
- **Wallet Integration**: Prepaid wallet system for payments
- **Automated Billing**: Automatic payment processing
- **Collection Fees**: Configurable rates per municipality
- **Recycling Payments**: Dynamic pricing based on waste type

### 🔄 Multi-User Platform
- **Customers**: Bin linking, payment, recycler booking
- **Municipalities**: Dashboard, user approval, task assignment
- **Collection Agents**: Task management, waste collection
- **Recyclers**: Booking management, rate configuration
- **Admin**: System oversight and management

### ♻️ Recycling Integration
- **Waste Type Classification**: Plastic, Paper, Metal
- **Dynamic Pricing**: Different rates for different materials
- **Booking System**: Schedule recyclable waste collection
- **Agent Assignment**: Integrated collection workflow

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 3.2
- NodeMCU (for hardware implementation)
- SQLite/MySQL Database

### Installation

1. **Clone and Setup Project**
```bash
# Create project directory
django-admin startproject smartrash
cd smartrash
python manage.py startapp waste

# Install dependencies
pip install django==3.2 mysqlclient pillow



SMARTRASH - Smart Waste Management System
A comprehensive IoT-based waste management system that connects municipalities, customers, collection agents, and recyclers through an intelligent platform with smart bin monitoring.

https://img.shields.io/badge/Django-3.2-green
https://img.shields.io/badge/Python-3.8+-blue
https://img.shields.io/badge/IoT-Enabled-orange

🌟 Features
🤖 Smart Bin Monitoring
Real-time Level Detection: Ultrasonic sensors monitor waste levels

Automatic Notifications: Alerts when bins reach 75% capacity

IoT Integration: NodeMCU with WiFi connectivity

LED Status Indicators: Visual feedback for bin status

💰 Digital Payment System
Wallet Integration: Prepaid wallet system for payments

Automated Billing: Automatic payment processing

Collection Fees: Configurable rates per municipality

Recycling Payments: Dynamic pricing based on waste type

🔄 Multi-User Platform
Customers: Bin linking, payment, recycler booking

Municipalities: Dashboard, user approval, task assignment

Collection Agents: Task management, waste collection

Recyclers: Booking management, rate configuration

Admin: System oversight and management

♻️ Recycling Integration
Waste Type Classification: Plastic, Paper, Metal

Dynamic Pricing: Different rates for different materials

Booking System: Schedule recyclable waste collection

Agent Assignment: Integrated collection workflow

🚀 Quick Start
Prerequisites
Python 3.8+

Django 3.2

NodeMCU (for hardware implementation)

SQLite/MySQL Database

Installation
Clone and Setup Project

bash
# Create project directory
django-admin startproject smartrash
cd smartrash
python manage.py startapp waste

# Install dependencies
pip install django==3.2 mysqlclient pillow
Database Configuration

bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
Environment Setup

bash
# Create .env file with following variables:
DATABASE_NAME=smartrash
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=3306
SECRET_KEY=your_secret_key
Run Development Server

bash
python manage.py runserver
🏗️ Project Structure
text
smartrash/
├── waste/                    # Main application
│   ├── models.py            # Database models
│   ├── views.py             # Application logic
│   ├── urls.py              # URL routing
│   └── templates/           # HTML templates
├── smartrash/               # Project settings
│   ├── settings.py          # Django settings
│   └── urls.py              # Main URL config
└── static/                  # Static files
    ├── css/
    ├── js/
    └── images/
🔧 Configuration
Database Setup
python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartrash',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
IoT Hardware Requirements
NodeMCU ESP8266

Ultrasonic Sensor (HC-SR04)

LED Indicators (Red, Green, Yellow)

Jumper Wires & Breadboard

5V Power Supply

🔌 API Endpoints
Customer Endpoints
POST /api/customer/register/ - Customer registration

POST /api/customer/login/ - Customer login

GET /api/customer/bins/ - Get customer bins

POST /api/customer/link-bin/ - Link bin to customer

Municipal Endpoints
GET /api/municipal/dashboard/ - Municipal dashboard

POST /api/municipal/assign-task/ - Assign collection task

GET /api/municipal/pending-approvals/ - Get pending approvals

Collection Agent Endpoints
GET /api/agent/tasks/ - Get assigned tasks

POST /api/agent/update-task/ - Update task status

GET /api/agent/collection-history/ - Collection history

Recycler Endpoints
POST /api/recycler/set-rates/ - Set recycling rates

GET /api/recycler/bookings/ - Get recycling bookings

POST /api/recycler/update-booking/ - Update booking status

🎯 Usage Guide
For Customers
Register and verify account

Link your smart bin using bin ID

Add funds to wallet

Schedule recycling collections

Monitor bin status in real-time

For Municipalities
Approve customer registrations

Monitor bin fill levels across city

Assign collection tasks to agents

Configure collection rates

Generate reports and analytics

For Collection Agents
Receive task notifications

Update collection status

Process payments from customer wallets

Coordinate with recyclers

For Recyclers
Set dynamic pricing for materials

Accept recycling bookings

Coordinate collection with agents

Process recycling payments

🔬 IoT Integration
Hardware Setup
cpp
// NodeMCU Code Structure
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>

// Sensor pins
const int trigPin = D1;
const int echoPin = D2;
const int ledRed = D5;
const int ledGreen = D6;
const int ledYellow = D7;

void setup() {
  // Initialize sensors and WiFi
  // Connect to WiFi network
  // Setup HTTP client
}

void loop() {
  // Read ultrasonic sensor
  // Calculate distance/level
  // Update LED indicators
  // Send data to Django server
  // Handle server responses
}
2. 
