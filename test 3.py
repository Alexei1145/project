import sqlite3

con = sqlite3.connect('dat.db')
cur = con.cursor()
day = cur.execute("""SELECT num from data 
                    where name = 'day'""").fetchall()[0][0]
con.close()
print(day)
