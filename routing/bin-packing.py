########## bin_packing.py ##########
# Source: https://www.localsolver.com/docs/last/exampletour/binpacking.html#tab-python


import localsolver
import sys
import math

if len(sys.argv) < 2:
    print ("Usage: python bin_packing.py inputFile [outputFile] [timeLimit]")
    sys.exit(1)


def read_integers(filename):
    with open(filename) as f:
        return [int(elem) for elem in f.read().split()]


with localsolver.LocalSolver() as ls:

    # Reads instance data
    file_it = iter(read_integers(sys.argv[1]))

    nb_items = int(next(file_it))
    bin_capacity= int(next(file_it))
    nb_max_bins = nb_items

    item_weights = [int(next(file_it)) for i in range(nb_items)]
    nb_min_bins = int(math.ceil(sum(item_weights)/float(bin_capacity)));

    # Declares the optimization model
    model = ls.model

    # Set decisions: bin[k] represents the items in bin k
    bins = [model.set(nb_max_bins) for k in range(nb_max_bins)]

    # Each item must be in one bin and one bin only
    model.constraint(model.partition(bins));

    weight_array = model.array(item_weights)
    weight_selector = model.function(lambda i: weight_array[i])

    # Weight constraint for each bin
    bin_weights = [model.sum(b, weight_selector) for b in bins]
    for w in bin_weights:
        model.constraint(w <= bin_capacity)

    # Bin k is used if at least one item is in it
    bins_used = [model.count(b) > 0 for b in bins]

    # Count the used bins
    totalBinsUsed = model.sum(bins_used)

    # Minimize the number of used bins
    model.minimize(totalBinsUsed)
    model.close()

    # Parameterizes the solver
    if len(sys.argv) >= 4: ls.param.time_limit = int(sys.argv[3])
    else: ls.param.time_limit = 5

    # Stop the search if the lower threshold is reached
    ls.param.set_objective_threshold(0, nb_min_bins);

    ls.solve()

    # Writes the solution in a file
    if len(sys.argv) >= 3:
        with open(sys.argv[2], 'w') as f:
            for k in range(nb_max_bins):
                if bins_used[k].value:
                    f.write("Bin weight: %d | Items: " % bin_weights[k].value);
                    for e in bins[k].value:
                        f.write("%d " % e)
                    f.write("\n")
