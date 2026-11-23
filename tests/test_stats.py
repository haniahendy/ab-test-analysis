import numpy as np
import pytest

from abtest.stats import bootstrap_diff_ci, sample_size_per_group, simulate_false_positive_rate, two_proportion_z


def test_known_z_test_values():
    r = two_proportion_z(200, 2000, 250, 2000)
    assert r["p2"] == 0.125 and r["p1"] == 0.1 and r["lift"] == pytest.approx(0.025)
    assert r["z"] == pytest.approx(2.5, abs=0.01)  # hand check: 0.025 / sqrt(0.1125*0.8875*2/2000)
    assert 0.01 < r["p_value"] < 0.03
    assert r["ci95"][0] < r["lift"] < r["ci95"][1]


def test_identical_groups_not_significant():
    r = two_proportion_z(100, 1000, 100, 1000)
    assert r["z"] == 0 and r["p_value"] == pytest.approx(1.0)


def test_sample_size_matches_textbook_order():
    # detecting +1pp from 10% needs roughly 14-15k per group
    assert 14000 < sample_size_per_group(0.10, 0.01) < 15500


def test_aa_false_positive_rate_near_five_percent():
    assert 0.02 < simulate_false_positive_rate() < 0.09


def test_bootstrap_ci_contains_true_difference():
    rng = np.random.default_rng(0)
    a, b = rng.normal(0, 1, 500), rng.normal(0.5, 1, 500)
    lo, hi = bootstrap_diff_ci(a, b)
    assert lo < 0.5 < hi and lo > 0
