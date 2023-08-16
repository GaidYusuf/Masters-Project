from django.shortcuts import render, get_object_or_404
from .models import IslamicEvent, EventDetail
from django.utils import timezone


def islamic_calendar(request, year=None):
    if year is None:
        year = timezone.now().year

    distinct_years = IslamicEvent.objects.filter(
        date__year__gte=timezone.now().year).values('date__year').distinct()

    upcoming_events = IslamicEvent.objects.filter(
        date__year=year).order_by('date')

    return render(request, 'islamic_calendar/islamic_calendar.html', {
        'upcoming_events': upcoming_events,
        'selected_year': year,
        'distinct_years': distinct_years
    })


def islamic_calendar_year(request, year):
    distinct_years = IslamicEvent.objects.filter(
        date__gte=timezone.now()).values('date__year').distinct()
    upcoming_events = IslamicEvent.objects.filter(
        date__year=year, date__gte=timezone.now()).order_by('date')
    return render(request, 'islamic_calendar/islamic_calendar.html', {'upcoming_events': upcoming_events, 'selected_year': year, 'distinct_years': distinct_years})


def event_detail(request, event_id):
    event = get_object_or_404(IslamicEvent, id=event_id)
    event_detail = EventDetail.objects.filter(event__name=event.name).first()
    return render(request, 'islamic_calendar/event_detail.html', {'event': event, 'event_detail': event_detail})
