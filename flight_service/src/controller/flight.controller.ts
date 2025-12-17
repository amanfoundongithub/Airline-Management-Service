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
            FLIGHT_CONTROLLER_LOGGER.info("Received request for creating new airline")

            const newFlight = await this.flightRepository.create(req.body);
            return res.status(201).json({
                message : "created",
                details : newFlight
            })
            
        } catch(e) {
            FLIGHT_CONTROLLER_LOGGER.error("Error in creating flight:" + e);
            return res.status(500).json({
                error : "Internal Server Error",
                details : e
            })

        } finally {
            FLIGHT_CONTROLLER_LOGGER.info("Completed request for creating new airline")
        }
    }
}