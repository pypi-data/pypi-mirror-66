from base_model.attribute_validation import AttributeValidation
from base_model.base_model_exception import BaseModelException
from base_model.base_model_validation import BaseModelValidation
from base_model.json import dumps, loads
from base_model.not_found_attribute import NotFoundAttribute
from base_model.tools import get_class_name


class BaseModel:

    def __init__(self, from_object=None):
        self._validations: BaseModelValidation = \
            BaseModelValidation.get_validation(self.__class__)
        if from_object:
            self.load_from_object(from_object)
        else:
            self.clear()

    def clear(self):
        """
        Reset fields
        """
        for field_name in self._validations.get_fields():
            setattr(self,
                    field_name,
                    self._validations.get_field_default_value(field_name, self)
                    )

    def to_dict(self):
        result = {
            field_name: self.get_attribute_value(field_name)
            for field_name in self._validations.get_fields()
        }
        return result

    def to_json(self):
        return dumps(self.to_dict(), default=str)

    def get_attribute_value(self, field_name):
        attr_validation: AttributeValidation = \
            self._validations.get_attribute_validation(field_name)
        field_value = getattr(self, field_name, NotFoundAttribute())

        if isinstance(field_value, NotFoundAttribute):
            if attr_validation:
                field_value = attr_validation.get_default(self)
            else:
                field_value = None

        return field_value

    def load_from_object(self, from_object):
        if isinstance(from_object, str):
            from_object = self.validate_from_str(from_object)

        not_found_attributes = set()
        normalization_error_attributes = []
        for field_name in self._validations.get_fields():
            field_value = self._get_attribute_value(from_object, field_name)
            attr_validation: AttributeValidation = \
                self._validations.get_attribute_validation(field_name)
            required_field = attr_validation and attr_validation.is_required
            if required_field and \
                    (field_value is None or
                        isinstance(field_value, NotFoundAttribute)):
                not_found_attributes.add(field_name)
                continue

            if isinstance(field_value, NotFoundAttribute):
                if attr_validation:
                    field_value = attr_validation.get_default(self)
                else:
                    field_value = None

            if attr_validation.is_aggregate:
                if field_value is None:
                    success = True
                    field_value = attr_validation.get_default(self)
                else:
                    success, field_value = \
                        attr_validation.normalize_aggregator(
                            self, field_value)

            else:
                success, field_value = attr_validation.normalize_data(
                    field_value)
            if not success:
                normalization_error_attributes.append(field_name)
            else:
                setattr(self, field_name, field_value)

        if len(not_found_attributes) > 0:
            raise BaseModelException(
                "Missing required attributes '{0}' for model {1}".format(
                    not_found_attributes, get_class_name(self.__class__)
                ))

        if len(normalization_error_attributes) > 0:
            raise BaseModelException(
                "Normalization error on attributes '{0}' for model {1}".format(
                    normalization_error_attributes, get_class_name(
                        self.__class__)
                ))
        return True

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

    @staticmethod
    def _get_attribute_value(from_object: object, field_name: object) \
            -> object:
        result = NotFoundAttribute()
        if isinstance(from_object, dict):
            if field_name in from_object:
                result = from_object[field_name]
        else:
            result = getattr(from_object, field_name, NotFoundAttribute())

        return result
