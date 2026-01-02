import { Request, Response } from "express";
import { FlightRepository } from "../flight/flight.repository";
import { Logger } from "../logger/logger";
import {IFlight} from "../flight/flight.interface";
import {FlightStatus} from "../flight/flight-status.enum";

const FLIGHT_CONTROLLER_LOGGER = new Logger("FLIGHT_CONTROLLER")

export class FlightCrudController {

    flightRepository : FlightRepository;

    constructor() {
        this.flightRepository = new FlightRepository();
    }

    create = async (req : Request, res : Response) => {
            FLIGHT_CONTROLLER_LOGGER.info(`Received  request for creating new airline ${req.body.aircraft_id}`)
            this.flightRepository.create(req.body)
                .then((dbEntity) => {
                    return res.status(201).json({
                        message : "SUCCESS",
                        details : dbEntity
                    })
                })
                .catch((err) => {
                    FLIGHT_CONTROLLER_LOGGER.warn(`Error in creating flight : ${err}`)
                    if(err.code === 11000) {
                        return res.status(409).json({
                            error : {
                                code : "FLIGHT_ALREADY_EXISTS",
                                details : `A flight with ID: ${req.body.aircraft_id} already exists! Please try with a different id or query this flight.`
                            }
                        })
                    }
                    else {
                        return res.status(500).json({
                            error : {
                                code : "INTERNAL_SERVER_ERROR",
                                details : err
                            }
                        })
                    }
                })
                .finally(() => {
                    FLIGHT_CONTROLLER_LOGGER.info(`Completed request for creating new airline ${req.body.aircraft_id}`)
                })
    }

    get_by_id = async (req : Request, res : Response) => {
        const aircraft_id = req.params.aircraft_id
        FLIGHT_CONTROLLER_LOGGER.info(`Received  Request to get information on aircraft_id=${aircraft_id}`)
        this.flightRepository.findById(aircraft_id)
            .then((aircraft) => {
                if(aircraft) {
                    return res.status(200).json({
                        message : "SUCCESS",
                        details : aircraft
                    })
                } else {
                    return res.status(404).json({
                        error : {
                            code : 'FLIGHT_NOT_FOUND',
                            details : `No aircraft with aircraft_id:${aircraft_id} is found. Try again!`
                        }
                    })
                }

            })
            .catch((err) => {
                FLIGHT_CONTROLLER_LOGGER.warn(`Error during finding of aircraft : ${err}`)
                return res.status(500).json({
                    error : {
                        code : 'INTERNAL_SERVER_ERROR',
                        details : err
                    }
                })
            })
            .finally(() => {
                FLIGHT_CONTROLLER_LOGGER.info(`Completed Request to get information on aircraft_id=${aircraft_id}`)
            })
    }

    update_schedule = async (req : Request, res : Response) => {
        const aircraft_id = req.params.aircraft_id
        FLIGHT_CONTROLLER_LOGGER.info(`Received  Request to update schedules on aircraft_id=${aircraft_id}`)
        this.flightRepository.update(aircraft_id, req.body as Partial<IFlight>)
            .then((response) => {
                res.status(200).json({
                    message : "SUCCESS",
                    details : response
                })
            })
            .catch((err) => {
                FLIGHT_CONTROLLER_LOGGER.warn(`Error during updating of aircraft : ${err}`)
                return res.status(500).json({
                    error : {
                        code : 'INTERNAL_SERVER_ERROR',
                        details : err
                    }
                })
            })
            .finally(() => {
                FLIGHT_CONTROLLER_LOGGER.info(`Completed Request to update schedules on aircraft_id=${aircraft_id}`)

            })
    }

    delete_flight = async (req : Request, res : Response) => {
        const aircraft_id = req.params.aircraft_id
        FLIGHT_CONTROLLER_LOGGER.info(`Received  Request to delete aircraft_id=${aircraft_id}`)
        this.flightRepository.update(aircraft_id, {
            "current_status" : FlightStatus.CANCELLED
        } as Partial<IFlight>)
            .then((response) => {
                res.status(200).json({
                    message : "SUCCESS",
                    details : response
                })
            })
            .catch((err) => {
                FLIGHT_CONTROLLER_LOGGER.warn(`Error during deletion of aircraft : ${err}`)
                return res.status(500).json({
                    error : {
                        code : 'INTERNAL_SERVER_ERROR',
                        details : err
                    }
                })
            })
            .finally(() => {
                FLIGHT_CONTROLLER_LOGGER.info(`Completed Request to delete aircraft_id=${aircraft_id}`)

            })
    }
}