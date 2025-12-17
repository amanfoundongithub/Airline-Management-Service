import { Application, Request, Response } from "express"
import express from 'express';
import { API_PREFIX, API_VERSION, APP_DESC, APP_NAME } from "./config/constants";
import flightRouter from "./api/v1/flight.router";


/**
 * Configures an Express application based on the routers and the 
 * middlewares for the entire application.
 * 
 * @author amanfoundongithub 
 */
const configureApp = () => {

    const app : Application = express()

    // Parse JSON
    app.use(express.json()) 

    // Add a simple health checker
    app.get("/", (req : Request, res : Response) => {
        return res.status(200).json({
            "status" : "running",
            "name" : APP_NAME,
            "description" : APP_DESC,
            "version" : API_VERSION
        })
    })

    /**
     * Mapping the app with the respective controllers
     */
    app.use(API_PREFIX + "/flight", flightRouter);

    return app;
}


// Export an instance of this application
export const app = configureApp();

