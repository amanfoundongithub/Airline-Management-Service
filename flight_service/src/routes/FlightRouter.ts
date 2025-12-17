import { Router } from "express";
import { FlightController, validateFlightCreationRequestMiddleware } from "../controllers/FlightController.js";




const router = Router()
const flightController = new FlightController()

router.post(
    '/create',
    validateFlightCreationRequestMiddleware,
    flightController.create
)

export default router;