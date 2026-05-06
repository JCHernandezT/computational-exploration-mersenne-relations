from sympy import sieve
import argparse
import os
import csv


def get_args():
    parser = argparse.ArgumentParser(description="Validation script for u, v, r parameters")
    parser.add_argument("--u", type=int, default=1)
    parser.add_argument("--v", type=int, default=13)
    parser.add_argument("--r", type=int, default=2)
    return parser.parse_args()


def validate_inputs(u, v, r):
    assert u >= 1, "u must be > 1"
    assert v >= 1, "v must be > 1"
    assert r >= 0, "r must be >= 0"
    assert v >= u, "v must be >= u"


def main():
    """
    Computes and validates the sum S(u, v, r) = Σ_{i=u}^{v} p_i * p_{i+r},
    where p_i denotes the i-th prime number and r is a fixed shift.

    Output:
        A CSV file named S_<u>_<v>_<r>.csv containing:
        - Metadata header with the final sum and term count
        - Columns: i, p_i, i+r, p_{i+r}, product
    """
    args = get_args()

    index_u = args.u
    index_v = args.v
    r = args.r

    validate_inputs(index_u, index_v, r)
    
    print("Extracting primes from the sieve...")
    # Sympy sieve uses 1-based indexing; slice must extend to index_v + r to cover shifted primes
    primes_array = list(sieve[index_u: index_v + r + 1])
    print("Prime extraction complete...")

    filename = f"S_{index_u}-{index_v}-{r}.csv"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    filepath = os.path.join(results_dir, filename)

    sum = 0
    terms_counter = 0
    terms_list = []

    print("Working...")

    # Range covers terms from i=u to i=v (inclusive); +2 accounts for Python's exclusive upper bound
    for i in range(1, index_v - index_u + 2):
        p_actual = primes_array[i - 1]
        p_shifted = primes_array[i - 1 + r]

        term = p_actual * p_shifted
        terms_counter += 1
        sum += term
         # Map loop counter i back to original prime indices: actual_index = i + index_u - 1
        terms_list.append([i + index_u - 1, p_actual, i + r + index_u - 1, p_shifted, term])

    with open(filepath, "w", encoding='utf-8', newline='') as fl:
        writer = csv.writer(fl)
        fl.write(f"# S_({index_u},{index_v},{r}) = {sum}, terms: {terms_counter}\n")
        # CSV Headers
        writer.writerow(['i', 'p_i', 'i+r', 'p_{i+r}', 'product'])
        writer.writerows(terms_list)

    print(f"Completed.")


if __name__ == '__main__':
   main()