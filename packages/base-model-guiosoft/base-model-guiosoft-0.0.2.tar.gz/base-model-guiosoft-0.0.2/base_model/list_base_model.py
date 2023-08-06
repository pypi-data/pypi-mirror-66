from base_model.base_model_exception import BaseModelException
from base_model.json import dumps, loads
from base_model.tools import get_class_name


class ListBaseModel:

    def __init__(self, base_model_class, from_object=None):
        if not isinstance(base_model_class, type):
            raise BaseModelException(
                'base_model_class expected to be a type ({0})'
                .format(base_model_class))
        self._items = []
        self._base_model_class = base_model_class
        if from_object:
            self.load_from_object(from_object)

    def __iter__(self):
        return self._items

    def to_list(self, internal_conversion: bool = False):
        """ Returns a list of data

        :param internal_conversion: Parses objects, to primitive types
        """
        return [
            item.to_dict()
            if internal_conversion and hasattr(item, 'to_dict') else
            item.to_list(internal_conversion)
            if internal_conversion and hasattr(item, 'to_list') else
            item for item in self._items]

    def to_json(self):
        return dumps(self.to_list(True))

    def validate_from_str(self, from_object):
        """
        Parse object from json string
        """
        try:
            from_object = loads(from_object)

        except Exception as exc:
            raise BaseModelException(
                "Error on parsing JSON content for model {0}: {1}".format(
                    get_class_name(self.__class__),
                    str(exc)
                ))
        return from_object

    def load_from_object(self, from_object):
        if isinstance(from_object, str):
            from_object = self.validate_from_str(from_object)

        if not isinstance(from_object, list):
            from_object = [from_object]

        self._items = [self._base_model_class(item) for item in from_object]

    def __len__(self):
        return len(self._items)

    def __getitem__(self, key):
        if isinstance(key, int) and 0 <= key < len(self._items):
            return self._items[key]
        raise KeyError(key)
