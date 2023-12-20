##*****************************************************************************
##
## Description ----------------------------------------------------------------
##
##*****************************************************************************
##*
""" Collection of logging helper methods"""
##*
##* Modifications:
##* Date            User        Description
##* ---------------------------------------------------------------------------
##* 2022-12-20      DOBE        created script  
##* 2023-10-26      DOBE        added DO_NOTHING
##*
##*

import re
import socket
import inspect
import logging

from common.helper.list_helper import is_element_in_list


DO_NOTHING = "do nothing (there is no work to be done in this step)."

def current_method_name(level:int = 1)->str:
    """
    The function name that is being executed by the frame this record corresponds to, i.e.
    returns the name of the current method.

    :param level: Parameter which determines what should be considered as «current» method. 0 will be current_method_name(), 1 the caller of current_method_name() and so on.
    """
    method_name = f"{inspect.stack()[level][3]}()"

    if False:
        class_name = str(inspect.stack()[level + 1][4]).replace(method_name, "")
        class_name = (re.sub(pattern="(\[)|(\])|(\')",repl="",string=class_name)
                        .replace(".\\n","")
                        .strip()
            )

        return f'{class_name}.{method_name}'
    else:
        return method_name
    
def do_logging(txt:str,force_logging:bool=False,caller_lvl:int = 2):
    """
    Decides whether to create a log entry or print the output to the console.
    If the method will be called on a developer machine. The output will 
    be printed in the console.

    :param txt: the text of the output
    :param force_logging: should the logging be done even on the developer machine?
    :param caller_lvl: the lvl of the method, caller_lvl=1 would be do_logging(), caller_lvl=2, the method which calls do_logging
    """
    hostname = socket.gethostname()
    is_developer_machine = False
   
    if not force_logging & is_developer_machine:
        print(f"{current_method_name(level=caller_lvl)}: {txt}")
    else:
        logging.info(f"{current_method_name(level=caller_lvl)}: {txt}")


if __name__ == '__main__':

    execute_test1 = False
    if execute_test1:
        class A():
            @staticmethod
            def test_run_2():
                print(current_method_name())

        def test_run():
            print(current_method_name())

        test_run()
        A.test_run_2()

    execute_test2 = True
    if execute_test2:
        # CASE: force_logging = False & developer machine = True
        def case1():
            do_logging("bla bla") 
        case1() # expect print (and no logging)

        # CASE: force_logging = True & developer machine = True
        def case2():
            do_logging("bla bla", True) # expect no print and do logging
        case2()