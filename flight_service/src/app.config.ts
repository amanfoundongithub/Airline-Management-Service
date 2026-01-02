import { Application, Request, Response } from "express"
import express from 'express';
import { env } from "./config/env.load";
import flightRouter from "./api/v1/routers/flight.router";

const configureApp = () => {
    const app : Application = express()
    app.use(express.json())

    app.get("/", (req : Request, res : Response) => {
        return res.status(200).json({
            "status" : "running",
            "name" : env.NAME,
            "description" : env.DESC,
            "version" : env.API_VERSION
        })
    })

    app.use(env.API_PREFIX_FLIGHT, flightRouter);
    return app;
}


// Export an instance of this application
export const app = configureApp();

