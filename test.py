initial_weights = {0: 2, 1: 1, 2:0}
final_weights   = {0: 0, 1: 1, 2:1}
transitions = [
    (0, 'a', 0, -1), (1, 'a', 0, 1),(1, 'a', 2, 1),(2, 'a', 0, 1),(2, 'a', 2, 1),
    (0, 'b', 1, -1), (0, 'b', 2, 2) , (1, 'b', 1, -1) , (1, 'b', 2, 2) , (2, 'b', 2, 1)
]

minimiser = WFA_PCSA_Minimiser(initial_weights, final_weights, transitions, 0.0)
print("Minimal States:", minimiser.minimize())
