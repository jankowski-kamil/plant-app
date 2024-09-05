from django_filters import rest_framework as filter


class RankingFilters(filter.FilterSet):
    total_litres = filter.NumberFilter(field_name="total_litres", label="Total Litres")
    count_waterings = filter.NumberFilter(
        field_name="count_waterings",
        label="Count Waterings",
    )
