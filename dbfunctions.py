from secret_file import pword
import psycopg2

conn = ""
cur = ""

def connectDB():
    conn = psycopg2.connect(database = "ScrapeDB",
                            user="postgres",
                            host="localhost",
                            password = pword,
                            port = 5432)
    cur = conn.cursor()
    print("\nDB CONNECTED\n")
    return 0

def writeToDB(urlToSave):
    #SQL goes here to write to DB
    return 0

def disconnectDB():
    cur.close()
    conn.close()
    return 0
