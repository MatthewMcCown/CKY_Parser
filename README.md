NLP: Implementation of the CKY Parser Algorithm for context-free grammars. Given an input sentence and probabilistic context-free grammar, the algorithm generates parse trees in accordance with the grammar.  
  
# Sample input:  
  
> Startsymbols  
TOP ; 1.0  
  
> Phrasal rules  
ADJP -> ASEARLY PP ; 0.0588235294118  
ADVP -> NP APART ; 0.153846153846  
FRAG -> ADVP NP ; 0.0344827586207  
FRAGBAR -> NP FRAGBAR ; 0.153846153846  
NP -> A FLIGHT ; 0.00903614457831  
NP -> A NPBAR ; 0.00301204819277  
  
> Lexical rules  
ABBREVIATION -> abbreviation ; 1.0  
ABOUT -> about ; 1.0  
ADJP -> better ; 0.117647058824  
ADJP -> possible ; 0.0588235294118  
ADVP -> actually ; 0.0384615384615  