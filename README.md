# SMARTRASH - Smart Waste Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2+-green.svg)](https://www.djangoproject.com/)

A comprehensive IoT-enabled waste management system that connects municipalities, collection agents, recyclers, and customers for efficient waste collection and recycling services.

## 📋 Table of Contents
- [About](#about)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Hardware Requirements](#hardware-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributors](#contributors)
- [License](#license)

## 🎯 About

SMARTRASH is a B.Tech final year project developed at MES College of Engineering, Kuttippuram (2021-2022). The system aims to implement efficient waste management by creating a seamless link between municipalities, collection agents, recyclers, and customers (hotels, industries, households, etc.).

The project features a **Smart Waste Bin** equipped with IoT sensors that automatically detects when waste reaches 75% capacity and notifies the municipality for timely collection.

## ✨ Features

### For Customers
- 🏠 **Smart Bin Integration** - Link and monitor IoT-enabled waste bins
- 💰 **Digital Wallet** - Secure payment system for waste collection services
- ♻️ **Recycler Booking** - Sell recyclable waste to recyclers
- 📊 **Booking History** - Track all waste collection activities
- 🆘 **Enquiry System** - Submit queries, complaints, and feedback

### For Collection Agents
- 📋 **Task Management** - View and manage assigned collection tasks
- 🚛 **Waste Collection** - Enter bin IDs and verify collections
- 📜 **History Tracking** - Access complete collection history

### For Municipalities
- 👥 **User Management** - Approve customers, agents, and recyclers
- 📅 **Task Assignment** - Assign collection tasks to agents
- 💵 **Pricing Control** - Set collection charges
- 📊 **Analytics Dashboard** - Monitor all operations

### For Recyclers
- 🗑️ **Recycling Requests** - Receive and process recycling bookings
- 💳 **Payment Management** - Handle transactions through digital wallet
- 📈 **Task Tracking** - Monitor recycling operations

### For Admin
- 🏛️ **Municipality Management** - Add and manage municipalities

## 🏗️ System Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Customer  │────▶│ Municipality │◀────│    Admin    │
└─────────────┘     └──────────────┘     └─────────────┘
       │                    │
       │                    │
       ▼                    ▼
┌─────────────┐     ┌──────────────┐
│  Smart Bin  │     │  Collection  │
│   (IoT)     │     │    Agent     │
└─────────────┘     └──────────────┘
       │                    │
       └────────┬───────────┘
                │
                ▼
         ┌──────────────┐
         │   Recycler   │
         └──────────────┘
```

## 🛠️ Technologies Used

### Backend
- **Python 3.8+**
- **Django 3.2+** - Web framework
- **MySQL** - Database

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 4/5** - UI framework

### Hardware
- **NodeMCU (ESP8266)** - WiFi-enabled microcontroller
- **HC-SR04 Ultrasonic Sensor** - Distance measurement
- **LEDs** - Status indicators (Blue: WiFi, Green: Normal, Red: Full)

### Tools
- **Git** - Version control
- **Arduino IDE** - Hardware programming
- **VS Code** - Development environment

## 🔌 Hardware Requirements

### Smart Bin Components
- NodeMCU ESP8266
- HC-SR04 Ultrasonic Sensor
- 3x LEDs (Blue, Green, Red)
- Resistors and connecting wires
- Power supply (5V)

### Pin Configuration
```
NodeMCU Pin | Component
------------|----------
D1          | Trigger Pin (Ultrasonic)
D2          | Echo Pin (Ultrasonic)
D5          | Blue LED (WiFi Status)
D6          | Green LED (Normal)
D7          | Red LED (Bin Full)
GND         | Ground
VIN         | 5V Power
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- Git
- Arduino IDE (for hardware programming)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/smartrash.git
cd smartrash
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**
- Create a MySQL database named `smartrash_db`
- Update `settings.py` with your database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartrash_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

### Hardware Setup

1. **Install Arduino IDE**
   - Download from [arduino.cc](https://www.arduino.cc/en/software)

2. **Add ESP8266 Board Support**
   - Go to File → Preferences
   - Add to Additional Board Manager URLs:
     ```
     http://arduino.esp8266.com/stable/package_esp8266com_index.json
     ```
   - Go to Tools → Board → Board Manager
   - Search and install "esp8266"

3. **Upload Smart Bin Code**
   - Open `hardware/smart_bin/smart_bin.ino`
   - Configure WiFi credentials
   - Select Board: NodeMCU 1.0 (ESP-12E Module)
   - Select correct Port
   - Upload to NodeMCU

## 🚀 Usage

### Customer Portal
1. Register on the platform
2. Wait for municipality approval
3. Link your smart bin using Bin ID
4. Monitor bin status
5. Receive notifications for collection
6. Manage wallet and payments

### Collection Agent Portal
1. Register and get approved
2. View assigned tasks
3. Collect waste and verify using Bin ID
4. Track collection history

### Municipality Portal
1. Login with credentials
2. Approve/reject registrations
3. Assign collection tasks
4. Monitor smart bins
5. Set collection charges
6. View analytics

### Recycler Portal
1. Register and get approved
2. Receive recycling requests
3. Assign collection dates
4. Manage payments

## 📁 Project Structure

```
smartrash/
├── hardware/
│   └── smart_bin/
│       ├── smart_bin.ino
│       └── config.h
├── smartrash_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── customer/
│   ├── collection_agent/
│   ├── municipality/
│   ├── recycler/
│   └── admin_panel/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   ├── home.html
│   └── ...
├── media/
├── requirements.txt
├── manage.py
├── .gitignore
└── README.md
```

## 👥 Contributors

This project was developed by:

- **Anaina R** (MES18CS015)
- **Jumana Mampalli** (MES18CS042)
- **Nimisha K Rajesh** (MES18CS076)
- **Shamila P** (MES18CS099)

**Project Guide:** Ms. Swathy Sekhar, Assistant Professor, CSE Department

**Institution:** MES College of Engineering, Kuttippuram

**Academic Year:** 2021-2022

## 🙏 Acknowledgments

- Dr. K. A. Navas, Principal, MES College of Engineering
- Dr. Anil K Jacob, Head of Department, CSE
- Mr. Sherikh K K & Ms. Farseena P, Project Coordinators
- Suchitwa Mission, Local Self Government Department of Kerala

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For queries and support:
- **Institution:** MES College of Engineering, Kuttippuram
- **Location:** Thrikkanapuram P.O, Malappuram Dt, Kerala, India 679582

## 🔮 Future Enhancements

- [ ] Mobile application for Android and iOS
- [ ] Real-time GPS tracking for collection vehicles
- [ ] AI-based waste categorization
- [ ] Integration with smart city infrastructure
- [ ] Advanced analytics and reporting
- [ ] Multi-language support

## 📸 Screenshots

Screenshots of the application are available in the `/docs/screenshots` directory.

---

**Note:** This project was submitted to APJ Abdul Kalam Technological University in partial fulfillment of the requirements for the Bachelor of Technology degree in Computer Science and Engineering.

**⭐ If you find this project useful, please consider giving it a star!**
