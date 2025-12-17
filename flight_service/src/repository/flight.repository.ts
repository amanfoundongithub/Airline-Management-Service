import { FlightModel, IFlight } from '../models/Flight.js';

/**
 * Repository helper to interact with database directly
 * 
 * @author amanfoundongithub
 */
export class FlightRepository {

    create = async (flightData : Partial<IFlight>) => {
        const flight = new FlightModel(flightData);
        return await flight.save();
    }

    findByNumber = async (flightNumber : string) => {
        return await FlightModel.findOne({
            flight_number : flightNumber.toUpperCase()
        })
    }

    findAll = async (filter : object = {}) => {
        return await FlightModel.find(filter).sort({
            departure_time : 1
        })
    }

    update = async (id : string, updateData : Partial<IFlight>) => {
        return await FlightModel.findByIdAndUpdate(id, updateData, {
            new : true
        })
    }

}