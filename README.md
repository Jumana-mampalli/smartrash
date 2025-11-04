


```markdown
# SMARTRASH - Smart Waste Management System

A **complete, simple, and functional** Django + IoT-based waste management platform.

---

## Features

| Feature | Description |
|--------|-------------|
| **IoT Smart Bins** | Real-time fill level via NodeMCU + Ultrasonic sensor |
| **Auto Full Detection** | Triggers at ≥75% |
| **Digital Wallet** | Pay for collection, earn from recycling |
| **Role-Based Dashboards** | Customer, Agent, Municipality, Recycler, Admin |
| **Recycler Booking** | Sell plastic/paper/metal with auto pricing |
| **Task Assignment** | Municipality assigns agents |
| **Approval Workflow** | New users need municipality approval |
| **REST API** | `/api/bin/update/` for bin status |

---

## Tech Stack

- **Backend**: Django 3.2
- **Database**: SQLite (default)
- **Frontend**: HTML + CSS (inline, responsive)
- **IoT**: NodeMCU ESP8266 + HC-SR04
- **Communication**: HTTP JSON API

---

## User Roles

| Role | Permissions |
|------|-------------|
| **Customer** | Link bin, book recycler, verify collection, manage wallet |
| **Collection Agent** | View tasks, collect waste, enter bin ID |
| **Municipality** | Approve users, assign tasks, monitor full bins |
| **Recycler** | Set rates, accept bookings, assign agent |
| **Admin** | Create municipalities, manage system |

---

## Project Structure

```
smartrash/
├── manage.py
├── smartrash/
│   ├── settings.py
│   ├── urls.py
├── waste/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
└── requirements.txt
```

---

## Setup Instructions

```bash
# 1. Create project
django-admin startproject smartrash
cd smartrash
python manage.py startapp waste

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy code from smartrash_simple_code.py into:
#    - waste/models.py
#    - waste/views.py
#    - waste/forms.py
#    - waste/urls.py
#    - templates/

# 4. Update smartrash/urls.py
path('', include('waste.urls'))

# 5. Migrate & run
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## IoT Hardware (Smart Bin)

### Components:
- NodeMCU ESP8266
- HC-SR04 Ultrasonic Sensor
- 3 LEDs (WiFi, Normal, Full)

### Arduino Code:
- Upload to NodeMCU
- Update WiFi & server URL
- Sends level every **60 seconds**

---

## API Endpoint

```http
POST /api/bin/update/
Content-Type: application/json

{
  "bin_id": "BIN001",
  "level": 82
}
→ { "status": "success" }
```

---

## Workflow

```
1. Customer links bin
2. Bin fills → IoT sends level
3. Municipality sees full bin → Assigns agent
4. Agent collects → Enters bin ID
5. Customer verifies → Pays from wallet
6. Municipality earns fee
```

**Recycler Flow:**
```
Customer → Book (type + weight)
Recycler → Assign agent
Agent → Collect
Customer → Pays recycler
```

---

## Key URLs

| Page | URL |
|------|-----|
| Home | `/` |
| Login | `/login/` |
| Customer Dashboard | `/customer/dashboard/` |
| Municipality | `/municipality/dashboard/` |
| Agent | `/agent/dashboard/` |
| Recycler | `/recycler/dashboard/` |

---

## Initial Setup (Admin)

1. Login as superuser → `/admin`
2. Create **Municipality**
3. Add **Smart Bins** (e.g., `BIN001`)
4. Users register → Municipality approves

---

## Future Ideas

- Mobile App
- GPS Tracking
- Push Notifications
- QR Code Bin Linking
- Analytics Dashboard

---

## License

**MIT License** – Free to use, modify, distribute.

---
