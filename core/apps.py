from django.apps import AppConfig



class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # 启动应用后导入业务调度器: scheduler
        import core.scheduler
