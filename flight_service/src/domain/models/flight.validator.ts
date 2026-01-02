import {convertToNumber} from "../../helpers/number.helper";
import axios from "axios";

const checkDepartureBeforeArrival = (departure : Date, arrival : Date) : boolean => {
    if(!departure || !arrival) {
        throw new Error("Departure or arrival not provided");
    }
    return departure.getTime() < arrival.getTime()
}

const checkAirportId = (airport_id : string) : boolean => {
    // TODO: Implement the logic to get the airport id checked from the server
    return true
}

