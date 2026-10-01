# 🎓 Quminity

### The Digital Hub for College Events, Clubs & Student Communities

**Quminity** is a modern college event and club management platform designed to bring **students, clubs, organizers, and college communities** together in one place.

From discovering events and registering online to **QR-based attendance, location validation, memberships, and secure payments**, Quminity simplifies the complete campus-event experience.

---

## ✨ Why Quminity?

Managing college events often involves scattered registration forms, manual attendance, payment handling, and difficulty keeping students updated.

**Quminity brings everything together.**

> **Discover → Register → Attend → Verify → Connect**

It provides students with a centralized platform while giving organizers the tools they need to manage events efficiently.

---

## 🚀 Key Features

### 🎪 Event Discovery

* Explore upcoming college events
* Browse events by category
* View complete event information
* Check date, time, venue, and organizer details
* Discover events happening across the campus

### 📝 Event Registration

* Online event registration
* User-friendly registration flow
* Registration confirmation
* Track registered events
* Prevent duplicate registrations

### 💳 Online Payments

* Secure event ticket payments
* Membership payment support
* Payment gateway integration
* Transaction verification
* Payment status tracking

### 📱 QR Code Attendance

* Generate QR codes for registered participants
* Scan QR codes at event venues
* Quickly mark participant attendance
* Reduce manual attendance work
* Prevent unauthorized attendance

### 📍 Location-Based Verification

Quminity can validate whether a participant is physically present at the event location.

* Geolocation-based attendance validation
* Venue proximity verification
* Helps prevent remote/fake attendance
* Useful for campus events and workshops

### 🏛️ College Clubs

* Discover college clubs
* View club information
* Explore club activities
* Join club memberships
* Manage club-related events

### 👤 Student Dashboard

Students can manage their complete event activity from a centralized dashboard.

* Registered events
* Upcoming events
* Previous events
* Attendance history
* Payment history
* Club memberships

### 📊 Organizer Management

Organizers can manage events and participants efficiently.

* Create and manage events
* Monitor registrations
* Track payments
* Verify attendance
* Manage participants
* View event statistics

---

# 🧠 System Workflow

```text
                    ┌───────────────────┐
                    │      Student      │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Discover Events    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Event Registration │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Payment Required? │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Payment Gateway    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Registration Done  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Event Venue     │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ QR Code Scanning  │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ Location Verify   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Attendance Marked │
                    └───────────────────┘
```

---

# 🛠️ Tech Stack

### Frontend

* **Next.js**
* **React**
* **TypeScript**
* **HTML5**
* **CSS3**
* **JavaScript**

### Backend

* **Django**
* **Django REST Framework**
* **Python**

### Database

* **MongoDB**

### Authentication & Security

* User authentication
* Role-based access
* Secure API communication
* Registration validation
* Payment verification

### Integrations

* 💳 Payment Gateway
* 📱 QR Code Generation & Scanning
* 📍 Browser Geolocation API

### Deployment

* ☁️ AWS EC2
* 🔐 Environment Variables
* 🐳 Docker *(optional/planned)*

---

# 🏗️ Project Architecture

```text
QUMINITY
│
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── utils/
│   └── public/
│
├── backend/
│   ├── apps/
│   ├── api/
│   ├── models/
│   ├── serializers/
│   ├── views/
│   └── urls/
│
├── database/
│
├── docs/
│
├── .env.example
├── README.md
└── LICENSE
```

---

# 🔐 Core Modules

| Module           | Description                         |
| ---------------- | ----------------------------------- |
| 🎪 Events        | Create, discover and manage events  |
| 🏛️ Clubs        | Discover and manage college clubs   |
| 📝 Registration  | Register students for events        |
| 💳 Payments      | Process event & membership payments |
| 📱 QR Attendance | QR-based participant verification   |
| 📍 Geolocation   | Validate physical event presence    |
| 👤 Users         | Student and organizer management    |
| 📊 Dashboard     | Event and participation analytics   |

---

# 👥 User Roles

### 👨‍🎓 Student

Students can:

* Create an account
* Discover events
* Register for events
* Purchase tickets
* Join clubs
* View registrations
* Access QR-based attendance
* Track attendance and payments

### 🧑‍💼 Organizer

Organizers can:

* Create events
* Manage registrations
* Manage participants
* Verify payments
* Scan QR codes
* Monitor attendance
* Manage event information

### 👨‍💻 Administrator

Administrators can:

* Manage users
* Manage clubs
* Manage events
* Monitor platform activity
* Manage platform-level settings

---

# 📸 Screenshots

> Add screenshots of your application here.

### 🏠 Home Page

```text
[ Add Screenshot Here ]
```

### 🎪 Events

```text
[ Add Screenshot Here ]
```

### 📝 Registration

```text
[ Add Screenshot Here ]
```

### 📱 QR Attendance

