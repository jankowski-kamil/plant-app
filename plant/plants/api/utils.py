from django.db.models import Func


class Interval(Func):
    function = "INTERVAL"
    template = "(%(expressions)s * %(function)s '1' DAY)"