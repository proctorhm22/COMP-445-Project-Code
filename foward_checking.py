"""
Author:         Hannah Proctor
Assignment:     COMP 445 Research Project
Date:           March 10, 2025

Implementation of foward-checking algorithm to solve Parks problem instances (1-2 trees).** Pseudocode inspiration 
taken from class slides.

**Currently, all 2-tree problems are solved as if they are 1-tree problems. 
"""

# TODO: get 2-tree implementation working

# TODO: adjust comments in foward_checking() to better align with pseudocode

import copy
from park import Park

def start_search(park: Park, verbosity=0):
    # set of variables currently assigned
    done = set()
    return foward_checking(park.n, park.num_trees, park.variables, park.domains, done, 
                            pick_next_var(park.n, park.variables, park.domains, done), park, 
                                verbosity)

def foward_checking(n: int, num_trees: int, variables: set, domains: list, done: set, next_var: int, park: Park, 
                        verbosity: int):
    # if len(done) == len(variables): return domains
    if len(done) == 3*n:
        if verbosity > 0:
            print()
        return [domain.pop() for domain in domains[0:n]], park.num_nodes_explored
    # else: iterate through values in domains[next_var]
    values_to_try = domains[next_var]
    for value in values_to_try:
        # try it
        # new_domains[next_var] = {value}
        park.num_nodes_explored = park.num_nodes_explored + 1
        if verbosity > 0:
            print(f"next_var = {next_var}")
            print(f"\ttry {value}; {park.num_nodes_explored} nodes explored")
        new_domains = copy.copy(domains)
        new_domains = constraint_propogation(n, num_trees, variables, new_domains, value)
        if verbosity == 2:
            print(f"domains = {domains}")
            print(f"new_domains = {new_domains}")
        # if new_domains has no empty domains: ...
        noEmptyDomains = True
        for domain in new_domains:
            if len(domain) == 0:
            # if len(domain) < num_trees:
                noEmptyDomains = False
                break
        if noEmptyDomains:
            new_done = copy.copy(done)
            new_done.add(next_var)
            result = foward_checking(n, num_trees, variables, new_domains, new_done, 
                                     pick_next_var(n, variables, new_domains, new_done), park,
                                       verbosity) 	
            if result is not None:
                return result
    # tried all consistent values and none worked
    if verbosity > 0:
        print(f"backtrack [{next_var}]")
    return None


"""
Strategically picks next variable to try (minimum remaining value).
"""
def pick_next_var(n, variables, domains, done):
    i = 0
    while variables[i] in done and i < 3*n - 1:
        i = i + 1
    next_var = i
    min_len = len(domains[i])
    for j in range(i, 3*n):
        if variables[j] not in done and len(domains[j]) < min_len:
            next_var = j
            min_len = len(domains[j])
    return next_var


"""
Runs constraint propogation on the given set of domains. 
Constraints:    Exactly num_trees trees in each row, column, and color. 
                Trees cannot be placed adjacently (all surrounding cells blocked off).
"""
def constraint_propogation(n, num_trees, variables, domains, value):
    # value = (i, j)
    i = value[0]
    j = value[1]
    for k in range(0, 3*n):
        if value in domains[k]:
            domains[k] = {value}
        else:
            domains[k] = {coord for coord in domains[k] if coord[0] != i and coord[1] != j}
            domains[k] = domains[k] - {(i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)}
    return domains
    