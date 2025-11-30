from scipy.stats import kruskal
import json
import matplotlib.pyplot as plt

ACC = 'ACC'
DEC = 'DEC'
file_name = 'acc_60_I2T'
data_chosen = 'taus'
title = 'SFM Acceleration Tau Boxplot'
y_label = 'Tau'
process = ACC # ACC or DEC


with open(f'./analisis/{file_name}.json', 'r') as f:
    data = json.load(f)

all_datasets = []

if process == ACC:
    for ped_id, ped_data in data['pastos'].items():
        all_datasets.append(ped_data[data_chosen])
elif process == DEC:
    for ped_id, ped_events in data['deceleration_info'].items():
        curr_ped_data = []
        for event_name, event_data in ped_events.items():
            if event_name == 'avgs':
                continue
            curr_ped_data.append(event_data[data_chosen])
        all_datasets.append(curr_ped_data)


stat, p = kruskal(*all_datasets)

print("Kruskal-Wallis H-statistic:", stat)
print("p-value:", p)


k = len(all_datasets)
n = sum(len(t) for t in all_datasets)

eta2 = (stat - k + 1) / (n - k)
print("Effect size (eta²):", eta2)

plt.boxplot(all_datasets, showfliers=True)
plt.gcf().set_size_inches(14, 8)

ax = plt.gca()
plt.xlabel("Pedestrian", fontsize=24)
plt.ylabel(y_label, fontsize=24)
plt.title(title, fontsize=26)
plt.xticks(rotation=45, ha='right', fontsize=20)
plt.yticks(fontsize=20)

# Thicken boxplot lines for better visibility
for artist in ax.artists:  # boxes
    artist.set_edgecolor('black')
    artist.set_linewidth(1.5)
for line in ax.lines:  # whiskers, medians, caps
    line.set_linewidth(1.5)

plt.tight_layout()
plt.show()

