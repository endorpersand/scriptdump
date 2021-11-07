class CapitalizeMeta(type): # the metaclass

    # this method in classes creates new instances
    def __new__(cls, clsname, bases, attrs):
        # cls: the metaclass to create
        # clsname: the name of the class to create
        # bases: ignore it
        # attrs: attributes declared on the class

        new_attrs = {}
        for k, v in attrs.items():
            new_attrs[k.upper()] = v

        return super(CapitalizeMeta, cls).__new__(cls, clsname, bases, new_attrs)
    
class NormalClass:
    this_is_an_attribute = 1
    def say_hello(self):
        print("hiya")


class A(metaclass=CapitalizeMeta):
    this_is_an_attribute = 1

    def say_hello(self):
        print("hiya")


print(NormalClass.this_is_an_attribute) # 1
NormalClass().say_hello() # hiya

print(A.THIS_IS_AN_ATTRIBUTE) # 1
A().SAY_HELLO() # hiya