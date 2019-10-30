''' 
    Simple: a toy pl
    1.定义一个简单的虚拟机, 进行简单的规约和求值操作
    2.添加 赋值 和 if分支
        规约过程返回一个元组 (新语句, 环境)
        表达式只能求值, 语句才能改变环境
    3.添加 sequence 和 while

'''

class Machine(object):
    def __init__(self, expression, context={}):
        self.expression = expression
        self.context = context
    
    def step(self):
        self.expression, self.context = self.expression.reduces(self.context)

    def run(self):
        while(self.expression.reducible):
            print(self.expression, "\tcontext ==> ", self.context)
            self.step()
        
        print(self.expression, "\tcontext ==> ", self.context)


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
            return Add(self.left.reduces(context)[0], self.right), context
        if(self.right.reducible):
            return Add(self.left, self.right.reduces(context)[0]), context
        return Number(self.left.value + self.right.value), context

    def __repr__(self):
        return f"{self.left} + {self.right}"


class Mul(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.reducible = True

    def reduces(self, context):
        if(self.left.reducible):
            return Mul(self.left.reduces(context)[0], self.right), context
        if(self.right.reducible):
            return Mul(self.left, self.right.reduces(context)[0]), context
        return Number(self.left.value * self.right.value), context     

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
            return Lessthan(self.left.reduces(context)[0], self.right), context
        if(self.right.reducible):
            return Lessthan(self.left, self.right.reduces(context)[0]), context
        return Bool(self.left.value < self.right.value), context

    def __repr__(self):
        return f"{self.left} < {self.right}"

class Not(object):
    def __init__(self, right):
        self.right = right
        self.reducible = True
    
    def reduces(self, context):
        if(self.right.reducible):
            return (Not(self.right.reduces(context)[0]), context)
        return Bool(not self.right.value), context

    def __repr__(self):
        return f"!({self.right})"


# 变量
class Variable(object):
    def __init__(self, name):
        self.name = name
        self.reducible = True
    
    def reduces(self, context):
        return (context.get(self.name), context)
    
    def __repr__(self):
        return f"{self.name}"
    
# do-nothing
class DoNothing(object):
    def __init__(self):
        self.reducible = False
    def __repr__(self):
        return "do-nothing"

# 赋值
class Assign(object):
    def __init__(self, varname, expression):
        self.varname = varname
        self.expression = expression
        self.reducible = True
    
    def reduces(self, context):
        if(self.expression.reducible):
            return (Assign(self.varname, self.expression.reduces(context)[0]), context)
        newcontext = {}
        newcontext.update(context)
        newcontext[self.varname] = self.expression
        return DoNothing(), newcontext

    def __repr__(self):
        return f"{self.varname} = {self.expression}"


# if分支
class If(object):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative
        self.reducible = True
    
    def reduces(self, context):
        if(self.condition.reducible):
            return If(self.condition.reduces(context)[0], self.consequence, self.alternative), context
        if(self.condition.value == Bool(True).value):
            return self.consequence, context
        return self.alternative, context
    
    def __repr__(self):
        return f"if({self.condition}) {self.consequence} else {self.alternative}"


# sequence
class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.reducible = True
    def reduces(self, context):
        if(isinstance(self.first, DoNothing)):
            return self.second, context
        reduced_first, reduced_context = self.first.reduces(context)
        return Sequence(reduced_first, self.second), reduced_context
    
    def __repr__(self):
        return f"{self.first}; {self.second};"

# while
class While(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.reducible = True
    
    def reduces(self, context):
        return If(self.condition, Sequence(self.body, self), DoNothing()), context
    
    def __repr__(self):
        return f"while({self.condition}) {self.body}"


class Print(object):
    def __init__(self, expression):
        self.expression = expression
        self.reducible = True
    def reduces(self, context):
        if(self.expression.reducible):
            return Print(self.expression.reduces(context)[0]), context
        # 执行print
        print(f"print({self.expression}):\t", self.expression)
        return DoNothing(), context

    def __repr__(self):
        return f"print({self.expression})"


if __name__ == "__main__":

    print("\ntest print!")
    Machine(
        Print(
            Mul(Variable("x"), Number(3))
        ),
        {"x": Number(2)}
    ).run()




    print("\ntest while!")
    Machine(
        While(
            Lessthan(Variable("x"), Number(5)),
            Assign("x", Add(Variable("x"), Number(2)))
        ),
        {"x": Number(0)}
    ).run()



    print("\ntest sequence!")
    Machine(
        Sequence(
            Sequence(
                Assign("x", Add(Number(1), Number(2))),
                Assign("y", Add(Variable("x"), Number(3)))
            ),
            Assign("x", Add(Variable("x"), Variable("y")))
        ),
        {"x": Number(0), "y": Number(0)}
    ).run()


    print("\ntest if else!")
    Machine(
        If(
            Lessthan(Number(1), Number(2)),
            Assign("y", Number(1)),
            Assign("y", Number(2))   
        ),
        {"y": Number(4)}
    ).run()
    
    print("\ntest if!")
    Machine(
        If(
            Variable("x"),
            Assign(Variable("y"), Number(1)),
            DoNothing()
        ),
        {"x": Bool(False)}
    ).run()




    print("\ntest assign!")
    Machine(
        Assign(
            Variable("x"), 
            Add(
                Number(2), Variable("x")
            )
        ),
        {"x": Number(3)}
    ).run()





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
