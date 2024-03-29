from user.models import User
from .pullup import check_pullup_achievements
from .totalpullup import check_totalpullup_achievements
from .diff import check_diff_achievements
from .totaldiff import check_totaldiff_achievements
from .row import check_row_achievements


def check_user_achievements(user: User) -> None:
    check_pullup_achievements(user)
    check_totalpullup_achievements(user)
    check_diff_achievements(user)
    check_totaldiff_achievements(user)
    check_row_achievements(user)
