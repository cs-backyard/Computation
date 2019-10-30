'''
    确定性有限自动机
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


class DFARulebook(object):
    def __init__(self, rules):
        self.rules = rules
    
    def next_state(self, current_state, character):
        return self.current_rule(current_state, character).follow()

    def current_rule(self, current_state, character):
        return list(filter((lambda rule: rule.current_state==current_state and rule.character==character), self.rules))[0]


class DFA(object):
    def __init__(self, current_state, accept_state, rulebook):
        self.current_state = current_state
        self.accept_state = accept_state
        self.rulebook = rulebook
    
    # 当前DFA所处状态是否为可接受状态
    def accepting(self):
        return self.current_state in self.accept_state
    
    # DFA读入一个字符, 改变当前状态
    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state, character)
    
    def read_string(self, string):
        for s in string:
            self.read_character(s)


if __name__ == "__main__":
    rulebook = DFARulebook([
        FARule(1, "a", 2), FARule(1, "b", 1),
        FARule(2, "a", 2), FARule(2, "b", 3),
        FARule(3, "a", 3), FARule(3, "b", 3)
    ])
    # print(rulebook.next_state(1, 'b'))

    dfa = DFA(1, [3], rulebook)
    print(rulebook.current_rule(1, "a"))
    
    while(True):
        print(f"当前状态:\t{dfa.current_state}\t是否可以结束:\t{dfa.accepting()}")
        character = input("输入下一个字符串:")
        if(character == "exit"):
            break
        dfa.read_string(character)
    
    print("DFA finish!")
        