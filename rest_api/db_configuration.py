from peewee import PostgresqlDatabase

pgdb = PostgresqlDatabase('postgres', user='postgres', password='admin', host='localhost', port=5432)
