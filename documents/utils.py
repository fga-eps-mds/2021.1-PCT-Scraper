from datetime import datetime
from django.db.models import Q


def apply_all_filters(queryset, date_lte, date_gte,
                      source, category, keyword):
    queryset = filter_by_date(queryset, date_lte, date_gte)
    queryset = filter_by_source(queryset, source)
    queryset = filter_by_category(queryset, category)
    queryset = filter_by_keyword(queryset, keyword)

    return queryset


def filter_by_date(queryset, date_lte, date_gte):
    if date_lte is not None:
        queryset = queryset.filter(
            Q(updated_at__lte=convert_to_max_datetime(date_lte))
        )

    if date_gte is not None:
        queryset = queryset.filter(
            Q(updated_at__gte=convert_to_min_datetime(date_gte))
        )

    return queryset


def filter_by_source(queryset, source):
    if source is not None:
        queryset = queryset.filter(
            Q(source=source)
        )
    return queryset


def filter_by_category(queryset, category):
    if category is not None:
        queryset = queryset.filter(
            Q(classification=category)
        )
    return queryset


def filter_by_keyword(queryset, keyword):
    if keyword is not None:
        queryset = queryset.filter(
            Q(url__contains=keyword) |
            Q(slug__contains=keyword) |
            Q(title__contains=keyword) |
            Q(content__contains=keyword)
        )

    return queryset


def convert_to_max_datetime(date):
    # Converte um datetime para o maior
    # horario possivel do dia
    return datetime\
        .fromisoformat(date)\
        .replace(
            minute=59,
            hour=23,
            second=59,
            microsecond=999999
        )


def convert_to_min_datetime(date):
    # Converte um datetime para o menor
    # horario possivel do dia
    return datetime\
        .fromisoformat(date)\
        .replace(
            minute=0,
            hour=0,
            second=0,
            microsecond=0
        )
