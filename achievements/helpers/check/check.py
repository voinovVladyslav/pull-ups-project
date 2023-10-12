from user.models import User
from .pullup import check_pullup_achievements


def check_user_achievements(user: User) -> None:
    check_pullup_achievements(user)
