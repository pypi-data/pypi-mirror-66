# from celery import Celery
from typing import Tuple, Any

class Celery:
    @property
    def conf(self): ...
    @conf.setter
    def conf(self, d): ...
    def task(self, *args, **opts): ...
    def send_task(
        self,
        name,
        args: Tuple[Any, ...] = None,
        kwargs=None,
        countdown=None,
        eta=None,
        task_id=None,
        producer=None,
        connection=None,
        router=None,
        result_cls=None,
        expires=None,
        publisher=None,
        link=None,
        link_error=None,
        add_to_parent=True,
        group_id=None,
        retries=0,
        chord=None,
        reply_to=None,
        time_limit=None,
        soft_time_limit=None,
        root_id=None,
        parent_id=None,
        route_name=None,
        shadow=None,
        chain=None,
        task_type=None,
        **options,
    ): ...