```text
[ Add Screenshot Here ]
```

### 📊 Dashboard

```text
[ Add Screenshot Here ]
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Quminity.git

cd Quminity
```

---

## 2️⃣ Backend Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configure Environment Variables

Create a `.env` file:

```env
DEBUG=True

SECRET_KEY=your_secret_key

DATABASE_URL=your_database_url

PAYMENT_KEY_ID=your_payment_key
PAYMENT_KEY_SECRET=your_payment_secret

ALLOWED_HOSTS=localhost,127.0.0.1
```

> Never commit your `.env` file or expose API/payment credentials publicly.

---

## 4️⃣ Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5️⃣ Create Admin User

```bash
python manage.py createsuperuser
```

---

## 6️⃣ Start Backend Server

```bash
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8000/
```

---

# 🔄 Registration & Attendance Flow

### Step 1 — Discover

Student browses available college events.

### Step 2 — Register

Student selects an event and submits registration details.

### Step 3 — Payment

If the event requires payment, the student completes the payment through the integrated payment gateway.

### Step 4 — Confirmation

After successful verification, the registration is confirmed.

### Step 5 — Event Day

Student reaches the event venue.

### Step 6 — QR Verification

Organizer scans the student's QR code.

### Step 7 — Location Validation

The system can verify the participant's location against the configured event venue.

### Step 8 — Attendance

After successful validation, attendance is recorded.

---

# 📊 Example Data Flow

```text
Student
   │
   ▼
Frontend
   │
   ▼
Django REST API
   │
   ├──────────────► Authentication
   │
   ├──────────────► Event Management
   │
   ├──────────────► Registration
   │
   ├──────────────► Payment Verification
   │
   ├──────────────► QR Verification
   │
   └──────────────► Attendance
                     
```

---

# 🧪 Testing

Run backend tests:

```bash
python manage.py test
```

For frontend:

```bash
npm run lint
```

Build the frontend:

```bash
npm run build
```

---

# 🚀 Future Improvements

Quminity is designed to evolve into a complete digital campus community platform.

### Planned Features

* 🤖 AI-powered event recommendations (Future Scope)
* 🔔 Real-time notifications
* 📅 Calendar integration
* 💬 Event discussions and announcements
* 🏆 Gamification & student points
* 🥇 Event participation badges
* 📈 Advanced analytics
* 📧 Automated email notifications
* 📱 Progressive Web App
* 🔎 Advanced event search and filtering
* 🧑‍🤝‍🧑 Student networking
* 📢 Club announcements
* 🎟️ Digital event certificates
* 🗺️ Interactive campus event map

---

# 🌟 What Makes Quminity Different?

Quminity isn't just an event listing website.

It connects multiple parts of the campus-event ecosystem:

```text
             ┌─────────────┐
             │   STUDENTS  │
             └──────┬──────┘
                    │
                    ▼
┌──────────┐   ┌──────────┐   ┌──────────────┐
│  EVENTS  │──►│ QUMINITY │◄──│    CLUBS     │
└──────────┘   └─────┬────┘   └──────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       PAYMENT       QR       LOCATION
       SYSTEM     ATTENDANCE   VERIFY
```

The platform combines **event management + registration + payments + QR attendance + location validation + club management** into one ecosystem.

---

# 💡 Use Cases

Quminity can be used for:

* College festivals
* Technical events
* Hackathons
* Workshops
* Seminars
* Cultural programs
* Sports events
* Club activities
* Student competitions
* Paid events
* Club memberships
* Campus communities

---

# 🔒 Security Considerations

The platform is designed with security in mind:

* Environment-based secret management
* Authentication & authorization
* API validation
* Payment verification
* Registration validation
* Role-based permissions
* Protected administrative operations
* Secure database communication

---

# 🤝 Contributing

Contributions are welcome!

### 1. Fork the repository

```bash
git fork https://github.com/YOUR_USERNAME/Quminity.git
```

### 2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

### 3. Commit your changes

```bash
git commit -m "feat: add new feature"
```

### 4. Push your branch

```bash
git push origin feature/new-feature
```

### 5. Open a Pull Request

Please describe the changes and provide relevant screenshots when applicable.

---

# 📌 Project Status

🚧 **Active Development**

Quminity is continuously being developed with new features, improvements, and optimizations.

---

# 👨‍💻 Developer

### Amitabh Raj

**B.Tech CSE | Full Stack Developer**

Interested in:

* Full Stack Development
* Django & REST APIs
* Next.js & React
* Cloud Deployment
* AI/ML
* Scalable Web Applications

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

## ⭐ Support

If you find Quminity interesting, consider giving the repository a ⭐.

Your support helps motivate further development!

---

<div align="center">

### 🎓 Quminity

**Connecting Students • Clubs • Events • Communities**

Made with ❤️ for the Campus Community

</div>
