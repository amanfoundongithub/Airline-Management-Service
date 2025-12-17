import { Router } from "express";
import { FlightController } from "../../controller/flight.controller.js";
import { validateFlightCreationRequestMiddleware, validateFlightLookupRequestMiddleware } from "../../middleware/flight.middleware.js";




const router = Router()
const flightController = new FlightController()

router.post(
    '/create',
    validateFlightCreationRequestMiddleware,
    flightController.create
)

router.get(
    '/lookup',
    validateFlightLookupRequestMiddleware,
    flightController.lookup
)

export default router;