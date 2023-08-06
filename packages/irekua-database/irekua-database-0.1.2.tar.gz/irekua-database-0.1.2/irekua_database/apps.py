from django.apps import AppConfig


class IrekuaDatabaseConfig(AppConfig):
    name = 'irekua_database'
    verbose_name = 'irekua-database'

    def ready(self):
        # import irekua_database.signals
        pass
