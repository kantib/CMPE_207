
Server code assumes you have installed mysql server installed on the machine you are running the server. Server try to log into mysql server using <host:127.0.0.1> <login:testuser> and <password:testpassword> <db:bank>. Hence create respective login and password on MySQL server before executing the server code. Below are few required MySQL commands for your reference (For Ubuntu Linux). More detailed information on different operating systems can be read at:
1. http://www.ntu.edu.sg/home/ehchua/programming/sql/MySQL_HowTo.html#zz-3.
2. http://www.ntu.edu.sg/home/ehchua/programming/howto/Ubuntu_HowTo.html#mysql 

1. First install pip for your python version
> sudo apt-get install python-pip

2. Upgrade pip version
> sudo pip install --upgrade pip

3. Install dependencies first
> sudo apt-get install python-dev libmysqlclient-dev

4. Install MySQLdb module
> sudo pip install MySQL-python

5. To create testuser login on mysql server use root login and password which is provided while installing mysql server.
6. login with root login
> mysql -u root -p

7. create testuser login
mysql> create user 'testuser'@'localhost' identified by 'testpassword';

8. set kind of permissions user can have. (*.*) means this user has all the privileges on all the databases and all the tables similar to "root" user except "grant" command.
mysql> grant all on *.* to 'testuser'@'localhost';

9. create a new database called 'bank'
mysql> create database if not exists bank;

10. show existing databases.
mysql> show databases;

11. use a particular database as the current one.
mysql> use bank;

12. create a table named customer with 3 columns
mysql> create table customer (id int, name varchar(50), address varchar(100));

13.  Describe the customer table (list its column definitions)
mysql> describe customer;

14. Insert a row into customer table (Strings are single-quoted, NO quotes for INT and FLOAT values)
mysql> insert into customer values (11, 'Bob', '265 Norwalk Dr. Tampa, FL')

15.  select all columns from table "customer" and all rows
mysql> select * from customer;

16. select some columns from tanble customer and rows that match the condition
mysql> select name, address from customer where id = 22;

17. Update the given field of the selected record
mysql> update customer set address = '56 merrimack NH' where name = 'Kevin';

18. delete selected records
mysql> delete from customer where id = 22;

19. drop a table
mysql> drop table if exists customer; 

20. Create database, tables all in one go using sql script. (with .sql extention)
    ~ denotes your home directory on linux machines.
mysql> source ~/myproject/mycommands.sql

************************************************************************************************************

Instructions specific this project to create a "Bank" Database and create all CUSTOMER related database tables 
using mysql script. Tables related to Teller and Admin should be created in similar manner.

$ mysql -u testuser -p
testpassword

mysql> create database if not exists Bank;
mysql> show databases;
mysql> use Bank;
mysql> create table customer_login (CUSTOMER_ID varchar(25), USERNAME varchar(25), PASSWORD varchar(50), SECURITY_QUES1 varchar(100), SECURITY_ANS1 varchar(100), SECURITY_QUES2 varchar(100), SECURITY_ANS2 varchar(100));
mysql> describe customer_login;
mysql> insert into customer_login values('123456', 'kanti', MD5('kanti'), 'what is your favorite game?', 'soccer', 'which country you are from?', 'India');
mysql> select * from customer_login;
mysql> create table account_table (CUSTOMER_ID varchar(25), CHECKING_ACCOUNT_NUM varchar(25), SAVING_ACCOUNT_NUM varchar(25), CHECKING_ACCOUNT_BAL int, SAVING_ACCOUNT_BAL int);
mysql> insert into account_table values (123456, 333333, 444444, 300, 400);
mysql> select * from account_table;
mysql> create table customer_info_table (CUSTOMER_ID varchar(25), FIRST_NAME varchar(25), LAST_NAME varchar(25), DATE_OF_BIRTH varchar(25), EMAIL_ID varchar(25), ADDRESS varchar(50));
mysql> insert into customer_info_table values('123456', 'kanti', 'bhat', '27Feb1988','kanti@rediffmail.com','654 N.First St. Sanjose CA 95777');
mysql> select * from customer_info_table;
mysql> create table transaction_table (CUSTOMER_ID varchar(25), DATE_OF_TXN varchar(25), TIME_OF_TXN varchar(25), FROM_ACCT_NUM varchar(25), TO_ACCT_NUM varchar(25), AMOUNT float, STATUS varchar(15));
mysql> describe transaction_table;
mysql> 