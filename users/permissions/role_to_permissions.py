ROLE_TO_PERMISSIONS = {
    "admin": [
        # Admins get full control over user management
        # Standard Django default permissions for CustomUser
        "users.add_customuser",
        "users.view_customuser",
        "users.change_customuser",
        "users.delete_customuser",
        "users.can_suspend_user",
        "users.can_verify_user",
        "users.can_change_user_role",
        "users.can_change_user_status",
        "users.can_change_user_password",
        "users.can_change_user_email",
        "users.can_change_user_phone_number",
        "users.can_change_user_age",
        # Admins can also oversee/manage all bid actions
        "users.can_create_bid",
        "users.can_accept_bid",
        "users.can_reject_bid",
        "users.can_cancel_bid",
        "users.can_complete_bid",
    ],
    "driver": [
        # Drivers typically create bids on jobs/deliveries and can complete or cancel them
        "users.can_create_bid",
        "users.can_cancel_bid",
        "users.can_complete_bid",
    ],
    "client": [
        # Clients typically create requests and can accept or reject bids made by drivers
        "users.can_create_bid",
        "users.can_accept_bid",
        "users.can_reject_bid",
        "users.can_cancel_bid",
    ],
}
