from dataclasses import dataclass


@dataclass
class Node:
    """A class that contains the node object
    Attributes:
        name: A str value of the name of the function __name__
        function_reference: The actual function or callable
        next: None by default, list value of what is next node, assigned in __post_init__
        doc: Docstring of method assigned in __post_init__
    """

    name: str
    function_reference: callable

    def __post_init__(self):
        """In post init we get the next node if
        it is there"""
        # store the __doc__ as attribute docstring
        self.docstring = self.function_reference.__doc__
        # if next has value
        if self.function_reference.next:
            if isinstance(self.function_reference.next, list):
                # we do a check to see that all elements in the list
                # are a string
                element_types = [
                    type(element) for element in self.function_reference.next
                ]
                elements_unique = list(set(element_types))
                # we make sure that the types are uniform
                # if the len of the set is more than 1 then we raise an error
                if len(elements_unique) > 1:
                    raise TypeError(
                        f"More than 1 type of element found, next can be str or list of str, found: {elements_unique}"
                    )
                # if all the elements are uniform, we make sure that
                # they are all of string type
                if isinstance(type(elements_unique[0]), str):
                    raise TypeError(
                        f"'next' value can only be 'list of str' or 'str', found: {type(elements_unique[0])}"
                    )
                # then we assign the next
                self.next = self.function_reference.next
            elif isinstance(self.function_reference.next, str):
                # we make sure that the next is put in a list
                self.next = [self.function_reference.next]
        else:
            self.next = []

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)
