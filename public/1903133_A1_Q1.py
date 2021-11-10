# coding: utf-8

def check_problem_instance(N,minterms,dont_cares,variable_names):
	# A function to check if the minterms and dont_cares lists are valid.
	# The list should have no duplicates, be in ascending order, 
	# and each entry should be between 0 and 2^N -1.
	print("Problem Instance:")
	print("---------------------------")
	print("Variables:",variable_names)
	print("Minterms:",minterms)
	print("Don't cares:",dont_cares)
	print("---------------------------")

	print "Checking problem instance...",
	m1 = [x for x in sorted(set(minterms)) if (x>=0 and x<(2**N))]
	d1 = [x for x in sorted(set(dont_cares)) if (x>=0 and x<(2**N))]
	assert(minterms == m1), "ERROR: The minterm list is Invalid."
	assert(dont_cares == d1), "ERROR: The dont_cares list is invalid."
	assert (not (set(minterms)&set(dont_cares))), "ERROR: The minterms list and dont_cares list have some common elements."
	print("OK.")


minterms = [int(i) for i in raw_input("Enter minterms seperated by commas: ").split(",")]
dont_cares = [int(i) for i in raw_input("Enter don't care seperated by commas: ").split(",")]
variables_name = [str(i) for i in raw_input("Enter variables name seperated by commas: ").split(",")]
N = len(variables_name)
check_problem_instance(N,minterms,dont_cares,variables_name)

def convert_to_binary(x,N):
    binary= []
    for i in range(0,N):
        bit = x & 1
        binary.insert(0,bit)
        x = x >> 1
    return binary

import copy

class Term(object):
    def __init__(self,N,minterm):
        self.N=N
        self.minterms_covered=set([minterm])
        self.binary=convert_to_binary(minterm,N)
        self.was_combined=False
    def try_combining(self,other_term):
        assert(self.N==other_term.N)
        a=self.binary
        b=other_term.binary
        combined_term = copy.deepcopy(self)
        combined_term.was_combined=False
        count = 0
        for i in range(0,len(a)):
            if(a[i] != b[i]):
                if(a[i]== '-' or b[i] == '-'):
                    return False,None
                else:
                    count += 1
                    combined_term.binary[i] = '-'
                if count > 1:
                    return False,None
        combined_term.minterms_covered = self.minterms_covered.union(other_term.minterms_covered)
        self.was_combined = True
        other_term.was_combined = True
        return True, combined_term
    def __str__(self):
        s = str(self.minterms_covered)+ "  " + str(self.binary)
        if self.was_combined:
            s+= u'\u2713'.encode('utf-8')
        return s
	
def find_prime_implicants(minterms, dont_cares,N):
    prime_implicants = []
    G = []
    for i in range(0,N+1):
        G.append([])
    G_NEXT = []
    for i in range(0,N+1):
        G_NEXT.append([])
    print("Grouping the minterms and don't care terms based on the number of ones:")
    for m in (minterms + dont_cares):
        t = Term(N, m)
        num_of_ones = t.binary.count(1)
        G[num_of_ones].append(t)
    for i in range(0,len(G)):
        print("GROUP", i,"--------")
        for m in G[i]:
            print "\t",m
    print("Combining terms in adjacent groups...")

    converged = False
    iteration = 0

    while(not converged):
        print("====================")
        print("Pass:", iteration+1)
        print("====================")

        for i in range(len(G) - 1):
            for j in (G[i]):
                for k in (G[i+1]):
                    x = j.try_combining(k)
                    if(x[0]):
                        already = False
                        for element in G_NEXT[i]:
                            if(element.__str__().split("  ")[1] == x[1].__str__().split('  ')[1]):
                                already = True
                        if(not already):
                            G_NEXT[i].append(x[1])
        for i in range(len(G)):
            print "Group", i,"- - - - - -"
            for m in G[i]:
                print "\t",m
        converged = True
        for grp in range(len(G)):
            for i in range(len(G[grp])):
                if(G[grp][i].was_combined):
                    converged = False
                else:
                    if(G[grp][i] not in prime_implicants):
                        prime_implicants.append(G[grp][i])
        print("\n Prime implicants identified by the end of this phase: ")
        for m in prime_implicants:
            print "\t",m
        G = G_NEXT
        G_NEXT = []
        for i in range(N+1):
            G_NEXT.append([])
        iteration += 1
    return prime_implicants
def print_implicants(PI,N,variable_names):
	for i in range(len(PI)):
		for j in range(N):
			if PI[i].binary[j]==1:
				print variable_names[j],
			if PI[i].binary[j]==0:
				print variable_names[j]+"'",
		if (i<len(PI)-1):
			print "  ",
	print("")



PI = find_prime_implicants(minterms,dont_cares,N)
print "\nPrime Implicants are: ",
print_implicants(PI, N, variables_name)