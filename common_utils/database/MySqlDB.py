import sys,os
import mysql.connector.pooling
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from database.BaseDB import BaseDatabase
from helpers import common_ut as common_util

def convert_to_dict(columns_, results):
    allResults = []
    columns = [columns[0] for col in columns_]
    if type(results) is list:
        for value in results:
            allResults.append(dict(zip(columns, value)))
        return allResults
    elif type(results) is tuple:
        allResults.append(dict(zip(columns, results)))
        return allResults
 
 
def make_dict_factory(cursor):
    column_names = [d[0].lower() for d in cursor.description]
 
    def create_row(*args):
        return dict(zip(column_names, args))
 
    return create_row
 
 
def query_from_data(insert_data):  #formulate query for insert data
    condition = ''
    for key,value in insert_data.items():
        if type(value) == str:
            condition += "'{}'".format(value)+','
        else:
            condition += '{}'.format(value)+','
 
    return condition[:-1]



def query_from_filter(filters, type_='AND', search=False):
    params = ''
 
    if search:
        for key, value in filters.items():
            params += "lower({0}) LIKE '%{1}%' {2} ".format(key, value.lower(), type)
    else:
        for key, value in filters.items():
            if type(value) == str:
                params += "%s = '%s' %s " % (key, value, type_)
            else:
                params += '''{} = {} {} '''.format(key, value, type_)
 
 
    return params[:-(len(type_)+2)]


class MysqlDatabase(BaseDatabase):
    __instance = None
    __connected = False
    logger = False

    def __init__(self, logger_, **kwargs):
        """
        :param kwargs:
        """
        self.logger = logger_
        self.__cnx_pool = None
        self.pool_name = kwargs.get('mysql_pool_name', '')
        self.pool_size = int(kwargs.get('mysql_pool_size', 10))
        self.host = kwargs.get('mysql_host', 'localhost')
        self.port = kwargs.get('mysql_port', 3306)
        self.user = kwargs.get('mysql_user', 'root')
        self.password = kwargs.get('mysql_password', '')
        self.auth_plugin= kwargs.get('auth_plugin', 'mysql_native_password')
        self.database = kwargs.get('database_name', '')
        super(MysqlDatabase, self).__init__()

    def connect(self):
        """
        :return:
        """
        try:
            self.__cnx_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                host=self.host, 
                port=self.port,
                user=self.user, 
                password=self.password,
                database=self.database,
                autocommit=True,
                auth_plugin =self.auth_plugin
            )
            self.__connected = True
        except Exception as e:
            error = common_util.get_error_traceback(sys, e)
            if self.logger : self.logger.error('>>>>>>>> Mysql connect Error %s' %(error))
            print (error)
            raise e

    def get_connection(self):
        """
        :return:
        """
        try:
            if not self.__connected:
                self.connect()
            return self.__cnx_pool.get_connection()
        except Exception as e:
            error = common_util.get_error_traceback(sys, e)
            if self.logger : self.logger.error('>>>>>>>> Mysql Error %s' %(error))
            print (error)
            raise e



    def find_sql(self, table_name, filters={}, columns='', sort=False):
        try:
            data = None
            if not self.__connected:
                self.connect()
            connection_object = self.__cnx_pool.get_connection()
    
            cursor = connection_object.cursor(dictionary=True)

            if columns:
                columns = ','.join(columns)
            else:
                columns = '*'

            if filters:
                params = query_from_filter(filters)
                query = 'SELECT %s FROM %s WHERE %s' %(columns, table_name, params)
                # print(query)
            else:
                query = 'SELECT %s FROM %s' %(columns, table_name)

            if sort:
                query += ' ORDER BY timestamp DESC '

            cursor.execute(query)
            data = cursor.fetchall()
            # print('>>>>>>>> MYSQL Find Success : %s' %(query))
            if self.logger:  self.logger.info('>>>>>>>> MYSQL Find Success : %s' %(query))

        except Exception as e:
            error = common_util.get_error_traceback(sys, e)
            if self.logger: self.logger.error('>>>>>>>> Mysql Error %s' %(error))
        finally:
            if self.__connected: cursor.close()
            self.__connected = False
            return data


    def insert_sql(self, table_name, insert_data):
        try:
            data = None
            ret_status = False
            if not self.__connected:
                self.connect()
            connection_object = self.__cnx_pool.get_connection()
    
            cursor = connection_object.cursor(dictionary=True)

            query = 'insert into %s (%s) Values (%s)' %(table_name, ','.join([key for key in insert_data]), query_from_data(insert_data))
            # print(query)
            cursor.execute(query)
            ret_status = {
                'success':True,
                'inserted_id' : cursor._last_insert_id
            }
            # print('>>>>>>>> MYSQL Insert Success : %s' %(query))
            
            if self.logger:  self.logger.info('>>>>>>>> MYSQL Insert Success : %s' %(query))

        except Exception as e :
            error = common_util.get_error_traceback(sys, e)
            print ('>>>>>>>> MYSQL  Error : %s ' %error)
            if self.logger: self.logger.error('>>>>>>>> Mysql Error %s' %(error))
            raise e
        finally:
            if self.__connected: cursor.close()
            self.__connected = False
            return ret_status


    def update_sql(self,  table_name, filters, updated_values):
        """
        """
        db_con = None
        ret_status = False
        try:

            if self.find_sql(table_name, filters):
                if not self.__connected:
                    self.connect()
                    connection_object = self.__cnx_pool.get_connection()
            
                    cursor = connection_object.cursor(dictionary=True)

                update_params = query_from_filter(updated_values,type_=',')
                filter_params = query_from_filter(filters)

                query = 'UPDATE %s SET %s WHERE %s' % (table_name, update_params, filter_params)
                cursor.execute(query)
                # print('>>>>>>>> MYSQL update Success : %s' % (query))
                if self.logger:  self.logger.info('>>>>>>>> MYSQL UPDATE Success : %s' %(query))
                ret_status = True

        except Exception as e:
            error = common_util.get_error_traceback(sys, e)
            print (error)
            if self.logger : self.logger.error('>>>>>>>> Mysql Error %s' %(error))
            raise error
        finally:
            if self.__connected: cursor.close()
            self.__connected = False
            return ret_status

    
    def handel_raw_qry(self, query):
        try:
            data = None

            if not self.__connected:
                self.connect()
            connection_object = self.__cnx_pool.get_connection()
    
            cursor = connection_object.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()
            # print('>>>>>>>> MYSQL handel_raw_qry Success %s ' %query)
            if self.logger:  self.logger.info('>>>>>>>> MYSQL handel_raw_qry Success : %s' %(query))
            return data
        except Exception as e :
            error = common_util.get_error_traceback(sys, e)
            print (error)
            if self.logger:  self.logger.error('>>>>>>>> Mysql Error %s' %(error))
            raise e
        finally:
            if self.__connected: cursor.close()
            self.__connected = False


    def create_sql_qry(self, query):
        try:
            data = None

            if not self.__connected:
                self.connect()
            connection_object = self.__cnx_pool.get_connection()
    
            cursor = connection_object.cursor(dictionary=True)
            cursor.execute(query)
            return True
        except Exception as e :
            error = common_util.get_error_traceback(sys, e)
            print (error)
            if self.logger:  self.logger.error('>>>>>>>> Mysql Error %s' %(error))
            raise e
        finally:
            if self.__connected: cursor.close()
            self.__connected = False


    