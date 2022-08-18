import mysql.connector
from typing import Tuple
from datetime import datetime
DB_HOST = "xxxxxxxxxxx"
DB_NAME = "xxxxxxxxxxx"
DB_USER = "xxxxxxxxx"
DB_PASSWORD = "xxxxxxxx"
DB_INSERT_QUERY = "INSERT INTO Orchestrator (DateTime, ServiceName, EventType, ExceptionMessage, EventStatus) VALUES "
DB_QUERY_BATCH_ID = "SELECT DISTINCT Batch_Id FROM vacancy2EmployeeUpdates WHERE Is_Dirty = 1"


class Database:
    def __init__(self):
        self.__connection = mysql.connector.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        self.__cursor = self.__connection.cursor()

    def recordEvent(self, event_record: Tuple):
        if Tuple:
            timestamp = datetime.strftime(datetime.now(), '%Y/%m/%d-%H:%M:%S')
            event_record = (timestamp,) + event_record
            query = DB_INSERT_QUERY + str(event_record)
            with self.__connection.cursor() as cursor:
                cursor.execute(query)
                self.__connection.commit()

    def getUniqueBatchIds(self):
        """
        This method returns all the unique batch_ids where is_dirty is false
        :return: List of batch_ids
        """
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(DB_QUERY_BATCH_ID)
                results = cursor.fetchall()
                batch_ids = [batch_id[0] for batch_id in results]
                print(f'Unique batch_ids: {batch_ids}')
                return batch_ids
        except Exception as ex:
            print(f'Error: {ex}')
            return []


# Integration Test
def main():
    event = ('filtering_service', 'Response', 'None', 'Success')
    db = Database()
    db.recordEvent(event)
    db.getUniqueBatchIds()


if __name__ == '__main__':
    main()
