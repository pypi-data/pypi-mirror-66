import sys, logging
from ras.RasConnect import RasConnect
from ras.RasOperator import RasOperator
import ras.Constants as constants
import rethinkdb as rdb
from rethinkdb.errors import RqlRuntimeError

class RasHandler:
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    @staticmethod
    def insert(ras_data_type, json):
        r = rdb.RethinkDB()
        ras_conn = RasConnect(r)
        conn = ras_conn.open()
        try:
            ras_operator = RasOperator(r, conn)

            if ras_data_type == constants.TRANSACTION_DATA:
                ras_operator.insert_transaction_data(json)
            elif ras_data_type == constants.ERROR:
                ras_operator.insert_error(json)
            elif ras_data_type == constants.NODE_DEFINITIONS:
                ras_operator.insert_node_definitions(json)
            elif ras_data_type == constants.USAGE_ACTIVITY_DATA:
                ras_operator.insert_usage_activity_data(json)
        except RqlRuntimeError as err:
            logging.error(err.message)
        finally:
            conn.close()


