import { Request, Response } from "express";
import { FlightRepository } from "../repository/flight.repository.js";

import { Logger } from "../logger/logger";
import {getServiceToken} from "../services/token.service";
import {checkAirportId} from "../validators/flight.validator";

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

    lookup = async (req : Request, res : Response) => {
        const { flightNumber } = req.query;
        try {

            FLIGHT_CONTROLLER_LOGGER.info(`Request for Info on Airline #${flightNumber} received.`);
            const flightDetails = await this.flightRepository.findByNumber(String(flightNumber).toUpperCase());

            if(!flightDetails) {
                FLIGHT_CONTROLLER_LOGGER.info(`Airline #${flightNumber} not found.`)
                return res.status(404).json({
                    message: "The request airline could not be found."
                })
            } else {
                FLIGHT_CONTROLLER_LOGGER.info(`Airline #${flightNumber} found.`)
                return res.status(200).json({
                    message : "FOUND",
                    details : flightDetails
                })
            }

        } catch(e) {
            FLIGHT_CONTROLLER_LOGGER.error(`Error in findind details: ${e}`);
            return res.status(500).json({
                error : "Internal Server Error",
                details : e
            })
        } finally {
            FLIGHT_CONTROLLER_LOGGER.info(`Request for Info on Airline #${flightNumber} completed.`)
        }
    }

    search = async (req : Request, res : Response) => {
        try {
            FLIGHT_CONTROLLER_LOGGER.info(`Request for Search on Airline received.`)

            const filter : any = {};
            Object.keys(req.query).forEach((key) => {
                const value = req.query[key]

                if(value) {
                    filter[key] = {
                        $regex : value,
                        $options : "i"
                    }
                }
            })

            const listOfFlights = await this.flightRepository.findAll(filter);
            return res.status(200).json({
                "message" : "FOUND",
                "results" : listOfFlights
            })
        } catch(e) {
            FLIGHT_CONTROLLER_LOGGER.error(`Error in findingflights: ${e}`)
            return res.status(500).json({
                error : "Internal Server Error",
                details : e
            })
        } finally {
            FLIGHT_CONTROLLER_LOGGER.info(`Request for Search on Airline completed.`)
        }
    }

    timepass = async (req : Request, res : Response) => {
        const airport_id = "abcd"
        checkAirportId(airport_id)
            .then((valid) => {
                return res.send({
                    valid
                })
            })
            .catch((err) => {
                console.log(err)
            })
    }
}