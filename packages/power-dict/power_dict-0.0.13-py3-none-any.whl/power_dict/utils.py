import datetime
from try_parse.utils import ParseUtils
from decimal import Decimal

from power_dict.errors import InvalidParameterError, NoneParameterError


class DictUtils:
    @staticmethod
    def get_value(properties: dict, key: str, **kwargs) -> object:
        """
        Get the dictionary value and cast it to type data_type
        :param properties: dict data
        :param key: key
        :return: data_type object
        """
        data_type, kwargs = DictUtils._InternalUtils.remove_key(kwargs, 'data_type', "str")

        map_func = {
            "object": DictUtils.get_dict_property,
            "str": DictUtils.get_str_dict_property,
            "int": DictUtils.get_int_dict_property,
            "datetime": DictUtils.get_datetime_dict_property,
            "date": DictUtils.get_date_dict_property,
            "bool": DictUtils.get_bool_dict_property,
            "decimal": DictUtils.get_decimal_dict_property,
            "list": DictUtils.get_list_dict_property,
            "float": DictUtils.get_float_dict_property
        }

        if data_type not in map_func:
            func = DictUtils.get_dict_property
        else:
            func = map_func[data_type]

        return func(properties, key, **kwargs)

    @staticmethod
    def get_required_value(properties: dict, key: str, **kwargs) -> object:
        """
        Get the required dictionary value and cast it to type data_type
        :param properties: dict data
        :param key: key
        :return: data_type object
        """
        data_type, kwargs = DictUtils._InternalUtils.remove_key(kwargs, 'data_type', "str")

        map_func = {
            "object": DictUtils.get_required_dict_property,
            "str": DictUtils.get_required_str_dict_property,
            "int": DictUtils.get_required_int_dict_property,
            "datetime": DictUtils.get_required_datetime_dict_property,
            "date": DictUtils.get_required_date_dict_property,
            "bool": DictUtils.get_required_bool_dict_property,
            "decimal": DictUtils.get_required_decimal_dict_property,
            "list": DictUtils.get_required_list_dict_property,
            "float": DictUtils.get_required_float_dict_property
        }

        if data_type not in map_func:
            func = DictUtils.get_required_dict_property
        else:
            func = map_func[data_type]

        return func(properties, key, **kwargs)

    @staticmethod
    def get_setting_by_path(properties: dict, path: str, **kwargs) -> object:
        """
        Get the dictionary value and cast it to type data_type by path
        :param properties: dict data
        :param path: key as full path
        :return: data_type object
        """
        if not DictUtils.str_is_null_or_empty(path) and properties is not None:
            separator, kwargs = DictUtils._InternalUtils.remove_key(kwargs, 'separator', ".")

            ps = path.split(separator)
            i = 0
            ps_len = len(ps)

            if ps_len > 0:
                for key in ps:
                    i = i + 1
                    if i == ps_len:
                        return DictUtils.get_value(properties, key, **kwargs)

                    properties = DictUtils.get_dict_property(properties, key)

        return None

    @staticmethod
    def get_dict_property(properties: dict, key: str, default_value=None) -> object:
        """
        Get the dictionary value
        :param properties: dict data
        :param key: key
        :param default_value: default value
        :return: object
        """
        if properties is None or DictUtils.str_is_null_or_empty(key):
            return default_value

        if key in properties:
            v = properties[key]
            if v is None:
                return default_value
            else:
                return v

        return default_value

    @staticmethod
    def get_required_dict_property(properties: dict, key: str, required_error=None) -> object:
        """
        Get the required dictionary value
        :param properties: dict data
        :param key: key
        :param required_error: error message if parameter is none
        :return: object
        """
        value = DictUtils.get_dict_property(properties, key)

        if value is not None:
            return value

        DictUtils.raise_none_parameter_error(key, required_error)

    @staticmethod
    def get_str_dict_property(properties: dict, key: str, default_value='') -> str:
        """
        Get the dictionary value and cast it to type 'str'
        :param properties: dict data
        :param key: key
        :param default_value: default value
        :return: str object
        """
        value = DictUtils.get_dict_property(properties, key)

        if DictUtils.str_is_null_or_empty(value):
            if default_value is None:
                return None
            value = default_value

        return str(value).strip()

    @staticmethod
    def get_required_str_dict_property(properties: dict, key: str, required_error=None) -> str:
        """
        Get the required dictionary value and cast it to type 'str'
        :param properties: dict data
        :param key: key
        :param required_error: error message if parameter is none
        :return: str object
        """
        value = DictUtils.get_required_dict_property(properties, key, required_error)
        value = str(value)

        if DictUtils.str_is_null_or_empty(value):
            DictUtils.raise_none_parameter_error(key, required_error)

        return value

    @staticmethod
    def get_int_dict_property(properties: dict, key: str, default_value=None) -> int:
        """
        Get the dictionary value and cast it to type 'int'
        :param properties: dict data
        :param key: key
        :param default_value: default value
        :return: int object
        """
        value = DictUtils.get_dict_property(properties, key)

        if DictUtils.str_is_null_or_empty(value):
            value = default_value

        status, result = ParseUtils.try_parse_int(value)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a number')

    @staticmethod
    def get_required_int_dict_property(properties: dict, key: str, required_error=None) -> int:
        """
        Get the required dictionary value and cast it to type 'int'
        :param properties: dict data
        :param key: key
        :param required_error: error message if parameter is none
        :return: int object
        """
        value = DictUtils.get_required_dict_property(properties, key, required_error)

        status, result = ParseUtils.try_parse_int(value)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a int')

    @staticmethod
    def get_datetime_dict_property(properties: dict, key: str, default_value: datetime = None,
                                   format: str = None) -> datetime:
        """
        Get the dictionary value and cast it to type 'datetime'
        :param format: date time format
        :param properties: dict data
        :param key: key
        :param default_value: default value
        :return: datetime object
        """
        value = DictUtils.get_dict_property(properties, key)

        if DictUtils.str_is_null_or_empty(value):
            value = default_value

        status, result = ParseUtils.try_parse_datetime(value, format=format)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a datetime')

    @staticmethod
    def get_required_datetime_dict_property(properties: dict, key: str, required_error=None,
                                            format: str = None) -> datetime:
        """
        Get the required dictionary value and cast it to type 'datetime'
        :param format: date time format
        :param properties: dict data
        :param key: key
        :param required_error: error message if parameter is none
        :return: datetime object
        """
        value = DictUtils.get_required_dict_property(properties, key, required_error)

        status, result = ParseUtils.try_parse_datetime(value, format=format)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a datetime')

    @staticmethod
    def get_date_dict_property(properties: dict, key: str, default_value=None, format: str = None) -> datetime.date:
        """
        Get the dictionary value and cast it to 'date'
        :param format: date format
        :param properties: dict data
        :param key: key
        :param default_value: default value
        :return: date object
        """
        value = DictUtils.get_dict_property(properties, key)

        if DictUtils.str_is_null_or_empty(value):
            value = default_value

        status, result = ParseUtils.try_parse_date(value, format=format)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a date')

    @staticmethod
    def get_required_date_dict_property(properties: dict, key: str, required_error=None,
                                        format: str = None) -> datetime.date:
        """
        Get the required dictionary value and cast it to 'date'
        :param format: date format
        :param properties: dict data
        :param key: key
        :param required_error: error message if parameter is none
        :return: date object
        """
        value = DictUtils.get_required_dict_property(properties, key, required_error)

        status, result = ParseUtils.try_parse_date(value, format=format)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a date')

    @staticmethod
    def get_bool_dict_property(properties: dict, key: str, default_value=None) -> bool:
        """
        Get the dictionary value and cast it to 'bool'
        :param properties: dict data
        :param key: key
        :param default_value: default value
        :return: bool object
        """
        value = DictUtils.get_dict_property(properties, key)

        if DictUtils.str_is_null_or_empty(value):
            value = default_value

        status, result = ParseUtils.try_parse_bool(value)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a bool')

    @staticmethod
    def get_required_bool_dict_property(properties: dict, key: str, required_error=None) -> bool:
        """
        Get the required dictionary value and cast it to 'bool'
        :param properties: dict data
        :param key: key
        :param required_error: error message if parameter is none
        :return: bool object
        """
        value = DictUtils.get_required_dict_property(properties, key, required_error)
        status, result = ParseUtils.try_parse_bool(value)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a bool')

    @staticmethod
    def get_decimal_dict_property(properties: dict, key: str, default_value=None) -> Decimal:
        """
        Get the dictionary value and cast it to 'decimal'
        :param properties: dict data
        :param key: key
        :param default_value: default value
        :return: decimal object
        """
        value = DictUtils.get_dict_property(properties, key)

        if DictUtils.str_is_null_or_empty(value):
            value = default_value

        status, result = ParseUtils.try_parse_decimal(value)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a decimal')

    @staticmethod
    def get_required_decimal_dict_property(properties: dict, key: str, required_error=None) -> Decimal:
        """
        Get the required dictionary value and cast it to 'decimal'
        :param properties: dict data
        :param key: key
        :param required_error: error message if parameter is none
        :return: decimal object
        """
        value = DictUtils.get_required_dict_property(properties, key, required_error)

        status, result = ParseUtils.try_parse_decimal(value)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a decimal')

    @staticmethod
    def get_list_dict_property(properties: dict, key: str, default_value=None) -> list:
        """
        Get the dictionary value and cast it to 'list'
        :param properties: dict data
        :param key: key
        :param default_value: default value
        :return: list object
        """
        v = DictUtils.get_dict_property(properties, key)
        if v is None:
            return default_value
        else:
            return list(v)

    @staticmethod
    def get_required_list_dict_property(properties: dict, key: str, required_error=None) -> list:
        """
        Get the required dictionary value and cast it to 'list'
        :param properties: dict data
        :param key: key
        :param required_error: error message if parameter is none
        :return: list object
        """
        required_object = DictUtils.get_required_dict_property(properties, key, required_error)

        return list(required_object)

    @staticmethod
    def get_float_dict_property(properties: dict, key: str, default_value=None) -> float:
        """
        Get the dictionary value and cast it to 'float'
        :param properties: dict data
        :param key: key
        :param default_value: default value
        :return: float object
        """
        value = DictUtils.get_dict_property(properties, key)

        if DictUtils.str_is_null_or_empty(value):
            value = default_value

        status, result = ParseUtils.try_parse_float(value)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a float')

    @staticmethod
    def get_required_float_dict_property(properties: dict, key: str, required_error=None) -> float:
        """
        Get the required dictionary value and cast it to 'float'
        :param properties: dict data
        :param key: key
        :param required_error: error message if parameter is none
        :return: float object
        """
        value = DictUtils.get_required_dict_property(properties, key, required_error)

        status, result = ParseUtils.try_parse_float(value)
        if status:
            return result
        else:
            raise InvalidParameterError(f'Parameter "{key}" could not be converted to a float')

    @staticmethod
    def str_is_null_or_empty(text) -> bool:
        """
        String is null or empty?
        :param text: string
        :return: status
        """
        return text is None or not str(text).strip()

    @staticmethod
    def raise_none_parameter_error(key=None, error=None):
        """
        Raise 'NoneParameterError'
        :param key: key
        :param error: error message
        :return:
        """
        if error is not None:
            message = error
        elif key is not None:
            message = f'Parameter "{key}" is none'
        else:
            message = 'No parameter specified'

        raise NoneParameterError(message)

    class _InternalUtils:
        @staticmethod
        def remove_key(kwargs, key, default_value):
            if key not in kwargs or kwargs[key] is None:
                value = default_value
            else:
                value = kwargs[key]
                del kwargs[key]

            return value, kwargs
