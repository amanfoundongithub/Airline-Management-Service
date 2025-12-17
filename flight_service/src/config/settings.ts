import * as dotenv from 'dotenv';

// Configure the file to fetch .env from the local 
dotenv.config();

/**
 * Mongo settings for connection
 * 
 * @author amanfoundongithub
 */
export interface IMongoSettings {
    MONGO_URL: string;
    MONGO_DB:  string;
}


/**
 * Main configuration class to store all the settings from .env file
 * 
 * @author amanfoundongithub
 */
export interface ISettings {

    // General configuration for the environment
    PORT :       number;
    DEBUG_MODE : boolean;

    // MongoDB specific configurations 
    mongo :      IMongoSettings;
}

/**
 * Implementation of the class that returns the concrete settings
 * 
 * @author amanfoundongithub
 */
export const settings : ISettings = {
    PORT :       parseInt(process.env.FLIGHT_SERVICE_PORT || '4800', 10),
    DEBUG_MODE : process.env.DEBUG_MODE === 'True',

    mongo : {
        MONGO_URL: process.env.FLIGHT_MONGO_URI || 'mongodb://localhost:27017/',
        MONGO_DB:  process.env.FLIGHT_MONGO_DB_NAME || 'flight_service',
    }
}