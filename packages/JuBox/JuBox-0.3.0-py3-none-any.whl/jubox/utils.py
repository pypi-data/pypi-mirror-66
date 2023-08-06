

def inplace(content_attr):

    def decorator(func):
        def wrapper(self, *args, inplace=False, **kwargs):
            attr_value = getattr(self, content_attr)
            data = copy.deepcopy(attr_value) if not inplace else attr_value
            func(self, *args, **kwargs)
            if not inplace:
                return data
        return wrapper
    return decorator