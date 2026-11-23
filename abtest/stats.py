import math

import numpy as np


def two_proportion_z(x1: int, n1: int, x2: int, n2: int) -> dict:
    """Two-sided z-test for a difference in conversion rates (pooled variance)."""
    p1, p2 = x1 / n1, x2 / n2
    p = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se if se else 0.0
    p_value = math.erfc(abs(z) / math.sqrt(2))
    se_diff = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return {"p1": p1, "p2": p2, "lift": p2 - p1, "z": z, "p_value": p_value,
            "ci95": (p2 - p1 - 1.96 * se_diff, p2 - p1 + 1.96 * se_diff)}


def sample_size_per_group(p_base: float, mde: float, alpha_z: float = 1.96, power_z: float = 0.8416) -> int:
    """Approximate n per group to detect an absolute lift `mde` (alpha 0.05 two-sided, power 80%)."""
    p2 = p_base + mde
    var = p_base * (1 - p_base) + p2 * (1 - p2)
    return math.ceil((alpha_z + power_z) ** 2 * var / mde ** 2)


def bootstrap_diff_ci(a, b, n_boot: int = 2000, seed: int = 0):
    """95% bootstrap CI for mean(b) - mean(a)."""
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    diffs = [rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean() for _ in range(n_boot)]
    return tuple(np.percentile(diffs, [2.5, 97.5]))


def simulate_false_positive_rate(n: int = 2000, p: float = 0.1, runs: int = 500, seed: int = 1) -> float:
    """A/A test: both groups identical, so about 5% of runs should be 'significant'."""
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(runs):
        x1, x2 = rng.binomial(n, p), rng.binomial(n, p)
        hits += two_proportion_z(x1, n, x2, n)["p_value"] < 0.05
    return hits / runs
