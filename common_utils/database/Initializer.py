from database import MySqlDB


class Initializer:
    __mapper = {
        'MysqlDB': MySqlDB.MysqlDatabase
    }

    __instances = {
        'MysqlDB': None
    }

    def __init__(self, db=None):
        if db is None:
            raise Exception('Please provide database to initialize')
        else:
            if self.__instances[db] is None:
                self.__instances[db] = self.__mapper[db]()

    def get_instance(self, db=None):
        if db is None:
            raise Exception('Please provide database to get instance')
        if self.__instances[db] is None:
            raise Exception('Please Initialize database first to get instance')
        return self.__instances[db]


if __name__ == "__main__":
    instance = Initializer('MysqlDB')
    print(instance.get_instance('MysqlDB'))
    print(MySqlDB.MysqlDatabase())
