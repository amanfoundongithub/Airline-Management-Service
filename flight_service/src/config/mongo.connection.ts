import mongoose from "mongoose";
import { settings } from './settings';
import { Logger } from "../common/logger";

// Get logger
const MONGO_LOGGER = new Logger("MONGO_CONNECTION")

/**
 * Utility function to establish connection with MongoDB
 * 
 * @author amanfoundongithub
 */
export const connectWithMongoDB = async () => {
    try {
        await mongoose.connect(settings.mongo.MONGO_URL, 
        {
            dbName : settings.mongo.MONGO_DB
        })
        MONGO_LOGGER.info("MongoDB Connection Successful!");
    } catch(error) {
        MONGO_LOGGER.error("Could not connect to MongoDB:" + error);
    }
}

/**
 * Utility function to establish disconnection with MongoDB
 * 
 * @author amanfoundongithub
 */
export const disconnectWithMongoDB = async () => {
    try {
        await mongoose.disconnect();
        MONGO_LOGGER.info("MongoDB Connection Disconnected!");
    } catch(error) {
        MONGO_LOGGER.error("Failed to close connection with MongoDB:" + error);
    }
}

