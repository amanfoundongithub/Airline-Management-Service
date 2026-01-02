import { Router } from "express";
import { FlightCrudController } from "../../../controller/flight.crud.controller";
import { validateFlightCreationRequestMiddleware } from "../../../middleware/flight.middleware";
import {authenticate, authorize} from "../../../middleware/auth.middleware";

const router = Router()
const flightController = new FlightCrudController()

router.post(
    '',
    authenticate,
    authorize(["flight.create"]),
    validateFlightCreationRequestMiddleware,
    flightController.create
)

router.get(
    '/:aircraft_id',
    authenticate,
    authorize(["flight.view"]),
    flightController.get_by_id
)

router.put(
    '/:aircraft_id',
    authenticate,
    authorize(["flight.update"]),
    flightController.update_schedule
)

router.delete(
    '/:aircraft_id',
    authenticate,
    authorize(["flight.cancel"]),
    flightController.delete_flight
)

export default router;