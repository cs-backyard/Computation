'''
    NFA转换为DFA

'''
from FreeMove import *
from DFA import *

class NFAToDFA(object):
    def __init__(self, nfa_design):
        self.nfa_design = nfa_design
        self.rules = []
        self.states = []
    
    def get_allchar(self):
        return list(set([rule.character for rule in self.nfa_design.rulebook.rules if rule.character != None]))

    def next_states(self, states, character):
        nfa = self.nfa_design.new_nfa(states)
        nfa.read_string(character)
        return nfa.current_states
    
    def rules_for(self, states):
        return [FARule(states, character, self.next_states(states, character)) for character in self.get_allchar()]

    def discover_rules(self, states_list):
        rules = []
        for states in states_list:
            rules += self.rules_for(states)
        
        next_states = []
        for rule in rules:
            next_states.append(rule.follow())
        if(self.issub(next_states, states_list)):
            return [states_list, rules]
        return self.discover_rules(states_list + next_states)

    def issub(self, first, second):
        for f in first:
            for s in second:
                if(not f.issubset(s)):
                    return False
        return True
            
                   






if __name__ == "__main__":
    rulebook = NFARulebook([
        FARule(1, None, 2), FARule(1, None, 4),
        FARule(2, "a", 3), FARule(3, "a", 2),
        FARule(4, "a", 5), FARule(5, "a", 6),
        FARule(6, "a", 4)
    ])

    nfa = NFADesign(1, {2,4}, rulebook)
    nd = NFAToDFA(nfa)
    # print(nd.next_states({5}, "a"))
    print(nd.discover_rules([{1,2,4}]))