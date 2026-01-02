import { Router } from "express";
import { FlightController } from "../../../controller/flight.controller";
import { validateFlightCreationRequestMiddleware, validateFlightLookupRequestMiddleware } from "../../../middleware/flight.middleware";




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

router.get(
    '/search',
    flightController.search
)

router.get(
    '/timepass',
    flightController.timepass
)
export default router;