from django.contrib import admin

from flags.forms import FlagConditionForm
from flags.models import FlagCondition


class FlagsAdmin(admin.ModelAdmin):
    form = FlagConditionForm


admin.site.register(FlagState, FlagStateAdmin)
admin.site.register(FlagCondition, FlagsAdmin)
