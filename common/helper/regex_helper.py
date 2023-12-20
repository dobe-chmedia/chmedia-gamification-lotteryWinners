##*****************************************************************************
##
## Description ----------------------------------------------------------------
##
##*****************************************************************************
##*
""" Collection of string regex helper methods"""
##*
##* Modifications:
##* Date            User        Description
##* ---------------------------------------------------------------------------
##* 2022-08-15      bettlerd    created script
##*
##*

import re

def find_pattern(input:str, pattern:str)->bool:
    """
    Check if a given pattern exists within an input string.

    Args:
        input (str): The input string to search within.
        pattern (str): The pattern to match.

    Returns:
        bool: True if the pattern is found, False otherwise.
    
    Examples:
        >>> find_pattern("The quick brown fox", r"quick")
        True

        >>> find_pattern("Hello, world!", r"\d+")
        False
    """
    return bool(re.search(pattern, input))


if __name__ == "__main__":

    execute_test1 = True
    if execute_test1:
        test_str = "Some text List[bla-lba]"
        pattern = r"List\[[^\]]*\]"
        print(find_pattern(test_str, pattern))

        test_str = "List_ANALYTICS_263509169"
        print(find_pattern(test_str, pattern))
