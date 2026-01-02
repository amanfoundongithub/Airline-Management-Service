import mongoose from "mongoose";
import { env } from '../config/env.load';
import { Logger } from "../logger/logger";

const MONGO_LOGGER = new Logger("MONGO_CONNECTION")

export const connectWithMongoDB = async () => {
    try {
        await mongoose.connect(env.MONGO_URI,
        {
            dbName : env.MONGO_DB_NAME
        })
        MONGO_LOGGER.info("MongoDB Connection Successful!");
    } catch(error) {
        MONGO_LOGGER.error("Could not connect to MongoDB:" + error);
        throw error;
    }
}

const disconnectWithMongoDB = async () => {
    try {
        await mongoose.disconnect();
        MONGO_LOGGER.info("MongoDB Connection Disconnected!");
    } catch(error) {
        MONGO_LOGGER.error("Failed to close connection with MongoDB:" + error);
    }
}

process.on("SIGINT", async () => {
    await disconnectWithMongoDB()
    process.exit(0)
})

