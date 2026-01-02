import {model} from 'mongoose'
import {IFlight} from "../interfaces/flight.interface";
import {FlightSchema} from "../schemas/flight.schema";

export const FlightModel = model<IFlight>("Flight", FlightSchema)