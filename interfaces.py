from abc import ABC, abstractmethod

# reference: https://rednafi.github.io/digressions/python/2020/07/03/python-mixins.html


class ICalc(ABC):
    """Formal interface: Abstract calculator class."""

    @abstractmethod
    def add(self, a, b):
        pass

    @abstractmethod
    def sub(self, a, b):
        pass

    @abstractmethod
    def mul(self, a, b):
        pass

    @abstractmethod
    def div(self, a, b):
        pass

    def method_c(self):
        '''
        This method can have a real implementation on this class,
        since it is not decorated with "abstractmethod".
        '''
        # implement something
        pass
