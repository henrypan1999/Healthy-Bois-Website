from src.HealthCareSystem import HealthCareSystem


def bootstrap_system(auth_manager, root_path, hc_manager, user_manager, booking_system, rating_manager, referral_system):
    
    HCsystem = HealthCareSystem(auth_manager, root_path, hc_manager, user_manager, booking_system, rating_manager, referral_system)

    return HCsystem
