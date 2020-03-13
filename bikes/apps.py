from django.apps import AppConfig


class BikesConfig(AppConfig):
    name = 'bikes'
    
    def ready(self):
        import bikes.signals
