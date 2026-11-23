from abtest.stats import sample_size_per_group, simulate_false_positive_rate, two_proportion_z

print(two_proportion_z(200, 2000, 250, 2000))
print("n per group to detect +1pp from 10%:", sample_size_per_group(0.10, 0.01))
print("A/A false positive rate:", simulate_false_positive_rate())
