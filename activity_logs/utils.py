from .models import ActivityLog


def log_activity(user, action, module_name='General'):
    business = None

    if getattr(user, 'is_authenticated', False):
        try:
            business = user.profile.business
        except Exception:
            business = None

    ActivityLog.objects.create(
        business=business,
        user=user if getattr(user, 'is_authenticated', False) else None,
        action=action,
        module_name=module_name,
    )