import {Schema} from "mongoose"
import {FlightStatus} from "../enums/flight-status.enum";

export const FlightSchema = new Schema({
    aircraft_id: {
        type: String,
        required: [true, "Aircraft ID is required for maintenance"],
        trim: true,
    },

    // Flight details
    flight_number: {
        type: String,
        required: [true, "Flight number is required for managing flight"],
        unique: true,
        trim: true,
        uppercase: true,
        match: [/^[A-Z]{2}\d{3,4}$/, 'Flight number format must be like AA1234.']
    },

    passenger_capacity: {
        type: Number,
        required: [true, "Flight capacity is required"],
        min: [1, "Capacity must have at least 1 seat"]
    },

    departure_airport: {
        type: String,
        required: [true, "Need a departure airport to send flight from"],
    },

    arrival_airport: {
        type: String,
        required: [true, "Need a arrival airport to send flight to"],
    },

    departure_time: {
        type: Date,
        required: [true, "Scheduled departure time is required"],
    },

    arrival_time: {
        type: Date,
        required: [true, "Scheduled arrival time is required"],
    },

    actual_departure_time: {
        type: Date,
        default: null,
    },

    actual_arrival_time: {
        type: Date,
        default: null,
    },

    current_status: {
        type: String,
        enum: Object.values(FlightStatus),
        default: FlightStatus.SCHEDULED,
    }
},
    {
        timestamps : true,
        collection : "flights"
    }
)

FlightSchema.index({
    departure_airport: 1,
    arrival_airport: 1,
    departure_time: 1,
})

