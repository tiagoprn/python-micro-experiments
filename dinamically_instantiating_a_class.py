import importlib


def str_to_class(fullpath: str):
    '''
    To allow dynamic instantiation of classes, given a string namespace to a
    class, returns the class so that it can be dynamically instantiated.
    '''
    module_name = '.'.join(fullpath.split('.')[:-1])
    class_name = fullpath.split('.')[-1]
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    return class_


