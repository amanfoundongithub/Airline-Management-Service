import { Document } from "mongoose";
import { FlightStatus } from "./flight-status.enum";

export interface IFlight extends Document {

  // Identifiers
  aircraft_id: string;

  // Flight details
  flight_number: string;
  passenger_capacity: number;

  departure_airport: string;
  arrival_airport: string;

  // Scheduled times
  departure_time: Date;
  arrival_time: Date;

  // Actual times (optional)
  actual_departure_time?: Date | null;
  actual_arrival_time?: Date | null;

  // State
  current_status: FlightStatus;

  // Audit purposes
  createdAt: Date;
  updatedAt: Date;
}
