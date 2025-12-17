/**
 * This file contains all the constants related to app level configuration. Use this 
 * file to change configurations regarding the application's basic information as well
 * as parameters related to the APIs.
 * 
 * @author amanfoundongithub
 */



// Application level information
export const APP_NAME = "Flight Service"
export const APP_DESC = "A microservice to deal with flight related configurations."

// API description
export const API_VERSION = "v1"
export const API_PREFIX  = `/api/${API_VERSION}`

// API of other microservices
export const AUTH_MICROSERVICE_VERIFICATION_URL = "http://localhost:4500/api/v1/users/me"

// NFR parameters (will be added later)

// Other constants will be added similarly as the project progresses...