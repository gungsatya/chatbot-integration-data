import sqlite3, mysql.connector,time

def sqliteListenner():
    db_dwh_set = {"host": "localhost", "user": "root", "password": "", "db": "dwh_datawarehouse"}
    connMySql = mysql.connector.MySQLConnection(**db_dwh_set)
    cMySql = connMySql.cursor(buffered=True)

    connSqlite = sqlite3.connect('mirror.db')
    cSqlite = connSqlite.cursor()

    cSqlite.execute('SELECT * FROM trxClient')
    for row in cSqlite.fetchall():
        query = "INSERT INTO trx(code_trx,sender_id,name,code_pulse)VALUES('%s','%s','%s','%s')" % (
            row[1], row[2], row[3], row[4])
        cMySql.execute(query)
        connMySql.commit()

        query = "DELETE FROM trxClient WHERE code_trx = '%s'" % (row[1])
        cSqlite.execute(query)
        connSqlite.commit()

while(True):
    sqliteListenner()
    time.sleep(1)
