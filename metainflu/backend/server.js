const express = require('express');
const dotenv = require('dotenv');
const mongoose = require('mongoose');
const cors = require('cors');

// Import only the required routes
const authRoutes = require('./routes/authRoutes');
const forecastRoutes = require('./routes/forecastRoutes');

const { errorHandler } = require('./middleware/errorMiddleware');
const { protect } = require('./middleware/authMiddleware');

dotenv.config();

const app = express();
const port = process.env.PORT || 5000;
const mongoURI = process.env.MONGO_URI;

// --- ✅ CORRECTED CORS MIDDLEWARE ---
// Added the frontend's actual origin to the list of allowed origins.
const allowedOrigins = ['https://souraksh-v0.vercel.app'];

app.use(cors({
  origin: function (origin, callback) {
    // allow requests with no origin (like mobile apps or curl requests)
    if (!origin) return callback(null, true);
    if (allowedOrigins.indexOf(origin) === -1) {
      const msg = 'The CORS policy for this site does not allow access from the specified Origin.';
      return callback(new Error(msg), false);
    }
    return callback(null, true);
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));

app.use(express.json());

// Database Connection ty
mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('✅ Connected to MongoDB Atlas'))
.catch(err => {
  console.error('❌ MongoDB Connection Error:', err.message);
  process.exit(1);
});

// --- ✅ CORRECTED ROUTES ---
// Re-added the '/api' prefix to match the frontend's API calls.
// The server will now correctly handle requests to '/api/auth' and '/api/forecast'.
app.use('/api/auth', authRoutes);
app.use('/api/forecast', forecastRoutes);

// Test protected route
app.get('/protected', protect, (req, res) => {
  res.status(200).json({ message: `Hello, ${req.user.name}! Access granted.` });
});

// Health check route
app.get('/', (req, res) => {
  res.send('API is running...');
});

// Error handler
app.use(errorHandler);

// Start server
app.listen(port, () => {
  console.log(`🚀 Server running on port ${port}`);
});