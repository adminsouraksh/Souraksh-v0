
// File: backend/config/db.js

// Asynchronous function to connect to the database
const connectDB = async () => {
  try {
    // Attempt to connect to the MongoDB URI directly
    const conn = await mongoose.connect('mongodb://localhost:27017/mb_influencer', {
      // Use new URL parser and unified topology, recommended by MongoDB
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });

    console.log(`MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    // Log the error and exit the process if connection fails
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

// Export the function to be used in server.js
module.exports = connectDB;
