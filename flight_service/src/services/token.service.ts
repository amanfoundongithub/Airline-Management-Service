import {env} from "../config/env.load";
import axios from "axios";
import jwt from "jsonwebtoken";

let cachedToken : string | null = null
let tokenExpiry : number | null = null

let tokenDuration : number = 300 * 100

export const getServiceToken = async () => {
    console.log(`here ${cachedToken} ${tokenDuration}`)
    const now = Date.now()

    if(cachedToken && tokenExpiry && now < tokenExpiry - tokenDuration) {
        return cachedToken
    }

    const response = await axios.post(env.AUTH_URL, {
        email : env.AUTH_USERNAME,
        password : env.AUTH_PASSWORD,
    })

    const {access_token} = response.data
    cachedToken = access_token
    tokenExpiry = getTokenExpiry(access_token)
    return cachedToken
}

const getTokenExpiry = (token : string) : number => {
    const decoded = jwt.decode(token) as {
        exp? : number
    }
    if(!decoded.exp) {
        throw new Error("Token has no expiry")
    }
    return decoded.exp
}