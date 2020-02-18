from django.apps import AppConfig


class LoginregistrationConfig(AppConfig):
    name = 'Loginregistration'

    def ready(self):
        import Loginregistration.signals
