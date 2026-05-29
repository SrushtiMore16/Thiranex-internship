# 🔐 Thiranex Cybersecurity Internship

This repository contains all tasks completed during my Cybersecurity Internship at **Thiranex**.  
Each task is focused on building practical security tools and understanding core cybersecurity concepts.

---

## 👩‍💻 About Me
**Srushti** — B.Tech CSE (AI/ML Honours), JSPM University Pune  
Cybersecurity Intern @ Thiranex

---

## 📁 Tasks

### ✅ Task 1 — Password Strength Analyzer
**File:** `password-strength-analyzer.html`

A browser-based tool that evaluates the strength of user-entered passwords in real time.

**Features:**
- Checks password length, complexity (uppercase, lowercase, numbers, symbols)
- Detects commonly used/weak passwords
- Calculates entropy in bits and estimates crack time
- Suggests 3 strong alternative passwords (regeneratable)
- Session-based password history to prevent reuse
- Clean, responsive UI — no dependencies, runs in any browser

**Concepts Learned:**
- Password entropy and cryptographic strength
- Character pool mathematics
- Common attack vectors (brute force, dictionary attacks)
- Secure password design principles

---

### ✅ Task 2 — Vulnerability Scanner
**File:** `vulnerability_scanner.py`

A Python-based CLI tool that scans a target website for common security vulnerabilities and generates a detailed HTML report.

**Features:**
- Scans 15 common ports (FTP, SSH, HTTP, MySQL, RDP etc.)
- Checks for 7 critical security headers
- Detects exposed software/server version information
- Calculates an overall risk score (0–100)
- Auto-generates a clean HTML vulnerability report

**Concepts Learned:**
- Port scanning and network security
- HTTP security headers and their importance
- Information leakage vulnerabilities
- Penetration testing basics and vulnerability assessment

**How to Run:**
```bash
pip3 install requests
python3 vulnerability_scanner.py
```

---

### ✅ Task 3 — Phishing Email Detection Model
**File:** `phishing_detector.py`

A machine learning model built with Scikit-learn that classifies emails as Phishing or Safe with 100% accuracy.

**Features:**
- Trained on 80 emails (40 phishing + 40 safe)
- TF-IDF text feature extraction with bigrams
- Custom feature engineering (URL count, urgency words, suspicious TLDs)
- Random Forest Classifier achieving 100% accuracy
- Displays confusion matrix and classification report
- Auto-generates a detailed HTML report

**Concepts Learned:**
- Machine learning for cybersecurity
- TF-IDF vectorization and NLP basics
- Feature engineering for email analysis
- Model evaluation (accuracy, precision, recall, confusion matrix)
- Phishing attack patterns and detection techniques

**How to Run:**
```bash
pip3 install scikit-learn pandas numpy matplotlib seaborn
python3 phishing_detector.py
```

---

### ✅ Task 4 — Secure Login System 🚀
**Folder:** `secure-login/`

> 🏆 A production-grade, full-stack secure authentication web application built from scratch using Node.js and Express — implementing industry-standard security practices used by real-world applications.

This isn't just a login form. This is a complete authentication system with multiple layers of security, session management, and Two-Factor Authentication — the kind of system that protects real user data in production environments.

#### 🏗️ Architecture
```
secure-login/
├── server.js          → Express backend (REST API)
├── package.json       → Dependencies
├── users.json         → Persistent JSON database (auto-generated)
└── public/
    ├── login.html     → Login page with 2FA support
    ├── register.html  → Registration with live validation
    ├── dashboard.html → User dashboard with 2FA management
    └── style.css      → Clean, responsive UI
```

#### 🔒 Security Features

| Feature | Implementation |
|---|---|
| Password Hashing | bcrypt with 12 salt rounds |
| SQL Injection Protection | Parameterized logic, no raw queries |
| Session Management | express-session with HttpOnly cookies |
| Input Validation | express-validator on all endpoints |
| Two-Factor Authentication | TOTP via speakeasy (Google Authenticator compatible) |
| QR Code Generation | Dynamic QR codes for 2FA setup |
| Session Expiry | Auto-expiry after 2 hours |
| Secure Cookies | HttpOnly flag preventing XSS cookie theft |

#### ✨ App Features
- 📝 **User Registration** - with full validation (username, email, strong password enforcement)
- 🔑 **Secure Login** - bcrypt password comparison, no plaintext ever stored
- 📱 **Two-Factor Authentication** — scan QR code with Google Authenticator or Authy
- 🖥️ **User Dashboard** — view account info, manage 2FA, see active security features
- 🚪 **Logout** — proper session destruction on logout
- ⚡ **REST API** — clean API endpoints for all auth operations

#### 🛡️ How It Protects Users
- Passwords are **never stored in plaintext** — bcrypt hashes them with 12 rounds of salting
- **HttpOnly cookies** prevent JavaScript from accessing session tokens (XSS protection)
- **Input validation** on every field blocks malformed or malicious data
- **2FA adds a second layer** — even if a password is stolen, the account stays safe
- **Session expiry** automatically logs users out after 2 hours of inactivity

#### 🚀 How to Run
```bash
cd secure-login
npm install
node server.js
```
Open `http://localhost:3000` in your browser.

**Tech Stack:** Node.js, Express.js, bcryptjs, speakeasy, express-session, express-validator, QRCode

---

## 🛠️ Overall Tech Stack
- HTML5, CSS3, Vanilla JavaScript — Task 1
- Python 3, Requests — Task 2
- Python 3, Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn — Task 3
- Node.js, Express.js, bcryptjs, speakeasy, express-session — Task 4

---

## 🚀 How to Run
1. Clone or download this repository
2. **Task 1:** Open `.html` file directly in any browser
3. **Task 2 & 3:** Install requirements and run the Python script
4. **Task 4:** Run `npm install` inside `secure-login/` folder, then `node server.js`

---

*Internship Period: 2025–2026 | Organization: Thiranex*
