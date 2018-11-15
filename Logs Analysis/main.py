import psycopg2



class Report:


    def __init__(self):
        self.conn = psycopg2.connect(dbname="news", user="postgres", password="bgmdsjy054", host="localhost", port="5432")




    def most_popular_article(self):
        cur = self.conn.cursor()

        cur.execute('''select ar.title, count(l."path") from log l LEFT JOIN articles ar on l."path" like concat('%',ar.slug) WHERE l.status != '404 NOT FOUND' and l."path" != '/' GROUP BY ar.title, l."path" ORDER BY count("path") DESC LIMIT 3''')
        rows = cur.fetchall()
        print("The most popular three articles of all time")
        for i in rows:
            print(i[0], " -- ", i[1], " views")

    def most_popular_article_author(self):
        cur = self.conn.cursor()

        cur.execute('''select au.name, count(l."path") from log l LEFT JOIN articles ar on l."path" like concat('%',ar.slug) LEFT JOIN authors au on ar.author = au."id" WHERE l.status != '404 NOT FOUND' and l."path" != '/' GROUP BY au.name ORDER BY count(au.name) DESC''')
        rows = cur.fetchall()
        print("The most popular article authors of all time")
        for i in rows:
            print(i[0], " -- ", i[1], " views")

    def error_request(self):
        result = {}
        cur = self.conn.cursor()

        cur.execute('''select date(time), count(status) from log WHERE status != '200 OK' GROUP BY date(time) ORDER BY date(time)''')
        error = cur.fetchall()
        cur.execute('''select date(time), count(status) from log WHERE status = '200 OK' GROUP BY date(time) ORDER BY date(time)''')
        no_error = cur.fetchall()
        print("The days have more than 1% of requests lead to errors")
        for i, j in enumerate(error):
            error_rate = round(j[1] / no_error[i][1] * 100, 3)
            if error_rate > 1:
                result[j[0]] = error_rate

        for date in result:
            print(date, " -- ", result[date], "% errors")





report = Report()
report.most_popular_article()
report.most_popular_article_author()
report.error_request()