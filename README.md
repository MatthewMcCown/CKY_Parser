NLP: Implementation of the CKY Parser Algorithm for context-free grammars. Given an input sentence and probabilistic context-free grammar, the algorithm generates parse trees in accordance with the grammar. \n

Sample input: \n

# Startsymbols \n
TOP ; 1.0 \n

# Phrasal rules
ADJP -> ASEARLY PP ; 0.0588235294118 \n
ADVP -> NP APART ; 0.153846153846 \n
FRAG -> ADVP NP ; 0.0344827586207 \n
FRAGBAR -> NP FRAGBAR ; 0.153846153846 \n
NP -> A FLIGHT ; 0.00903614457831 \n
NP -> A NPBAR ; 0.00301204819277 \n
\n
# Lexical rules \n
ABBREVIATION -> abbreviation ; 1.0 \n
ABOUT -> about ; 1.0 \n
ADJP -> better ; 0.117647058824 \n
ADJP -> possible ; 0.0588235294118 \n
ADVP -> actually ; 0.0384615384615 \n