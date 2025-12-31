from enum import Enum

class UserRole(str, Enum):
    # ===== Platform / Airline Level =====
    SUPER_ADMIN = "super_admin"
    AIRLINE_ADMIN = "airline_admin"

    # ===== Operations & Planning =====
    OPERATIONS_MANAGER = "operations_manager"
    FLIGHT_MANAGER = "flight_manager"
    AIRPORT_MANAGER = "airport_manager"

    # ===== Flight & Airport Staff =====
    PILOT = "pilot"
    CABIN_CREW = "cabin_crew"
    GROUND_STAFF = "ground_staff"

    # ===== Customer & Support =====
    CUSTOMER_SERVICE = "customer_service"
    PASSENGER = "passenger"
    TRAVEL_AGENT = "travel_agent"

    # ===== Finance & Compliance =====
    FINANCE = "finance"
    AUDITOR = "auditor"