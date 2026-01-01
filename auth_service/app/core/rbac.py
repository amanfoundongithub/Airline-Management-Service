from app.core.enums.role import UserRole
from app.core.enums.permissions import Permission

ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.SUPER_ADMIN: set(Permission),

    UserRole.AIRLINE_ADMIN: {
        Permission.USER_CREATE,
        Permission.USER_READ,
        Permission.USER_UPDATE,

        Permission.FLIGHT_CREATE,
        Permission.FLIGHT_UPDATE,
        Permission.FLIGHT_CANCEL,

        Permission.AIRPORT_CREATE,
        Permission.AIRPORT_UPDATE,
        Permission.AIRPORT_VIEW,

        Permission.PAYMENT_VIEW,
    },

    UserRole.FLIGHT_MANAGER: {
        Permission.FLIGHT_CREATE,
        Permission.FLIGHT_UPDATE,
        Permission.FLIGHT_CANCEL,
        Permission.FLIGHT_VIEW,
    },

    UserRole.AIRPORT_MANAGER: {
        Permission.AIRPORT_UPDATE,
        Permission.AIRPORT_VIEW,
    },

    UserRole.PILOT: {
        Permission.FLIGHT_VIEW,
    },

    UserRole.CABIN_CREW: {
        Permission.FLIGHT_VIEW,
    },

    UserRole.GROUND_STAFF: {
        Permission.BOOKING_VIEW,
    },

    UserRole.CUSTOMER_SERVICE: {
        Permission.BOOKING_VIEW,
        Permission.BOOKING_CANCEL,
    },

    UserRole.PASSENGER: {
        Permission.BOOKING_CREATE,
        Permission.BOOKING_VIEW,
        Permission.BOOKING_CANCEL,
    },

    UserRole.SYSTEM: {
        Permission.SYSTEM_ACCESS,
    },
}

def get_user_permissions(role : UserRole) -> set[Permission]:
    return ROLE_PERMISSIONS[role]
