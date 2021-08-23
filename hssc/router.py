# 多数据库路由
# database router to multiple database by app label

class DatabaseRouter:
    route_app_labels = {'AppUseAnotherDatabase'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'dictionaries'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'dictionaries'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        dictionaries数据库中的表不允许migrate
        """
        if app_label in self.route_app_labels:
            return False
        return True