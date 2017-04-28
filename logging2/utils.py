class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance
        return cls._instance
