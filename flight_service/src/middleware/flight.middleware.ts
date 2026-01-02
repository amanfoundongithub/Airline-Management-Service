import { NextFunction, Request, Response } from "express";
import {validateFlightDocument} from "../flight/flight.validator";
import {IFlight} from "../flight/flight.interface";

const findMissingFieldsInCreateRequest = (req : Request) => {
    return []
}
export const validateFlightCreationRequestMiddleware = (req : Request, res : Response, next : NextFunction) => {

    const missingFields = findMissingFieldsInCreateRequest(req)

    if (missingFields.length > 0) {
        return res.status(400).json({
            error: "Some fields are missing to create the required aircraft.",
            missingFields
        });
    }

    const validationResults = validateFlightDocument(req.body as IFlight)
    if(validationResults.length > 0) {
        return res.status(400).json({
            details : validationResults
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