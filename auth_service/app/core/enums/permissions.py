from enum import Enum

class Permission(str, Enum):
    # ----- User / Auth -----
    USER_CREATE = "user.create"
    USER_READ = "user.read"
    USER_UPDATE = "user.update"
    USER_DEACTIVATE = "user.deactivate"

    # ----- Flights -----
    FLIGHT_CREATE = "flight.create"
    FLIGHT_UPDATE = "flight.update"
    FLIGHT_CANCEL = "flight.cancel"
    FLIGHT_VIEW = "flight.view"

    # ----- Airports -----
    AIRPORT_CREATE = "airport.create"
    AIRPORT_UPDATE = "airport.update"
    AIRPORT_VIEW = "airport.view"

    # ----- Bookings -----
    BOOKING_CREATE = "booking.create"
    BOOKING_CANCEL = "booking.cancel"
    BOOKING_VIEW = "booking.view"

    # ----- Finance -----
    REFUND_APPROVE = "refund.approve"
    PAYMENT_VIEW = "payment.view"

    # ----- System -----
    SYSTEM_ACCESS = "system.access"