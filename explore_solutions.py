import time
import os
import argparse
from sympy import sieve
from datetime import datetime


def explore_solutions(index_u, terms_max, r, primes_array, fl):
    """
    Iteratively computes cumulative sums of prime pair products and identifies 
    when the running total matches the structural form `objective = 2^a * (2^n - 1)`.
    
    The function leverages bitwise operations to efficiently test whether the 
    cumulative sum satisfies this condition.

    Args:
        index_u (int): Starting index in `primes_array` for the outer loop. 
        terms_max (int): Maximum number of consecutive prime pairs to sum 
                         in each iteration.
        r (int): Prime gap/offset parameter. Determines the shift applied to 
                 the second prime in each product pair.
        primes_array (list[int]): Precomputed array of prime numbers, 
                                  expected to be large enough to cover 
                                  indices up to `index_u + terms_max + r`.
        fl (io.TextIOWrapper): Open file handle for CSV output. Must remain 
                               open and writable during execution.

    Output Format (CSV Line):
        Writes a single line per solution containing:
        `first_term, last_term, terms, u, v, r, objective, a, power_2_a, n, m_n`

    Notes:
        - Deterministic: No randomness or external state modification.
    """

    objective = 0
    terms_counter = 0

    for i in range(1, terms_max + 1):
        p_actual = primes_array[index_u + i - 2]
        p_shifted = primes_array[index_u + i - 2 + r]
        
        term = p_actual * p_shifted
        terms_counter += 1
        objective += term

        # Isolates the lowest set bit (equivalent to 2^a)
        p2a = objective & -objective
        y = objective + p2a

        # Check if (objective + 2^a) is a power of 2
        if (y & (y - 1)):
            continue
        
        # Extract binary parameters: a=exponent, R=odd part, n=bit length
        a = p2a.bit_length() - 1    
        R = objective >> a
        n = R.bit_length()

        fl.write(f"{primes_array[index_u - 1]}*{primes_array[index_u - 1 + r]},"
                f"{p_actual}*{p_shifted},{terms_counter},{index_u},{index_u + i - 1},{r},"
                f"{objective},{a},{p2a},{n},{R}\n")


def get_args():
    parser = argparse.ArgumentParser(description="Experimental number theory computation")
    parser.add_argument("--u_min", type=int, default=1)
    parser.add_argument("--u_max", type=int, default=1000)
    parser.add_argument("--r_max", type=int, default=2**7)
    parser.add_argument("--terms_max", type=int, default=2**7)
    return parser.parse_args()


def validate_inputs(u_min, u_max, r_max, terms_max):
    assert u_min >= 1
    assert u_max >= u_min
    assert r_max >= 0
    assert terms_max > 0


def compute_mask(range_size):
    # Compute a bitmask to trigger checkpoints every ~10% of the u-range
    target = max(1, range_size // 10)
    power = 1 << (target.bit_length() - 1) 
    return power - 1


def main():
    args = get_args()

    index_u_min = args.u_min
    index_u_max = args.u_max
    r_max = args.r_max
    terms_max = args.terms_max

    validate_inputs(index_u_min, index_u_max, r_max, terms_max)

    print("Extracting primes from the sieve...")
    # Extend sieve limit to safely cover all required prime indexes
    sieve_limit = index_u_max + terms_max - 1 + r_max
    primes_array = list(sieve[1:sieve_limit + 1])
    print("Prime extraction complete.")

    assert len(primes_array) >= sieve_limit

    # Checkpoint calculation
    u_range = index_u_max - index_u_min + 1
    u_mask = compute_mask(u_range)

    # Execution
    t_ini = time.perf_counter()
    print("Working...")

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    filename = f"{index_u_min}-{index_u_max}-{r_max}-{terms_max}_{timestamp}.csv"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    filepath = os.path.join(results_dir, filename)

    with open(filepath, "w", encoding='utf-8', newline='') as fl:
        # Metadata
        fl.write(f"# u_min={index_u_min}, u_max={index_u_max}, r_max={r_max}, terms_max={terms_max}\n")
        fl.write(f"# sieve_limit={sieve_limit}\n")
        fl.write(f"# timestamp={timestamp}\n")
        # CSV Headers
        fl.write("first_term,last_term,terms,u,v,r,objective,a,power_2_a,n,m_n\n")

        for index_u in range(index_u_min, index_u_max + 1):
            # Bitwise checkpoint: prints when the lowest set bit aligns with the mask
            if not (index_u & u_mask):
                print(f"Checkpoint u: {index_u}")

            for r in range(0, r_max + 1):
                explore_solutions(index_u, terms_max, r, primes_array, fl)

    print("Finished.")

    t_end = time.perf_counter()
    total_time = t_end - t_ini

    print("-" * 30)
    print(f"Analysis completed in: {total_time:.4f} seconds")


if __name__ == "__main__":
    main()