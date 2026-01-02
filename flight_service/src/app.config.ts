import { Application, Request, Response } from "express"
import express from 'express';
import { env } from "./config/env.load";
import v1_router from "./api/v1/router";

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

    app.use(env.API_PREFIX_FLIGHT, v1_router);
    return app;
}


// Export an instance of this application
export const app = configureApp();

