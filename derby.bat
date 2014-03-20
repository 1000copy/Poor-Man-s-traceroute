set DERBY_INSTALL=C:\jdk\db
set CLASSPATH=%DERBY_INSTALL%\lib\derby.jar;%DERBY_INSTALL%\lib\derbytools.jar;.
java org.apache.derby.tools.ij
java org.apache.derby.tools.sysinfo
java org.apache.derby.tools.ij

connect 'jdbc:derby:derbyDB;create=true';
create table man (name varchar(10),age int);
insert into man values('a',1);
insert into man values('a',2);
select * from man;
exit;

ij> connect 'jdbc:derby:derbyDB;create=true';
ij> connect 'jdbc:derby:derbyDB;create=true';
create table man (name varchar(10),age int);
insert into man values('a',1);
insert into man values('a',2);
警告01J01：未创建数据库“derbyDB”，而是建立到现有数据库的连接。
ij(CONNECTION1)> 已插入/更新/删除 0 行
ij(CONNECTION1)> 已插入/更新/删除 1 行
ij(CONNECTION1)> 已插入/更新/删除 1 行
ij(CONNECTION1)> select * from man;
NAME      |AGE
----------------------
a         |1
a         |2

已选择 2 行