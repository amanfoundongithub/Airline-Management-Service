import {Router} from "express";
import crud_router from "./routers/flight.crud.router";

const v1_router = Router()
v1_router.use(crud_router)

export default v1_router