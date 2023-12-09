import pandas as pd

df = pd.read_csv('944_corrupted_incidents.csv')
# Убираем дубликаты
df.drop_duplicates(
    subset=['name', 'description', 'type', 'events_count', 'crit_rate', 'assets_id', 'vulnerabilities_id', 'start_time',
            'end_time'],
    inplace=True,
    ignore_index=True,
)
# Исправляем description
count = 0
while count < len(df['type'].values):
    df['description'].values[count] = f'Обнаружена активность "{df['type'].values[count]}" с уязвимостями {str(df['vulnerabilities_id'].values[count].replace('[','').replace(']','').replace("'","").replace("'",""))}'
    count += 1


df = df.loc[df['events_count'] > 0]
df = df.dropna()


df.to_csv('csv_copy.csv', index=False)
