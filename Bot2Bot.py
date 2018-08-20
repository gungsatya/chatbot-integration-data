import requests, mysql.connector, sqlite3, sys

base_url = "https://api.groupme.com/v3/"
token = "248wrFugY2IJcneDTfUSs0dhPODmWh2KutAxWrpm"
group_id = "27128649"
bot_id = "96ea87701fab32cb546bc35460"
header = ("/do")

db_msg_set = {"host": "localhost", "user": "root", "password": "", "db": "dwh_messages"}
db_dwh_set = {"host": "localhost", "user": "root", "password": "", "db": "dwh_datawarehouse"}
Trx       = "trx"
TrxClient = 'trxClient'
TrxCol = ('_id', 'code_trx', 'sender_id', 'name', 'code_pulse', 'buy_at')
Pulse = "pulse"
PulseCol = ('_id', 'code_pulse', 'name', 'balance', 'status')


def getLastIdMessageIN():
    db_msg = mysql.connector.MySQLConnection(**db_msg_set)
    c_msg = db_msg.cursor()
    query = "SELECT id FROM msg_in WHERE group_id = '%s' ORDER BY _id DESC LIMIT 1" % (group_id)
    c_msg.execute(query)
    row = c_msg.fetchone()
    if not row:
        return ""
    else:
        return row[0]


def insertMessagesIN(id, sender_id, name, text, group_id, user_type):
    db_msg = mysql.connector.MySQLConnection(**db_msg_set)
    c_msg = db_msg.cursor()
    query = '''INSERT INTO msg_in(id,sender_id,name,text,group_id,user_type)''' \
            '''VALUES("%s","%s","%s","%s","%s","%s")''' % (id, sender_id, name, text, group_id, user_type)
    c_msg.execute(query)
    db_msg.commit()


def sendMessage(text=""):
    parameter = {'token': token, 'bot_id': bot_id, 'text': text}
    requests.post(base_url + "bots/post", params=parameter)


def isExistData(type=0, table="", tabelCol="", key=""):
    if (type == 0):
        try:
            connMySql = mysql.connector.MySQLConnection(**db_dwh_set)
            cMySql = connMySql.cursor(buffered=True)
            query = "SELECT * FROM %s WHERE %s = '%s'" % (table, tabelCol, key)
            cMySql.execute(query)
            rowCount = 0
            for count in cMySql:
                rowCount += 1
            if (rowCount > 0):
                return True
            else:
                return False
        except mysql.connector.Error as e:
            print("isExistData 0 :")
            print(e)
            sys.exit(-1)
    elif (type == 1):
        try:
            connSqlite = sqlite3.connect('temporary.db')
            cSqlite = connSqlite.cursor()
            query = "SELECT * FROM %s WHERE %s = '%s'" % (table, tabelCol, key)
            cSqlite.execute(query)
            rowCount = 0
            for count in cSqlite: rowCount += 1
            if (rowCount > 0):
                return True
            else:
                return False
        except mysql.connector.Error as e:
            print("isExistData 1 :")
            print(e)
            sys.exit(-1)


def do(query=""):
    try:
        connMySql = mysql.connector.MySQLConnection(**db_dwh_set)
        cMySql = connMySql.cursor(buffered=True)
        cMySql.execute(query)
        connMySql.commit()

        connSqlite = sqlite3.connect('temporary.db')
        cSqlite = connSqlite.cursor()
        cSqlite.execute(query)
        connSqlite.commit()
    except mysql.connector.Error as e:
        print("Error do MySQL")
        print(e)
    except sqlite3.Error as e:
        print("Error do SQLite")
        print(e)


