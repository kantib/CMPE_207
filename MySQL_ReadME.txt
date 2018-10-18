Server code assumes you have installed mysql server on the machine you are running the server.
Server try to log into mysql server using <host:127.0.0.1> <login:testuser> and <password:testpassword> <db:bank>.
Hence create respective login and password on MySQL server before executing the server code. 
Below are few required MySQL commands for your reference (For Ubuntu Linux). 
More detailed information on different operating systems can be read at:
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
