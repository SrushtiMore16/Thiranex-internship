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

## 🛠️ Tech Stack
- HTML5, CSS3, Vanilla JavaScript — Task 1
- Python 3, Requests library — Task 2

---

## 🚀 How to Run
1. Clone or download this repository
2. For Task 1: open the `.html` file directly in any browser
3. For Task 2: install requirements and run the Python script

---

*Internship Period: 2025–2026 | Organization: Thiranex*
