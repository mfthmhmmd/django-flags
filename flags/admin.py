from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from flags.forms import FlagConditionForm
from flags.middleware import FlagConditionsMiddleware
from flags.models import FlagCondition
from flags.sources import get_flags


class FlagsChangeList(ChangeList):
    """
    This is a proxy-ChangeList that behaves like a ChangeList but is
    really multiple ChangeList objects — one per feature flag.
    """

    def __init__(self, request, *args, **kwargs):
        super(FlagsChangeList, self).__init__(request, *args, **kwargs)

        if hasattr(request, FlagConditionsMiddleware.request_attribute):
            flags = getattr(
                request, FlagConditionsMiddleware.request_attribute
            )
        else:
            flags = get_flags()

        self.flags = [
            (
                flag,
                self.get_changelist_for_flag(flag, request, *args, **kwargs)
            )
            for flag in flags.values()
        ]

    def get_changelist_for_flag(self, flag, request, *args, **kwargs):
        cl = ChangeList(request, *args, **kwargs)
        # Filter the ChangeList's queryset on the flag name
        # cl.root_queryset = cl.root_queryset.filter(name=flag.name)
        return cl


class FlagsAdmin(admin.ModelAdmin):
    form = FlagConditionForm
    change_list_template = 'flags/admin/change_list.html'

    def get_changelist(self, request, **kwargs):
        return FlagsChangeList


admin.site.register(FlagCondition, FlagsAdmin)
