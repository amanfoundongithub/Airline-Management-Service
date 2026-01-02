import { Router } from "express";
import { FlightCrudController } from "../../../controller/flight.crud.controller";
import { validateFlightCreationRequestMiddleware } from "../../../middleware/flight.middleware";




const router = Router()
const flightController = new FlightCrudController()



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

router.delete(
    '/:aircraft_id',
    flightController.delete_flight
)

export default router;