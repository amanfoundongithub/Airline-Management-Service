import { model, Schema } from "mongoose";
import { FlightStatus } from "../domain/enums/flight-status.enum";

/**
 * Defines the interface for the Flight object that persist in MongoDB
 * 
 * @author amanfoundongithub
 */
export interface IFlight {
    flight_number : string,
    aircraft_id : string,   
    
    departure_airport : string,
    arrival_airport : string, 

    departure_time : Date,
    arrival_time : Date,

    actual_departure_time?: Date; 
    actual_arrival_time?: Date;   

    capacity: number; 
    current_status: FlightStatus;

};

/**
 * Defines the actual MongoDB schema with the constraints
 * 
 * @author amanfoundongithub
 */
const FlightSchema: Schema = new Schema({
    flight_number: { 
        type: String, 
        required: [true, 'Flight number is required.'],
        unique: true,
        trim: true,
        uppercase: true,
        match: [/^[A-Z]{2}\d{2,8}$/, 'Flight number format must be like AA1234.']
    },
    aircraft_id: {
        type: String,
        required: [true, 'Aircraft ID is required to link to the asset.'], 
        trim: true,
    },

    departure_airport: { 
        type: String, 
        required: [true, 'Departure airport is required.'], 
        match: [/^[A-Z]{3}$/, 'Departure airport must be a 3-letter IATA code.'],
        uppercase: true
    },
    arrival_airport: { 
        type: String, 
        required: [true, 'Arrival airport is required.'], 
        match: [/^[A-Z]{3}$/, 'Arrival airport must be a 3-letter IATA code.'],
        uppercase: true
    },
    departure_time: { 
        type: Date, 
        required: [true, 'Scheduled departure time is required.'] 
    },
    arrival_time: { 
        type: Date, 
        required: [true, 'Scheduled arrival time is required.'] 
    },
    
    actual_departure_time: { 
        type: Date, 
        default: null 
    },
    actual_arrival_time: { 
        type: Date, 
        default: null 
    },

    capacity: { 
        type: Number, 
        required: [true, 'Capacity is required.'], 
        min: [1, 'Capacity must be at least 1 seat.'] 
    },
    current_status: { 
        type: String, 
        enum: Object.values(FlightStatus),
        default: FlightStatus.SCHEDULED
    },
    }, 
    { 
        timestamps: true, 
        collection: 'flights'
    });

// Create a compound index for fast searching by route and date.
FlightSchema.index({ departure_airport: 1, arrival_airport: 1, departure_time: 1 }); 


// Create the Mongoose Model
export const FlightModel = model<IFlight>('Flight', FlightSchema);