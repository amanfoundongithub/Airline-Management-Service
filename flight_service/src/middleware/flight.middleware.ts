import { NextFunction, Request, Response } from "express";
import {validateFlightDocument} from "../flight/flight.validator";
import {IFlight} from "../flight/flight.interface";

const findMissingFieldsInCreateRequest = (req : Request) => {
    const required_fields = [
        "flight_number",
        "departure_airport",
        "arrival_airport",
        "departure_time",
        "arrival_time",
        "passenger_capacity",
        "aircraft_id"
    ]

    return required_fields.filter(field => {
        const value = req.body[field]
        return value === undefined || value === null || value === ""
    })
}
export const validateFlightCreationRequestMiddleware = (req : Request, res : Response, next : NextFunction) => {

    const missingFields = findMissingFieldsInCreateRequest(req)

    if (missingFields.length > 0) {
        return res.status(400).json({
            error : {
                code : "MISSING_FIELDS",
                details : "Some fields are missing from the request. Check the `missingFields` attribute for more details.",
                missingFields
            }
        });
    }

    const validationResults = validateFlightDocument(req.body as IFlight)
    if(validationResults.length > 0) {
        return res.status(400).json({
            error : {
                code : "INVALID_REQUEST",
                details : validationResults
            }
        });
    }

    next();
    
}

export const validateFlightLookupRequestMiddleware = (req : Request, res : Response, next : NextFunction) => {

    const { flightNumber } = req.query;

    if(!flightNumber) {
        return res.status(400).json({
            error : "Invalid request. Missing flightNumber query param"
        })
    }

    next();

}