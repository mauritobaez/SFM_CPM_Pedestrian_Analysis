import csv
import json


with open('analisis/dec_60.json', 'r') as f:
    deceleration_info = json.load(f)["deceleration_info"]

# Prepare CSV file
with open('Des_all.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow([
        "ppee", "Tau1", "Tau2", "Tau3", "Tau4",
        "ECM1", "ECM2", "ECM3", "ECM4"
    ])

    for ped_code, events in deceleration_info.items():
        for i in range(1, 9):
            event_number = f"{i:02}"
            event = events.get(f"event_{i}", {})
            row = [
                f'{ped_code}{event_number}',               # ppee
                event.get("tau_both", ""),      # Tau1
                event.get("tau", ""),           # Tau2
                event.get("tau_vm_fix", ""),    # Tau3
                event.get("tau_following_distance", ""),  # Tau4
                event.get("ecm_both", ""),      # ECM1
                event.get("ecm", ""),           # ECM2
                event.get("ecm_vm_fix", ""),    # ECM3
                event.get("ecm_following_distance", "")   # ECM4
            ]
            writer.writerow(row)
