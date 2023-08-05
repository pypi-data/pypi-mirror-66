class Registry(object):
    def __init__(self):
        self._registry = {}
        self._registry_models = {}
        self._registry_composites = {}

    def register(self, cls):
        from .types import PynamoObjectType
        assert issubclass(
            cls, PynamoObjectType), 'Only PynamoObjectType can be registered, received "{}"'.format(
            cls.__name__)
        assert cls._meta.registry == self, 'Registry for a Model have to match.'
        # assert self.get_type_for_model(cls._meta.model) in [None, cls], (
        #     'SQLAlchemy model "{}" already associated with '
        #     'another type "{}".'
        # ).format(cls._meta.model, self._registry[cls._meta.model])
        self._registry[cls._meta.model] = cls

    def get_type_for_model(self, model):
        return self._registry.get(model)


registry = None


def get_global_registry():
    global registry
    if not registry:
        registry = Registry()
    return registry
