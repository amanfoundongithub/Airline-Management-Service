import { Router } from "express";
import { FlightController, validateFlightCreationRequestMiddleware } from "../controllers/flight.controller.js";




const router = Router()
const flightController = new FlightController()

router.post(
    '/create',
    validateFlightCreationRequestMiddleware,
    flightController.create
)

export default router;