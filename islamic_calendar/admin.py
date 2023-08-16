from django.contrib import admin
from .models import IslamicEvent, EventDetail


class IslamicEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'hijri_date')

    def get_queryset(self, request):
        # Sort the events by year in descending order
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('-date__year')
        return queryset


class EventDetailInline(admin.StackedInline):
    model = EventDetail
    extra = 1


class EventDetailAdmin(admin.ModelAdmin):
    list_display = ('event', 'description')

    def get_queryset(self, request):
        # Sort the events by year in descending order
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('-event__date__year')
        return queryset


admin.site.register(IslamicEvent, IslamicEventAdmin)
admin.site.register(EventDetail, EventDetailAdmin)
