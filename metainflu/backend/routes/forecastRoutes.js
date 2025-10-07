const express = require('express');
const router = express.Router();
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const { protect } = require('../middleware/authMiddleware');

// Use memory storage for multer to avoid saving files to disk
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// AI backend URL from environment variable or default
const AI_BACKEND_URL = process.env.AI_BACKEND_URL || 'http://localhost:8000';

router.post('/', protect, upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ message: 'File is required.' });
    }

    const form = new FormData();
    form.append('file', req.file.buffer, {
        filename: req.file.originalname,
        contentType: req.file.mimetype,
    });

    // Append other form fields from the original request
    for (const key in req.body) {
        form.append(key, req.body[key]);
    }

    const response = await axios.post(`${AI_BACKEND_URL}/api/forecast`, form, {
      headers: {
        ...form.getHeaders(),
      },
      // Important: Pass stream size to avoid issues with large files
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
    });

    res.status(response.status).json(response.data);
  } catch (error) {
    console.error('Error proxying to AI backend:', error.message);
    if (error.response) {
        // Forward the error from the AI backend
        res.status(error.response.status).json(error.response.data);
    } else if (error.request) {
        // The request was made but no response was received
        res.status(504).json({ message: 'Gateway Timeout: No response from AI service.' });
    } else {
        // Something happened in setting up the request that triggered an Error
        res.status(500).json({ message: 'Internal Server Error' });
    }
  }
});

module.exports = router;
