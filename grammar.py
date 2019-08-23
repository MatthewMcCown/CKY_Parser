import sys
from collections import defaultdict
from math import fsum

class Pcfg(object): 
    """
    Represent a probabilistic context free grammar. 
    """

    def __init__(self, grammar_file): 
        self.rhs_to_rules = defaultdict(list)
        self.lhs_to_rules = defaultdict(list)
        self.startsymbol = None 
        self.read_rules(grammar_file)     
        self.grammar_check()

    def grammar_check(self):
        grammar_bool = self.verify_grammar()
        if grammar_bool == True:
            print('Grammar is a valid PCFG in CNF')
        elif grammar_bool == False:
            print('Error: Grammar is not a valid PCFG in CNF')

    def read_rules(self,grammar_file):
        
        for line in grammar_file: 
            line = line.strip()
            if line and not line.startswith("#"):
                if "->" in line: 
                    rule = self.parse_rule(line.strip())
                    lhs, rhs, prob = rule
                    self.rhs_to_rules[rhs].append(rule)
                    self.lhs_to_rules[lhs].append(rule)
                else: 
                    startsymbol, prob = line.rsplit(";")
                    self.startsymbol = startsymbol.strip()
                    
    def parse_rule(self,rule_s):
        lhs, other = rule_s.split("->")
        lhs = lhs.strip()
        rhs_s, prob_s = other.rsplit(";",1) 
        prob = float(prob_s)
        rhs = tuple(rhs_s.strip().split())
        return (lhs, rhs, prob)

    def verify_grammar(self):
        """
        Return True if the grammar is a valid PCFG in CNF.
        Otherwise return False. 
        """
        for value in self.lhs_to_rules.values():
            # Each value is a list of [(lhs,rhs,probability)]
            # Compute the total probability and check that it sums to 1
            total_probability = fsum([rule[2] for rule in value])
            tolerance_threshold = 0.0001
            probability_check = abs(total_probability - 1)
            if probability_check > tolerance_threshold:
                cnf_check = False
                return cnf_check
            for rule in value:
                # Check that each non-terminal maps to two non-terminals
                if len(rule[1]) == 2 and rule[1][0].isupper() and rule[1][1].isupper():
                    cnf_check = True
                # If a non-terminal does not map to two non-terminals, 
                # check that it maps to one terminal.
                # Anything that is not a nonterminal (uppercase), is considered a terminal
                elif len(rule[1]) == 1 and not rule[1][0].isupper():
                    cnf_check = True
                else:
                    cnf_check = False
                    return cnf_check
        return cnf_check 

if __name__ == "__main__":
    with open(sys.argv[1],'r') as grammar_file:
        grammar = Pcfg(grammar_file)

