from .choices import UserType
from .models import UserProfile

def set_user_roles(request):
    """ Adds user role context variable to each template in the project """

    # defaults
    permissions = {
        "can_view_manager": False,
        "can_view_operator": False
    }

    if request.user.is_anonymous or request.user.userprofile.user_type == UserType.CUSTOMER:
        return permissions

    user_profile = request.user.userprofile
    if user_profile.user_type == UserType.OPERATOR:
        permissions['can_view_operator'] = True
        return permissions
    if user_profile.user_type == UserType.MANAGER:
        permissions['can_view_manager'] = True
        permissions['can_view_operator'] = True
        return permissions