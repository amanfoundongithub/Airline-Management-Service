import dotenv from 'dotenv'
import { convertToNumber } from "../helpers/number.helper"

dotenv.config()

const load_from_env = (key : string) : string => {
    const value = process.env[key]
    if(!value) {
        throw new Error(`Missing environment variable: ${key}`)
    }
    return value
}

const API_VERSION = load_from_env("API_VERSION")

export const env = {
    // Service related configuration
    PORT : convertToNumber(load_from_env("PORT")),
    NAME : load_from_env("SERVICE_NAME"),
    DESC: load_from_env("SERVICE_DESC"),

    // API related configuration
    API_VERSION,
    API_PREFIX: `/api/${API_VERSION}`,
    API_PREFIX_FLIGHT: `/api/${API_VERSION}/flight`,

    // Mongo related configuration
    MONGO_URI : load_from_env("MONGO_URI"),
    MONGO_DB_NAME : load_from_env("MONGO_DB_NAME"),
    MONGO_COLLECTION_NAME : load_from_env("MONGO_COLLECTION_NAME"),

    JWT_SECRET : load_from_env("JWT_SECRET"),

    // Client related configuration
    AUTH_USERNAME : load_from_env("AUTH_USERNAME"),
    AUTH_PASSWORD : load_from_env("AUTH_PASSWORD"),
    AUTH_URL : load_from_env("AUTH_URL"),

    // Airport validation URL
    AIRPORT_ID_DETAILS_URL : load_from_env("AIRPORT_ID_DETAILS_URL"),
}

export const AUTH_MICROSERVICE_VERIFICATION_URL = ""