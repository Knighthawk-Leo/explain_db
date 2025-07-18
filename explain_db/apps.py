from django.apps import AppConfig


class ExplainDbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'explain_db'
    verbose_name = 'Explain DB'
    
    def ready(self):
        """
        Called when the app is ready.
        This is where you can perform any app-specific initialization.
        """
        pass 