import { Router } from "express";
import { FlightController } from "../../../controller/flight.controller";
import { validateFlightCreationRequestMiddleware } from "../../../middleware/flight.middleware";




const router = Router()
const flightController = new FlightController()



router.post(
    '',
    validateFlightCreationRequestMiddleware,
    flightController.create
)

router.get(
    '/:aircraft_id',
    flightController.get_by_id
)

router.put(
    '/:aircraft_id',
    flightController.update_schedule
)

export default router;