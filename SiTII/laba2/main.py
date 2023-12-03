import xml.etree.ElementTree as ET
from sqlalchemy import text, Row
from sqlalchemy.engine import create_engine, Engine
import requests

incident_id = 664608

def get_table_data() -> dict[str, str]:
    """
    Принимаемые аргументы:
        - Функция не принимает никаких аргументов

    Возвращаемые значения:
        - Функция возвращает результат работы функции processing (см. выше)

    Работа функции:
        - С помощью контекстного менеджера with используем функцию connect() для создания соединения с
        БД.
        - Метод execute() выполняет запросы к БД. В данном случае SELECT запрос. Т.к. алхимия не принимает строки как
        запросы, поэтому преобразуем запрос с помощью функции text из библиотеки sqlalchemy.
        - Метод keys() возвращает названия столбцов таблицы.
        Тип данных: RMKeyView.
        Такой формат для удобной работы не подходит, поэтому явно преобразуем его в список (list).
        - Метод one() возвращает строку с данными из таблицы в виде кортежа (неизменяемого аналога списка).

    Дополнительные комментарии:
        Зачем используем контекстный менеджер?
            Если мы открыли соединение, то его надо закрыть.
            Писать engine.close() - дурной тон.
            Контекстынй менеджер открывает соеднинение и сам же его закрывает.
    """
    engine: Engine = create_engine(
        url='postgresql+psycopg2://postgres:123@localhost:5432/db1'
    )
    with engine.begin() as conn:
        db_response = conn.execute(text(f"SELECT * FROM sitii_lr2_incidents WHERE id = '{incident_id}'"))

    db_values = db_response.one()
    # print("db_response: ",db_response)
    # print("db_values: ",db_values)

    return {
        "Название": db_values[2],
        "Тип": db_values[4],
        "Количество событий, составляющих инцидент": db_values[5],
        "Критичность": db_values[6],
        "ID Активов": db_values[7],
        "ID Уязвимостей": db_values[8],
        "Время": f'Время: от {db_values[9].strftime("%d/%m/%Y, %H:%M:%S")} '
                 f'до {db_values[10].strftime("%d/%m/%Y, %H:%M:%S")}'
    }
def get_api_data(asset_id: str) -> dict[str, str | int]:
    """
    Принимаемые аргументы:
        - asset_id: ID актива.
          Тип данных: str

    Возвращаемые значения:
        - словарь, содержащий в себе следующие данные:
            - asset_id: идентификатор актива
            - asset_data: информация об активе
                - hostname: имя хоста
                - account_name: имя аккаунта
                - equipment_type: тип оборудования
        - все ключи и значения словаря имеют строковый тип данных (str)
          (кроме asset_data, у него значение dict[str, str]

    Работа функции:
        - по указанному URL отправляется get-запрос, с указанием метода get-asset-by-id.
          В URL параметром передаётся asset-id.
        - в headers говорим, что общаться с API мы будем в формате JSON.
        - чтобы получить данные из ответа (response) вызываем метод json() и по ключам получаем данные.
    """
    print(f"assed if {asset_id}")
    response = requests.get(
        url=f"https://d5d9e0b83lurt901t9ue.apigw.yandexcloud.net/get-asset-by-id?asset-id={asset_id}",
        headers={
            'content-type': 'application/json'
        }

    )
    print("assed if"+" " +asset_id)
    print({"ID актива": asset_id,"Данные актива": {
            'Имя хоста': response.json()['result']['hostname'],
            'Имя аккаунта': response.json()['result']['account_name'],
            'Тип оборудования': response.json()['result']['equipment_type']}})
    return {
        "ID актива": asset_id,
        "Данные актива": {
            'Имя хоста': response.json()['result']['hostname'],
            'Имя аккаунта': response.json()['result']['account_name'],
            'Тип оборудования': response.json()['result']['equipment_type']
        }
    }
def get_incident_data(vulner_id: str) -> dict[str, str]:
    """
        Принимаемые аргументы:
            - vulner_id: ID уязвимости.
              Тип данных: str
        
        Возвращаемые значения:
            - словарь со следующими данными:
                - vulner_id: ID уязвимости
                - vulner_title: Заголовок уязвимости

        Работа функции:
            - Метод parse() считывает XML файл.
            - Метод getroot() возрващает корневой элемент дерева.
            - В корневом элементе ищем единственный элемент под тегом 'vulnerabilities'.
              Внутри этого элемента ищем все элементы под тегом 'vulner'.
              Присваиваем все эти данные переменной vulnerabilities.
            - Циклом проходимся по каждому найденному элементу vulner.
              Если поле global_id совпадает с переданным в функцию значением,
              то возвращаем данные и завершаем работу функции.
    """
    root = ET.parse(f'asset_31873_vuln_report.xml').getroot()
    vulnerabilities = root.find('vulnerabilities').findall('vulner')
    print(vulnerabilities)
    for vulner in vulnerabilities:
        if str(vulner.find('global_id').text) == vulner_id:
            return {
                'ID уязвимости': vulner_id,
                'Название уязвимости': vulner.find('title').text
            }

def main():
    # Данные из таблицы из БД
    table_data = get_table_data()

    # Данные из API
    api_data = [get_api_data(asset_id) for asset_id in table_data['ID Активов']]

    # Данные из XML
    incidents_data = [get_incident_data(vulner_id) for vulner_id in table_data['ID Уязвимостей']]


    name = f'Название: {table_data["Название"]}\n'

    type = f'Тип: {table_data["Тип"]}\n'

    actions = f'Количество событий, составляющих инцидент: {table_data["Количество событий, составляющих инцидент"]}\n'

    crit_rate = f'Критичность: {table_data["Критичность"]}\n'

    usernames_hosts_etc = f'Названия учетных записей и хостов и типы связанных активов:\n'
    usernames_hosts_etc += "\n".join([f'\tID актива: {asset["ID актива"]}\n'
                                      f'\tИмя хоста: {asset["Данные актива"]["Имя хоста"]}\n'
                                      f'\tИмя аккаунта: {asset["Данные актива"]["Имя аккаунта"]}\n'
                                      f'\tТип оборудования: {asset["Данные актива"]["Тип оборудования"]}\n'
                                      for asset in api_data])

    vulnerabilities = f'Предполагаемые проэксплуатированные уязвимости:\n'
    vulnerabilities += "\n".join([f'\tID уязвимости: {incident_data["ID уязвимости"]}\n'
                                  f'\tНазвание уязвимости: {incident_data["Название уязвимости"]}\n'
                                  for incident_data in incidents_data])

    time_since_to = table_data['Время']

    with open('result.txt', 'w', encoding='utf-8') as result_file:
        result_file.write(name + type + actions + crit_rate + usernames_hosts_etc + vulnerabilities + time_since_to)

    print(name + type + actions + crit_rate + usernames_hosts_etc + vulnerabilities + time_since_to)

if __name__ == '__main__':
    main()

