##**************************************************************************
##
## Description -------------------------------------------------------------
##
##**************************************************************************
##*
""" Enum extension which adds the method(s)"""
##*     - list()
##*
##* Modifications:
##* Date                User        Description
##* ------------------------------------------------------------------------
##* 2023-02-20          bettlerd    created script
##* 2023-05-15          bettlerd    added __str__() method
##* 2023-05-16          bettlerd    added from_string() method
##* 2023-05-16          bettlerd    added ExtendedEnumByIdentityString class
##* 2023-09-28          bettlerd    added detects_if_enum_in_x() method
##* 2023-10-02          bettlerd    added Arg method in detects_if_enum_in_x() 
##*                                 method
##* 2023-10-02          bettlerd    added check if value is None in 
##*                                 detects_if_enum_in_x() method
##* 2023-10-02          bettlerd    added check if value DEFAULT exists in 
##*                                 detects_if_enum_in_x() method
##* 2023-10-02          bettlerd    added where() method
##*
##*

from enum import Enum
from typing import List, Any, Callable

class ExtendedEnum(Enum):
    """
    Adds some extensions to the enums

    source: https://stackoverflow.com/a/54919285/11026899
    """

    @classmethod
    def list(cls):
        """Returns a list"""
        return list(map(lambda c: c.value, cls))

    @classmethod
    def to_dict(cls):
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}
    
    @classmethod
    def keys(cls):
        """Returns a list of all the enum keys."""
        return cls._member_names_
    
    @classmethod
    def values(cls):
        """Returns a list of all the enum values."""
        return list(cls._value2member_map_.keys())

    @classmethod
    def print(cls) -> None:
        """prints all the values."""
        [print(f"{member.name}: {member.value}") for member in cls]

    @classmethod
    def from_string(cls, string_value:str):
        """Returns the enum value corresponding to the given string.

        Args:
            string_value (str): The string value to cast to the enum.

        Returns:
            TypeEnum: The enum value corresponding to the given string.

        Raises:
            ValueError: If no matching enum value is found.
        """
        for member in cls:
            if member.name == string_value:
                return member
        raise ValueError(f"No matching enum value for {string_value}")
    
    @classmethod
    def detects_if_enum_in_x(cls, x:str, method:Callable=None) -> 'ExtendedEnum':
        """
        Determines if an enum value is present in a string.

        Args:
            x (str): The string to search for the enum value.
            method (callable): An optional method to apply to the string before 
            searching for the enum value.

        Returns:
            ExtendedEnum: The enum value that was found in the string.

        Raises:
            ValueError: If no matching enum value is found.
        """
        if method is not None:
            x = method(x)
        for member in cls:
            if member.value is not None and member.value in x:
                return member
        if hasattr(cls, 'DEFAULT'):
            return cls.DEFAULT    
        raise ValueError(f"Enum could not be found in the string «{x}».")

    def __str__(self):
        """method is called when you use an enum object as a string, 
        allowing you to define the string representation of the enum."""
        return str(self.value)

    @classmethod
    def where(cls, predicate: Callable[[Any], bool]) -> List['ExtendedEnum']:
        """
        Filters the enum members based on the given predicate.

        Args:
            predicate (callable): A function that takes an enum member as input and returns a boolean.

        Returns:
            list: A list of enum members that satisfy the predicate.

        Example «greater than 2»:
            >>> class Color(ExtendedEnum):
            ...     RED = 1
            ...     GREEN = 2
            ...     BLUE = 3
            ...     YELLOW = 4
            ...     PURPLE = 5
            ...
            >>> # Filter the enum members based on a condition
            >>> filtered_colors = Color.where(lambda c: c.value > 2)
            >>> # Print the filtered enum members
            >>> for color in filtered_colors:
            ...     print(color.name, color.value)
            ...
            BLUE 3
            YELLOW 4
            PURPLE 5
        
        Example «starts with B»:
            >>> class Color(ExtendedEnum):
            ...     RED = 1
            ...     GREEN = 2
            ...     BLUE = 3
            ...     YELLOW = 4
            ...     PURPLE = 5
            ...
            >>> # Filter the enum members based on a condition
            >>> filtered_colors = Color.where(lambda c: c.name.startswith('B'))
            >>> # Print the filtered enum members
            >>> for color in filtered_colors:
            ...     print(color.name, color.value)
            ...
            BLUE 3

        Example «not equal RED and BLUE»:
            >>> class Color(ExtendedEnum):
            ...     RED = 1
            ...     GREEN = 2
            ...     BLUE = 3
            ...     YELLOW = 4
            ...     PURPLE = 5
            ...
            >>> # Filter the enum members based on a condition
            >>> filtered_colors = Color.where(lambda c: c != Color.RED and c != Color.BLUE)
            >>> # Print the filtered enum members
            >>> for color in filtered_colors:
            ...     print(color.name, color.value)
            ...
            GREEN 2
            YELLOW 4
            PURPLE 5
        """
        return [member for member in cls if predicate(member)]

class ExtendedEnumByIdentityString(ExtendedEnum):
    """
    method auto() returns the identity string.
    """
    @classmethod
    def _generate_next_value_(cls, name:str, start:int, count:int, last_values:List[Any]):
        """Defines the return values of auto() and it will return the name only.
        
        :param name: the name of the member
        :param start: the initial start value or None
        :param count: the number of existing members
        :param last_values: the list of values assigned
        """
        return name
    
if __name__ == "__main__":
    class Color(ExtendedEnum):
        RED = 1
        GREEN = 2
        BLUE = 3
        YELLOW = 4
        PURPLE = 5

    # Filter the enum members based on a condition
    filtered_colors = Color.where(lambda c: c != Color.GREEN and c != Color.YELLOW and c != Color.PURPLE)

    # Print the filtered enum members
    for color in filtered_colors:
        print(color.name, color.value)