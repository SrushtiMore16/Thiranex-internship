/**
 * ================================================
 *  Secure Login System
 *  Thiranex Cybersecurity Internship — Task 4
 *  Author: Srushti | B.Tech CSE (AI/ML), JSPM Pune
 * ================================================
 */

const express = require("express");
const bcrypt = require("bcryptjs");
const session = require("express-session");
const speakeasy = require("speakeasy");
const QRCode = require("qrcode");
const { body, validationResult } = require("express-validator");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;
const DB_FILE = "users.json";

// ─────────────────────────────────────────────
//  JSON FILE DATABASE (no native modules needed)
// ─────────────────────────────────────────────

function readDB() {
  if (!fs.existsSync(DB_FILE)) fs.writeFileSync(DB_FILE, JSON.stringify([]));
  return JSON.parse(fs.readFileSync(DB_FILE, "utf8"));
}

function writeDB(data) {
  fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
}

function findUser(key, value) {
  return readDB().find(u => u[key] === value);
}

function createUser(username, email, hashedPassword) {
  const users = readDB();
  const newUser = {
    id: Date.now(),
    username,
    email,
    password: hashedPassword,
    twofa_secret: null,
    twofa_enabled: false,
    created_at: new Date().toISOString()
  };
  users.push(newUser);
  writeDB(users);
  return newUser;
}

function updateUser(id, updates) {
  const users = readDB();
  const idx = users.findIndex(u => u.id === id);
  if (idx !== -1) { users[idx] = { ...users[idx], ...updates }; writeDB(users); }
}

console.log("✅ JSON database ready");

// ─────────────────────────────────────────────
//  MIDDLEWARE
// ─────────────────────────────────────────────

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

app.use(session({
  secret: "thiranex-super-secret-key-2024",
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    secure: false,
    maxAge: 1000 * 60 * 60 * 2
  }
}));

function requireAuth(req, res, next) {
  if (req.session && req.session.userId) return next();
  res.redirect("/login.html");
}

// ─────────────────────────────────────────────
//  ROUTES
// ─────────────────────────────────────────────

app.get("/", (req, res) => {
  if (req.session.userId) return res.redirect("/dashboard.html");
  res.redirect("/login.html");
});

// REGISTER
app.post("/api/register", [
  body("username").trim().isLength({ min: 3, max: 20 }).withMessage("Username must be 3–20 characters").isAlphanumeric().withMessage("Username can only contain letters and numbers"),
  body("email").trim().isEmail().withMessage("Please enter a valid email"),
  body("password").isLength({ min: 8 }).withMessage("Password must be at least 8 characters")
    .matches(/[A-Z]/).withMessage("Password must contain an uppercase letter")
    .matches(/[0-9]/).withMessage("Password must contain a number")
    .matches(/[^a-zA-Z0-9]/).withMessage("Password must contain a special character"),
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({ success: false, errors: errors.array().map(e => e.msg) });

  const { username, email, password } = req.body;

  try {
    const existingUsername = findUser("username", username);
    const existingEmail = findUser("email", email);
    if (existingUsername || existingEmail) return res.status(400).json({ success: false, errors: ["Username or email already taken"] });

    const hashedPassword = await bcrypt.hash(password, 12);
    createUser(username, email, hashedPassword);
    res.json({ success: true, message: "Account created! Please login." });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, errors: ["Server error. Please try again."] });
  }
});

// LOGIN
app.post("/api/login", [
  body("username").trim().notEmpty().withMessage("Username is required"),
  body("password").notEmpty().withMessage("Password is required"),
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({ success: false, errors: errors.array().map(e => e.msg) });

  const { username, password } = req.body;

  try {
    const user = findUser("username", username);
    if (!user) return res.status(401).json({ success: false, errors: ["Invalid username or password"] });

    const passwordMatch = await bcrypt.compare(password, user.password);
    if (!passwordMatch) return res.status(401).json({ success: false, errors: ["Invalid username or password"] });

    if (user.twofa_enabled) {
      req.session.pending2FA = { userId: user.id, username: user.username };
      return res.json({ success: true, requires2FA: true });
    }

    req.session.userId = user.id;
    req.session.username = user.username;
    res.json({ success: true, requires2FA: false });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, errors: ["Server error. Please try again."] });
  }
});

// VERIFY 2FA
app.post("/api/verify-2fa", (req, res) => {
  const { token } = req.body;
  if (!req.session.pending2FA) return res.status(400).json({ success: false, message: "No pending 2FA session" });

  const { userId, username } = req.session.pending2FA;
  const user = findUser("id", userId);

  const verified = speakeasy.totp.verify({ secret: user.twofa_secret, encoding: "base32", token, window: 1 });
  if (!verified) return res.status(401).json({ success: false, message: "Invalid or expired OTP code" });

  delete req.session.pending2FA;
  req.session.userId = userId;
  req.session.username = username;
  res.json({ success: true });
});

// SETUP 2FA
app.get("/api/setup-2fa", requireAuth, async (req, res) => {
  const secret = speakeasy.generateSecret({ name: `SecureLogin (${req.session.username})`, length: 20 });
  req.session.temp2FASecret = secret.base32;
  try {
    const qrCodeUrl = await QRCode.toDataURL(secret.otpauth_url);
    res.json({ success: true, qrCode: qrCodeUrl, secret: secret.base32 });
  } catch (err) {
    res.status(500).json({ success: false, message: "Failed to generate QR code" });
  }
});

// ENABLE 2FA
app.post("/api/enable-2fa", requireAuth, (req, res) => {
  const { token } = req.body;
  const secret = req.session.temp2FASecret;
  if (!secret) return res.status(400).json({ success: false, message: "Please generate QR code first" });

  const verified = speakeasy.totp.verify({ secret, encoding: "base32", token, window: 1 });
  if (!verified) return res.status(401).json({ success: false, message: "Invalid OTP. Please try again." });

  updateUser(req.session.userId, { twofa_secret: secret, twofa_enabled: true });
  delete req.session.temp2FASecret;
  res.json({ success: true, message: "2FA enabled successfully!" });
});

// DISABLE 2FA
app.post("/api/disable-2fa", requireAuth, (req, res) => {
  updateUser(req.session.userId, { twofa_secret: null, twofa_enabled: false });
  res.json({ success: true, message: "2FA disabled." });
});

// GET USER INFO
app.get("/api/me", requireAuth, (req, res) => {
  const user = findUser("id", req.session.userId);
  if (!user) return res.status(404).json({ success: false });
  const { password, twofa_secret, ...safeUser } = user;
  res.json({ success: true, user: safeUser });
});

// LOGOUT
app.post("/api/logout", (req, res) => {
  req.session.destroy(() => res.json({ success: true }));
});

// ─────────────────────────────────────────────
//  START SERVER
// ─────────────────────────────────────────────

app.listen(PORT, () => {
  console.log(`\n🔐 Secure Login System running at http://localhost:${PORT}`);
  console.log("   Thiranex Cybersecurity Internship — Task 4\n");
});
