import { Router } from "express";
import { FlightCrudController } from "../../../controller/flight.crud.controller";
import { validateFlightCreationRequestMiddleware } from "../../../middleware/flight.middleware";
import {authenticate, authorize} from "../../../middleware/auth.middleware";

const crud_router = Router()
const flightController = new FlightCrudController()

crud_router.post(
    '',
    authenticate,
    authorize(["flight.create"]),
    validateFlightCreationRequestMiddleware,
    flightController.create
)

crud_router.get(
    '/:aircraft_id',
    authenticate,
    authorize(["flight.view"]),
    flightController.get_by_id
)

crud_router.get(
    '',
    authenticate,
    authorize(["flight.view"]),
    flightController.get_by_params
)

crud_router.put(
    '/:aircraft_id',
    authenticate,
    authorize(["flight.update"]),
    flightController.update_schedule
)

crud_router.delete(
    '/:aircraft_id',
    authenticate,
    authorize(["flight.cancel"]),
    flightController.delete_flight
)

export default crud_router;