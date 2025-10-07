// File: backend/controllers/authController.js
const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const asyncHandler = require('express-async-handler');
// You would use a library like this to verify Google tokens
// const { OAuth2Client } = require('google-auth-library');
// const client = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET, {
    expiresIn: '30d',
  });
};

const registerUser = asyncHandler(async (req, res) => {
  const { name, email, password } = req.body;
  if (!name || !email || !password) {
    res.status(400);
    throw new Error('Please add all fields');
  }
  const userExists = await User.findOne({ email });
  if (userExists) {
    res.status(400);
    throw new Error('User already exists');
  }
  const salt = await bcrypt.genSalt(10);
  const hashedPassword = await bcrypt.hash(password, salt);

  const user = await User.create({
    name,
    email,
    password: hashedPassword,
    role: 'client',
    accountType: 'c2c',
  });

  if (user) {
    res.status(201).json({
      _id: user.id,
      name: user.name,
      email: user.email,
      role: user.role,
      accountType: user.accountType,
      token: generateToken(user._id),
    });
  } else {
    res.status(400);
    throw new Error('Invalid user data');
  }
});

const loginUser = asyncHandler(async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });
  if (user && user.password && (await bcrypt.compare(password, user.password))) {
    res.json({
      _id: user.id,
      name: user.name,
      email: user.email,
      role: user.role,
      accountType: user.accountType,
      token: generateToken(user._id),
    });
  } else {
    res.status(400);
    throw new Error('Invalid credentials');
  }
});

// @desc    Authenticate user with Google
// @route   POST /api/auth/google
// @access  Public
const googleLogin = asyncHandler(async (req, res) => {
  const { token } = req.body;

  // In a real application, you would verify the token with Google's servers
  // const ticket = await client.verifyIdToken({
  //     idToken: token,
  //     audience: process.env.GOOGLE_CLIENT_ID,
  // });
  // const { name, email, sub: googleId } = ticket.getPayload();

  // --- MOCK VERIFICATION FOR DEMONSTRATION ---
  // This is a placeholder. A real implementation MUST verify the token.
  // A simple decode is used here for mock purposes and is NOT secure for production.
  const decodedToken = JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString());
  if (!decodedToken || !decodedToken.email) {
      res.status(401);
      throw new Error('Invalid Google token');
  }
  const { name, email, sub: googleId } = decodedToken;
  // --- END MOCK ---

  let user = await User.findOne({ googleId });

  if (!user) {
    // If user with googleId doesn't exist, check if an account with that email already exists
    user = await User.findOne({ email });
    if (user) {
      // If email exists, link the Google ID to the existing account
      user.googleId = googleId;
      await user.save();
    }
  }

  if (user) {
    // User already exists, log them in
    res.json({
      _id: user.id,
      name: user.name,
      email: user.email,
      role: user.role,
      accountType: user.accountType,
      token: generateToken(user._id),
    });
  } else {
    // New user, create an account for them
    user = await User.create({
      name,
      email,
      googleId,
      role: 'client',
      accountType: 'c2c', // Default to personal account for Google sign-ups
    });

    if (user) {
      res.status(201).json({
        _id: user.id,
        name: user.name,
        email: user.email,
        role: user.role,
        accountType: user.accountType,
        token: generateToken(user._id),
      });
    } else {
      res.status(400);
      throw new Error('Invalid user data');
    }
  }
});


module.exports = {
  registerUser,
  loginUser,
  googleLogin, // This line is crucial
};

