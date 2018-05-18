'''Basic Python Functions'''

print("__file__: " + __file__)
print("__name__: " +  __name__)
globals()["Test"] = 12345

print(globals())
import os
print("FilePath: " + os.path.dirname(os.path.realpath(__file__)))
