from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketplace'
    
    def ready(self):
        """Import signals when app is ready"""
        import marketplace.signals
        from marketplace.twitter_service import twitter_service