def importDb():
    try:
        connSqliteTemp = sqlite3.connect('temporary.db')
        cSqliteTemp = connSqliteTemp.cursor()

        connSqlite = sqlite3.connect('mirror.db')
        cSqlite = connSqlite.cursor()

        query = '''CREATE TABLE IF NOT EXISTS `%s` (
          `%s` INTEGER PRIMARY KEY AUTOINCREMENT ,
          `%s` varchar(10) DEFAULT NULL,
          `%s` varchar(30) DEFAULT NULL,
          `%s` int(11) DEFAULT NULL,
          `%s` varchar(30) DEFAULT NULL
        )''' % (Pulse, PulseCol[0], PulseCol[1], PulseCol[2], PulseCol[3], PulseCol[4])
        cSqliteTemp.execute(query)
        connSqliteTemp.commit()
        cSqlite.execute(query)
        connSqlite.commit()

        query = '''CREATE TABLE IF NOT EXISTS `%s` (
          `%s` INTEGER PRIMARY KEY AUTOINCREMENT,
          `%s` text,
          `%s` text,
          `%s` text,
          `%s` varchar(20) DEFAULT NULL,
          `%s` timestamp
        )''' % (Trx, TrxCol[0], TrxCol[1], TrxCol[2], TrxCol[3], TrxCol[4], TrxCol[5])
        cSqliteTemp.execute(query)
        connSqliteTemp.commit()
        cSqlite.execute(query)
        connSqlite.commit()

        query = '''CREATE TABLE IF NOT EXISTS `%s` (
                 `%s` INTEGER PRIMARY KEY AUTOINCREMENT,
                 `%s` text,
                 `%s` text,
                 `%s` text,
                 `%s` varchar(20) DEFAULT NULL,
                 `%s` timestamp
               )''' % (TrxClient, TrxCol[0], TrxCol[1], TrxCol[2], TrxCol[3], TrxCol[4], TrxCol[5])
        cSqlite.execute(query)
        connSqlite.commit()

        connMySql = mysql.connector.MySQLConnection(**db_dwh_set)
        cMySql = connMySql.cursor(buffered=True)

        count = 0
        cSqliteTemp.execute("SELECT * FROM " + Pulse)
        for row in cSqliteTemp.fetchall(): count = +1
        cMySql.execute("SELECT * FROM " + Pulse)
        if (count == 0):
            for row in cMySql.fetchall():
                query = "INSERT INTO %s(code_pulse,name,balance,status)VALUES('%s','%s',%i,'%s')" % (
                    Pulse, row[1], row[2], row[3], row[4])
                cSqliteTemp.execute(query)
                connSqliteTemp.commit()

        count = 0
        cSqlite.execute("SELECT * FROM " + Pulse)
        for row in cSqlite.fetchall(): count = +1
        cMySql.execute("SELECT * FROM " + Pulse)
        if (count == 0):
            for row in cMySql.fetchall():
                query = "INSERT INTO %s(code_pulse,name,balance,status)VALUES('%s','%s',%i,'%s')" % (
                    Pulse, row[1], row[2], row[3], row[4])
                cSqlite.execute(query)
                connSqlite.commit()

        count = 0
        cSqliteTemp.execute("SELECT * FROM " + Trx)
        for row in cSqliteTemp.fetchall(): count = +1
        if (count == 0):
            cMySql.execute("SELECT * FROM " + Trx)
            for row in cMySql.fetchall():
                query = "INSERT INTO %s(code_trx,sender_id,name,code_pulse,buy_at)VALUES('%s','%s','%s','%s','%s')" % (
                    Trx, row[1], row[2], row[3], row[4],row[5])
                cSqliteTemp.execute(query)
                connSqliteTemp.commit()

        count = 0
        cSqlite.execute("SELECT * FROM " + Trx)
        for row in cSqlite.fetchall(): count = +1
        if (count == 0):
            cMySql.execute("SELECT * FROM " + Trx)
            for row in cMySql.fetchall():
                query = "INSERT INTO %s(code_trx,sender_id,name,code_pulse,buy_at)VALUES('%s','%s','%s','%s','%s')" % (
                    Trx, row[1], row[2], row[3], row[4], row[5])
                cSqlite.execute(query)
                connSqlite.commit()

    except mysql.connector.Error as e:
        print("Error importing data in MySQL side")
        print(e)
    except sqlite3.Error as e:
        print("Error importing data in SQLite side")
        print(e)


