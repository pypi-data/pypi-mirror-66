from django.contrib import admin
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from sarscov2.admin import CoronaKapModelAdminMixin, fieldsets

from .forms import CoronavirusKapForm
from .models import CoronavirusKap

my_fieldsets = fieldsets.copy()
my_fieldsets.pop(0)


@admin.register(CoronavirusKap)
class CoronavirusKapAdmin(
    CoronaKapModelAdminMixin,
    FormLabelModelAdminMixin,
    FieldsetsModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = CoronavirusKapForm

    fieldsets = my_fieldsets
