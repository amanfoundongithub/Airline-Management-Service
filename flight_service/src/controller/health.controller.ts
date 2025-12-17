import { Request, Response } from "express";
import { API_VERSION, APP_DESC, APP_NAME } from "../config/constants";


/**
 * A health controller to check the health of the server
 * and print the latest version that is currently running in the 
 * server.
 * 
 * @author amanfoundongithub
 */
export class HealthController {

    check = async (req : Request, res : Response) => {
        return res.status(200).json({
            "name" : APP_NAME,
            "description" : APP_DESC,
            "status" : "running",
            "version" : API_VERSION
        })
    }

}