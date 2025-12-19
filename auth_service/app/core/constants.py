from enum import Enum

class UserRole(Enum):
    PASSENGER = "passenger"
    PILOT = "pilot"
    CABIN_CREW = "cabin_crew"
    GROUND_STAFF = "ground_staff"
    MAINTENANCE = "maintenance"
    ADMIN = "admin"