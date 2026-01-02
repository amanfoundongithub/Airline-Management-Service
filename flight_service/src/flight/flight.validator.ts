import {convertToNumber} from "../helpers/number.helper";
import axios from "axios";
import {getServiceToken} from "../services/token.service";
import {env} from "../config/env.load";
import {IFlight} from "./flight.interface";

const checkDepartureBeforeArrival = (departure : Date, arrival : Date) : string => {
    if(!departure || !arrival) {
        throw new Error("Departure or arrival not provided");
    }

    if(new Date(departure).getTime() >= new Date(arrival).getTime()) {
        return "Departure time cannot be more than or equal to arrival time."
    } else {
        return ""
    }
}

const checkDepartureAndArrivalAirportDifference = (departure : string, arrival : string) : string => {
    if(!departure || !arrival) {
        throw new Error("Departure or arrival airports not provided")
    }
    if(convertToNumber(departure) === convertToNumber(arrival)) {
        return "The departure and the arrival airport cannot be same."
    } else {
        return ""
    }
}

export const checkAirportId =  (airport_id : string) => {
    const airportIdInteger = convertToNumber(airport_id)
    let result = ""
    getServiceToken().then(async (cachedToken) => {
        if(cachedToken) {
        const response = await axios.get(`${env.AIRPORT_ID_DETAILS_URL}/${airportIdInteger}`, {
            headers : {
                Authorization : `Bearer ${cachedToken}`
            },
            timeout : 2000
        })
        if(response.status === 200) {
            result = ""
        } else {
            result = `Invalid airport Id: ${airport_id}`
        }
    } else {
        throw new Error("Unable to get token from auth_microservice")
    }
    })
        .catch((err) => {
            console.log(err)
        })
    return result
}

export const validateFlightDocument = (flight : IFlight) : string => {
    return checkDepartureBeforeArrival(flight.departure_time, flight.arrival_time)
    || checkDepartureAndArrivalAirportDifference(flight.departure_airport, flight.arrival_airport)
    || checkAirportId(flight.arrival_airport)
    || checkAirportId(flight.departure_airport)
}