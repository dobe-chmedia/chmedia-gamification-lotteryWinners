##**************************************************************************
##
## Description -------------------------------------------------------------
##
##**************************************************************************
##*
"""
DTO which contains general API attributes.
"""
##*
##*
##* Modifications:
##* Date                User        Description
##* ------------------------------------------------------------------------
##* 2023-05-08          bettlerd    created script
##* 2023-05-08          bettlerd    added header
##* 2023-05-10          bettlerd    added from_string()
##* 2023-07-13          bettlerd    added scope, added get_optional_value
##* 2023-07-13          bettlerd    added ExtendedDTO
##* 2023-07-13          bettlerd    added expiration_time
##* 2023-08-08          bettlerd    added Id
##* 2023-08-08          bettlerd    added get_value()
##*
##*

import json
from dataclasses import dataclass
from typing import Any,List,Optional

from common.extensions.dto_extension import ExtendedDTO
from common.helper.dto_helper import get_optional_value

@dataclass
class Header(ExtendedDTO):
    content_type: Optional[str] = None
    accept: Optional[str] = None
    range: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Header':
        _content_type = get_optional_value(obj, "ContentType", str)
        _accept = get_optional_value(obj, "Accept", str)
        _range = get_optional_value(obj, "Range", str)
        return Header(_content_type, _accept, _range)
    
@dataclass
class Id(ExtendedDTO):
    name: Optional[str] = None
    value: Optional[str] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Id':
        _name = get_optional_value(obj, "name", str)
        _value = get_optional_value(obj, "value", str)
        _type = get_optional_value(obj, "type", str)
        return Id(_name,_value, _type)
    
    def get_value(self)->Any:
        return eval(f"{self.type}('{self.value}')")

@dataclass
class Settings(ExtendedDTO):
    ids: Optional[List[Id]] = None
    expiration_time: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Settings':
        _ids = get_optional_value(obj, "Ids", List[Id])
        _expiration_time = get_optional_value(obj, "ExpirationTime", int)
        return Settings(_ids,_expiration_time)

@dataclass
class APIConfigsDTO(ExtendedDTO):
    api_key: Optional[str] = None
    app_secret: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None
    header:Optional[Header] = None
    scope:Optional[List[str]] = None
    settings:Optional[Settings] = None

    @staticmethod
    def from_dict(obj: Any) -> 'APIConfigsDTO':
        _api_key = get_optional_value(obj, "ApiKey", str)
        _app_secret = get_optional_value(obj, "AppSecret", str)
        _url = get_optional_value(obj, "Url", str)
        _version = get_optional_value(obj, "Version", str)
        _header = get_optional_value(obj, "Header", Header)
        _scope = get_optional_value(obj, "scope", List[str])
        _settings = get_optional_value(obj, "Settings", Settings)
        return APIConfigsDTO(
            api_key = _api_key, 
            app_secret = _app_secret, 
            url = _url, 
            version = _version, 
            header = _header, 
            scope = _scope, 
            settings = _settings)
    
    @staticmethod
    def from_string(string:str) -> 'APIConfigsDTO':
        json_obj = json.loads(string)
        return APIConfigsDTO.from_dict(json_obj)