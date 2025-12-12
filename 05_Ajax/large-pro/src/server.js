require('dotenv').config();
const express = require('express');
const path = require('path');
const { Pool } = require('pg');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');
const crypto = require('crypto');

const app = express();
app.use(express.json());

app.use(express.static(path.join(__dirname, 'frontend')));
// --- Database Connection ---
const pool = new Pool({
  user: process.env.POSTGRES_USER,
  host: process.env.DB_HOST, // This will be the service name 'db'
  database: process.env.POSTGRES_DB,
  password: process.env.POSTGRES_PASSWORD,
  port: 5432,
});

// --- Security Middleware ---
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (token == null) return res.sendStatus(401);

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

// --- Routes ---

// 1. Register
app.post('/register', 
  body('email').isEmail(),
  body('password').isLength({ min: 6 }), 
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ errors: errors.array() });

    const { email, password } = req.body;
    try {
      const userCheck = await pool.query('SELECT * FROM users WHERE email = $1', [email]);
      if (userCheck.rows.length > 0) return res.status(400).json({ msg: "User already exists" });

      const salt = await bcrypt.genSalt(10);
      const hashedPassword = await bcrypt.hash(password, salt);

      const newUser = await pool.query(
        'INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id, email',
        [email, hashedPassword]
      );
      res.status(201).json({ msg: "User created", user: newUser.rows[0] });
    } catch (err) {
      console.error(err);
      res.status(500).send("Server Error");
    }
});

// 2. Login
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  try {
    const userResult = await pool.query('SELECT * FROM users WHERE email = $1', [email]);
    if (userResult.rows.length === 0) return res.status(400).json({ msg: "Invalid Credentials" });

    const user = userResult.rows[0];
    const validPassword = await bcrypt.compare(password, user.password_hash);
    if (!validPassword) return res.status(400).json({ msg: "Invalid Credentials" });

    const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.json({ token });
  } catch (err) {
    console.error(err);
    res.status(500).send("Server Error");
  }
});

// 3. Request Password Reset
app.post('/forgot-password', async (req, res) => {
  const { email } = req.body;
  try {
    const userResult = await pool.query('SELECT * FROM users WHERE email = $1', [email]);
    if (userResult.rows.length === 0) return res.status(400).json({ msg: "User not found" });

    const resetToken = crypto.randomBytes(20).toString('hex');
    const expireDate = new Date(Date.now() + 3600000); // 1 hour

    await pool.query(
      'UPDATE users SET reset_token = $1, reset_token_expires = $2 WHERE email = $3',
      [resetToken, expireDate, email]
    );
    // In production, send email here.
    res.json({ msg: "Reset token generated", resetToken });
  } catch (err) {
    console.error(err);
    res.status(500).send("Server Error");
  }
});

// 4. Reset Password
app.post('/reset-password', async (req, res) => {
  const { resetToken, newPassword } = req.body;
  try {
    const userResult = await pool.query(
      'SELECT * FROM users WHERE reset_token = $1 AND reset_token_expires > $2',
      [resetToken, new Date()]
    );
    if (userResult.rows.length === 0) return res.status(400).json({ msg: "Invalid or expired token" });

    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(newPassword, salt);

    await pool.query(
      'UPDATE users SET password_hash = $1, reset_token = NULL, reset_token_expires = NULL WHERE id = $2',
      [hashedPassword, userResult.rows[0].id]
    );
    res.json({ msg: "Password successfully updated" });
  } catch (err) {
    console.error(err);
    res.status(500).send("Server Error");
  }
});
// Add this near your other routes in server.js
app.get('/dashboard', authenticateToken, (req, res) => {
  res.json({ msg: "Secret data only logged-in users can see!", userId: req.user.id });
});
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
