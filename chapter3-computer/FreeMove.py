'''
    NFA: 非确定有限自动机
    记录当前时刻 "可能会处于那些状态"

    自由移动

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
    
    def follow_free_move(self, states):
        res_states = self.next_states(states, None)
        if(res_states.issubset(states)):
            return states
        return self.follow_free_move(states | res_states)

class NFA(object):
    def __init__(self, current_states, accept_states, rulebook):
        self.rulebook = rulebook
        self.current_states = self.rulebook.follow_free_move(current_states)
        self.accept_states = accept_states
    
    def accepting(self):
        return len(self.current_states & self.accept_states) != 0

    def read_character(self, character):
        res = set()
        for state in self.current_states:
            res = res | self.rulebook.next_states({state}, character)
        self.current_states = self.rulebook.follow_free_move(res)
    
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
        FARule(1, None, 2), FARule(1, None, 4),
        FARule(2, "a", 3), FARule(3, "a", 2),
        FARule(4, "a", 5), FARule(5, "a", 6),
        FARule(6, "a", 4)
    ])

    nf = NFADesign(1, {2,4}, rulebook)
    print("\nNFA free-move test!")
    while(True):
        string = input(">> ")
        if(string == "exit"):
            break
        print(nf.accepting(string))




