from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter
from .models import Announcement


class AnnouncementFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='time_add',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Announcement
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'head': ['icontains'],
            # поиск по категории
            'categoryType': ['exact'],
        }
