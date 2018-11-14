import psycopg2



class Report:


    def __init__(self):
        self.conn = psycopg2.connect(dbname="news", user="postgres", password="", host="localhost", port="5432")




    def most_popular_article(self):
        cur = self.conn.cursor()

        cur.execute('''select ar.title, count(l."path") from log l LEFT JOIN articles ar on l."path" ~ ar.slug WHERE l.status != '404 NOT FOUND' and l."path" != '/' GROUP BY ar.title, l."path" ORDER BY count("path") DESC LIMIT 3''')
        rows = cur.fetchall()
        print("The most popular three articles of all time")
        for i in rows:
            print(i[0], " -- ", i[1], " views")

    








report = Report()
report.most_popular_article()