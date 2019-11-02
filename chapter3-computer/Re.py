'''
    simple re engine
    precedence
        0. a | b
        1. ab
        2. a*
        3. a
'''
from FreeMove import *

class Pattern(object):
    def __init__(self, precedence):
        self.precedence = precedence
    
    def bracket(self, other):
        if(self.precedence > other.precedence):
            return f"({str(other)})" 
        return str(other)

    def matches(self, string):
        return self.to_nfa().accepting(string)

    def to_nfa(self):
        return None




class Empty(Pattern):
    def __init__(self):
        Pattern.__init__(self, 3)

    def to_nfa(self):
        start_state = object()
        accept_state = start_state
        rulebook = NFARulebook([])
        return NFADesign(start_state, {accept_state}, rulebook)

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
    
    def to_nfa(self):
        first_nfa = self.first.to_nfa()
        second_nfa = self.second.to_nfa()

        start_state = first_nfa.start_state
        accept_states = second_nfa.accept_states

        rules = first_nfa.rulebook.rules + second_nfa.rulebook.rules
        rules = rules + [FARule(start, None, second_nfa.start_state) for start in list(first_nfa.accept_states)]
        rulebook = NFARulebook(rules)
        return NFADesign(start_state, accept_states, rulebook)
        


    def __repr__(self):
        return "".join(list(map(self.bracket, [self.first, self.second])))

class Choose(Pattern):
    def __init__(self, first, second):
        Pattern.__init__(self, 0)
        self.first = first
        self.second = second
    
    def to_nfa(self):
        first_nfa = self.first.to_nfa()
        second_nfa = self.second.to_nfa()

        start_state = object()
        accept_states = first_nfa.accept_states | second_nfa.accept_states
        rules = [FARule(start_state, None, befree) for befree in [first_nfa.start_state, second_nfa.start_state]] + first_nfa.rulebook.rules + second_nfa.rulebook.rules
        rulebook = NFARulebook(rules)
        return NFADesign(start_state, accept_states, rulebook)


    def __repr__(self):
        return "|".join(list(map(self.bracket, [self.first, self.second])))

class Repeat(Pattern):
    def __init__(self, value):
        Pattern.__init__(self, 2)
        self.value = value

    def to_nfa(self):
        nfa = self.value.to_nfa()

        start_state = object()
        accept_states = {start_state} | nfa.accept_states
        rules = [FARule(start, None, nfa.start_state) for start in list(accept_states)] + nfa.rulebook.rules
        rulebook = NFARulebook(rules)
        return NFADesign(start_state, accept_states, rulebook)
    
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

    empty = Empty()
    literal = Literal("a")
    # print(empty.matches(""))
    # print(literal.matches("a"))
    literal2 = Literal("b")
    cons = Concatenate(literal, literal2)
    print(cons.matches("abc"))

    print("choose:\t", Choose(cons, literal).matches("abc"))
    print("repeat:\t", Repeat(literal).matches("aaaaaa"))

    test = Repeat(
        Concatenate(
            literal,
            Choose(Empty(), literal2)
        )
    )
    print("test ", test)
    print(test.matches("abba"))