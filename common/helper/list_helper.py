##*****************************************************************************
##
## Description ----------------------------------------------------------------
##
##*****************************************************************************
##*
"""Collection of list helper methods

There is a test class for this modul
"""
##*
##* Modifications:
##* Date            User        Description
##* ---------------------------------------------------------------------------
##* 2023-04-18      bettlerd    created script  
##* 2023-08-15      bettlerd    added filter_objects()
##* 2023-09-26      bettlerd    added example in filter_objects()
##* 2023-09-26      bettlerd    added example in is_element_in_list()
##* 2023-10-25      bettlerd    update is_element_in_list(): check if object is a list
##*
##*

from typing import List, Any, Callable

def is_element_in_list(elements:Any, list_obj:List)->bool:
    """
    Checks whether at least one or more items are in a list.

    This function checks if any of the specified elements are present in the given list.

    Args:
        elements (Any or List): The element(s) to be checked. Can be a single element or a list of elements.
        list_obj (List): The list in which the search is to be carried out.

    Returns:
        bool: True if at least one of the elements is found in the list, False otherwise.

    Examples:
        >>> is_element_in_list(3, [1, 2, 3, 4, 5])
        True

        >>> is_element_in_list(1, [])
        False

        >>> is_element_in_list(['apple', 'banana'], ['orange', 'pear', 'apple'])
        True

        >>> is_element_in_list('cat', ['dog', 'rabbit', 'mouse'])
        False
    """
    if not isinstance(elements, list):
        elements = [elements]

    if not isinstance(list_obj, list):
        raise TypeError(f"The second argument must be a list but is {type(list_obj)}")

    for element in elements:
        if element in list_obj:
            return True

    return False

def filter_objects(objects: List[Any], criteria: Callable[[Any], bool]) -> List[Any]:
    """
    Filter a list of objects based on a given criteria.

    Args:
        objects (List[Any]): The list of objects to be filtered.
        criteria (Callable[[Any], bool]): The filtering criteria function that returns True or False for each object.

    Returns:
        List[Any]: A list containing objects that match the filtering criteria.

    Examples:
        >>> def is_even(num):
        ...     return num % 2 == 0
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> even_numbers = filter_objects(numbers, is_even)
        >>> print(even_numbers)
        [2, 4, 6, 8, 10]
    """
    return [obj for obj in objects if criteria(obj)]

if __name__ == "__main__":

    execute_test_is_element_in_list = False
    if execute_test_is_element_in_list:
        print(is_element_in_list(3, []))

        print(is_element_in_list(3, [1, 2, 3, 4, 5]))

        print(is_element_in_list(['apple', 'banana'], ['orange', 'pear', 'apple']))

        print(is_element_in_list('cat', ['dog', 'rabbit', 'mouse']))

    execute_test_filter_objects = False
    if execute_test_filter_objects:

        class MyObject:
            def __init__(self, value):
                self.value = value

        def is_even(obj: MyObject) -> bool:
            return obj.value % 2 == 0
        
        my_objects = [MyObject(1), MyObject(2), MyObject(3), MyObject(4), MyObject(5)]
        filtered_objects = filter_objects(my_objects, is_even)

        # Print the filtered objects
        for obj in filtered_objects:
            print(obj.value)