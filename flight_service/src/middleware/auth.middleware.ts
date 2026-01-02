import {env} from "../config/env.load";
import {NextFunction, Request, Response} from "express";
import jwt from "jsonwebtoken";
import {Logger} from "../logger/logger";


const AUTH_MIDDLEWARE_LOGGER = new Logger("AUTH")

interface JwtPayload {
    name: string;
    email: string;
    permissions: string[];
    exp: number;
}

const JWT_SECRET = env.JWT_SECRET

interface AuthenticatedRequest extends Request {
    user? : JwtPayload;
}

export const authenticate = (req : AuthenticatedRequest, res : Response, next : NextFunction) => {
    const authHeader = req.headers.authorization
    if (!authHeader?.startsWith("Bearer ")) {
        return res.status(401).json({
            error : {
                code : 'MISSING_AUTH_HEADER',
                details : "Authorization header missing"
            }}
        )
    }
    const token = authHeader.split(" ")[1];
    try {
        req.user = jwt.verify(token, JWT_SECRET) as JwtPayload
        next()
    } catch (err) {
        AUTH_MIDDLEWARE_LOGGER.warn(`Cannot verify: ${err}`)
        return res.status(401).json({
                error : {
                    code : 'INVALID_TOKEN',
                    details : "Invalid/expired token"
                }}
            )
    }
}

export const authorize = (required : string[]) => {
    return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
        const permissions = req.user?.permissions;
        if (!permissions) {
            return res.status(403).json({
                error : {
                    code : 'MISSING_PERMISSIONS',
                    details : "Permissions not found for user"
                }
            })
        }
        const allowed = required.every(p => permissions.includes(p))
        if (!allowed) {
            return res.status(403).json({
                error : {
                    code : 'FORBIDDEN',
                    details : "You don't have the required permissions to use the resource"
                }
            })
        }
        next()
  };
}