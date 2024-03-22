from secret_file import pword
import psycopg2

#createDB()

def writeToDB(urlToSave, table, column):
    conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = pword,
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

def deleteDBDupes():
    conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = pword,
                            port = 5432)
    cur = conn.cursor()
    #urlToSave = str(urlToSave)
    selectSQL = "SELECT url, COUNT(url) FROM domains GROUP BY url HAVING COUNT(url)> 1;"
    deleteSQL = "DELETE FROM domains a USING domains b WHERE a.id < b.id AND a.url = b.url;"
    try:
        with  conn.cursor() as cur:
            cur.execute(selectSQL, ("domains"))
            print("select ran")
            cur.execute(deleteSQL, ("domains"))
            print("delete ran")
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        cur.close()
        conn.close()
        print(error)