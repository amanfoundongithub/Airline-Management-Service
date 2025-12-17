import { Router } from "express";
import { FlightController } from "../../controller/flight.controller.js";
import { validateFlightCreationRequestMiddleware } from "../../middleware/flight.middleware.js";




const router = Router()
const flightController = new FlightController()

router.post(
    '/create',
    validateFlightCreationRequestMiddleware,
    flightController.create
)

export default router;