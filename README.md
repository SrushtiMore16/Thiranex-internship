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

A machine learning model built with Scikit-learn that classifies emails as Phishing or Safe with high accuracy.

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
- Model evaluation using accuracy, precision, recall and confusion matrix
- Phishing attack patterns and detection techniques

**How to Run:**
```bash
pip3 install scikit-learn pandas numpy matplotlib seaborn
python3 phishing_detector.py
```

---

## 🛠️ Tech Stack
- HTML5, CSS3, Vanilla JavaScript — Task 1
- Python 3, Requests — Task 2
- Python 3, Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn — Task 3

---

## 🚀 How to Run
1. Clone or download this repository
2. For Task 1: open the `.html` file directly in any browser
3. For Task 2 & 3: install requirements and run the Python script

---

*Internship Period: 2025–2026 | Organization: Thiranex*
