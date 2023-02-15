from room_booking_app.models import Roles, Rooms
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


def get_role_names(user):
    role_ids = user.role.split(',')
    roles = Roles.objects.filter(id__in=role_ids)
    return [role.role_name for role in roles]


def check_role(roles):
    if 'approver' in roles and 'administrator' not in roles:
        return "approver"
    elif "administrator" in roles:
        return "administrator"
    else:
        return "default"


def check_user_role(user):
    roles = get_role_names(user)
    return check_role(roles)


@receiver(user_logged_in)
def unsuspend_rooms(sender, user, request, **kwargs):
    # Get all rooms that are currently suspended
    suspended_rooms = Rooms.objects.filter(is_suspended=True)

    # Call unsuspend_if_needed() on each suspended room
    for room in suspended_rooms:
        room.unsuspend_if_needed()
