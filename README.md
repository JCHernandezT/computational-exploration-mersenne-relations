# Computational Exploration of the S(u,v,r) Relation

This repository contains the code used to perform the computational experiment described in *Observaciones Sobre Sumas de Productos deSucesiones de Primos y Números de Mersenne*.

The implementation is designed for deterministic exploration in number theory, with emphasis on performance and reproducibility.


## Requirements

* Python 3
* `sympy`

Optional:

* PyPy (Highly recommended for significant performance improvements)

Install dependencies with:

```
pip install sympy==1.14.0
```

## Scripts

This repository contains two independent scripts:

### 1. explore_solutions.py

---

Performs experimental exploration over parameter ranges.
This script is used to generate the main CSV datasets used in the research note.

#### Usage

Run this command to explore solutions:

```
python explore_solutions.py --u_min 1 --u_max 128 --r_max 128 --terms_max 128
```

#### Parameters

* `--u_min`
  Lower bound of the index (u).
  Must satisfy: `u_min >= 1`

* `--u_max`
  Upper bound of the index (u).
  Must satisfy: `u_max >= u_min`

* `--r_max`
  Upper bound of parameter (r).
  Must satisfy: `r_max > 0`

* `--terms_max`
  Maximum number of terms (t) considered in the internal computation.
  Must satisfy: `terms_max > 0`

#### Output

Results are written to CSV files stored in:

```
./results/
```

Each file includes:

* Metadata header (parameters, sieve size, timestamp)
* Computed results

File naming convention:

```
{u_min}-{u_max}-{r_max}-{terms_max}_{timestamp}.csv
```

Example:

```
./results/1-20000-65536-8192_20260430-164131.csv
```
#### Output Format

The CSV files contain the following columns:

- `first_term`: Product of the initial prime pair.
- `last_term`: Product of the last prime pair.
- `terms`: Cumulative count of terms summed to reach `objective`.
- `u`, `v`: Indices in `primes_array` corresponding to the solution.
- `r`: shift parameter.
- `objective`: The cumulative sum (S) that satisfied the condition.
- `a`: Exponent such that `2^a`.
- `power_2_a`: Value `2^a`.
- `n`: Exponent of the Mersenne Number `2^n - 1`.
- `m_n`: The Mersenne Number, where `R = 2^n - 1` (matches `n` in the header).

#### Notes

* Filenames are automatically generated at runtime.
* Each execution produces a unique file (no overwriting).
* The naming convention allows easy identification and comparison across experiments.


### 2. compute_s.py

---

Computes the main function (S) studied in the reaseach note for given inputs.
This script can be used independently for validation and analysis.

#### Usage

Run this command to explore solutions:

```
python compute_s.py --u 1 --v 13 --r 2
```

#### Parameters

* `--u`
  Must satisfy: `u >= 1`

* `--v`
  Must satisfy: `v >= u`

* `--r`
  Must satisfy: `r >= 0`

#### Output

Results are written to CSV files stored in:

```
./results/
```
Each file includes:

* Total Sum (S) header S_(u, v, r), terms
* Computed terms of the sum.

File naming convention:

```
S_{u}-{v}-{r}.csv
```

Example:

```
./results/S_1-13-2.csv
```

#### Output Format

The CSV files contain the following columns:

- `i`: Index of the first prime in the term pair.
- `p_i`: The prime at index `i`.
- `i+r`: Index of the second prime in the term pair.
- `p_{i+r}`, The prime at index `i + r`.
- `product`: The computed term `(p_i * p_{i+r})`.

## Experimental Setup

The exploration was divided into two main scenarios.
Parameter ranges were selected based on computational constraints and preliminary empirical behavior.

### Scenario 1

* `u_min = 1`
* `u_max = 20000`
* `r_max = 2^16 = 65536`
* `terms_max = 2^13 = 8192`

Execution time (using PyPy):

```
39194.9366 seconds (~10.9 hours)
```

Output:

```
./results/1-20000-65536-8192_20260430-164131.csv
```

---

### Scenario 2

* `u_min = 1`
* `u_max = 10`
* `r_max = 2^27 = 134217728`
* `terms_max = 2^13 = 8192`

Execution time (using PyPy):

```
40480.2096 seconds (~11.2 hours)
```

Output:

```
./results/1-10-134217728-8192_20260429-153828.csv
```


## Computational Notes

* The implementation is fully deterministic.
* Progress monitoring is performed using lightweight bitwise checkpoints to minimize overhead.
* Output is streamed directly to disk to handle large-scale runs.



## Limitations

* Due to internal constraints of `sympy` (specifically array size limitations in the sieve implementation),
  a practical upper bound is imposed:

```
r_max <= 2^27
```

* Larger values may result errors or undefined behavior.


## Reproducibility

* All experiments are parameter-driven and deterministic.
* Output files contain sufficient metadata to reproduce each run.
* The computational environment can be recreated using the listed dependencies.


## Notes

* This repository provides the experimental framework and data generation pipeline used in the study.



## Citation

If you use this code, please cite:

Juan Camilo Hernández-Torres, *"Observaciones Sobre ...."*, 2026.

DOI: [10.5281/zenodo.20060273](https://doi.org/10.5281/zenodo.20060273)
