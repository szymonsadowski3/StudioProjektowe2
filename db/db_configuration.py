from peewee import PostgresqlDatabase

pgdb = PostgresqlDatabase('postgres', user='postgres', password='postgres', host='localhost', port=5432)