def pulseChecker():
    connMySql = mysql.connector.MySQLConnection(**db_dwh_set)
    cMySql = connMySql.cursor(buffered=True)
    connSqliteTemp = sqlite3.connect('temporary.db')
    cSqliteTemp = connSqliteTemp.cursor()
    connSqlite = sqlite3.connect('mirror.db')
    cSqlite = connSqlite.cursor()

    cMySql.execute("SELECT * FROM " + Pulse)
    for row in cMySql.fetchall():
        if (isExistData(1, Pulse, PulseCol[1], row[1]) != True):
            query = "INSERT INTO %s(code_pulse,name,balance,status)VALUES('%s','%s',%i,'%s')" % (
                Pulse, row[1], row[2], row[3], row[4])
            cSqliteTemp.execute(query)
            connSqliteTemp.commit()

            cSqlite.execute(query)
            connSqlite.commit()
            sendMessage("/do " + query)
        else:
            query = "SELECT CONCAT(code_pulse,name,balance,status) FROM %s WHERE code_pulse = '%s'" % (Pulse, row[1])
            cMySql.execute(query)
            mysqlRow = cMySql.fetchone()[0]

            query = "SELECT code_pulse||name||balance||status FROM %s WHERE code_pulse = '%s'" % (Pulse, row[1])
            cSqliteTemp.execute(query)
            sqliteRow = cSqliteTemp.fetchone()[0]

            if (mysqlRow != sqliteRow):
                query = "DELETE FROM %s WHERE code_pulse = '%s'" % (Pulse, row[1])
                cSqliteTemp.execute(query)
                connSqliteTemp.commit()
                cSqlite.execute(query)
                connSqlite.commit()
                sendMessage("/do " + query)

                query = "INSERT INTO %s(code_pulse,name,balance,status)VALUES('%s','%s',%i,'%s')" % (
                    Pulse, row[1], row[2], row[3], row[4])
                cSqliteTemp.execute(query)
                connSqliteTemp.commit()
                cSqlite.execute(query)
                connSqlite.commit()
                sendMessage("/do " + query)

    cSqliteTemp.execute("SELECT * FROM " + Pulse)
    for row in cSqliteTemp.fetchall():
        if (isExistData(0, Pulse, PulseCol[1], row[1]) != True):
            query = "DELETE FROM %s WHERE code_pulse = '%s'" % (Pulse, row[1])
            cSqliteTemp.execute(query)
            connSqliteTemp.commit()
            cSqlite.execute(query)
            connSqlite.commit()
            sendMessage("/do " + query)
    cMySql.close()
    cSqliteTemp.close()


def trxChecker():
    connMySql = mysql.connector.MySQLConnection(**db_dwh_set)
    cMySql = connMySql.cursor(buffered=True)
    connSqliteTemp = sqlite3.connect('temporary.db')
    cSqliteTemp = connSqliteTemp.cursor()
    connSqlite = sqlite3.connect('mirror.db')
    cSqlite = connSqlite.cursor()
    cMySql.execute("SELECT * FROM " + Trx)
    for row in cMySql.fetchall():
        if (isExistData(1, Trx, TrxCol[1], row[1]) != True):
            query = "INSERT INTO %s(code_trx,sender_id,name,code_pulse,buy_at)VALUES('%s','%s','%s','%s','%s')" % (
                Trx, row[1], row[2], row[3], row[4],row[5])
            cSqliteTemp.execute(query)
            connSqliteTemp.commit()

            cSqlite.execute(query)
            connSqlite.commit()
            sendMessage("/do " + query)
    cSqliteTemp.execute("SELECT * FROM " + Trx)
    for row in cSqliteTemp.fetchall():
        if (isExistData(0, Trx, TrxCol[1], row[1]) != True):
            query = "DELETE FROM %s WHERE code_trx = '%s'" % (Trx, row[1])
            cSqliteTemp.execute(query)
            connSqliteTemp.commit()
            cSqlite.execute(query)
            connSqlite.commit()
            sendMessage("/do " + query)
    cMySql.close()
    cSqliteTemp.close()

def getMyName():
    req = requests.get(base_url + "bots", params={'token': token})
    data = req.json()
    dataBots = data['response']
    for dataBot in dataBots:
        if dataBot['bot_id'] == bot_id:
            return dataBot['name']


def receiveMessages(myName="", last_id=""):
    if (last_id != ""):
        parameter = {'token': token, 'after_id': last_id}
    else:
        parameter = {'token': token}

    req = requests.get(base_url + "groups/" + group_id + "/messages", params=parameter)
    data = req.json()

    messages = data['response']['messages']
    temp_id = ""
    for message in reversed(messages):
        temp_id = message['id']
        msg = str(message['text'])
        head = msg.split(" ")[0]
        if (message['name'] != myName and message['sender_type'] == 'bot' and head in header):
            insertMessagesIN(
                message['id'],
                message['sender_id'],
                message['name'],
                message['text'],
                message['group_id'],
                message['sender_type']
            )
            if (head == "/do"):
                do(msg[4:])
    return temp_id
