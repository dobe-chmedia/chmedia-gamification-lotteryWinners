##**************************************************************************
##
## Description -------------------------------------------------------------
##
##**************************************************************************
##*
"""
DTO which stores the data of the table `chmedia-ent-regional.common.config_variables` 
in the column `value`.
"""
##*
##*
##* Modifications:
##* Date                User        Description
##* ------------------------------------------------------------------------
##* 2023-05-10          bettlerd    created script
##* 2023-05-10          bettlerd    added from_string
##*
##*

import json
from typing import Any
from dataclasses import dataclass

@dataclass
class ConfigVarDTO:
    dto_object: str
    dto_path: str
    value: str

    @staticmethod
    def from_dict(obj: Any) -> 'ConfigVarDTO':
        _dto_object = str(obj.get("DtoObject"))
        _dto_path = str(obj.get("DtoPath"))
        _value = str(obj.get("Value"))
        return ConfigVarDTO(_dto_object, _dto_path, _value)
    
    @staticmethod
    def from_string(string:str) -> 'ConfigVarDTO':
        json_obj = json.loads(string)
        return ConfigVarDTO.from_dict(json_obj)