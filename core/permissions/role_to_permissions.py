ROLE_TO_PERMISSIONS = {
    "admin": [
        # Full control over user management (Standard Django + Custom user actions)
        "users.add_customuser",
        "users.view_customuser",
        "users.change_customuser",
        "users.delete_customuser",
        "users.can_suspend_user",
        "users.can_verify_user",
        "users.can_change_user_role",
        # Full control over bids
        "bids.add_bid",
        "bids.view_bid",
        "bids.change_bid",
        "bids.delete_bid",
        "bids.can_create_bid",
        "bids.can_accept_bid",
        "bids.can_reject_bid",
        "bids.can_cancel_bid",
        "bids.can_complete_bid",
        # Full control over profiles
        "profiles.add_driver_profile",
        "profiles.view_driver_profile",
        "profiles.change_driver_profile",
        "profiles.delete_driver_profile",
        "profiles.add_client_profile",
        "profiles.view_client_profile",
        "profiles.change_client_profile",
        "profiles.delete_client_profile",
    ],
    "driver": [
        # Drivers can create, cancel, and complete bids
        "bids.view_bid",
        "bids.can_create_bid",
        "bids.can_cancel_bid",
        "bids.can_complete_bid",
        # Drivers can manage their own profiles
        "profiles.add_driver_profile",
        "profiles.view_driver_profile",
        "profiles.change_driver_profile",
        "profiles.delete_driver_profile",
    ],
    "client": [
        # Clients can create, accept, reject, and cancel bids on their requests
        "bids.view_bid",
        "bids.can_create_bid",
        "bids.can_accept_bid",
        "bids.can_reject_bid",
        "bids.can_cancel_bid",
        # client can manage their own profiles
        "profiles.add_client_profile",
        "profiles.view_client_profile",
        "profiles.change_client_profile",
        "profiles.delete_client_profile",
    ],
}
