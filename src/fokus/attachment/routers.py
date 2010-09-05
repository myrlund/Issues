
class ResourceRouter:
    db = 'resources'
    
    def instance_check(self, model):
        if model.__name__ == "URLResource":
            return self.db
        return None
    
    def db_for_read(self, model, **hints):
        return self.instance_check(model)
    
    def db_for_write(self, model, **hints):
        return self.instance_check(model)
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_syncdb(self, db, model):
        if self.db == db:
            return bool(self.instance_check(model))
        return None
