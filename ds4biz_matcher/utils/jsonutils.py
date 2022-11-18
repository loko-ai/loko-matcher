from json import JSONEncoder


class GenericJsonEncoder(JSONEncoder):
    def __init__(self, include_class=False, **kwargs):
        JSONEncoder.__init__(self)
        self.include_class = include_class

    def default(self, o):
        if hasattr(o, "__dict__"):
            temp = dict(o.__dict__)
            if self.include_class:
                temp['__class__'] = type(o).__name__
            return temp
        elif hasattr(o, "tolist"):
            return o.tolist()
        else:
            return str(o)
