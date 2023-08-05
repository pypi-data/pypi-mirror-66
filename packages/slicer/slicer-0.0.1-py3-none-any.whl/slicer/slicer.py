from typing import Union, Any

class Slicer:
    """ Wrapping object that will unify slicing across data structures.

    This is currently under active development.
    
    """

    def __init__(self, o: Any):
        self.o = o
    
    def __getitem__(self, key: Union[int, slice]):
        return self.o[key]