from config import secret
import psycopg2

#createDB()

def writeToDB(urlToSave, table, column):
    conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = secret,
                            port = 5432)
    cur = conn.cursor()
    urlToSave = str(urlToSave)
    sql = "INSERT INTO {} ({}) VALUES ('{}');".format(table, column, urlToSave)
    try:
        with  conn.cursor() as cur:
            cur.execute(sql, (table))
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        cur.close()
        conn.close()
        print(error)
    cur.close()
    conn.close()
    return 0