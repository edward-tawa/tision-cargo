ROLE_TO_PERMISSIONS = {
    "admin": [
        # Full control over user management
        "users.can_create_user",
        "users.can_read_user",
        "users.can_update_user",
        "users.can_delete_user",
        "users.can_suspend_user",
        "users.can_verify_user",
        "users.can_change_user_role",
        # Full control over bids
        "bids.can_create_bid",
        "bids.can_accept_bid",
        "bids.can_reject_bid",
        "bids.can_cancel_bid",
        "bids.can_complete_bid",
        "bids.can_view_bid",
        "bids.can_delete_bid",
        # Full control over bookings
        "bookings.can_create_booking",
        "bookings.can_accept_booking",
        "bookings.can_reject_booking",
        "bookings.can_cancel_booking",
        "bookings.can_complete_booking",
        "bookings.can_view_booking",
        "bookings.can_delete_booking",
        # Full control over profiles (Driver + Client)
        "profiles.can_create_driver_profile",
        "profiles.can_read_driver_profile",
        "profiles.can_update_driver_profile",
        "profiles.can_delete_driver_profile",
        "profiles.can_create_client_profile",
        "profiles.can_read_client_profile",
        "profiles.can_update_client_profile",
        "profiles.can_delete_client_profile",
        # Full control over trips
        "trips.can_create_trip",
        "trips.can_view_trip",
        "trips.can_update_trip_status",
        "trips.can_view_trip_location",
        "trips.can_cancel_trip",
        "trips.can_delete_trip",
        # Full control over notifications
        "notifications.can_create_notification",
        "notifications.can_read_notification",
        "notifications.can_delete_notification",
        # Full control over communications / chat (Messages + Threads)
        "communications.can_send_message",
        "communications.can_read_message",
        "communications.can_delete_message",
        "communications.can_create_thread",
        "communications.can_read_thread",
        "communications.can_delete_thread",
        # Full control over payments
        "payments.view_transaction",
        "payments.change_transaction",
        "payments.can_refund_transaction",
        "payments.can_view_analytics",
    ],
    "driver": [
        # Drivers can view their own user details
        "users.can_read_user",
        # Drivers can create, view, cancel, and complete bids
        "bids.can_create_bid",
        "bids.can_view_bid",
        "bids.can_cancel_bid",
        "bids.can_complete_bid",
        # Drivers can view bookings, accept, and complete assigned bookings
        "bookings.can_view_booking",
        "bookings.can_accept_booking",
        "bookings.can_complete_booking",
        # Drivers can manage their own driver profile
        "profiles.can_create_driver_profile",
        "profiles.can_read_driver_profile",
        "profiles.can_update_driver_profile",
        "profiles.can_delete_driver_profile",
        # Drivers can view trips, update their status, and view location
        "trips.can_view_trip",
        "trips.can_update_trip_status",
        "trips.can_view_trip_location",
        # Drivers can read and manage their own notifications
        "notifications.can_read_notification",
        "notifications.can_delete_notification",
        # Drivers can interact with chat threads and messages
        "communications.can_create_thread",
        "communications.can_read_thread",
        "communications.can_send_message",
        "communications.can_read_message",
        # Control over payments
        "payments.add_transaction",
        "payments.view_transaction",
        "payments.can_initiate_payment",
    ],
    "client": [
        # Clients can view their own user details
        "users.can_read_user",
        # Clients can view, accept, reject, and cancel bids on their requests
        "bids.can_view_bid",
        "bids.can_accept_bid",
        "bids.can_reject_bid",
        "bids.can_cancel_bid",
        # Clients can create, view, and cancel their own bookings
        "bookings.can_create_booking",
        "bookings.can_view_booking",
        "bookings.can_cancel_booking",
        # Clients can manage their own client profile
        "profiles.can_create_client_profile",
        "profiles.can_read_client_profile",
        "profiles.can_update_client_profile",
        "profiles.can_delete_client_profile",
        # Clients can view their trips, track real-time locations, and cancel trips
        "trips.can_view_trip",
        "trips.can_view_trip_location",
        "trips.can_cancel_trip",
        # Clients can read and manage their own notifications
        "notifications.can_read_notification",
        "notifications.can_delete_notification",
        # Clients can interact with chat threads and messages
        "communications.can_create_thread",
        "communications.can_read_thread",
        "communications.can_send_message",
        "communications.can_read_message",
    ],
}
