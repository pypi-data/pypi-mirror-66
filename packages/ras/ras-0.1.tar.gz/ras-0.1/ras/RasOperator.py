import sys, logging
import ras.Constants as constants


class RasOperator:
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    def __init__(self, r, conn):
        self.r = r
        self.conn = conn

    def insert_transaction_data(self, transaction_json):
        self.r.table(constants.TRANSACTION_DATA).insert({
            "_id": transaction_json['_id'],
            "ts": transaction_json['ts'],
            "endDate": transaction_json['endDate'],
            "run-time": transaction_json['run-time'],
            "tid": transaction_json['tid'],
            "startDate": transaction_json['startDate'],
            "input-file": transaction_json['input-file'],
            "client": transaction_json['client'],
            "batch": transaction_json['batch'],
            "name": transaction_json['name'],
            "host": transaction_json['host']
        }).run(self.conn)

    def insert_error(self, error_json):
        self.r.table(constants.ERROR).insert({
            "_id": error_json['_id'],
            "ts": error_json['ts'],
            "status-code": error_json['status-code'],
            "tid": error_json['tid'],
            "endpoint": error_json['endpoint'],
            "message": error_json['message'],
            "description": error_json['description'],
            "internal-status-code": error_json['internal-status-code'],
            "component": error_json['component'],
            "component-message": error_json['component-message'],
            "client": error_json['client'],
            "batch": error_json['batch']
        }).run(self.conn)

    def insert_node_definitions(self, node_definitions):
        nodes = []
        in_nodes = node_definitions['nodes']
        logging.debug('number of nodes are: ' + str(len(in_nodes)))
        if len(in_nodes) > 0:
            for a_node in node_definitions['nodes']:
                {
                    "id": a_node['id'],
                    "name": a_node['name'],
                    "flavor": a_node['flavor'],
                    "location": a_node['location'],
                    "memory": a_node['memory'],
                    "cores": a_node['cores']
                }
                nodes.append(a_node)

        self.r.table(constants.NODE_DEFINITIONS).insert({
            "_id": node_definitions['_id'],
            "timestamp": node_definitions['timestamp'],
            "nodes": nodes
        }).run(self.conn)

    def insert_usage_activity_data(self, usage_activity_json):
        self.r.table(constants.USAGE_ACTIVITY_DATA).insert({
            "_id": usage_activity_json['_id'],
            "offering_service_name": usage_activity_json['offering_service_name'],
            "timestamp": usage_activity_json['timestamp'],
            "sales_channel": usage_activity_json['sales_channel'],
            "activity": usage_activity_json['activity']
        }).run(self.conn)