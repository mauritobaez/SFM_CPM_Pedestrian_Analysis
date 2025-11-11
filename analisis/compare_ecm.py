import json
import numpy as np

# Read both JSON files
with open('analisis/dec_cpm_both_half_fix.json', 'r') as f:
    data_half = json.load(f)

with open('analisis/dec_cpm_both_no_tau.json', 'r') as f:
    data_fix = json.load(f)

# Lists to store all ECM differences
ecm_differences = []
relative_differences = []  # To store percentage differences
better_performance = {'half': 0, 'fix': 0}

# Iterate through all pedestrians and events
for ped_id, ped_data in data_half['deceleration_info'].items():
    for event_id, event_data in ped_data.items():
        # Get ECM values from both files
        ecm_half = event_data['ecm']
        ecm_fix = data_fix['deceleration_info'][ped_id][event_id]['ecm']
        
        # Calculate absolute difference
        difference = ecm_fix - ecm_half
        ecm_differences.append(difference)
        
        # Calculate relative difference (how many times bigger fix is compared to half)
        relative_diff = (ecm_fix / ecm_half) if ecm_half != 0 else float('inf')
        relative_differences.append(relative_diff)
        
        # Count which version performs better
        if ecm_half < ecm_fix:
            better_performance['half'] += 1
        else:
            better_performance['fix'] += 1

# Calculate statistics
avg_difference = np.mean(ecm_differences)
std_difference = np.std(ecm_differences)
median_difference = np.median(ecm_differences)

# Calculate relative statistics
avg_relative = np.mean(relative_differences)
median_relative = np.median(relative_differences)
std_relative = np.std(relative_differences)

print(f"ECM Comparison Statistics:")
print(f"Average difference (fix - half): {avg_difference:.6f}")
print(f"Standard deviation of differences: {std_difference:.6f}")
print(f"Median difference: {median_difference:.6f}")
print(f"\nRelative Comparison (fix/half):")
print(f"On average, fix version is {avg_relative:.2f}x times the half version")
print(f"Median: fix version is {median_relative:.2f}x times the half version")
print(f"Standard deviation of ratio: {std_relative:.2f}")
print("\nPerformance Comparison:")
print(f"Number of times half version was better: {better_performance['half']}")
print(f"Number of times fix version was better: {better_performance['fix']}")
print(f"Total comparisons: {len(ecm_differences)}")