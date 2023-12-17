import pandas as pd


df = pd.read_csv('incidents.csv')
# df.head() #возвращает 5 строк

# задание 1
# print(df.describe()) # статистика числовых значений
# print(df.info()) # Тип, число и кол-во столбцов
# print(df.describe(include=["object"])) # статистика типа "объект" (число, кол-во уникальных значений, верхнее, частота самого частого значения)
# print(df.sort_values(by="crit_rate", ascending=False).head()) # Верхние пять по крит рейту

# # задание 2

df['SYTKI'] = pd.cut(pd.to_datetime(df.start_time).dt.hour, # бининг по началу времени(часа в фрейме)
                        bins = [0, 6, 12, 18, 24],    # значения интервалов
                        labels = ['night', 'morning', 'afternoon', 'evening'],  #названия интервалов
                        right = False,  #исключения самого правого значения
                        )

print(df.groupby(['name', 'SYTKI']).agg({'SYTKI': 'count'})) #Агрегирование по числу инцидентов в сутки для каждого нейма

#  задание 3

import requests
# # # #
# API_URL = 'https://d5d9e0b83lurt901t9ue.apigw.yandexcloud.net'
# # #
# # #
# # # # # в инцидентах, имеющих несколько ассетов ассеты не разделяются, т.к. с точки зрения предметной области разумно выделить в отдельную категорию инциденты, затрагивающие несколько типов систем сразу
# def get_assets_os(assets_id):
#      assets_os = set()
#      for asset_id in assets_id.split(','):
#       assets_os.add(requests.get(f'{API_URL}/get-asset-by-id', params={'asset-id': asset_id}).json().get('result', {}).get('os'))
#       # print(assets_os)
#      return str(assets_os)
#
#
# # # # to reduce requests count
# test_df = df.head(100).copy()
# test_df.loc[:, 'assets_id'] = test_df['assets_id'].apply(lambda x: str(x).replace("[", '').replace("]", '').replace("'", ''))
# test_df.loc[:, 'asset_os'] = test_df['assets_id'].apply(get_assets_os)
# result = test_df.groupby('asset_os').agg({'events_count': 'mean', 'crit_rate': 'mean'})
# print(result)
# # ЗАДАНИЕ 4
# df['start_time'] = pd.to_datetime(df.start_time)
# df['end_time'] = pd.to_datetime(df.end_time)
# df_copy = df.copy()
# df_copy['relation'] = df.apply(lambda x: x['events_count'] / (
#    (x['end_time'] - x['start_time']).total_seconds() # считает отношение кол-во среднего кол-во инцидентов к времени инциденты
# ), axis=1)
# df_copy
#
# df_copy.sort_values('relation', inplace=True) # сортирует отношения
# median = df.head(5)['crit_rate'].median() # выводит медиану первых пяти
#
# df_copy.loc[df.crit_rate > median] # оставляем только те, что выше медианы

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
#         user = requests.get(f'{API_URL}/get-asset-by-id', params={'asset-id': asset_id}).json().get('result', {}).get('account_name') # получаем названием аккаунта
#         users_levels.append(user_access_levels[user]) # заполняем список значениями
#     return sum(users_levels) / len(users_levels) # возвращаем средние значение

# to reduce requests count
# test_df = df.head(100).copy()
# test_df.loc[:, 'assets_id'] = test_df['assets_id'].apply(lambda x: str(x).replace("[", '').replace("]", '').replace("'", ''))
# test_df.loc[:, 'avg_access_level'] = test_df['assets_id'].apply(get_level_access_by_asset_id) # создаем столбец со средними значениями
# # test_df.loc[:, 'asset_os']
# result_df = test_df.groupby('name').apply(lambda group: group['','',''].corr()) # таблица корреляции группировка по типам инцидента
#
# result_df.drop(result_df[(result_df['avg_access_level'] == -1.0)].index, inplace=True)
# result_df.drop(result_df[(result_df['avg_access_level'] == 1.0)].index, inplace=True)
# print(result_df[(result_df['avg_access_level'].abs() == result_df['avg_access_level'].abs().max())].index) # корреляция друг с другом
#
# print(result_df[(result_df['avg_access_level'].abs() == result_df['avg_access_level'].abs().max())])