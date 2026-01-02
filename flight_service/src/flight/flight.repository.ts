import { FlightModel } from './flight.model';
import { IFlight } from "./flight.interface";

export class FlightRepository {

    create = async (flightData : Partial<IFlight>) => {
        const flight = new FlightModel(flightData);
        return await flight.save();
    }

    findById = async (aircraft_id : string) => {
        return FlightModel.findOne({
            aircraft_id : aircraft_id
        })
    }

    findByNumber = async (flightNumber : string) => {
        return FlightModel.findOne({
            flight_number: flightNumber.toUpperCase()
        });
    }

    findAll = async (filter : object = {}) => {
        return FlightModel.find(filter).sort({
            departure_time: 1
        });
    }

    update = async (aircraft_id : string, updateData : Partial<IFlight>) => {
        return FlightModel.findOneAndUpdate(
            {
                aircraft_id
            },
            updateData,
            {
                new : true
            }
        )
    }
}