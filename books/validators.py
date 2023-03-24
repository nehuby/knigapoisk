from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validator(date_release: int) -> None:
    year = datetime.today().year
    if date_release > year:
        raise ValidationError(
            _("The year of publication cannot be greater than the current")
        )
    elif date_release < year - 300:
        raise ValidationError(_("The year of publication cannot be that old"))
