import dotenv from 'dotenv'
dotenv.config()

const load_from_env = (key : string) : string => {
    const value = process.env[key]
    if(!value) {
        throw new Error(`Missing environment variable: ${key}`)
    }
    return value
}

export const env = {
    // Service related configuration
    PORT : Number(load_from_env("PORT")),
    NAME : load_from_env("SERVICE_NAME"),
    DESC: load_from_env("SERVICE_DESC"),

    // API related configuration
    API_VERSION: load_from_env("API_VERSION"),
    API_PREFIX: `/api/${load_from_env("API_VERSION")}`,
    API_PREFIX_FLIGHT: `/api/${load_from_env("API_VERSION")}/flight`,

    // Mongo related configuration
    MONGO_URI : load_from_env("MONGO_URI"),
    MONGO_DB_NAME : load_from_env("MONGO_DB_NAME"),
    MONGO_COLLECTION_NAME : load_from_env("MONGO_COLLECTION_NAME"),
}