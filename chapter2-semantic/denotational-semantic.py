''' 
    Simple: a toy pl
    1.定义一个简单的虚拟机, 进行简单的规约和求值操作
    2.添加 赋值 和 if分支
        规约过程返回一个元组 (新语句, 环境)
        表达式只能求值, 语句才能改变环境
    3.添加 sequence 和 while
    4.
        大步语义
        big-step semantic

        在大步语义中, 每一种元素都可以 经过execute得到结果
    
    5. 指称语义
        直接把simple-ast转换成python代码，使用python执行


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

    def execute(self, context):
        return self

    def __repr__(self):
        return f"(lambda context: {self.value})(context)"

    def to_python(self):
        return "{}"

class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.reducible = True
    
    def execute(self, context):
        return Number(self.left.execute(context).value + self.right.execute(context).value)

    def reduces(self, context):
        if(self.left.reducible):
            return Add(self.left.reduces(context)[0], self.right), context
        if(self.right.reducible):
            return Add(self.left, self.right.reduces(context)[0]), context
        return Number(self.left.value + self.right.value), context

    def __repr__(self):
        return f"(lambda context: {self.left} + {self.right})(context)"


class Mul(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.reducible = True

    def execute(self, context):
        return Number(self.left.execute(context).value *self.right.execute(context).value) 

    def reduces(self, context):
        if(self.left.reducible):
            return Mul(self.left.reduces(context)[0], self.right), context
        if(self.right.reducible):
            return Mul(self.left, self.right.reduces(context)[0]), context
        return Number(self.left.value * self.right.value), context     

    def __repr__(self):
        return f"(lambda context: {self.left} * {self.right})(context)"

class Bool(object):
    def __init__(self, value):
        self.value = value
        self.reducible = False

    def execute(self, context):
        return self

    def __repr__(self):
        return f"(lambda context: {self.value})(context)"

class Lessthan(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.reducible = True


    def execute(self, context):
        return Bool(self.left.execute(context).value < self.right.execute(context).value)

    def reduces(self, context):
        if(self.left.reducible):
            return Lessthan(self.left.reduces(context)[0], self.right), context
        if(self.right.reducible):
            return Lessthan(self.left, self.right.reduces(context)[0]), context
        return Bool(self.left.value < self.right.value), context

    def __repr__(self):
        return f"(lambda context: {self.left} < {self.right})(context)"


class Not(object):
    def __init__(self, right):
        self.right = right
        self.reducible = True
    
    def execute(self, context):
        return Bool(not self.right.execute(context).value)

    def reduces(self, context):
        if(self.right.reducible):
            return (Not(self.right.reduces(context)[0]), context)
        return Bool(not self.right.value), context

    def __repr__(self):
        return f"(lambda context: !{self.right})(context)"


# 变量
class Variable(object):
    def __init__(self, name):
        self.name = name
        self.reducible = True
    

    def execute(self, context):
        return context.get(self.name)

    def reduces(self, context):
        return (context.get(self.name), context)
    
    def __repr__(self):
        return f"(lambda context: context.get(\"{self.name}\"))(context)"
    
# do-nothing
class DoNothing(object):
    def __init__(self):
        self.reducible = False
    
    def execute(self, context):
        return context

    def __repr__(self):
        return "(lambda context: context)(context)"

# 赋值
class Assign(object):
    def __init__(self, varname, expression):
        self.varname = varname
        self.expression = expression
        self.reducible = True
    def execute(self, context):
        newcontext = {}
        newcontext.update(context)
        newcontext[self.varname] = self.expression.execute(context)
        return newcontext

    def reduces(self, context):
        if(self.expression.reducible):
            return (Assign(self.varname, self.expression.reduces(context)[0]), context)
        newcontext = {}
        newcontext.update(context)
        newcontext[self.varname] = self.expression
        return DoNothing(), newcontext

    def __repr__(self):
        return "(lambda context: {**context, **{\"%s\":%s}})(context)"%(self.varname, self.expression)


# if分支
class If(object):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative
        self.reducible = True
    
    def execute(self, context):
        res = self.condition.execute(context)
        if(res.value == Bool(True).value):
            return self.consequence.execute(context)
        return self.alternative.execute(context)

    def reduces(self, context):
        if(self.condition.reducible):
            return If(self.condition.reduces(context)[0], self.consequence, self.alternative), context
        if(self.condition.value == Bool(True).value):
            return self.consequence, context
        return self.alternative, context
    
    def __repr__(self):
        return f"(lambda context: {self.consequence} if {self.condition} else {self.alternative})(context)"


# sequence
class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.reducible = True

    def execute(self, context):
        return self.second.execute(self.first.execute(context))

    def reduces(self, context):
        if(isinstance(self.first, DoNothing)):
            return self.second, context
        reduced_first, reduced_context = self.first.reduces(context)
        return Sequence(reduced_first, self.second), reduced_context
    
    def __repr__(self):
        return f"(lambda context:{self.second})((lambda context:{self.first})(context))"

# while
# class While(object):
#     def __init__(self, condition, body):
#         self.condition = condition
#         self.body = body
#         self.reducible = True
    
#     def execute(self, context):
#         res = self.condition.execute(context)
#         if(res.value == Bool(True).value):
#             return self.execute(self.body.execute(context))
#         return context

#     def reduces(self, context):
#         return If(self.condition, Sequence(self.body, self), DoNothing()), context
    
#     def __repr__(self):
#         return f""


# class Print(object):
#     def __init__(self, expression):
#         self.expression = expression
#         self.reducible = True

#     def execute(self, context):
#         print(f"print({self.expression}):\t", self.expression.execute(context))
#         return context

#     def reduces(self, context):
#         if(self.expression.reducible):
#             return Print(self.expression.reduces(context)[0]), context
#         # 执行print
#         print(f"print({self.expression}):\t", self.expression)
#         return DoNothing(), context

#     def __repr__(self):
#         return f"print({self.expression})"


if __name__ == "__main__":

    # print("\ntest print!")
    # res = Add(
    #     Mul(Number(2), Number(3)),
    #     Mul(Number(4), Number(2))
    # ).execute({})
    # print(res)

    # res = While(
    #     Lessthan(Variable("x"), Number(5)),
    #     Assign("x", Add(Variable("x"), Number(2)))
    # ).execute({"x": Number(4)})
    # print(res)


    res = str(
        Sequence(
            Assign("x", Number(2)),
            Assign("y", Add(Variable("x"), Number(6)))
        )
    )
   
    print(res)
    # a = compile(res, "", "exec")
    print(eval(res, {"context": {"x":"llllll"}}))
    # print((lambda a: 2+a)(2))