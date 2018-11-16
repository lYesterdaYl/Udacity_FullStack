import psycopg2



class Report:


    def __init__(self):
        self.conn = psycopg2.connect(dbname="news", user="postgres", password="1234", host="localhost", port="5432")




    def most_popular_article(self):
        cur = self.conn.cursor()

        cur.execute(
            '''
            SELECT
                ar.title,
                COUNT (l."path")
            FROM
                log l
            LEFT JOIN articles ar ON l."path" = concat ('/article/', ar.slug)
            WHERE
                l.status != '404 NOT FOUND'
            AND l."path" != '/'
            GROUP BY
                ar.title,
                l."path"
            ORDER BY
                COUNT ("path") DESC
            LIMIT 3
            ''')
        rows = cur.fetchall()
        print("The most popular three articles of all time")
        for i in rows:
            print(i[0], " -- ", i[1], " views")

    def most_popular_article_author(self):
        cur = self.conn.cursor()

        cur.execute(
            '''
            SELECT
                au. NAME,
                COUNT (l."path")
            FROM
                log l
            LEFT JOIN articles ar ON l."path" = concat ('/article/', ar.slug)
            LEFT JOIN authors au ON ar.author = au."id"
            WHERE
                l.status != '404 NOT FOUND'
            AND l."path" != '/'
            GROUP BY
                au. NAME
            ORDER BY
                COUNT (au. NAME) DESC            
            ''')
        rows = cur.fetchall()
        print("The most popular article authors of all time")
        for i in rows:
            print(i[0], " -- ", i[1], " views")

    def error_request(self):
        result = {}
        cur = self.conn.cursor()

        cur.execute(
            '''
            SELECT
                *
            FROM
                (
                    SELECT
                        all_request. DAY,
                        round(
                            (
                                CAST (
                                    error_request.error_count AS DECIMAL
                                ) / CAST (
                                    all_request.all_count AS DECIMAL
                                )
                            ) * 100,
                            2
                        ) AS rate
                    FROM
                        (
                            SELECT
                                DATE (TIME) AS DAY,
                                COUNT (ip) AS all_count
                            FROM
                                log
                            GROUP BY
                                DAY
                        ) AS all_request
                    INNER JOIN (
                        SELECT
                            DATE (TIME) AS DAY,
                            COUNT (ip) error_count
                        FROM
                            log
                        WHERE
                            status NOT LIKE '%200%'
                        GROUP BY
                            DAY
                    ) AS error_request ON all_request. DAY = error_request. DAY
                ) AS TEMP
            WHERE
                rate > 1
            ''')
        rows = cur.fetchall()
        print("The days have more than 1% of requests lead to errors")
        for i in rows:
            print(i[0], " -- ", i[1], "% errors")




report = Report()
report.most_popular_article()
report.most_popular_article_author()
report.error_request()