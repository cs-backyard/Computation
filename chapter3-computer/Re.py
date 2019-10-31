'''
    simple re engine
    precedence
        0. a | b
        1. ab
        2. a*
        3. a
'''
from NFA import *

class Pattern(object):
    def __init__(self, precedence):
        self.precedence = precedence
    
    def bracket(self, other):
        if(self.precedence > other.precedence):
            return f"({str(other)})" 
        return str(other)




class Empty(Pattern):
    def __init__(self):
        Pattern.__init__(self, 3)

    def to_nfa(self):
        start_state = object()
        accept_state = {start_state}
        rulebook = NFARulebook([])
        return NFADesign(start_state, accept_state, rulebook)

    def __repr__(self):
        return ""

class Literal(Pattern):
    def __init__(self, literal):
        Pattern.__init__(self, 3)
        self.literal = literal

    def to_nfa(self):
        start_state = object()
        accept_state = object()
        rulebook = NFARulebook([FARule(start_state, self.literal, accept_state)])
        return NFADesign(start_state, {accept_state}, rulebook)

    def __repr__(self):
        return self.literal

class Concatenate(Pattern):
    def __init__(self, first, second):
        Pattern.__init__(self, 1)
        self.first = first
        self.second = second
    
    def __repr__(self):
        return "".join(list(map(self.bracket, [self.first, self.second])))

class Choose(Pattern):
    def __init__(self, first, second):
        Pattern.__init__(self, 0)
        self.first = first
        self.second = second
    
    def __repr__(self):
        return "|".join(list(map(self.bracket, [self.first, self.second])))

class Repeat(Pattern):
    def __init__(self, value):
        Pattern.__init__(self, 2)
        self.value = value
    
    def __repr__(self):
        return self.bracket(self.value) + "*"



if __name__ == "__main__":
    res = Repeat(
        Choose(
            Concatenate(Literal("a"), Literal("b")),
            Literal("c")
        )
    )
    # print(res)

    empty = Empty().to_nfa()
    literal = Literal("a").to_nfa()
    print(empty.accepting("a"))
    print(literal.accepting("a"))