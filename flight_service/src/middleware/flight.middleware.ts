import { NextFunction, Request, Response } from "express";
import { findMissingFieldsInCreateRequest, validateArrivalBeforeDeparture } from "../common/flight.validation";


/**
 * Middleware for flight creation request to ascertain the 
 * structure of the object and the sanctity.
 * 
 * @author amanfoundongithub
 */
export const validateFlightCreationRequestMiddleware = (req : Request, res : Response, next : NextFunction) => {

    const missingFields = findMissingFieldsInCreateRequest(req) 

    if (missingFields.length > 0) {
        return res.status(400).json({
            error: "Some fields are missing to create the required aircraft.",
            missingFields
        });
    }

    if(!validateArrivalBeforeDeparture(req.body.arrival_time, req.body.departure_time)) {
        return res.status(400).json({
            error : "Arrival time must be before the departure time."
        });
    }

    next() 
    
}