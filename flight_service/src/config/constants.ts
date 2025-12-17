

/**
 * Defines the status of the flight
 * 
 * @author amanfoundongithub
 */
export enum FlightStatus {
    SCHEDULED = 'Scheduled',
    DELAYED   = 'Delayed',
    BOARDING  = 'Boarding',
    DEPARTED  = 'Departed',
    ARRIVED   = 'Arrived',
    CANCELLED = 'Cancelled',
}

/**
 * Defines the color of the logs, useful for logger
 * 
 * @author amanfoundongithub
 */
export enum Colors {
    RED    = "\x1b[31m",
    GREEN  = "\x1b[32m",
    YELLOW = "\x1b[33m",
    BLUE   = "\x1b[34m",
    CYAN   = "\x1b[36m",
    RESET  = "\x1b[0m",
}