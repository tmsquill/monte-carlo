from argparse import ArgumentParser
from pprint import pprint
from random import randint

def shape_load(shape_file):

    with open(shape_file, "r") as f:

        return [line.rstrip() for line in f.readlines()]

def shape_bounds(shape):

    width = len(max(shape, key=len))
    height = len(shape)

    return width, height

def shape_padding(shape, bounds):

    width, _ = bounds

    return [line.ljust(width, " ") for line in shape]

def monte_carlo(shape, bounds, darts=100):

    hits = 0
    width, height = bounds

    for _ in range(darts):

        x, y = (randint(0, width - 1), randint(0, height - 1))

        if shape[y][x] == "X":

            hits = hits + 1

        shape[y][x] = "*"

    return shape, hits, darts


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument("shape_file", help="path to a shape file")
    parser.add_argument("-d", "--darts", type=int, default=100, help="the number of samples to take")

    args = parser.parse_args()

    # Load the shape from the file.
    shape = shape_load(args.shape_file)

    # Determine the size of the bounding square.
    bounds = shape_bounds(shape)

    # Insert padding to make the shape fit the bounds of the square.
    shape = shape_padding(shape, bounds)

    # Strings are immutable, convert to list of lists for simulation.
    shape = [list(line) for line in shape]

    # Run the Monte Carlo simulation.
    shape, hits, darts = monte_carlo(shape, bounds, darts=args.darts)

    # Convert back to list of strings for pretty-printing result.
    shape = ["".join(line) for line in shape]

    print("Hits: {} | Bounding Box Area: {} | Shape Area (Monte Carlo): {}".format(
        hits,
        bounds[0] * bounds[1],
        bounds[0] * bounds[1] * (float(hits) / float(darts))
    ))

    pprint(shape)
