

/**
 * Custom type to define the flight status 
 */
export type FlightStatus =
    | 'Scheduled'
    | 'Delayed'
    | 'Departed'
    | 'Arrived'
    | 'Cancelled'
    | 'Boarding'


/**
 * Define http codes
 * 
 */
export const HTTPSTATUS = Object.freeze({
    // 200 series here
    OK : 200,
    CREATED : 201,
    NO_CONTENT : 204,

    // 400 series here
    BAD_REQUEST : 400,
    UNAUTHORIZED : 401,
    FORBIDDEN : 403,
    NOT_FOUND : 404,
    CONFLICT : 409,

    // 500 series here
    INTERNAL_SERVER_ERROR : 500,
    BAD_GATEWAY : 502,
    SERVICE_UNAVAILABLE : 503

})

