import * as dotenv from 'dotenv';
dotenv.config();

export interface IMongoSettings {
    FLIGHT_MONGO_URI: string;
    FLIGHT_MONGO_DB: string;
}

export interface ISettings {
    PORT : number;
    DEBUG_MODE : boolean;
    mongo : IMongoSettings;
}

// Settings defined from .env
export const settings : ISettings = {
    PORT : parseInt(process.env.FLIGHT_SERVICE_PORT || '4800', 10),

    DEBUG_MODE : process.env.DEBUG_MODE === 'True',

    mongo : {
        FLIGHT_MONGO_URI: process.env.FLIGHT_MONGO_URI || 'mongodb://localhost:27017/',
        FLIGHT_MONGO_DB: process.env.FLIGHT_MONGO_DB_NAME || 'flight_service',
    }
}