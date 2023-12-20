##**************************************************************************
##
## Description -------------------------------------------------------------
##
##**************************************************************************
##*
"""DTO extension which adds method(s)
         - to_dict()
         - get_object_by_name()
"""
##*
##* Modifications:
##* Date                User        Description
##* ------------------------------------------------------------------------
##* 2023-05-23          bettlerd    created script
##* 2023-08-08          bettlerd    added get_object_by_name()
##*
##*

from typing import Optional, List, TypeVar
from enum import Enum

T = TypeVar("T")

class ExtendedDTO():
    """
    Extends the DTO with some methods.
    """

    def to_dict(self):
        """
        Converts the DTO object to a dictionary.

        Returns:
            dict: A dictionary representation of the object.
        """
        result = {}
        
        for key, value in self.__dict__.items():
            value = self.__transform_value(value)

            if value is not None:
                if isinstance(value, list):
                    result[key] = [item.to_dict() for item in value]
                elif isinstance(value, Enum):
                    result[key] = value.value
                elif isinstance(value, ExtendedDTO):
                    result[key] = value.to_dict()
                else:
                    result[key] = value
        
        return result
    
    @staticmethod
    def get_object_by_name(objects: List[T], name_attr: str, name: str) -> Optional[T]:
        """
        Retrieve an object from a list based on the specified attribute name.

        Args:
            objects (List[T]): List of objects to search.
            name_attr (str): The name of the attribute to compare with.
            name (str): The value of the attribute to match.

        Returns:
            Optional[T]: The first object with a matching attribute value, or None if not found.
        """        
        if objects:
            for obj in objects:
                if getattr(obj, name_attr) == name:
                    return obj
        return None

    #region helper methods
    def __transform_value(self, x):
        if x == "None":
            return None
        return x
    #endregion