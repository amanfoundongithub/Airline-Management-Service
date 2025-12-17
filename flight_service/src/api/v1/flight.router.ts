import { Router } from "express";
import { FlightController } from "../../controller/flight.controller.js";
import { validateFlightCreationRequestMiddleware, validateFlightLookupRequestMiddleware } from "../../middleware/flight.middleware.js";
import { validateAuthenticationTokenMiddleware } from "../../middleware/auth.middleware.js";




const router = Router()
const flightController = new FlightController()



router.post(
    '/create',
    validateAuthenticationTokenMiddleware,
    validateFlightCreationRequestMiddleware,
    flightController.create
)

router.get(
    '/lookup',
    validateFlightLookupRequestMiddleware,
    flightController.lookup
)

router.get(
    '/search',
    flightController.search
)

export default router;