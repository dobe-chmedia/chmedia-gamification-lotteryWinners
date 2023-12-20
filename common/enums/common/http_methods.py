##**************************************************************************
##
## Description -------------------------------------------------------------
##
##**************************************************************************
##*
"""Defining the HTTP Methods for RESTful Services"""
##*
##* Modifications:
##* Date                User        Description
##* ------------------------------------------------------------------------
##* 2023-03-03          bettlerd    created script
##* 
##*
##*

from enum import unique, auto
from typing import List, Any

from common.extensions.enum_extension import ExtendedEnum

@unique
class HTTPmethodsEnum(ExtendedEnum):
    """
    Defining the HTTP Methods for RESTful Services

    source: https://medium.com/@9cv9official/what-are-get-post-put-patch-delete-a-walkthrough-with-javascripts-fetch-api-17be31755d28
    """
    # @staticmethod
    def _generate_next_value_(name:str, start:int, count:int, last_values:List[Any]):
        """Defines the return values of auto() and it will return the name only.
        
        :param name: the name of the member
        :param start: the initial start value or None
        :param count: the number of existing members
        :param last_values: the list of values assigned
        """
        return name

    GET = auto()
    """
    The GET method is used to retrieve data from the server.
    This is a read-only method, so it has no risk of mutating or 
    corrupting the data. For example, if we call the get method 
    on our API, we'll get back a list of all to-dos.
    """
    POST = auto()
    """
    The POST method sends data to the server and creates a new 
    resource. The resource it creates is subordinate to some 
    other parent resource. When a new resource is POSTed to 
    the parent, the API service will automatically associate 
    the new resource by assigning it an ID (new resource URI). 
    In short, this method is used to create a new data entry.
    """
    PUT = auto()
    """
    The PUT method is most often used to update an existing 
    resource. If you want to update a specific resource 
    (which comes with a specific URI), you can call the PUT 
    method to that resource URI with the request body 
    containing the complete new version of the resource you 
    are trying to update.
    """
    PATCH = auto()
    """
    The PATCH method is very similar to the PUT method because 
    it also modifies an existing resource. The difference 
    is that for the PUT method, the request body contains 
    the complete new version, whereas for the PATCH method, 
    the request body only needs to contain the specific 
    changes to the resource, specifically a set of instructions 
    describing how that resource should be changed, and the 
    API service will create a new version according to that 
    instruction.
    """
    DELETE = auto()
    """
    The DELETE method is used to delete a resource specified 
    by its URI.
    """


if __name__ == '__main__':

    HTTPmethodsEnum.print()