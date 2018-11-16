# Logs Analysis

This Project was created for my Udacity Nanodegree. It was built for data analysis for a news database log.


## Sample Data & Output

You can download the Postgresql Data File  [Here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

![sample output](sample_output.jpg)

## Installation

1. Clone the repository.
2. Load the data into localhost **Postgresql** Database.
3. Run main.py -- `$ python3 main.py`

## How to load the data into Database

To load the data, cd into the vagrant directory and use the command `psql -d news -f newsdata.sql`.
Here's what this command does:

`psql` — the PostgreSQL command line program

`-d news` — connect to the database named news which has been set up for you

`-f newsdata.sql` — run the SQL statements in the file newsdata.sql

## Author

* [Zhiyuan Du](https://github.com/lYesterdaYl)

## Built With

* [Postgresql](https://www.postgresql.org/) - Used to store the data.
* [psycopg2](http://initd.org/psycopg/docs/) - Used to connect to the Postgresql database

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details