# PCSA Minimiser for Weighted Finite Automata

Implementation of the Predecessor Class Split Algorithm (PCSA) from Morphisms and Minimisation of Weighted Automata (Lombardy & Sakarovitch), with an optional tolerance parameter.

The original algorithm assumes exact equality in a semiring. Since this implementation targets WFAs with floating-point weights, it introduces an optional numerical tolerance parameter to handle approximate equality of state signatures. When tolerance is set to zero, the behaviour aligns with the exact comparison.

The implementation also follows the partition refinement strategy described in Section 5.1 of the paper. The theoretical algorithm achieves 
𝑂(𝑛(𝑚+𝑛)) time complexity (where 𝑛 is the number of states and 𝑚 is the number of transitions of the
automaton) by avoiding full comparison-based sorting and instead using hashmaps (weak sorting) of state signatures.

In practice, Python dictionaries are used to approximate this grouping mechanism. Due to language-level operations (e.g. hashing and signature processing), the exact theoretical complexity bound is not formally guaranteed, but the implementation preserves the same structure in the refinement strategy.
