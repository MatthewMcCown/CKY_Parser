import math
import sys
from collections import defaultdict
import itertools
from grammar import Pcfg
import itertools

class CkyParser(object):
    """
    A CKY parser.
    """

    def __init__(self, grammar): 
        """
        Initialize a new parser instance from a grammar. 
        """
        self.grammar = grammar

    def is_in_language(self,tokens):
        """
        Membership checking. Parse the input tokens and return True if 
        the sentence is in the language described by the grammar. Otherwise
        return False
        """
        self.table = {}
        self.number_of_tokens = len(tokens)

        # Initialize the table by finding the nonterminal symbols 
        # in the grammar that map to each token
        for i in range(0,(self.number_of_tokens)):
            self.nested_dict = {}
            self.list_of_non_terminals = []
            for key, value in self.grammar.rhs_to_rules.items():
                for terminal in key:
                    if tokens[i] == terminal:
                        for item in value:
                            # Check whether the non-terminal is already in the list
                            # Could also pass the list to a set
                            if not any(item[0] in element for element in self.list_of_non_terminals):
                                self.list_of_non_terminals.append(item[0])
                            for element in self.list_of_non_terminals:
                                self.nested_dict[element] = tokens[i]
            self.table[(i,i+1)] = self.nested_dict
        
        # Main loop
        for length in range(2,self.number_of_tokens+1):
            for i in range(0,(self.number_of_tokens - length + 1)):
                j = (i + length)
                # Need to deal with substrings of length 2 separately
                # k is not in range when length = 2
                if length == 2:
                    self.A_nonterminals = []
                    self.B_nonterminals = []
                    for key, value in self.table.items():
                        if key == (i,i+1):
                            for keyA in value.keys():
                                self.A_nonterminals.append(keyA)
                        elif key == (i+1, i+2):
                             for keyB in value.keys():
                                self.B_nonterminals.append(keyB)    
                    cartesianAB = list(itertools.product(self.A_nonterminals,self.B_nonterminals))                      
                    self.temp_dict = {} 
                    for AB in cartesianAB:
                        for key,value in self.grammar.rhs_to_rules.items():
                            if AB == key:
                                for element in value:
                                    self.temp_dict[element[0]] = tuple(list(((AB[0],i,i+1),(AB[1],i+1,i+2))))
                    self.table[(i,i+2)] = self.temp_dict
                elif length > 2:
                    self.temp_dict2 = {}
                    for k in range((i + 1),(j)):
                        self.C_nonterminals = []
                        self.D_nonterminals = []
                        for key, value in self.table.items():
                            if key == (i,k):
                                for keyC in value.keys():
                                    self.C_nonterminals.append(keyC)
                            elif key == (k,j):
                                for keyD in value.keys():
                                    self.D_nonterminals.append(keyD)
                        cartesianCD = list(itertools.product(self.C_nonterminals,self.D_nonterminals))
                        for CD in cartesianCD:
                            for key,value in self.grammar.rhs_to_rules.items():
                                if CD == key:
                                    for element in value:
                                        # A given nonterminal could be derived from multiple splits
                                        # For example, FRAG could be (NP,PP) or (NP, FRAGBAR)
                                        # Here, we include all splits for a given nonterminal
                                        if element[0] not in self.temp_dict2.keys():
                                            self.temp_dict2[element[0]] = []
                                            self.temp_dict2[element[0]].append(((CD[0],i,k),(CD[1],k,j)))
                                        else:
                                            self.temp_dict2[element[0]].append(((CD[0],i,k),(CD[1],k,j)))
                    # Convert the dict values to tuples instead of lists
                    for key, value in self.temp_dict2.items():
                        self.temp_dict2[key] = tuple(value)
                    self.table[(i,j)] = self.temp_dict2
       
        if self.grammar.startsymbol in self.table[(0,self.number_of_tokens)]:
            return True
        else:
            return False

    def parse_with_backpointers(self, tokens):
            """
            Parse the input tokens and return a parse table and a probability table.
            """

            self.most_probable_table = {}
            self.probs = {}
            self.number_of_tokens = len(tokens)

            # Initialize the table by finding the nonterminal symbols 
            # in the grammar that map to each token
            for i in range(0,(self.number_of_tokens)):
                self.nested_dict = {}
                self.nested_dict_prob = {}
                self.list_of_non_terminals = []
                for key, value in self.grammar.rhs_to_rules.items():
                    for terminal in key:
                        if tokens[i] == terminal:
                            for item in value:
                                self.nested_dict[item[0]] = tokens[i]
                                self.nested_dict_prob[item[0]] = math.log2(item[2])
                self.most_probable_table[(i,i+1)] = self.nested_dict
                self.probs[(i,i+1)] = self.nested_dict_prob
            
            # Main loop
            for length in range(2,self.number_of_tokens+1):
                for i in range(0,(self.number_of_tokens - length + 1)):
                    j = (i + length)
                    # Need to deal with substrings of length 2 separately
                    # k is not in range when length = 2
                    if length == 2:
                        self.A_nonterminals = []
                        self.B_nonterminals = []
                        for key, value in self.most_probable_table.items():
                            if key == (i,i+1):
                                for keyA in value.keys():
                                    self.A_nonterminals.append(keyA)
                            elif key == (i+1, i+2):
                                for keyB in value.keys():
                                    self.B_nonterminals.append(keyB)    
                        cartesianAB = list(itertools.product(self.A_nonterminals,self.B_nonterminals))                      
                        self.temp_dict = {}
                        self.temp_dict_prob = {} 
                        for AB in cartesianAB:
                            for key,value in self.grammar.rhs_to_rules.items():
                                if AB == key:
                                    for element in value:
                                        # Find the split with the highest probability 
                                        # max_element = max(value,key = lambda item: item[1])
                                        self.temp_dict[element[0]] = tuple(list(((AB[0],i,i+1),(AB[1],i+1,i+2))))
                                        self.temp_dict_prob[element[0]] = math.log2(element[2])
                        self.most_probable_table[(i,i+2)] = self.temp_dict
                        self.probs[(i,i+2)] = self.temp_dict_prob
                    elif length > 2:
                        self.temp_dict2 = {}
                        self.temp_dict2_prob = {}
                        for k in range((i + 1),(j)):
                            self.C_nonterminals = []
                            self.D_nonterminals = []
                            for key, value in self.most_probable_table.items():
                                if key == (i,k):
                                    for keyC in value.keys():
                                        self.C_nonterminals.append(keyC)
                                elif key == (k,j):
                                    for keyD in value.keys():
                                        self.D_nonterminals.append(keyD)
                            cartesianCD = list(itertools.product(self.C_nonterminals,self.D_nonterminals))
                            for CD in cartesianCD:
                                for key,value in self.grammar.rhs_to_rules.items():
                                    if CD == key:
                                        for element in value:
                                        # A given nonterminal could be derived from multiple splits
                                        # For example, FRAG could be (NP,PP) or (NP, FRAGBAR)
                                        # Here, we include all splits for a given nonterminal
                                            if element[0] not in self.temp_dict2.keys():
                                                self.temp_dict2[element[0]] = []
                                                self.temp_dict2[element[0]].append(((CD[0],i,k),(CD[1],k,j),element[2]))
                                            else:
                                                self.temp_dict2[element[0]].append(((CD[0],i,k),(CD[1],k,j),element[2]))
                        # For a given nonterminal, find the split with the highest probability
                        # Then record that probability in the probability table
                        for key, value in self.temp_dict2.items():
                            self.max_split = max(value,key = lambda item: item[2])
                            self.temp_dict2[key] = (self.max_split[0],self.max_split[1])
                            self.temp_dict2_prob[key] = math.log2(self.max_split[2])
                        self.most_probable_table[(i,j)] = self.temp_dict2
                        self.probs[(i,j)] = self.temp_dict2_prob
            return self.most_probable_table, self.probs


def get_tree(chart, i,j,nt): 
    """
    Return the parse-tree rooted in non-terminal nt and covering span i,j.
    """
    # TODO: Part 4
    inner_dict = chart.get((i,j))
    if isinstance(inner_dict[nt],str):
        return (nt,inner_dict[nt])
    else:
        # Recursive call
        sentence_tree = (nt, get_tree(chart,inner_dict[nt][0][1],inner_dict[nt][0][2],inner_dict[nt][0][0]),get_tree(chart,inner_dict[nt][1][1],inner_dict[nt][1][2],inner_dict[nt][1][0]))
    return sentence_tree
  
