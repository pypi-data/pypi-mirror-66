from .utils import string, integer, list_, dict_


class Table:
    @classmethod
    def get_types(cls):
        vars_ = {}
        for k, i in vars(cls).items():
            if not k.startswith('__'):
                vars_[k] = i
        return vars_

    @classmethod
    def get_fields(cls):
        fields = [i for i in cls.get_types().keys()]
        fields.remove('id')
        return fields
