# coding=utf-8
# pylint: disable=import-error, broad-except
from resources.models.database import SqlConnection


class EnvDBResource(object):

    def __init__(self, db_name="production_test"):
        self.sql = SqlConnection(db_name=db_name)

    def get_all_nodes(self):
        sea_string = "SELECT * FROM node"
        result = self.sql.execute_sql_command(sea_string)
        return result
