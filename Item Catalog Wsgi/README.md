# Item Catalog Wsgi

This Project was created for my Udacity Nanodegree. It was built for Item management.


## Access Information
1. IP: ```52.38.28.190``` Port: ```2200```
2. URL: http://www.ordinaryzone.com/
3. Software: MySQL, Flask, mod_wsgi
4. Changes made: <br>
   ```1. created new user grader```<br>
   ```2. give sudo access and create key pair for user grader```<br>
   ```3. change ssh port from default 22 to 2200```<br>
   ```4. change timezone to UTC```<br>
   ```5. deploy item catalog project on apache server```<br>
   ```6. install MySQL database to store the data for the catalog project```
5. Private Key is [id_rsa](id_rsa)<br>
    grader can ssh log with command ```ssh -i id_rsa grader@52.38.28.190 -p 2200```
## Author

* [Zhiyuan Du](https://github.com/lYesterdaYl)

## Built With

* [MySQL](https://www.mysql.com/) - Used to store the data.
* [Flask](http://flask.pocoo.org/) - Used to construct server side code.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details