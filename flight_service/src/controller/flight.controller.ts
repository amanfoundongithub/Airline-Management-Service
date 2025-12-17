import { NextFunction, Request, Response } from "express";
import { FlightRepository } from "../repository/flight.repository.js";
import {findMissingFieldsInCreateRequest, validateArrivalBeforeDeparture} from "../common/flight.validation.js";

import { Logger } from "../common/logger.js";

// Get logger 
const FLIGHT_CONTROLLER_LOGGER = new Logger("FLIGHT_CONTROLLER")

/**
 * Utility class to orchestrate the flight controller to the respective
 * routes and perform validations. 
 * 
 * @author amanfoundongithub
 */
export class FlightController {

    flightRepository : FlightRepository;

    constructor() {
        this.flightRepository = new FlightRepository();
    }


    create = async (req : Request, res : Response) => {
        try {
            // Log the request
            console.log("Received request for creating new airline")

            // Now we will create the flight
            const newFlight = await this.flightRepository.create(req.body);

            return res.status(201).json({
                message : "created",
                details : newFlight
            })
            
        } catch(e) {

            console.log("Error in creating flight:", e);
            return res.status(500).json({
                error : "Internal Server Error",
                details : e
            })

        } finally {
            console.log("Request completed for creating new airline") 
        }
    }
}