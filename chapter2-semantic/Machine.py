''' 
    Simple: a toy pl
    1.定义一个简单的虚拟机, 进行简单的规约和求值操作
'''

class Machine(object):
    def __init__(self, expression, context={}):
        self.expression = expression
        self.context = context
    
    def step(self):
        self.expression = self.expression.reduces(self.context)

    def run(self):
        while(self.expression.reducible):
            print(self.expression)
            self.step()
        
        print(self.expression)


class Number(object):
    def __init__(self, value):
        self.value = value
        self.reducible = False
    
    def __repr__(self):
        return f"{self.value}"

class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.reducible = True
    
    def reduces(self, context):
        if(self.left.reducible):
            return Add(self.left.reduces(context), self.right)
        if(self.right.reducible):
            return Add(self.left, self.right.reduces(context))
        return Number(self.left.value + self.right.value)

    def __repr__(self):
        return f"{self.left} + {self.right}"


class Mul(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.reducible = True

    def reduces(self, context):
        if(self.left.reducible):
            return Mul(self.left.reduces(context), self.right)
        if(self.right.reducible):
            return Mul(self.left, self.right.reduces(context))
        return Number(self.left.value * self.right.value)     

    def __repr__(self):
        return f"{self.left} * {self.right}"

class Bool(object):
    def __init__(self, value):
        self.value = value
        self.reducible = False
    def __repr__(self):
        return f"{self.value}"

class Lessthan(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.reducible = True
    def reduces(self, context):
        if(self.left.reducible):
            return Lessthan(self.left.reduces(context), self.right)
        if(self.right.reducible):
            return Lessthan(self.left, self.right.reduces(context))
        return Bool(self.left.value < self.right.value)

    def __repr__(self):
        return f"{self.left} < {self.right}"

class Not(object):
    def __init__(self, right):
        self.right = right
        self.reducible = True
    
    def reduces(self, context):
        if(self.right.reducible):
            return Not(self.right.reduces(context))
        return Bool(not self.right.value)

    def __repr__(self):
        return f"!({self.right})"


# 变量
class Variable(object):
    def __init__(self, name):
        self.name = name
        self.reducible = True
    
    def reduces(self, context):
        return context.get(self.name)
    
    def __repr__(self):
        return f"{self.name}"
    


if __name__ == "__main__":

    print("\ntest binary op!")
    Machine(Add(
        Mul(Number(1), Number(2)),
        Mul(Number(3), Number(4))
    )).run()

    print("\ntest '<':")
    Machine(Lessthan(
        Add(Number(2), Number(3)),
        Mul(Number(1), Number(4))
    )).run()

    print("\ntest not!")
    Machine(Not(
        Add(
            Mul(Number(1), Number(2)),
            Mul(Number(3), Number(4))
        )
    )).run()
    print("\ntest not!")
    Machine(Not(
        Lessthan(
            Number(1),
            Number(0)
        )
    )).run()

    print("\ntest variable !")
    Machine(
        Add(
            Variable("x"),
            Variable("y")
        ),
        {"x": Number(2), "y": Number(3)}
    ).run()
