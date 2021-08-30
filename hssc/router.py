# 多数据库路由
# database router to multiple database by app label

class DatabaseRouter:
    route_app_labels = {'rcms'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'rcms'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'rcms'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        rcms数据库中的表不允许migrate
        """
        if app_label in self.route_app_labels:
            return False
        return True