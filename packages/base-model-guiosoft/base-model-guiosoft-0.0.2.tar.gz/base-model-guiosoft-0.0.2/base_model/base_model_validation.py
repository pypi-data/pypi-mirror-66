import inspect
import typing

from base_model.attribute_validation import AttributeValidation
from base_model.base_model_exception import BaseModelException
from base_model.tools import get_class_name


class BaseModelValidation:
    VALIDATIONS = {}

    def __init__(self, model_class):

        self._class_name = get_class_name(model_class)
        self._model_class = model_class
        _members = typing.get_type_hints(model_class)
        if not _members:
            raise BaseModelException(
                f"Class {self._class_name} has no typed declared members")

        _validations = {}

        for member in _members:
            _member_type = _members[member]

            _aggregator_type, _aggregate_type = self._get_aggregator(
                member, _member_type)

            if _aggregator_type:
                _member_type = _aggregator_type

            _validations[member] = AttributeValidation(
                model_class=model_class.__class__,
                attribute_name=member,
                attribute_type=_member_type,
                aggregator_type=_aggregator_type,
                aggregate_type=_aggregate_type)

        self._attributes_validations = _validations
        self._get_extra_validations()
        self._members = _members

    def get_attribute_validation(self, field_name):
        if field_name in self._attributes_validations:
            return self._attributes_validations[field_name]
        return None

    def __str__(self):
        return "Validation {0}: {1}".format(
            self._class_name,
            self._attributes_validations
        )

    def get_fields(self) -> list:
        """
        Returns list of field names
        """
        return [member for member in self._members]

    def get_field_type(self, field_name):
        if field_name not in self._members:
            raise BaseModelException("Field name {0} not found in model {1}".
                                     format(
                                         field_name,
                                         self._class_name))

        return self._members[field_name]

    def get_field_default_value(self, field_name, model_instance):
        if field_name in self._members:
            validation: AttributeValidation = \
                self._attributes_validations[field_name]
            return validation.get_default(model_instance)
        return None

    @classmethod
    def get_validation(cls, model_class):
        cn = get_class_name(model_class)
        if cn not in cls.VALIDATIONS:
            validation = BaseModelValidation(model_class)
            cls.VALIDATIONS[cn] = validation

        return cls.VALIDATIONS[cn]

    def _get_extra_validations(self):
        _docs = inspect.getdoc(self._model_class)
        if not isinstance(_docs, str):
            return
        for doc in _docs.splitlines():
            details = doc.strip().split(':')
            if len(details) > 1:
                attr_name = details[0].strip()
                if attr_name in self._attributes_validations:
                    attr_props = ' '.join([d.strip() for d in details[1:]])
                    self._attributes_validations[attr_name].\
                        set_extra_validations(attr_props)

    def _get_aggregator(self, field_name, member_type):

        if not getattr(member_type, '__args__', None):
            return None, None

        _aggregator_type, _aggregate_type = None, None
        str_mt = str(member_type)
        if str_mt.startswith('typing.List'):
            _aggregator_type = list
            if len(member_type.__args__) > 0:
                _aggregate_type = member_type.__args__[0]
        elif str_mt.startswith('typing.Dict'):
            _aggregator_type = dict
        elif str_mt.startswith('typing.Set'):
            _aggregator_type = set
        elif str_mt.startswith('typing.Tuple'):
            _aggregator_type = tuple

        if _aggregator_type:
            if not _aggregate_type:
                _aggregate_type = member_type.__args__

        else:
            raise BaseModelException(
                "Invalid type hint {0} for field {1} of model {2}".format(
                    member_type,
                    field_name,
                    self._class_name
                ))
        return _aggregator_type, _aggregate_type
