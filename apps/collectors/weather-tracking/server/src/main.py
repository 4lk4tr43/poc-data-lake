from json import dumps, load
from os import environ
from time import sleep, time
from mariadb import ConnectionPool
from requests import exceptions, get, post


def get_secrets(path):
    return load(open(path, 'r', encoding='utf-8'))


def get_db_pool():
    pool = ConnectionPool(
        user='root',
        host='weather_tracking-db',
        port=3306,
        database='weather-tracking',
        pool_name='weather_tracking-pool',
        pool_size=5,
        pool_reset_connection=False,
    )
    connection = pool.get_connection()
    cursor = connection.cursor()

    cursor.execute('''create table if not exists measures(
        id int auto_increment,
        location varchar(255) not null,
        temperature float not null,
        created_at timestamp  default current_timestamp,
        primary key(id)
    )''')

    cursor.close()
    connection.close()

    return pool


def get_db(pool):
    connection = pool.get_connection()
    cursor = connection.cursor()
    return {'connection': connection, 'cursor': cursor}


def read_locations(path):
    return [_.rstrip() for _ in open(path, 'r', encoding='utf-8').readlines()]


def get_weather_data(location_desc, api_key):
    try:
        response = get(
            f'{environ.get("ENDPOINT")}?q={location_desc}&appid={api_key}').json()

    except exceptions.RequestException:
        sleep(300)
        return None

    return {
        'location': location_desc,
        'temperature': response['main']['temp'],
        'created_at': time()
    }


def set_weather_data_record(weather_record, database):
    if weather_record is None:
        return

    database['cursor'].execute('insert into measures (location, temperature) values (%s, %d)',
                               (weather_record['location'], weather_record['temperature']))
    database['connection'].commit()


db_pool = get_db_pool()
while True:
    try:
        db_instance = get_db(db_pool)
        locations = read_locations('/static/locations.txt')

        secrets = get_secrets('/secrets/api-keys.json')
        if secrets['OpenWeatherApiKey'] is None:
            print('Error: no secrets file found.'
                  'Please create a json file [service-descriptions/secrets/api-keys.json.] and '
                  'add an object with the attribute "OpenWeatherApiKey" containing your api key')
            continue

        for location in locations:
            record = get_weather_data(location, secrets['OpenWeatherApiKey'])
            set_weather_data_record(record, db_instance)
            post(
                'http://service-descriptions_kafka-queue_receiver_1:80/store',
                headers={'Content-Type': 'application/json'},
                data=dumps(record),
            )

        db_instance['cursor'].close()
        db_instance['connection'].close()

    except FileNotFoundError:
        print('Locations file not found.')

    finally:
        sleep(30)
