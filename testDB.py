import sqlite3

class DBManager:
    def __init__(self, pachDB):

        self.conn = sqlite3.connect(pachDB, check_same_thread=False)  # или :memory: чтобы сохранить в RAM
        self.cursor = self.conn.cursor()

    def creatTable(self):
        # Создание таблицы
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS bus (
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          MAGOR INTEGER,
          MINOR INTEGER,
          CarNumber TEXT,
          PRICE FLOAT)
                       """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS people (
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          FIRSTNAME TEXT,
          MIDNAME TEXT,
          LASTNAME TEXT,
          WALLET FLOAT,
          PHONE INT)
                       """)
        print("ok")

    def pullData(self, DBtable, data):
        # Вставляем множество данных в таблицу используя безопасный метод "?"
        albums = [('Exodus', 'Andy Hunter', '7/9/2002', 'Sparrow Records', 'CD'),
                  ('Until We Have Faces', 'Red', '2/1/2011', 'Essential Records', 'CD'),
                  ('The End is Where We Begin', 'Thousand Foot Krutch', '4/17/2012', 'TFKmusic', 'CD'),
                  ('The Good Life', 'Trip Lee', '4/10/2012', 'Reach Records', 'CD')]

        query = 'INSERT INTO ' + DBtable + ' VALUES (' + '?,'*(len(data[0])-1) + '?)'

        print(query)
        #"INSERT INTO albums VALUES (?,?,?,?,?)"
        self.cursor.executemany(query, data)
        self.conn.commit()

    def getDataBus(self, minor, magor):
        '''
        Получает данные о маршрутки и возвращает цену и ID маршрутки
        :param minor: номер автобуса
        :param magor: номер маршрута
        :return: [(3, 20.0)]
        '''
        a = self.cursor.execute("SELECT ID, PRICE FROM bus WHERE MAGOR = " + str(magor) + " AND MINOR = " + str(minor))

        return a.fetchall()

    def getDataPeopleWallet(self, phone, password):
        '''
        Получаем количество денег у пользователя
        :param phone:
        :param password:
        :return:
        '''
        wallet = self.cursor.execute("SELECT WALLET FROM people WHERE PHONE = " + str(phone) + " AND PASSWORD = " + str(password))

        return wallet.fetchall()

    def payment(self, phone, password, price):
        self.cursor.execute("UPDATE people SET WALLET = WALLET - " + str(price) + " WHERE PHONE = " + str(phone) + " AND password = " + str(password))
        self.conn.commit()

if __name__ == "__main__":
    test = DBManager('mydatabase.db')
    #test.creatTable()
    print(test.getDataBus(1, 2))
    busData = [(None, 4, 1, 'Л123ШВ123', 21.)]
    #test.pullData('bus', busData)
    test.payment("79132931468", "1234", 18)
    a = test.getDataPeopleWallet('79994318576', '1111')
    print(len(a))