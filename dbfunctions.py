from secret_file import pword
import psycopg2

def writeToDB(urlToSave):
    conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = pword,
                            port = 5432)
    cur = conn.cursor()
    urlToSave = str(urlToSave)
    sql = "INSERT INTO Websites (URL) VALUES ('{}');".format(urlToSave)
    try:
        with  conn.cursor() as cur:
            cur.execute(sql, ("Websites"))
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        cur.close()
        conn.close()
        print(error)
        
    cur.close()
    conn.close()
    return 0
