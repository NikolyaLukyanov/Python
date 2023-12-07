import pandas as pd
import csv

with open('944_corrupted_incidents.csv', encoding="UTF-8") as csv_file:
    table = csv.reader(csv_file)
    log_data = {
        'id': [],
        'name': [],
        'description': [],
        'type': [],
        'events_count': [],
        'crit_rate': [],
        'assets_id': [],
        'vulnerabilities_id': [],
        'start_time': [],
        'end_time': []
    }

    for i, row in enumerate(table):
        if i == 0:
            continue
        log_data['id'].append(row[1])
        log_data['name'].append(row[2])
        log_data['description'].append(row[3])
        log_data['type'].append(row[4])
        log_data['events_count'].append(row[5])
        log_data['crit_rate'].append(row[6])
        log_data['assets_id'].append(row[7])
        log_data['vulnerabilities_id'].append(row[8])
        log_data['start_time'].append(row[9])
        log_data['end_time'].append(row[10])
df = pd.DataFrame(log_data)
