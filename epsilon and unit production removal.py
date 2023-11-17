# A class to represent a context free grammar
class CFG:
    # Initialize the grammar with a set of terminals, non-terminals, productions and start symbol
    def _init_(self, terminals, non_terminals, productions, start):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.start = start

    # A method to remove epsilon productions from the grammar
    def remove_epsilon_productions(self):
        # Find all the nullable non-terminals, i.e. those that can derive epsilon
        nullable = set()
        for nt in self.non_terminals:
            if [] in self.productions[nt]:
                nullable.add(nt)
        # Repeat until no new nullable non-terminals are found
        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for rhs in self.productions[nt]:
                    # If all the symbols in the right hand side are nullable, then the left hand side is also nullable
                    if all(symbol in nullable for symbol in rhs) and nt not in nullable:
                        nullable.add(nt)
                        changed = True
        # Remove the epsilon productions and add new productions without the nullable symbols
        new_productions = {}
        for nt in self.non_terminals:
            new_productions[nt] = []
            for rhs in self.productions[nt]:
                # If the right hand side is not epsilon, add it to the new productions
                if rhs != []:
                    new_productions[nt].append(rhs)
                    # For each nullable symbol in the right hand side, add a new production without that symbol
                    for i, symbol in enumerate(rhs):
                        if symbol in nullable:
                            new_rhs = rhs[:i] + rhs[i+1:]
                            if new_rhs not in new_productions[nt]:
                                new_productions[nt].append(new_rhs)
        # Update the productions of the grammar
        self.productions = new_productions

    # A method to remove unit productions from the grammar
    def remove_unit_productions(self):
        # Find all the unit pairs, i.e. pairs of non-terminals (A, B) such that A =>* B
        unit_pairs = set()
        for nt in self.non_terminals:
            # Initialize the unit pairs with the reflexive pairs
            unit_pairs.add((nt, nt))
            # Repeat until no new unit pairs are found
            changed = True
            while changed:
                changed = False
                # Use a copy of the set to avoid modifying it while iterating
                for pair in unit_pairs.copy():
                    # If A =>* B and B -> C, then A =>* C
                    if pair[0] == nt:
                        for rhs in self.productions[pair[1]]:
                            if len(rhs) == 1 and rhs[0] in self.non_terminals and (nt, rhs[0]) not in unit_pairs:
                                unit_pairs.add((nt, rhs[0]))
                                changed = True
        # Remove the unit productions and add new productions with the non-unit right hand sides
        new_productions = {}
        for nt in self.non_terminals:
            new_productions[nt] = []
            for rhs in self.productions[nt]:
                # If the right hand side is not unit, add it to the new productions
                if not (len(rhs) == 1 and rhs[0] in self.non_terminals):
                    new_productions[nt].append(rhs)
                else:
                    # For each unit pair (A, B) such that A -> B, add the non-unit productions of B to A
                    for pair in unit_pairs:
                        if pair[0] == nt and pair[1] == rhs[0]:
                            for new_rhs in self.productions[pair[1]]:
                                if not (len(new_rhs) == 1 and new_rhs[0] in self.non_terminals) and new_rhs not in new_productions[nt]:
                                    new_productions[nt].append(new_rhs)
        # Update the productions of the grammar
        self.productions = new_productions

    # A method to print the grammar in a readable format
    def print_grammar(self):
        print(f"Terminals: {self.terminals}")
        print(f"Non-terminals: {self.non_terminals}")
        print(f"Start symbol: {self.start}")
        print("Productions:")
        for nt in self.non_terminals:
            print(f"{nt} -> {' | '.join(''.join(rhs) for rhs in self.productions[nt])}")

# A driver code to test the methods
if _name_ == "_main_":
    # Define a grammar with epsilon and unit productions
    terminals = {'a', 'b', 'c'}
    non_terminals = {'S', 'A', 'B', 'C'}
    productions = {
        'S': [['A', 'B'], ['C']],
        'A': [['a', 'A'], []],
        'B': [['b', 'B'], ['c']],
        'C': [['S'], ['c', 'C']]
    }
    start = 'S'
    # Create a CFG object
    cfg = CFG(terminals, non_terminals, productions, start)
    # Print the original grammar
    print("Original grammar:")
    cfg.print_grammar()
    # Remove epsilon productions
    cfg.remove_epsilon_productions()
    # Print the grammar after removing epsilon productions
    print("Grammar after removing epsilon productions:")
    cfg.print_grammar()
    # Remove unit productions
    cfg.remove_unit_productions()
    # Print the grammar after removing unit productions
    print("Grammar after removing unit productions:")
    cfg.print_grammar()