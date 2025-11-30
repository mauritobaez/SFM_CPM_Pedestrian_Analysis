

import json
import numpy as np

with open('analisis/dec_60.json', 'r') as f:
    data = json.load(f)
deceleration_info = data['deceleration_info']


for ped_id, ped_data in deceleration_info.items():
    ecms = []
    taus = []
    taus_both = []
    ecms_both = []
    taus_fixed_vm = []
    ecms_fixed_vm = []
    taus_distance = []
    ecms_distance = []

    
    for event_key, event_data in ped_data.items():
        if event_key == 'avgs':
            continue
        taus.append(event_data['tau'])
        taus_both.append(event_data['tau_both'])
        taus_fixed_vm.append(event_data['tau_vm_fix'])
        taus_distance.append(event_data['tau_following_distance'])
        ecms.append(event_data['ecm'])
        ecms_both.append(event_data['ecm_both'])
        ecms_fixed_vm.append(event_data['ecm_vm_fix'])
        ecms_distance.append(event_data['ecm_following_distance'])
    
    
    avg_tau = np.mean(taus) if taus else None
    std_tau = np.std(taus) if taus else None

    avg_tau_both = np.mean(taus_both) if taus_both else None
    std_tau_both = np.std(taus_both) if taus_both else None
    
    avg_tau_fixed_vm = np.mean(taus_fixed_vm) if taus_fixed_vm else None
    std_tau_fixed_vm = np.std(taus_fixed_vm) if taus_fixed_vm else None
    
    avg_tau_distance = np.mean(taus_distance) if taus_distance else None
    std_tau_distance = np.std(taus_distance) if taus_distance else None
    
    avg_ecm = np.mean(ecms) if ecms else None
    avg_ecm_both = np.mean(ecms_both) if ecms_both else None
    avg_ecm_fixed_vm = np.mean(ecms_fixed_vm) if ecms_fixed_vm else None
    avg_ecm_distance = np.mean(ecms_distance) if ecms_distance else None
    std_ecm = np.std(ecms) if ecms else None
    std_ecm_both = np.std(ecms_both) if ecms_both else None
    std_ecm_fixed_vm = np.std(ecms_fixed_vm) if ecms_fixed_vm else None
    std_ecm_distance = np.std(ecms_distance) if ecms_distance else None
    
    
    ped_data['avgs'] = {
        'avg_tau_dec': avg_tau,
        'std_tau_dec': std_tau,
        'avg_tau_both': avg_tau_both,
        'std_tau_both': std_tau_both,
        'avg_tau_fixed_vm': avg_tau_fixed_vm,
        'std_tau_fixed_vm': std_tau_fixed_vm,
        'avg_tau_distance': avg_tau_distance,
        'std_tau_distance': std_tau_distance,
        'avg_ecm_dec': avg_ecm,
        'std_ecm_dec': std_ecm,
        'avg_ecm_both': avg_ecm_both,
        'std_ecm_both': std_ecm_both,
        'avg_ecm_fixed_vm': avg_ecm_fixed_vm,
        'std_ecm_fixed_vm': std_ecm_fixed_vm,
        'avg_ecm_distance': avg_ecm_distance,
        'std_ecm_distance': std_ecm_distance
    }


with open('analisis/dec_60.json', 'w') as f:
    json.dump(data, f, indent=4)

