import axios from "axios";
import { NextFunction, Request, Response } from "express";
import { AUTH_MICROSERVICE_VERIFICATION_URL } from "../config/constants";
import { Logger } from "../common/logger";

const AUTHORIZATION_LOGGER = new Logger("AUTHORIZATION")

const getAuthenticationDetails = async (token : string) => {
    const response = await axios.get(AUTH_MICROSERVICE_VERIFICATION_URL, {
        headers : {
            "Authorization" : `Bearer ${token}`
        }
    });
    return response.data;
}

export const validateAuthenticationTokenMiddleware = async (req : Request, res : Response, next : NextFunction) => {
    
    const authHeader = req.headers.authorization;
    if(!authHeader) {
        return res.status(401).json({
            error : "No Authorization Header provided"
        })
    }

    const token = authHeader.split(' ')[1];

    try {
        const userData = await getAuthenticationDetails(token);
        (req as any).userData = userData
        next()

    } catch(e : any) {
        AUTHORIZATION_LOGGER.error(`Error in receiving authorization response: ${e}`)

        const status = e.response?.status || 500;
        const message = e.response?.data?.message || "Internal Auth Error";
        
        return res.status(status).json({ 
            error: message 
        });


    }


}