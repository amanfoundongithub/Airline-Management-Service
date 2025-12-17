import { Request } from "express";


/**
 * This utility helps to validate if the arrival is before departure so that 
 * the times does seem reasonable enough!
 * 
 * @author amanfoundongithub
 */
export const validateArrivalBeforeDeparture = (arrival : string, departure : string) => {
    const departureDate = new Date(departure);
    const arrivalDate = new Date(arrival);
    return departureDate <= arrivalDate;
}

/**
 * This utility allows us to find if the fields are present or not in the 
 * request for flight creation.
 *  
 * @author amanfoundongithub
 */
export const findMissingFieldsInCreateRequest = (req : Request) => {

    const requiredFields = [
        "departure_time",
        "arrival_time",
        "flight_number",
        "aircraft_id"
    ]

    return requiredFields.filter(
        field => req.body[field] === undefined || req.body[field] === null
    )
}