// File: backend/models/User.js
const mongoose = require('mongoose');
const userSchema = mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Please add a name'],
    },
    email: {
      type: String,
      required: [true, 'Please add an email'],
      unique: true,
    },
    password: {
      type: String,
      // Password is not required for Google Sign-In users
      required: function() { return !this.googleId; },
    },
    googleId: {
      type: String,
      unique: true,
      sparse: true, // Allows multiple documents to have a null value for this field
    },
    role: {
      type: String,
      required: true,
      enum: ['client'],
      default: 'client',
    },
    accountType: {
      type: String,
      enum: ['b2b', 'c2c'],
      required: function() {
        return this.role === 'client';
      },
    },
  },
  {
    timestamps: true,
  }
);
module.exports = mongoose.model('User', userSchema);

