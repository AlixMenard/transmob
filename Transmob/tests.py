class Num:
    def __init__(self, value):
        self.value = value
    
    def __truediv__(self, other):
        print(self.value)
        print(other.value)

a = Num(8)
b = Num(2)
a/b