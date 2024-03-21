from secret_file import pword
import psycopg2

def writeToDB(urlToSave):
    conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = pword,
                            port = 5432)
    cur = conn.cursor()
    print("\nDB CONNECTED\n")
    urlToSave = str(urlToSave)
    print("1")
    sql = "INSERT INTO Websites (URL) VALUES ('{}');".format(urlToSave)
    print("2")
    try:
        print("3")
        with  conn.cursor() as cur:
            print("4")
            cur.execute(sql, ("Websites"))
            print("5")
            conn.commit()
            print("Mighta worked!")
    except (Exception, psycopg2.DatabaseError) as error:
        cur.close()
        conn.close()
        print(error)
        
    cur.close()
    conn.close()
    return 0
