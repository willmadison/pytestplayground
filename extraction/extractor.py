
def find_users_by_lastname(conn, last_name):
    cursor = conn.cursor()
    parameters = (last_name,)
    cursor.execute('SELECT * FROM users WHERE last_name = ?', parameters)
    return [User(i[0], i[1], i[2]) for i in cursor.fetchall()]


class User:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name


