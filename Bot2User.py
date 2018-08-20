import requests, mysql.connector, time
from time import gmtime, strftime

base_url = "https://api.groupme.com/v3/"
token = "248wrFugY2IJcneDTfUSs0dhPODmWh2KutAxWrpm"
group_id = "27055918"
bot_id = "436700f737186104406298c54f"
sintaks = ("/cari", "/beli", "/info")

db_msg_set = {"host": "localhost", "user": "root", "password": "", "db": "dwh_messages"}
db_dwh_set = {"host": "localhost", "user": "root", "password": "", "db": "dwh_datawarehouse"}

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
    query = "INSERT INTO msg_in(id,sender_id,name,text,group_id,user_type)" \
            "VALUES('%s','%s','%s','%s','%s','%s')" % (id, sender_id, name, text, group_id, user_type)
    c_msg.execute(query)
    db_msg.commit()


def search(key=""):
    db_dwh = mysql.connector.MySQLConnection(**db_dwh_set)
    c_dwh = db_dwh.cursor()
    query = "SELECT * FROM pulse WHERE `name` LIKE '%" + key + "%'"
    c_dwh.execute(query)
    count = 0
    result = ">"
    for data in c_dwh.fetchall():
        result += "Kode '" + data[1] + "' | " + data[2] + " | " + str(data[3]) + " | " + data[4] + "\n\n"
        count += 1
    if count == 0:
        return ">Pulsa yang ada cari tidak ada"
    else:
        return result


def buy(sender_id="", name="", code_pulse=""):
    db_dwh = mysql.connector.MySQLConnection(**db_dwh_set)
    c_dwh = db_dwh.cursor()
    query = "SELECT status FROM pulse WHERE code_pulse = '%s'" % code_pulse
    c_dwh.execute(query)
    row = c_dwh.fetchone()
    now = strftime("%Y%m%d%H%M%S", gmtime())
    code_trx = sender_id + now
    if not row:
        return "Pulsa yang ada cari tidak ditemukan"
    elif (row[0] != "tersedia"):
        return "Pulsa saat ini tidak tersedia"
    else:
        try:
            query = "INSERT INTO trx(code_trx, sender_id,name,code_pulse)VALUES('%s','%s','%s','%s')" % (
                code_trx, sender_id, name, code_pulse)
            c_dwh.execute(query)
            db_dwh.commit()
            return "Transaksi berhasil"
        except mysql.connector.Error as e:
            print(e)
            return "Transaksi gagal"


def sendMessage(text=""):
    parameter = {'token': token, 'bot_id': bot_id, 'text': text}
    requests.post(base_url + "bots/post", params=parameter)


def receiveMessages(last_id=""):
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
        query = msg.split(" ")[0]
        if (message['sender_type'] == 'user' and query in sintaks):
            insertMessagesIN(
                message['id'],
                message['sender_id'],
                message['name'],
                message['text'],
                message['group_id'],
                message['sender_type']
            )
            if (query == "/cari"):
                results = search(msg[6:])
                sendMessage(results)
            elif (query == "/info"):
                sendMessage(
                    ">/cari<spasi>pulsa yang dicari : untuk mencari pulsa\n\n/beli<spasi>kodepulsa : untuk membeli pulsa")
            elif (query == "/beli"):
                results = buy(message['sender_id'], message['name'], msg.split(" ")[1])
                sendMessage(results)

    return temp_id


last_id = getLastIdMessageIN()

while (True):
    temp = receiveMessages(last_id)
    if (temp != ""): last_id = temp
    time.sleep(3)
