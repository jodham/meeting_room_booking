from room_booking_app.models import Roles


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

