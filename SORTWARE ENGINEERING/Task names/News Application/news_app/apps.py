from django.apps import AppConfig


class NewsAppConfig(AppConfig):
    '''
    Configuration for the news_app application.
    Registers signal handlers when the app is ready.
    '''
    name = 'news_app'
    default_auto_field = 'django.db.models.BigAutoField'
    
    def ready(self):
        '''
        Import signal handlers when app is ready.
        This ensures signals are registered and will fire appropriately.
        '''
        import news_app.signals

