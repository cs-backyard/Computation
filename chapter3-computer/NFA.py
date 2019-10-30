'''
    NFA: 非确定有限自动机
    记录当前时刻 "可能会处于那些状态"

'''

class FARule(object):
    def __init__(self, current_state,  character, next_state):
        self.current_state = current_state
        self.character = character
        self.next_state = next_state
    
    def follow(self):
        return self.next_state
    def __repr__(self):
        return f"<FARule: {self.current_state} ==={self.character}===>> {self.next_state}>"

class NFARulebook(object):
    def __init__(self, rules):
        self.rules = rules
    
    # 处于current_states中的可能状态，遇到character后的可能状态集合
    def next_states(self, states, character):
        res = self.current_states(states, character)
        res = [ rule.follow() for rule in res]
        return set(res)

    # 处于current_states中的可能状态，遇到character后可能遵守的转移rule
    def current_states(self, states, character):
        res = []
        for state in list(states):
            res += list(filter((lambda rule: rule.current_state==state and rule.character==character), self.rules))
        return res

class NFA(object):
    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook
    
    def accepting(self):
        return len(self.current_states & self.accept_states) != 0
        
    def read_character(self, character):
        res = set()
        for state in self.current_states:
            res = res | self.rulebook.next_states({state}, character)
        self.current_states = res
    
    def read_string(self, string):
        for s in string:
            self.read_character(s)

class NFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook
    def new_nfa(self):
        return NFA({self.start_state}, self.accept_states, self.rulebook)
    
    def accepting(self, string):
        res = self.new_nfa()
        res.read_string(string)
        return res.accepting()


if __name__ == "__main__":
    rulebook = NFARulebook([
        FARule(1, "a", 1), FARule(1, "b", 1),
        FARule(1, "b", 2), FARule(2, "b", 3)
    ])

    # print(rulebook.next_states({1,2}, "b"))
    nfa = NFA({1}, {3}, rulebook)
    # print(nfa.accepting())
    nf = NFADesign(1, {3}, rulebook)
    print("\nNFA test!")
    while(True):
        string = input(">> ")
        if(string == "exit"):
            break
        print(nf.accepting(string))



    print("\nNFA start!")
    while(True):
        print(f"当前可能的状态集合:\t{nfa.current_states}\t是否可以结束:\t{nfa.accepting()}")
        character = input("输入下一个字符串:")
        if(character == "exit"):
            break
        nfa.read_string(character)
    print("NFA finish!")




