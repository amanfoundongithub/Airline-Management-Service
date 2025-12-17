import { Application } from "express"
import express from 'express';
import { API_PREFIX } from "./config/constants";
import healthRouter from './api/health.router';
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

    /**
     * Mapping the app with the respective controllers
     */
    app.use(API_PREFIX,             healthRouter);
    app.use(API_PREFIX + "/flight", flightRouter);

    return app;
}


// Export an instance of this application
export const app = configureApp();

