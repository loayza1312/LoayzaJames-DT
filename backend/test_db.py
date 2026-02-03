from DatabaseWrapper import DatabaseWrapper

db = DatabaseWrapper()
db.create_tables()
db.close()
print("Tabelle create correttamente!")
