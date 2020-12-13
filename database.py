import pymysql


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    db='words_db',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

def add_word_to_db(cursor, word, word_count):

    try:
        sql = "INSERT INTO words (word, word_count) VALUES (%s, %s)"
        val = (word, word_count)
        cursor.execute(sql, val)
        cursor.execute(sql,val)
        connection.commit()
    except Exception as e:
        print("Error while adding new receiver", e)

cursor = connection.cursor()

def get_word_count_from_db(cursor, word):
    name= "\"" + str(word).replace('/', '_') + "\""
    query = "select word_count from words as r where r.word = " + str(name)
    cursor.execute(query)
    res = cursor.fetchall()
    if len(res) == 0:
        return None
    return res[0]['word_count']
def get_word_from_db(cursor, word):
    name= "\"" + str(word).replace('/', '_') + "\""
    query = "select word from words as r where r.word = " + str(name)
    cursor.execute(query)
    res = cursor.fetchall()
    if len(res) == 0:
        return None
    return res[0]['word']

def add(word):
    word_count = get_word_count_from_db(cursor, word)
    if word_count != None:
        word_count = int(word_count) +1
    add_word_to_db(cursor, word ,word_count)

def delete_word_from_db(cursor, word):
    name= "\"" + str(word).replace('/', '_') + "\""
    query = "delete from words as r where r.word = " + str(name)
    cursor.execute(query)
    res = cursor.fetchall()
    if len(res) == 0:
        return None
    return res[0]['word']

def select_top_five_from_db(cursor):

    query = "Select Top 5 word, word_count from words order by word_count Desc"
    cursor.execute(query)
    res = cursor.fetchall()
    if len(res) == 0:
        return None
    return res
