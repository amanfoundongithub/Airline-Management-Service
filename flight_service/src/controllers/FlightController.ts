import { NextFunction, Request, Response } from "express";
import { HTTPSTATUS } from '../config/constants';
import { flightRepository } from "../repository/FlightRepository";


const validateArrivalBeforeDeparture = (arrival : string, departure : string) => {
    const departureDate = new Date(departure);
    const arrivalDate = new Date(arrival);
    return departureDate >= arrivalDate;
}




export class FlightController {

    create = async (req : Request, res : Response) => {
        try {
            // Log the request
            console.log("Received request for creating new airline")

            // Now we will create the flight
            const newFlight = await flightRepository.create(req.body);

            return res.status(HTTPSTATUS.CREATED).json({
                message : "created",
                details : newFlight
            })
            
        } catch(e) {

            console.log("Error in creating flight:", e);
            return res.status(HTTPSTATUS.INTERNAL_SERVER_ERROR).json({
                error : "Internal Server Error",
                details : e
            })

        } finally {
            console.log("Request completed for creating new airline") 
        }
    }
}

export const validateFlightCreationRequestMiddleware = (req : Request, res : Response, next : NextFunction) => {

    const requiredFields = [
        "departure_time",
        "arrival_time",
        "flight_number",
        "aircraft_id"
    ]

    const missingFields = requiredFields.filter(
        field => req.body[field] === undefined || req.body[field] === null
    )

    if (missingFields.length > 0) {
        return res.status(HTTPSTATUS.BAD_REQUEST).json({
            error: "Some fields are missing to create the required aircraft.",
            missingFields
        });
    }

    if(!validateArrivalBeforeDeparture(req.body.arrival_time, req.body.departure_time)) {
        return res.status(HTTPSTATUS.BAD_REQUEST).json({
            error : "Arrival time must be before the departure time."
        });
    }

    next() 
    
}

