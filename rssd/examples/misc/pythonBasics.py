'''Basic Python Functions'''

print("__file__: " + __file__)
print("__name__: " +  __name__)
globals()["Test"] = 12345

print(globals())
import os
print("FilePath: " + os.path.dirname(os.path.realpath(__file__)))

asdf = 8
for i in range(2,int(asdf/2)+1):
    print(i)