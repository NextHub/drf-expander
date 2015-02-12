from django.utils.translation import ugettext_lazy as _
from rest_framework import status

from rest_framework.exceptions import APIException


class ExpanderException(APIException):
    pass


class ExpanderAdapterMissing(ExpanderException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("No such adapter.")


class ExpanderDepthBreached(ExpanderException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Expander depth breached.")


class ExpanderFieldMissing(ExpanderException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Expander field missing.")
