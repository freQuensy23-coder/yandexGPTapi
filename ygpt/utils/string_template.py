from typing import LiteralString


class StringTemplate(str):
    """String template class for string with partial format"""
    def format(self, **kwargs) -> LiteralString:
        for key in kwargs:
            if key not in self:
                raise KeyError(f'Key {key} not found in template')
            return self.replace('{' + key + '}', kwargs[key])
