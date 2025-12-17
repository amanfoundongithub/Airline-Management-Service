import { Router } from "express";
import { HealthController } from '../controller/health.controller';



const router = Router()
const healthController = new HealthController() 


router.get(
    "/",
    healthController.check
)

export default router;