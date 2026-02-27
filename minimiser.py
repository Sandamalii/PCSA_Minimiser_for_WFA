import math
from collections import defaultdict

class WFA_PCSA_Minimiser:
    def __init__(self, initial_weights, final_weights, transitions, tolerance=0):
        """
        Initialises the WFA and immediately converts it into the "Augmented" form.
        In augmented form, add an element $ to the alphabet.
        Automatically extracts all true states from the provided transitions and weights.

        """
        self.tolerance = tolerance
        self.out_edges = defaultdict(list)
        self.in_edges = defaultdict(list)
        self.true_states = set()

        # Add normal transitions and dynamically extract true states
        for start, symbol, target, weight in transitions:
            if weight != 0:
                self.add_edge(start, symbol, target, weight)
                self.true_states.update([start, target])

        # Encode initial weights and extract states (augmented automaton)
        for state, weight in initial_weights.items():
            if weight != 0:
                self.add_edge('i', '$', state, weight)
                self.true_states.add(state)

        # Encode final weights and extract states
        for state, weight in final_weights.items():
            if weight != 0:
                self.add_edge(state, '$', 't', weight)
                self.true_states.add(state)

        # The augmented automaton section 2.2
        self.states = self.true_states.union({'i', 't'})

    def add_edge(self, start, symbol, target, weight):
        self.out_edges[start].append((symbol, target, weight))
        self.in_edges[target].append((symbol, start, weight))

    def minimize(self):

        c_i, c_Q, c_t = 0, 1, 2
        classes = {
          c_i: {'i'},
          c_t: {'t'},
          c_Q: set(self.true_states)
        }
        print(classes)
        state_to_class_id = {}
        for pid, members in classes.items():
          for state in members:
              state_to_class_id[state] = pid

        next_cid = 3

        print(f"Initial classes: {[classes[c] for c in classes]}")

        queue = [c_Q, c_t]
        while queue:
          # pop the first class from the queue
          # It is the domain first explored
          D_id = queue.pop(0)
          if D_id not in classes:
              continue
          # get states in the domain
          D = classes[D_id]
          
          print("domain is", D, "---------------------")

          # collect affected classes from the selected domain
          affected_class_ids = set()
          for q in D: #for each state q in the domain
              for symbol, state, weight in self.in_edges[q]: #consider input edges to the q (from state to q)
                  # look at classes only with predecessors
                  #  as true_states are already collected, state is guaranteed to be in state_to_class_id
                  affected_class_ids.add(state_to_class_id[state])

          for c_id in list(affected_class_ids):
              states_in_class = classes[c_id]
              # split only if there is more than one state in a class
              if len(states_in_class) <= 1:
                  continue

              # finding the signature
              # signature is the summation of weights from a state to some other state that belongs to the considered domain D
              # so consider our edges where we can track transitions to a given state in the domain D
              signature_groups = defaultdict(list)

              for s in states_in_class: #get a state in the class
                  signature_dict = defaultdict(float)
                  for symbol, q, weight in self.out_edges[s]:
                      if state_to_class_id[q] == D_id: #q in Domain
                          signature_dict[symbol] += weight


                  # Apply error tolerance to cut down noise
                  processed_signature = []
                  for symbol, val in signature_dict.items():
                      if self.tolerance > 0.0:
                          decimals = abs(int(math.log10(self.tolerance)))
                          rounded_val = round(val, decimals)
                          if rounded_val != 0.0:
                              processed_signature.append((symbol, rounded_val))
                      else:
                          # Standard exact matching
                          if val != 0:
                              processed_signature.append((symbol, val))

                  # freeze the signature so the dictionary can hash it
                  sig_tuple = tuple(sorted(processed_signature))
                  signature_groups[sig_tuple].append(s)
                  print("sig group",signature_groups)

              # apply the split
              if len(signature_groups) > 1:
                  print(f"splitting class {states_in_class} into {list(signature_groups.values())}")

                  del classes[c_id]
                  if c_id in queue:
                      queue.remove(c_id)

                  for sig_tuple, members in signature_groups.items():
                      new_cid = next_cid
                      next_cid += 1

                      classes[new_cid] = set(members)
                      for m in members:
                          state_to_class_id[m] = new_cid

                      queue.append(new_cid)
        # print(signature_groups)
        return [c for c in classes.values() if not c.intersection({'i', 't'})]

