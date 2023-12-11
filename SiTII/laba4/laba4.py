import pandas as pd
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 500)

df = pd.read_csv('incidents.csv')


# # задание 1
# print(df.describe()) #Знание статистических сведений о датафрейме
# print(df.info()) #Общая информация о датафрейме в виде заголовка, колличества значений и типов данных столбцов
# my_describe = df.describe(include=["object"]) #Знание статистических сведений о датафрейме, которые включают тип данных object
# my_describe.to_csv('my_describe.csv')
# sort_values = df.sort_values("crit_rate", ascending=False).head()
# sort_values.to_csv('sort_values.csv')

# задание 2

# df['start_tod'] = pd.cut(pd.to_datetime(df.start_time).dt.hour,
#                         bins = [0, 6, 12, 18, 24],
#                         labels = ['night', 'morning', 'afternoon', 'evening'],
#                         right = False)
#
#
# data = df.groupby(['name', 'start_tod']).agg({'start_tod': 'count'})
# data.to_csv('data.csv')


 # задание 3

import requests

API_URL = 'https://d5d9e0b83lurt901t9ue.apigw.yandexcloud.net'


 # в инцидентах, имеющих несколько ассетов ассеты не разделяются, т.к. с точки зрения предметной области разумно выделить в отдельную категорию инциденты, затрагивающие несколько типов систем сразу

def get_assets_os(assets_id):
    assets_os = set()
    for asset_id in assets_id.split(','):
        response = requests.get(f'{API_URL}/get-asset-by-id', params={'asset-id': asset_id}).json().get('result',{})
        assets_os.add(response.get('os'))
    return str(assets_os)

# to reduce requests count
test_df = df.head(100)
test_df.loc[:, 'assets_id'] = test_df['assets_id'].apply(lambda x: str(x).replace("[", '').replace("]", '').replace("'", ''))
test_df.loc[:, 'asset_os'] = test_df.assets_id.apply(get_assets_os)
result = test_df.groupby('asset_os').agg({'events_count': 'mean', 'crit_rate': 'mean'})

print(result)

# # ЗАДАНИЕ 4
# df['start_time'] = pd.to_datetime(df.start_time)
# df['end_time'] = pd.to_datetime(df.end_time)
# df_copy = df.copy()
# df_copy['relation'] = df.apply(lambda x: x['events_count'] / (
#    (x['end_time'] - x['start_time']).total_seconds()
# ), axis=1)
# df_copy
#
# df_copy.sort_values('relation', inplace=True)
# median = df.head(5)['crit_rate'].median()
#
# df_copy.loc[df.crit_rate > median]
#
# # задание 5
# user_access_levels = {
#     "admin": 1,
#     "user123": 0.4,
#     "dbadmin": 0.8,
#     "guest": 0.2,
#     "developer": 0.7,
#     "tester": 0.75,
#     "analyst": 0.6,
#     "operator": 0.5,
#     "manager": 0.65,
#     "consultant": 0.55,
# }
#
# def get_level_access_by_asset_id(assets_id):
#     users_levels = []
#     for asset_id in assets_id.split(','):
#         user = requests.get(f'{API_URL}/get-asset-by-id', params={'asset-id': asset_id}).json().get('result', {}).get('account_name')
#         users_levels.append(user_access_levels[user])
#     return sum(users_levels) / len(users_levels)
#
# # to reduce requests count
# test_df = df.head(100)
# test_df['assets_id'] = test_df['assets_id'].apply(lambda x: str(x).replace("[", '').replace("]", '').replace("'", ''))
# test_df['avg_access_level'] = test_df.assets_id.apply(get_level_access_by_asset_id)
#
# result_df = test_df.groupby('name').apply(lambda group: group['', '' ,''].corr())
# result_df
#
# result_df.drop(result_df[(result_df['avg_access_level'] == -1.0)].index, inplace=True)
# result_df.drop(result_df[(result_df['avg_access_level'] == 1.0)].index, inplace=True)
# print(result_df[(result_df['avg_access_level'].abs() == result_df['avg_access_level'].abs().max())].index)
#
# result_df[(result_df['avg_access_level'].abs() == result_df['avg_access_level'].abs().max())]