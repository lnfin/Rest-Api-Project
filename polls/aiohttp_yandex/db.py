from settings import config_db
import psycopg2

conf = config_db['postgres']


def time_check(hours):
    for hour in hours:
        try:
            h1 = int(hour[:2])
            m1 = int(hour[3:5])
            h2 = int(hour[6:8])
            m2 = int(hour[9:11])

            if 0 <= h1 <= 23 and 0 <= h2 <= 23 and 0 <= m1 <= 59 and 0 <= m2 <= 59:
                if h1 * 60 + m1 < h2 * 60 + m2:
                    return True
        except ValueError:
            return False
    return False


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(host=conf['host'],
                                     user=conf['user'],
                                     password=conf['password'],
                                     dbname=conf['database'])

    def add_courier(self, couriers):
        cur = self.conn.cursor()
        fields = ['courier_id', 'courier_type', 'regions', 'working_hours']
        errors = []
        success = []
        for courier in couriers:
            if fields == list(courier.keys()) and [] not in courier.values():
                if time_check(courier['working_hours']):
                    sql = f'''INSERT into couriers VALUES (\
                            {courier['courier_id']},\
                            '{courier['courier_type']}',\
                            '{str(set(courier['regions']))}',\
                            '{str(set(courier['working_hours'])).replace("'", '"')}');'''
                    cur.execute(sql)
                    success.append({'id': courier['courier_id']})
            else:
                errors.append({'id': courier['courier_id']})

        if errors:
            return False, errors
        else:
            self.conn.commit()
            return True, success
