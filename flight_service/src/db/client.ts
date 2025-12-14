import mongoose from 'mongoose';
import { settings } from "../config/settings";


const MONGO_URI = settings.mongo.FLIGHT_MONGO_URI;
const MONGO_DB  = settings.mongo.FLIGHT_MONGO_DB;

/**
 * Utility to establish connection with MongoDB
 */
export const connectWithMongoDB = async () => {
    try {
        await mongoose.connect(MONGO_URI, {
            dbName : MONGO_DB
        });
        console.log("[INFO] MongoDB Connection Successful!");
    } catch(error) {
        console.error("[ERROR] Could not connect to MongoDB:", error);
    }
}

/**
 * Utility to establish disconnection with MongoDB
 */
export const disconnectWithMongoDB = async () => {
    try {
        await mongoose.disconnect();
        console.log("[INFO] MongoDB Connection Disconnected!");
    } catch(error) {
        console.error("[ERROR] Failed to close connection with MongoDB:", error);
    }
}