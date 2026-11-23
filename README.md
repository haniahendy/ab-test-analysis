# ab-test-analysis

Statistics for A/B tests written from first principles: two-proportion z-test with confidence interval, sample-size calculation, bootstrap CI for means, and an A/A simulation to check the false-positive rate.

## Run
```bash
pip install -r requirements.txt
python -m pytest -q   # 5 tests
python run.py
```

## Measured result (23 Nov 2026)
- 200/2000 vs 250/2000 conversions: lift +2.5pp, z = 2.50, p = 0.0124, 95% CI for the lift 0.5pp to 4.5pp.
- Sample size to detect +1pp from a 10% baseline (alpha 0.05, power 80%): 14,749 per group.
- A/A simulation (500 runs): 4.0% significant, close to the expected 5%.
The z value was also checked by hand in the test.

## Limits
Normal approximation (not for tiny counts), fixed-horizon test only (peeking inflates false positives), no multiple-testing correction, no sequential or Bayesian methods.

## Provenance
A learning and portfolio project.
