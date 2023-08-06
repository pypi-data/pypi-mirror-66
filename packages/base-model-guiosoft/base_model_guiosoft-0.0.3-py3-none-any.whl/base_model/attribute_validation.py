from datetime import datetime, date, time

from dateutil.parser import parse

from base_model.tools import get_class_name, parse_quotes
from logging import getLogger


class AttributeValidation:
    DATE_FORMATS = [
        '%Y-%m-%d',
        '%d/%m/%Y'
    ]
    DATETIME_FORMATS = [
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S.%f%z',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S.%f%z',
        '%d/%m/%Y %H:%M:%S'
    ]

    TIME_FORMATS = [
        '%H:%M:%S',
        '%H:%M',
        '%H:%M:%S.%f'
    ]

    def __init__(self, model_class, attribute_name: str,
                 attribute_type, aggregator_type=None, aggregate_type=None):
        self._model_class = model_class
        self._attribute = attribute_name
        self._type = attribute_type
        self._required = False
        self._extra = None
        self._default = lambda instance: None
        self._aggregator_type = aggregator_type
        self._aggregate_type = aggregate_type
        if self._aggregator_type:
            self._default = self.get_aggregator_default_method(
                self._aggregator_type)

        self._logger = getLogger(__file__)

    @property
    def is_required(self):
        return self._required

    @property
    def is_aggregate(self):
        return self._aggregator_type is not None

    def set_extra_validations(self, extra):
        """
        Extra validations must be space delimited

        required
        default=expression
        """
        for validation in parse_quotes(extra):
            if validation.upper() == 'REQUIRED':
                self._required = True
            elif validation.upper().startswith('DEFAULT='):
                self.set_default(validation.split('=')[1])

        return True

    def set_default(self, default_expression):
        """
        Set default value for reset or init


        """
        if default_expression is None or default_expression == "None":
            self._default = lambda instance: None
            return

        if "self." in default_expression:
            self._default = eval(
                "lambda instance: instance" + default_expression[4:])
        elif default_expression == "MIN_TIMESTAMP":
            if self._type == datetime:
                self._default = lambda instance: datetime(
                    1970, 1, 1, 0, 0, 0, 0)
            elif self._type == date:
                self._default = lambda instance: date(1970, 1, 1)
        else:
            self._default = eval("lambda instance: " + default_expression)

    def get_default(self, model_instance):
        return self._default(model_instance)

    def normalize_data(self, value, _type=None, _aggregate_type=None):
        """
        Normalize data

        :param value: original value received
        :param _type: type for convert data (default = self._type)
        :param _aggregate_type:
        :returns: (bool success, object converted value)
        """
        if _type is None:
            _type = self._type
            _aggregate_type = self._aggregate_type

        if isinstance(value, self._type):
            return True, value
        if value is None:
            return not self.is_required, value

        if _type == date:
            success, value = self._normalize_date(value)
        elif _type == datetime:
            success, value = self._normalize_datetime(value)
        elif _type == time:
            success, value = self._normalize_time(value)
        elif _type == bool:
            success, value = self._normalize_bool(value)
        elif _aggregate_type:
            success, value = self._normalize_aggregator(value, _aggregate_type)
        elif value is not None:
            try:
                value = _type(value)
                success = True
            except Exception as exc:
                self._logger.debug(
                    'BASE_MODEL.AttributeValidation %s.%s %s(%s) %s',
                    self._model_class,
                    self._attribute,
                    _type,
                    value,
                    str(exc))
                success = False
        elif self.is_required:
            success = False
        else:
            success = True

        return success, value

    def _normalize_bool(self, value) -> bool:
        try:
            return True, str(value).upper() in ['TRUE', 'T', 'Y', '1']
        except Exception as exc:
            self._logger.debug(
                'BASE_MODEL.AttributeValidation '
                '_normalize_bool %s.%s %s',
                self._model_class,
                self._attribute,
                str(exc))
            return False, None

    def _normalize_date(self, value) -> date:
        for format in self.DATE_FORMATS:
            try:
                _date = datetime.strptime(value, format)
                return True, _date.date()
            except Exception as exc:
                # try another
                self._logger.debug(
                    'BASE_MODEL.AttributeValidation '
                    '_normalize_date %s.%s %s',
                    self._model_class,
                    self._attribute,
                    str(exc))

        try:
            _date = parse(value)
            return True, _date.date()
        except Exception as exc:
            self._logger.debug(
                'BASE_MODEL.AttributeValidation '
                '_normalize_date %s.%s %s',
                self._model_class,
                self._attribute,
                str(exc))
            return False, None

    def _normalize_datetime(self, value):
        for format in self.DATETIME_FORMATS:
            try:
                _date = datetime.strptime(value, format)
                return True, _date
            except Exception as exc:
                # try another
                self._logger.debug(
                    'BASE_MODEL.AttributeValidation '
                    '_normalize_datetime %s.%s %s',
                    self._model_class,
                    self._attribute,
                    str(exc))
        try:
            _date = parse(value)
            return True, _date
        except Exception as exc:
            self._logger.debug(
                'BASE_MODEL.AttributeValidation '
                '_normalize_datetime %s.%s %s',
                self._model_class,
                self._attribute,
                str(exc))
            return False, None

    def _normalize_time(self, value):
        for format in self.TIME_FORMATS:
            try:
                _time = datetime.strptime(value, format)
                return True, _time.time()
            except Exception as exc:
                # try another
                self._logger.debug(
                    'BASE_MODEL.AttributeValidation '
                    '_normalize_time %s.%s %s',
                    self._model_class,
                    self._attribute,
                    str(exc))

        try:
            _time = parse(value)
            return True, _time.time()
        except Exception as exc:
            self._logger.debug(
                'BASE_MODEL.AttributeValidation '
                '_normalize_time %s.%s %s',
                self._model_class,
                self._attribute,
                str(exc))
            return False, None

    def normalize_aggregator(self, model_instance,
                             value, _aggregator_type=None):
        if value is None:
            return True, self.get_default(model_instance)
        if _aggregator_type is None:
            _aggregator_type = self.get_aggregator_type(self._aggregator_type)

        if _aggregator_type == list:
            return self._normalize_aggregator_list(model_instance, value)
        elif _aggregator_type == dict:
            return self._normalize_aggregator_dict(model_instance, value)
        # elif _aggregator_type == set:
        #     return self._normalize_aggregator_set(model_instance, value)
        # elif _aggregator_type == tuple:
        #     return self._normalize_aggregator_tuple(model_instance, value)

        return False, None

    def _normalize_aggregator_list(self, model_instance, value):
        if not isinstance(value, list):
            value = [value]

        try:
            normalized_values = []
            for v in value:
                success, data = self.normalize_data(v, self._aggregate_type)
                normalized_values.append(None if not success else data)

            return True, normalized_values
        except Exception as exc:
            self._logger.debug(
                'BASE_MODEL.AttributeValidation '
                '_normalize_aggregator_dict %s.%s %s',
                self._model_class,
                self._attribute,
                str(exc))
            return False, None

    def _normalize_aggregator_dict(self, model_instance, value):
        if not isinstance(value, dict):
            return False, None

        try:
            normalized_values = dict()
            for key in value:
                v = value[key]
                success, key = self.normalize_data(
                    key, self._aggregate_type[0])
                if success:
                    success, data = self.normalize_data(
                        v, self._aggregate_type[1])
                    normalized_values[key] = None if not success else data
                if not success:
                    return False, None
            return True, normalized_values
        except Exception as exc:
            self._logger.debug(
                'BASE_MODEL.AttributeValidation '
                '_normalize_aggregator_dict %s.%s %s',
                self._model_class,
                self._attribute,
                str(exc))
            return False, None

    def _normalize_aggregator_set(self, model_instance, value):
        raise NotImplementedError()

    def _normalize_aggregator_tuple(self, model_instance, value):
        raise NotImplementedError()

    @staticmethod
    def get_aggregator_type(aggregator):
        if aggregator in [list, dict, set, tuple]:
            return aggregator

        return None

    @staticmethod
    def get_aggregator_default_method(aggregator):

        if aggregator == list:
            return lambda instance: list()
        elif aggregator == dict:
            return lambda instance: dict()
        elif aggregator == set:
            return lambda instance: set()
        elif aggregator == tuple:
            return lambda instance: tuple()

        return lambda instance: None

    def __str__(self):
        return "{0}.{1}:{2} ({3})".format(
            get_class_name(self._model_class),
            self._attribute,
            str(self._type),
            self._extra)

    def __repr__(self):
        return str(self)
