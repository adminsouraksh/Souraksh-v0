// File: backend/routes/authRoutes.js

const express = require('express');
const router = express.Router();
const { registerUser, loginUser, googleLogin } = require('../controllers/authController');

// Define the routes for user authentication
router.post('/register', registerUser);
router.post('/login', loginUser);

// Add the new route for Google authentication
router.post('/google', googleLogin);

module.exports = router;
