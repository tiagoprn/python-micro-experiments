import inspect
import json
import traceback
import os
import types

'''
This print the full stack trace from the current point in the code
(from where "stack = inspect.stack()", below, is called).

It can be useful, e.g., to understand code that makes many calls
or to get information for debugging exceptions.
'''

# reference:
# http://mahmoudimus.com/blog/2011/02/arbitrary-stack-trace-in-python/


def print_stack_history(limit=-1):
    stack = inspect.stack()

    # TODO: Turn into an optional parameter on this function parameters list
    # removes the first element of the stack, which is the current function
    stack.pop(0)

    # reverse the stack trace so the most recent is at the bottom of the stack
    # (the same order of the calls were made :)
    stack.reverse()

    # TODO: make relevant_stack be stack sliced
    #       to just the last "limit" elements
    relevant_stack = stack

    stack_list = {}

    try:
        for idx, s in enumerate(relevant_stack):
            current_function_arguments = inspect.getargvalues(s.frame)

            _, filename, line_no, func_name, code_list, index_in_code_list = s
            code_str = code_list[index_in_code_list]

            for name, data in inspect.getmembers(s.frame):
                if name == 'f_locals':
                    break
            params_and_vars_dict = {}
            for item in data:
                if not item.startswith('__'):
                    if isinstance(data[item], str) or isinstance(data[item], int) or isinstance(data[item], dict) or isinstance(data[item], list) or isinstance(data[item], set) or (data[item] is None):
                        params_and_vars_dict[item] = data[item]

            current_stack_dict = {'filename': filename,
                                  'line_number': line_no,
                                  'function_name': func_name,
                                  'params_and_vars': params_and_vars_dict,
                                  'code': code_str}

            stack_list[idx] = current_stack_dict

        debugging = json.dumps(stack_list)
    finally:
        # avoid memory leak issues
        del stack

    return debugging

def func_one():
    var_first = 'var1'
    print('func 1')
    func_two(f2param2=99)

def func_two(f2param1='teste', f2param2=15, f2param3=['el1']):
    var_second = ['var2']
    print('func 2')
    func_three()

def func_three():
    var_three = {'key3': 'value3'}
    var_three_another = [("field3A", "value3A"),("field3B", "value3B")]
    print('func 3')
    func_four()

def func_four():
    var_four = 4
    print('func 4')
    history = print_stack_history()
    print('To get to the current point on the code, the calls order (stack) '
          'was the following: \n {}'.format(history))

func_one()
