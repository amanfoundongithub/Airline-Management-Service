import {convertToNumber} from "../../helpers/number.helper";
import axios from "axios";
import {getServiceToken} from "../../services/token.service";
import {env} from "../../config/env.load";

const checkDepartureBeforeArrival = (departure : Date, arrival : Date) : boolean => {
    if(!departure || !arrival) {
        throw new Error("Departure or arrival not provided");
    }
    return departure.getTime() < arrival.getTime()
}

export const checkAirportId =  async (airport_id : string) => {
    const airportIdInteger = convertToNumber(airport_id)
    const cachedToken = await getServiceToken()
    if(cachedToken) {
        const response = await axios.get(`${env.AIRPORT_ID_DETAILS_URL}/${airportIdInteger}`, {
            headers : {
                Authorization : `Bearer ${cachedToken}`
            },
            timeout : 2000
        })
        return response.status === 200
    } else {
        throw new Error("Unable to get token from auth_microservice")
    }
}

