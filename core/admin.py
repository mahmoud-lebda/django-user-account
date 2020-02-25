from django.contrib import admin
from .models import Governorate, City


class Cities(admin.TabularInline):
    model = City
    template = 'admin/edit_inline/tabular.html'


@admin.register(Governorate)
class GovernorateAdmin(admin.ModelAdmin):
    inlines = [
        Cities,
    ]
