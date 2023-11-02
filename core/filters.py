from admin_auto_filters.filters import AutocompleteFilter


class UserFilter(AutocompleteFilter):
    title = 'User'
    field_name = 'user'


class BarFilter(AutocompleteFilter):
    title = 'Pull Up Bar'
    field_name = 'bar'
