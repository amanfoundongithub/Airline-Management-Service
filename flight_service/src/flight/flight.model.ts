import {model} from 'mongoose'
import {IFlight} from "./flight.interface";
import {FlightSchema} from "./flight.schema";

export const FlightModel = model<IFlight>("Flight", FlightSchema)