# from celery.schedules import crontab

class crontab:
    def __init__(
        self,
        minute="*",
        hour="*",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
        **kwargs,
    ): ...
