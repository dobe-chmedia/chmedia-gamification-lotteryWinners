##**************************************************************************
##
## Description -------------------------------------------------------------
##
##**************************************************************************
##*
"""helper methods which two work with dto's\n
    
source: https://docs.airship.com/api/ua/
"""
##*
##* Modifications:
##* Date                User        Description
##* ------------------------------------------------------------------------
##* 2023-05-10          bettlerd    created script
##* 2023-05-26          bettlerd    added get_optional_value
##* 2023-05-31          bettlerd    simplified get_optional_value
##* 2023-05-31          bettlerd    added List support in create_dto_object()
##*
##*

import json
from typing import Any,Dict,Tuple,TypeVar, get_origin, get_args

from common.extensions.dto_extension import ExtendedDTO
from common.extensions.enum_extension import ExtendedEnum
from common.helper.regex_helper import find_pattern
from domain_objects.dto.big_query.config_variables.config_var_dto import ConfigVarDTO

T = TypeVar('T')

PATTERN_LIST = r"List\[[^\]]*\]"

#region create_dto_object
def create_dto_object(config_dto:ConfigVarDTO):
    """
    This function creates a DTO object from a ConfigVarDTO object.

    Parameters:
        - config_dto (ConfigVarDTO): The ConfigVarDTO object to create the DTO from

    Returns:
        - object: The DTO object created from the ConfigVarDTO object
    """
    is_list, class_name = __extract_dto_name(config_dto)
    import_string = __generate_import_string(config_dto.dto_path, class_name)
    
    exec(import_string)
    config_var_dto = locals()[class_name]

    if is_list:
        dto_object = [config_var_dto.from_dict(item) for item in json.loads(config_dto.value.replace("'","\""))]
    else:
        dto_object = config_var_dto.from_string(config_dto.value.replace("'","\""))
    return dto_object

def __extract_dto_name(config_dto:ConfigVarDTO) -> Tuple[bool, str]:
    dto_is_list = find_pattern(config_dto.dto_object, PATTERN_LIST)
    dto_name = config_dto.dto_object.replace("List[","").replace("]","")

    return dto_is_list, dto_name

def __generate_import_string(dto_path:str,
                             dto_name:str
                             ):
    """
    This function generates a string to be used as the argument to the exec() function in __create_dto_object().
    The string is an import statement that imports the DTO object specified in the ConfigVarDTO object.

    Parameters:
        - dto_path (str): The path of the DTO
        - dto_name (str): Name of the DTO

    Returns:
        - str: The import statement string
    """
    
    return f"from {dto_path} import {dto_name}"
#endregion

#region get_optional_value
def get_optional_value(obj: Dict[str, Any], key: str, value_type: type) -> T:
    """
    Retrieves an optional value from a dictionary and converts it to the specified type.

    Args:
        obj (Dict[str, Any]):
            The dictionary to retrieve the value from.

        key (str):
            The key to access the value.

        value_type (type):
            The desired type to convert the value to.

    Returns:
        Optional[T]:
            The converted value if it exists and is not None, otherwise None.

    Examples:
        >>> value1 = get_optional_value({"key": 123}, "key", int)
        >>> value1
        123

        >>> value2 = get_optional_value({"key": "hello"}, "key", str)
        >>> value2
        'hello'

        >>> value3 = get_optional_value({"other_key": True}, "key", bool)
        >>> value3
        None
    """

    if obj is None or key not in obj:
        return None

    obj_by_key = obj.get(key)
    if get_origin(value_type) is list:
    ## list cases:
        type_args = get_args(value_type)[0]
        if __check_if___int_str_float_bool(type_args):
            return [type_args(y) for y in obj_by_key]
        elif __check_if__enum(type_args):
            return [type_args.from_string(y) for y in obj_by_key]
        elif __check_if__dto(type_args):
            return [type_args.from_dict(y) for y in obj_by_key]
        else:
            __raise_type_error()
    else:
    ## scalar cases:
        if __check_if___int_str_float_bool(value_type):
           return value_type(obj_by_key)
        elif __check_if__enum(value_type):
            return value_type.from_string(obj_by_key)
        elif __check_if__dto(value_type):
            return value_type.from_dict(obj_by_key)
        else:
            __raise_type_error()

def __check_if___int_str_float_bool(type_args)->bool:
    if type(type_args) is type and type_args in (str, int, float, bool):
        return True
    return False

def __check_if__enum(type_args)->bool:
    if issubclass(type_args, ExtendedEnum):
        return True
    return False

def __check_if__dto(type_args)->bool:
    if issubclass(type_args, ExtendedDTO):
        return True
    return False

def __raise_type_error()->None:
    raise TypeError("This type has not yet been implemented!")
#endregion

if __name__ == "__main__":
    import json
    dto_string = json.loads("""
    {
        "DtoObject":"APIConfigsDTO",
        "DtoPath":"domain_objects.dto.common.api_config_dto",
        "Value":  "{\'ApiKey\': \'***secret KEY***\',\'AppSecret\':\'*** Secret ***\',\'Url\':\'go.airship.eu\',\'Version\':\'3\',\'Header\': {\'ContentType\':\'application/json\',\'Accept\':\'application/vnd.urbanairship+json; version=#VERSION#\'}}"
    }
    """)

    config_dto = ConfigVarDTO.from_dict(dto_string)

    dto = create_dto_object(config_dto)
    print(dto)