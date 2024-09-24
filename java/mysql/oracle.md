>   1.   创建用户:
>
>        ```sql
>        CREATE USER user_name
>        IDENTIFIED BY your_password
>        DEFAULT TABLESPACE tablespace_name
>        TEMPORARY TABLESPACE temp_tablespace_name
>        QUOTA UNLIMITED/20M ON tablespace_name;
>        ```
>
>   2.   修改数据库密码：`alter user system identified by xxx`。
>
>   3.   一些数据库概念：
>        1.    数据库：整个数据库系统，包括多个用户和相关的对象。一个Oracle数据库可以包含多个用户。
>        2.   模式：一个用户在数据库中拥有的所有数据库对象，包括表、视图、索引等。每个用户都有自己的模式，模式与用户通常是一对一的关系。
>        3.   表空间：是数据库中的逻辑存储单元，用于组织和管理物理存储。一个表空间可以包含多个模式，一个模式可以包含多个表。
>        4.   实例：是Oracle数据库在内存中的运行状态，与数据库进程一一对应。一个实例可以服务于多个用户和数据库。
>
>   4.   (前几年试卷多次出现)oracle注释：
>        1.   单行注释`--`。
>        2.   多行注释`/*  */`
>
>   5.   (选择题)一些缩写：
>        1.   `SGA`（共享全局区） 是用于存储数据库实例共享数据和控制信息的内存区域。
>        2.   `PGA`（程序全局区） 是用于存储每个用户进程私有数据的内存区域。
>        4.   `XID `: `XID `是事务 ID，用于唯一标识一个事务。在 Oracle 数据库中，每个事务都会被分配一个唯一的 `XID`。`XID `包括全局事务 ID 和分支事务 ID，全局事务 ID 在整个数据库实例中是唯一的，而分支事务 ID 用于标识事务的不同分支。
>        5.   `SID `(Session ID): 用于唯一标识一个用户会话或连接。每个用户与数据库的连接都有一个唯一的 SID。在多用户环境中，不同的用户连接会有不同的 SID。每个数据库实例都有一个唯一的 SID。
>        6.   `SCN `: SCN 是系统变更号，用于唯一标识数据库中的某个时间点或事件。`SCN `是一个递增的数字，它在数据库中用于跟踪数据的变更和一致性。可以通过查询 `DBA_OBJECTS` 等数据字典视图来获取对象的最后变更 SCN。
>
>   6.   事务四大特性(`ACID`)：原子性、持久性、一致性、隔离性。

>oracle与mysql的比较：
>
>1.   在Oracle中，对应于MySQL中的数据库的概念是**用户**（User）。在Oracle数据库中，每个用户都有自己的模式（Schema），包含了该用户拥有的所有数据库对象，如表、视图、索引等。用户在Oracle中通常与登录认证相关联，用户可以连接到数据库，并且具有访问其模式下对象的权限。
>2.   在MySQL中，通常使用术语**数据库**（Database）表示一个独立的数据存储区域，包含了数据表、视图、存储过程等。MySQL数据库是一个物理实体，而在Oracle中，用户和模式的概念更强调了数据库对象的逻辑组织和权限管理。

###  

### oracle 体系结构

#### 需掌握的知识

1.   能够讲解内存结构、进程结构和存储结构主要关联关系。

     ```
     内存结构: 
     	SGA:系统全局区  Oracle 数据库实例的内存区域，包括共享的数据库缓存，例如缓存数据块、共享 SQL 语句和共享池等。
     		共享池
     		大池
     		java池
     		流池
     		数据库缓存区
     		日志缓存区
     	PGA:进程全局区 用户进程的私有内存区域，用于存储特定用户或进程的数据和控制信息。
     		排序区
     		会话区
     		堆栈区
     		游标区
     进程结构:
     	DBWn 数据写进程模块(将数据库缓冲区数据写到数据库文件中)
         LGWR 日志写进程模块
         略
     存储结构:
     	物理结构:
     		控制文件  很小的二进制文件、存放数据库名字(版本)、数据文件和日志文件的名称和存放路径信息。
     				 控制文件中内容能通过数据字典查看。
     		(SELECT  NAME from V$CONTROLFILE)
     		数据文件 一个数据文件对应一个数据库、是oracle存储数据的最小单位(select * from DBA_DATA_FILES)
     		日志文件 也叫重做日志文件、数据库变更的记录文件。归档模式(Archivelog)是比非归档模式(noarchivelog)安全。
     		参数文件 记录oracle数据库基本参数
     	逻辑结构：
     		表空间 最大的逻辑存储结构、由一个或者多个段组成
     		段 存储特定类型的逻辑存储单元
     		区 数据库存储空间分配的一个逻辑单元，由连续数据块组成				
     		数据块 I/O的最小单位、最小的逻辑部件
     数据库实例:	
     ```

2.   掌握体系结构中 `SGA`、`PGA `缩写含义，知晓 `SGA `内存区域中那个区域是负责存储 sql查询或排序的区域。

     ```tex
     SGA:系统全局区  Oracle 数据库实例的内存区域，包括共享的数据库缓存，例如缓存数据块、共享 SQL 语句和共享池等。
     PGA:进程全局区 用户进程的私有内存区域，用于存储特定用户或进程的数据和控制信息。
     
     shared pool(共享池)
     ```

3.   掌握表空间作为最大逻辑存储单位的定义语法，`oracle `数据库安装一般会自动安装`SYSTEM`、`SYSAUX`、`UNDOTBS1`、`TEMP `和 `USERS `表空间，了解表空间主要功能，<span style="color:red">`system `表空间是必须一直在线的。</span>

     ```tex
     SYSTEM 表空间： 存储系统表和索引，是数据库中最重要的表空间，必须一直在线。通常包含了数据库的数据字典。
     	一个表空间可以对应多个数据文件。
     	任何数据对象都必须存储在表空间中。
     	不是数据库的最大逻辑概念、是最大的逻辑存储结构
     SYSAUX 表空间： 存储一些附加的系统级别的对象，提供一些额外的管理特性。在数据库运行过程中可能会增长。
     UNDOTBS1 表空间： 存储撤销段，用于支持事务的回滚操作。必须在线，但可以有多个。
     TEMP 表空间： 用于存储临时数据，例如排序和临时表。不是持久性的表空间。
     USERS 表空间： 用于存储用户创建的数据库对象，例如表、索引等。
     ```

     ```sql
     --创建表空间
     CREATE TABLESPACE tablespace_name
     DATAFILE 'filename' SIZE file_size [AUTOEXTEND ON [NEXT file_size] [MAXSIZE max_size]]
     --创建临时表空间
     create temporary tablespace  tablespace_name tempfile '文件名.dbf' size 空间大小
     --删除表空间
     DROP TABLESPACE tablespace_name [INCLUDING CONTENTS] [AND DATAFILES];
     --重命名
     Alter TABLESPACE tablespace_name RENAME TO new_name
     --只读
     Alter TABLESPACE tablespace_name READ ONLY -- 读写:READ WRITE
     
     -- 举例
     create tablespace stu
     datafile 'D:\STU.dbf' 
     size 500M autoextend on next 5M maxsize unlimited;  -- 大小 500M，每次 5M 自动增大，最大不限制
     
     DROP TABLESPACE stu INCLUDING CONTENTS AND DATAFILES;
     
     /*
     tablespace_name： 表空间的名称。
     filename： 数据文件的名称和路径。
     file_size： 数据文件的初始大小。
     AUTOEXTEND ON： 允许数据文件自动扩展。
     NEXT file_size： 每次自动扩展的大小。
     MAXSIZE max_size： 数据文件的最大大小。
     
     tablespace_name： 要删除的表空间的名称。
     INCLUDING CONTENTS： 可选项，表示删除表空间时同时删除其中的所有对象，包括表、索引等。
     AND DATAFILES： 可选项，表示同时删除表空间关联的数据文件。
     */
     ```

     ```sql
     --(重点)查看默认表空间:创建用户时未指定，则默认users未默认表空间,temp未默认临时表空间。
     SELECT PROPERTY_VALUE
     FROM database_properties
     WHERE PROPERTY_NAME in ('DEFAULT_PERMANENT_TABLESPACE','DEFAULT_TEMP_TABLESPACE')
     
     --修改默认永久表空间
     ALTER DATABASE DEFAULT TABLESPACE spacece_name;
     --修改默认临时表空间
     ALTER DATABASE DEFAULT TEMPORARY TABLESPACE  spacece_name;
     ```

4.   掌握实例的概念以及有关的数据字典。`select instance_name from v$instance`;

     ```tex
     1. 实例（Instance）： 是Oracle数据库在内存中的运行状态。每个实例都有自己的SGA和后台进程，与其他实例相互独立。
     2. Oracle实例(instance)是一组Oracle后台进程和内存结构的集合。
     3. 一个实例只能对应一个数据库(整个Oracle数据库系统)，一个数据库有可能对应多个实例。
     ```

5.   知晓控制文件(Control File)是一个很小的二进制文件，用于描述和维护数据库的物理结构，类比数据库心脏。

6.   知晓日志（也称重做日志）文件是保证数据库安全的最重要文件之一，重做日志分为联机重做日志和归档重做日志 `Archivelog`。

7.   知晓监听器在 oracle 数据中的作用（`lister.ora` 和` lsnrctl status`） 。

     ```tex
     启动监听: lsnrctl start
     关闭监听: lsnrctl stop
     查询监听程序状态:lsnrctl status
     重要的参数文件: listener.ora tnsnames.ora
     ```

     >   数据库的启动与关闭：
     >
     >   1.   启动：`STARTUP [MOUNT | OPEN | NOMOUNT] [RESTRICT]`
     >        *   **`STARTUP NOMOUNT`：** 不加载数据库实例，只启动数据库服务。这个模式通常用于数据库恢复操作。
     >        *   **`STARTUP MOUNT`：** 将数据库实例挂载到内存，但不打开数据库。
     >        *   **`STARTUP OPEN`：** 完全打开数据库实例，允许用户连接并执行操作。
     >   2.   关闭：`SHUTDOWN [IMMEDIATE | NORMAL | TRANSACTIONAL]`
     >        *   **`IMMEDIATE`：** 立即关闭数据库，当前执行的事务将被回滚。
     >        *   **`NORMAL`：** 等待当前事务完成后关闭数据库。
     >        *   **`TRANSACTIONAL`：** 在事务完成后关闭数据库，但不接受新的事务。
     >
     >   日志：Oracle数据库中有两种主要的日志模式，分别是归档模式（Archivelog Mode）和非归档模式（Noarchivelog Mode）：
     >
     >   1.  非归档模式（Noarchivelog Mode）：
     >       *   特点： 在非归档模式下，数据库不会将日志文件归档保存，旧的归档日志文件会被覆盖，数据库只保留最新的在线重做日志文件。
     >       *   适用场景： 适用于一些测试环境或小型数据库，对于一些不需要数据备份和恢复到某个特定时间点的应用。
     >   2.  归档模式（Archivelog Mode）：
     >       *   特点： 在归档模式下，数据库会将重做日志文件归档保存到一个或多个归档日志文件中，这样可以保留数据库的历史操作记录，支持数据的完整备份和恢复。
     >       *   适用场景： 适用于生产环境，对数据的完整性和可用性要求较高的场景。归档模式提供了数据库恢复到某个特定时间点的能力。

#### 需具备的能力

1.   能够绘制 oracle 数据库体系结构图；

2.   能够根据用户要求写出创建指定表空间的定义。参见实验。

     >   习题：
     >
     >   1.   以下属于 oracle 数据库自动创建的表空间包括 (ABCDE )
     >        A. SYSTEM	 B. SYSAUX	C. UNDOTBS1	D. TEMP	E. USERS	F. USER
     >   2.   创建控制文件时，数据库需要处于 (A ) 阶段
     >        A. NOMOUNT	B. MOUNT	C. OPEN 	D. RESTRIC



### SQL*PLUS

#### 需掌握的知识

1.   `conn `连接数据库的方法，知悉用户连接时带有 `as sysdba` 含义。

     >   1.    `conn scott/password [as sysdba] `
     >   2.   `as sysdba`表示是一种特殊的连接方式，表示连接为数据库管理员(SYSDBA角色)。连接为SYSDBA具有更高的权限，可以执行一些需要管理员权限的操作，如创建和管理数据库实例、修改数据库配置等。
     >   3.   SYSTEM 用户：
     >        *   `SYSTEM` 用户在 Oracle 数据库中确实具有 `DBA` 权限，但并不具备 `SYSDBA` 权限。`DBA` 权限允许用户执行一些数据库管理员的任务，但不包括某些敏感的操作，如数据库启动和关闭。
     >        *   `SYSTEM` 用户可以通过正常的身份（不需要 `as sysdba`）登录数据库，以执行一般性的数据库管理任务。
     >   4.   SYS 用户：
     >        *   `SYS` 用户是 Oracle 数据库中的超级用户，具有 `SYSDBA` 和 `SYSOPER` 权限。
     >        *   `SYS` 用户只能通过 `as sysdba` 的方式登录数据库，确保其具备最高的权限。`SYSDBA` 权限授予用户对数据库进行广泛更改的权利，包括启动和关闭数据库。
     >   5.   `SYSTEM `用户主要用于存储 Oracle 数据库的系统管理信息，但不是数据字典的所有者。`SYS  `是 Oracle 数据库的超级用户，拥有最高权限，包括存储和管理数据字典表和视图。

2.   常用的 `sqlplus `命令，例如，`desc`、`show`、`help `等。

     >   1.   `show`: 显示当前环境变量。例如`show user\all\SGA\parameters\errors `等
     >   2.   `desc`：返回数据库中所存储的对象的描述。对于表和视图等可以列出各个列以及各个列的属性，该命令还可以输出过程、函数和程序包的规范。如`desc scott.emp`查看表结构。
     >   3.   `edit`：可以将 SQL*Plus 缓冲区的内容复制到一个名为 `afiedt.buf` 的文件中，然后启动操作系统中默认的编辑器打开这个文件，并且对于文件内容能够进行编辑。
     >   4.   `save`：将当前缓冲区的内容保存到文件中，即使缓冲区中的内容被覆盖，也保留有前面的执行语句。
     >   5.   `help`： 用于获取 SQL*Plus 帮助信息。
     >   6.   `start `或 `@`： 用于执行存储在文件中的 SQL 脚本。

3.   掌握 `DBA_`、`ALL_`和 `user_`为前缀的数据字典的含义。

     >   1.   Oracle 数据字典在创建数据库时生成，它是 oracle 数据库系统的信息核心，由一系列表和视图构成，记录了 oracle 数据库系统信息以及数据库中所有的对象信息。数据字典拥有者为 SYS 用户，物理存储在 SYSTEM 表空间中。对于所有用户(包括 DBA)数据字典是只读的，只能通过 SELECT 语句访问查询数据，数据的维护与管理由 Oracle 数据服务器内部完成。
     >   2.   前缀：
     >        1.   以 `dba `开头的数据字典名称记录数据库实例的所有对象信息。如 dba tables.
     >        2.   以 `all `开头的数据字典记录用户对象的信息和被授权访问的对象信息。
     >        3.   以 `user `开头的数据字典名称记录用户对象信息，如 user tables。

     

#### 需具备的能力

1.   能够熟练使用 `sqlplus `和 `pl/sql developer` 与 oracle 数据库交互。

2.   能够结合数据库体系结构知识，阐述 oracle 数据库 `startup `时 `nomount`、`mount `和`open `三个阶段的特点。

3.   能够运用常见的数据字典进行信息查询



### 用户、权限和模式 schema

#### 需掌握的知识

1.   知晓用户和 `schema `的区别。

     >   用户和 `schema` 的区别：
     >
     >   *   用户： 在 Oracle 中，用户是数据库的登录实体，具有自己的用户名和密码。用户可以拥有和管理自己的对象，如表、视图等。用户是数据库中的身份标识，用于验证和授权访问。
     >   *   模式(Schema) 是用户所拥有的数据库对象的集合，是一个容器，可包括表、视图、触发器、序列和索引等，通过创建一个用户的方法自动创建。模式与用户是一一对应的关系个用户对应一个 `schema`，二者名称相同。在同一模式下不能存在同名对象，但在不同模式中的对象名称可以相同。用户如果要访问其他模式对象,则必须具有对象权限,必须附加对象的完整名称为 `schema.object`。
     >
     >   *   **`Schema`：** 一个逻辑上的命名空间，用于组织和管理数据库对象。一个用户拥有一个默认的 `schema`，其名称与用户名相同。用户可以在自己的 `schema` 中创建对象，也可以访问其他用户的 `schema` 中的对象，前提是有相应的权限。

2.   掌握常见的系统权限（`create session`）和用户权限（`create table`）等。

     >   系统权限：
     >
     >   1.  `CREATE SESSION`： 允许用户连接到数据库，是最基本的系统权限。
     >   2.  `CREATE TABLE`： 允许用户在其模式（`schema`）中创建表。
     >   3.  `CREATE PROCEDURE`： 允许用户在其模式中创建存储过程或函数。
     >   4.  `CREATE SEQUENCE`： 允许用户在其模式中创建序列。
     >   5.  `CREATE VIEW`： 允许用户在其模式中创建视图。
     >   6.  `CREATE ANY TABLE`： 允许用户在任何模式中创建表，而不仅仅是在自己的模式中。
     >   7.  `unlimited tablespace`:允许用户在其他表空间创建任意表。
     >
     >   对象权限：
     >
     >   1.  `SELECT`： 允许用户查询表或视图的数据。
     >   2.  `INSERT`： 允许用户向表中插入新的行。
     >   3.  `UPDATE`： 允许用户更新表中已存在的行。
     >   4.  `DELETE`： 允许用户删除表中的行。
     >   5.  `ALTER`： 允许用户修改表的结构，如添加、删除、修改列等。
     >   6.  `DROP`： 允许用户删除表或视图。
     >   7.  `REFERENCES`： 允许用户定义外键关系。
     >   8.  `EXECUTE`： 允许用户执行存储过程或函数。
     >   9.  `USAGE`： 用于序列，允许用户使用序列。

3.   掌握常见的角色 `CONNECT`、`RESOURCE `和 `DBA `的含义。

     >   角色的含义：
     >
     >   *   `CONNECT `角色： 提供最基本的连接权限，允许用户连接到数据库。<span style="color:red">通常包含了 `CREATE SESSION` 权限，允许用户连接到数据库。这是一个较为基本的权限，适用于允许用户建立会话的场景。</span>
     >   *   `RESOURCE `角色： 提供一组更广泛的权限，允许用户在其 `schema` 中创建一些对象，如表、过程等。这个权限授予用户在其自己的 `schema` 中创建表的能力。 <span style="color:red">包含了 `CREATE TABLE`、`CREATE CLUSTER`、`CREATE SEQUENCE`、`CREATE PROCEDURE`、`CREATE TRIGGER` 等权限</span>。
     >   *   `DBA `角色： 数据库管理员角色，具有最高级别的数据库访问权限，可以执行几乎所有的数据库管理操作。

4.   授权时带有 `with admin option` 和 `with grant option`

     >   1.    带有 `WITH ADMIN OPTION` 和 `WITH GRANT OPTION` 的授权：
     >
     >         *   **`WITH ADMIN OPTION`：** 允许被授权者将授予的权限再授予给其他用户。例如，如果用户A授予用户B某个权限，并且该权限带有 `WITH ADMIN OPTION`，则用户B可以将该权限授予用户C。
     >   
     >      *   **`WITH GRANT OPTION`：** 允许被授权者将授予的权限再授予给其他用户，类似于 `WITH ADMIN OPTION`。但在某些情况下，`WITH GRANT OPTION` 可能受到更严格的限制，具体取决于所授予权限的类型。

```sql
-- 利用命令行或者 PL/SQL Developer 创建一个表空间 tbs_tsgl,数据文件大小为100M，存储路径为“d:\oracle\oradata\tsgl”，数据文件具有自动扩展性，每次增量50M，最大值为无限制。
CREATE TABLESPACE tbs_tsgl
  DATAFILE 'd:\oracle\oradata\tsgl\tbs_tsgl.dbf' SIZE 100M
  AUTOEXTEND ON NEXT 50M MAXSIZE UNLIMITED;


-- 定义一个用户 booker，定义其登录口令为 visit，设置其缺省表空间为 tbs_tsgl，临时表空间为 temp，用户 booker 在该表空间下分配定额为 20M，建立用户后保持账号锁定状态。
CREATE USER booker
  IDENTIFIED BY visit
  DEFAULT TABLESPACE tbs_tsgl
  TEMPORARY TABLESPACE temp
  QUOTA 20M ON tbs_tsgl
  ACCOUNT LOCK;


-- 修改用户 booker 状态为 unlock，授予 booker 用户 CREATE SESSION 和 SELECT ANYTABLE 和 CREATE USER 权限。授予用户 SELECT、INSERT、UPDATE、DELETE 等对象权限。
ALTER USER booker ACCOUNT UNLOCK;
GRANT CREATE SESSION, SELECT ANY TABLE, CREATE USER TO booker;
GRANT SELECT, INSERT, UPDATE, DELETE ON your_table TO booker;


-- 通过数据字典查看当前用户具有的权限有哪些。
-- 查询用户的系统权限
SELECT * FROM DBA_SYS_PRIVS WHERE GRANTEE = 'BOOKER';
-- 查询用户的对象权限
SELECT * FROM DBA_TAB_PRIVS WHERE GRANTEE = 'BOOKER';


-- 将 CONNECT、RESOURCE 角色权限授予 booker，再次查看数据字典有哪些变化？
GRANT CONNECT, RESOURCE TO booker;
-- 查询用户的系统权限
SELECT * FROM DBA_SYS_PRIVS WHERE GRANTEE = 'BOOKER';
-- 查询用户的对象权限
SELECT * FROM DBA_TAB_PRIVS WHERE GRANTEE = 'BOOKER';


-- 以 DBA 身份回收 booker 用户的各种权限。
-- 回收系统权限
REVOKE CREATE SESSION, SELECT ANY TABLE, CREATE USER FROM booker;
-- 回收对象权限
REVOKE SELECT, INSERT, UPDATE, DELETE ON your_table FROM booker;
-- 回收角色权限
REVOKE CONNECT, RESOURCE FROM booker;

-- 修改用户密码
alter user xxx identified by xxx
```



#### 需具备的能力

1.   能够按照用户要求创建用户、指定密码，并设置在表空间上的磁盘配额。

2.   能够对上述创建用户进行系统权限授权和用户权限授权。



### 数据表的定义及完整性约束

#### 需掌握的知识

1.   掌握常见数据类型定义，例如数值型` number(8.2)`、字符型 `varchar2`、`date `类型、`char `类型等。

     >1.   `NUMBER(p,s)`:既可以存储整数，也可以存储浮点数，`p `表示可存储的总位数长度，`s` 表示小数位宽。
     >2.   `CHAR(size [BYTE CHAR])`: 存储固定长度的字符串，最大支持 2000 字节,参数 `size`指定了长度，如果存储字符比 `size `小，则用空格补充填满。
     >3.   `VARCHAR2(size [BYTE|CHAR])`:用于存储可变长度的字符串，参数 `size `指定了长度,最大支持 4000 个字节，与 `char `类型不同，如果存储字符小于 `size `长度，则按照实际长度存储。
     >4.   `DATE`:存储时间日期，存储纪元、4 位年、月、日、时、分、秒，它的范围从公元前 4712年 1月 1 日到公元 9999 年 12 月 31日(共同时代)。
     >5.   `TO_DATE(string, format)`：`TO_DATE` 是一个函数，用于将字符串转换为日期类型。
     >6.   `TO_CHAR(data,format)`：将`data`类型按照所给`format`格式转为字符类型。

     ```sql
     -- 创建表
     CREATE TABLE student
     (
         student_id VARCHAR2(10) PRIMARY KEY,
         student_name VARCHAR2(50) NOT NULL,
         gender VARCHAR2(6) CHECK (gender IN ('男', '女')) NOT NULL,
         class VARCHAR2(20),
         monitor_id VARCHAR2(10) REFERENCES student(student_id),
         major_id VARCHAR2(6) REFERENCES major(major_id),
         exam_time DATE,
         score NUMBER CHECK (score > 0 AND score < 710),
         remarks VARCHAR2(100)
     );
     
     -- 插入数据
     INSERT INTO student (student_id, student_name, gender, class, monitor_id, major_id, exam_time, score, remarks)
     VALUES 
         ('001', '张三', '男', 'ClassA', '002', '181031', TO_DATE('2023-01-01', 'YYYY-MM-DD'), 90, '优秀'),
         ('002', '李四', '女', 'ClassB', '003', '181032', TO_DATE('2023-01-02', 'YYYY-MM-DD'), 85, '良好'),
     
     
     -- 删除表
     DROP TABLE your_table;
     
     
     -- 修改表:
     -- 添加列
     ALTER TABLE your_table ADD (new_column datatype);
     -- 删除列
     ALTER TABLE your_table DROP COLUMN column_to_drop;
     -- 修改数据类型
     ALTER TABLE your_table MODIFY (column_to_modify new_datatype);
     -- 添加约束
     ALTER TABLE your_table
     ADD CONSTRAINT fk_constraint FOREIGN KEY (column1) REFERENCES other_table(column1);
     -- 删除约束
     ALTER TABLE your_table
     DROP CONSTRAINT constraint_name;
     ```

2.   创建约束、主键、外键索引等

     >   1.   表约束：
     >
     >        1.   主键约束（Primary Key Constraint）： 主键用于唯一标识表中的每一行数据，并确保该列中的值不为空。主键约束的创建方式如下：
     >             
     >             ```sql
     >                CREATE TABLE your_table
     >                 (
     >                     column1 datatype PRIMARY KEY,
     >                     ...
     >                 );
     >             ```
     >
     >        3.   唯一约束（Unique Constraint）： 唯一约束确保表中的每个值都是唯一的，但允许空值。创建方式如下：
     >
     >             ```sql
     >             CREATE TABLE your_table
     >             (
     >                 column1 datatype UNIQUE,
     >                 ...
     >             );
     >             ```
     >
     >        4.   检查约束（Check Constraint）： 检查约束用于限制列中的值必须满足一定条件。例如，限制年龄必须大于等于 18：
     >
     >             ```sql
     >             CREATE TABLE your_table
     >             (
     >                 column1 datatype,
     >                 column2 datatype CHECK (column2 >= 18),
     >                 ...
     >             );
     >             ```
     >
     >        5.   外键约束（Foreign Key Constraint）： 外键用于在两个表之间建立关系，确保一个表的外键列的值在另一个表的主键列中存在。创建方式如下：
     >
     >             ```sql
     >             CREATE TABLE table1
     >             (
     >                 column1 datatype PRIMARY KEY,
     >                 ...
     >             );
     >             
     >             CREATE TABLE table2
     >             (
     >                 column1 datatype,
     >                 column1  datatypeREFERENCES table1(column1)
     >             );
     >             ```
     >
     >        6.   默认约束（Default Constraint）： 默认约束用于指定在没有为列提供值时将使用的默认值。例如：
     >
     >             ```sql
     >             CREATE TABLE your_table
     >             (
     >                 column1 datatype DEFAULT default_value,
     >                 ...
     >             );
     >             ```
     >
     >   2.   主键
     >
     >        ```sql
     >        CREATE TABLE your_table
     >        (
     >            column1 datatype,
     >            column2 datatype,
     >            ...
     >            CONSTRAINT pk_constraint PRIMARY KEY (column1) -- 多字段主键
     >        );
     >        ```
     >
     >        ```sql
     >        CREATE TABLE table1
     >        (
     >            column1 datatype PRIMARY KEY,
     >            ...
     >        );
     >        ```
     >
     >   3.   索引
     >
     >        ```sql
     >        -- 格式
     >        CREATE [unique] INDEX [user.] index_name
     >        ON [user.]table (column [ASC | DESC] [,column[ASC | DESC] ] ... )
     >                                                                                                  
     >        -- 创建学生表的索引
     >        CREATE INDEX idx_student_name ON student(student_name);
     >                                                                                                  
     >        -- 查看已创建的索引
     >        SELECT index_name, table_name, column_name
     >        FROM user_ind_columns
     >        WHERE table_name = 'STUDENT';
     >        ```

3.   知晓 NULL 的含义，能够区别于空字符和 0；

     >   1.   在oracle数据库中，`NULL` 是一个特殊的值，表示缺失或未知的数据。与其他值不同，`NULL` 不等于任何其他值，包括空字符和零。
     >
     >   2.   下面是对这三个概念的简要解释：
     >
     >        1.   `NULL`： 表示缺失或未知的值。当某一列的数据未知或不适用时，该列可以存储 `NULL` 值。`NULL` 不是空字符串或零，而是一种特殊的占位符。
     >        2.   空字符： 表示一个包含零个字符的字符串。空字符是一个有效的字符串，但与 `NULL` 不同。例如，在某些情况下，用户可能希望将空字符串与非空字符串进行区分。
     >        3.   零： 表示数字零。零是一个具体的数字值，与 `NULL` 和空字符都不同。在数值计算中，零有其特定的意义，而 `NULL` 表示缺失的值。
     >
     >   3.   在 SQL 查询中，可以使用`IS NULL `或 `IS NOT NULL` 来检查某一列是否包含 `NULL` 值(不能直接使用等号 `=`)。例如：
     >
     >        ```sql
     >        -- 查询包含 NULL 值的行
     >        SELECT * FROM your_table WHERE your_column IS NULL;
     >        
     >        -- 查询不包含 NULL 值的行
     >        SELECT * FROM your_table WHERE your_column IS NOT NULL;
     >        ```
     >
     >   4.   对`null`做加、减、乘、除等运算操作，结果仍为空
     >
     >   5.   `NVL(expr1, expr2)`:`NVL` 是 Oracle的一个函数，第一个参数是 `NULL`，则返回第二个参数的值；否则返回第一个参数的值。



#### 需具备的能力

1.   能够按照表的完整性约束要求，对创建给定字段的数据表并标注主键、外键和非空检查约束等。

2.   能够熟练掌握 scott 模式下 `emp `表和 dept 表的创建、定义等





### SQL 查询及优化技术

#### 需掌握的知识

1.   掌握在查询语句中对于字段空值额处理（`NVL `函数）。

2.   掌握分组查询、连接查询、子查询、相关子查询等常见查询语句写法。

3.   掌握一般 SQL 语句执行次序，了解常见的 SQL 语句优化技术。

     >SQL 语句的执行顺序主要包括以下几个步骤：
     >
     >1.   `FROM `子句： 在这个阶段，系统从指定的表中获取数据。如果查询涉及多个表，系统会执行连接操作，生成一个虚拟的表格。
     >2.  ` WHERE `子句： 在这个阶段，系统会根据 WHERE 子句中的条件筛选出满足条件的行。只有满足 WHERE 子句的条件的行才会被包含在结果集中。
     >3.  ` GROUP BY` 子句： 如果查询包含 GROUP BY 子句，系统会按照 GROUP BY 子句中指定的列对数据进行分组。这个阶段会生成一个分组的结果。
     >4.  ` HAVING `子句： 如果查询包含 HAVING 子句，系统会根据 HAVING 子句中的条件筛选出满足条件的分组。只有满足 HAVING 子句的条件的分组才会被包含在结果集中。
     >5.  `SELECT `子句： 在这个阶段，系统会从之前生成的结果集中选择出需要的列。这是查询的最终输出。
     >6.  `ORDER BY `子句： 如果查询包含 ORDER BY 子句，系统会根据 ORDER BY 子句中指定的列对结果进行排序。

4.   掌握并读懂 SQL 语句的查询计划，了解基于 CBO。

####  <span style="color:red">(重点)需具备的能力</span>

1.    能够按照 sql 查询语法撰写比较复杂的 SQL 语句。包括但不限于以下内容，例如在emp 表中：

      >   1.   插入数据（增）：使用 `INSERT INTO` 语句插入数据。
      >
      >       ```sql
      >       INSERT INTO table_name (column1, column2, column3, ...)
      >       VALUES (value1, value2, value3, ...);
      >       ```
      >
      >   2.   查询数据（查）：使用 `SELECT` 语句查询数据。
      >
      >       ```sql
      >       SELECT column1, column2, ...
      >       FROM table_name
      >       WHERE condition;
      >       ```
      >
      >   3.   更新数据（改）：使用 `UPDATE` 语句更新数据。
      >
      >       ```sql
      >       UPDATE table_name
      >       SET column1 = value1, column2 = value2, ...
      >       WHERE condition;
      >       ```
      >
      >   4.  删除数据（删）：使用 `DELETE FROM` 语句删除数据。
      >
      >       ```sql
      >       DELETE FROM table_name
      >       WHERE condition;
      >       ```
      >
      >   5.   模糊查询
      >
      >        1.   使用 `%` 通配符：`%` 通配符表示零个或多个字符。例如，`LIKE 'abc%'` 表示以 "abc" 开头的任何字符串。
      >
      >             *   `LIKE '%abc'` 表示以 "abc" 结尾的任何字符串。
      >             *   `LIKE '%abc%'` 表示包含 "abc" 的任何字符串。
      >
      >             ```sql
      >             SELECT * FROM employees WHERE last_name LIKE 'S%';
      >             ```
      >
      >        2.   使用 `_` 通配符：`_` 通配符表示一个单个字符。例如，`LIKE '_a%'` 表示第二个字符是 "a" 的任何字符串。
      >
      >             ```sql
      >             SELECT * FROM customers WHERE customer_name LIKE 'A_';
      >             ```
      >
      >        3. 使用 `LIKE` 和其他通配符的组合：可以组合多个通配符来实现更复杂的模糊查询。
      >
      >            ```sql
      >            SELECT * FROM products WHERE product_name LIKE '%apple%';
      >            ```
      >
      >        4.   使用 `REGEXP_LIKE` 函数进行正则表达式模糊查询：有些数据库系统支持正则表达式，通过使用 `REGEXP_LIKE` 函数可以进行更灵活的模糊查询。
      >
      >             ```sql
      >            SELECT * FROM employees WHERE REGEXP_LIKE(first_name, '^(J|K)');
      >            ```

      1.   模糊查询含有某个字母的员工信息。

      2.   查询工资 sal 收入在 1000 元和 1500 元之间人员信息。 
      3.   查询工资比 Blake 高的员工的姓名和工种。
      4.   查询各个部门的名称和员工人数。
      5.   查询各部门的平均工资。
      6.   查询工资高于所有部门平均工资的员工信息；
      7.   查询工资最高的前 3 名员工信息；
      8.   查询员工工资与各部门最低工资相同的员工信息。
      9.   查询 emp 表中哪些员工的工资高于其所在部门的平均工资。
      10.   查询部门名称为“Analyst”的员工信息。
      11.   查询工资高于与自己职位相同的员工信息。
      12.   查询 emp 中第 2 条至第 5 条记录信息。

      ```sql
      -- 1
      SELECT * FROM employees WHERE last_name LIKE '%a%';
      
      -- 2
      SELECT * FROM employees WHERE sal BETWEEN 1000 AND 1500;
      
      -- 3
      SELECT empno, ename, job FROM employees WHERE sal > (SELECT sal FROM employees WHERE ename = 'Blake');
      
      -- 4
      SELECT deptno, COUNT(*) AS employee_count FROM employees GROUP BY deptno;
      
      -- 5
      SELECT deptno, AVG(sal) AS avg_salary FROM employees GROUP BY deptno;
      
      -- 6
      SELECT * FROM employees WHERE sal > ALL (SELECT AVG(sal) FROM employees GROUP BY deptno);
      SELECT * FROM employees WHERE sal > MAX (SELECT AVG(sal) FROM employees GROUP BY deptno);
      
      -- 7
      select empno, ename, sal, ROWNUM
      from (select * from EMP order by SAL desc)
      where ROWNUM <= 3
      
      SELECT empno, ename, sal, row_num
      FROM ( SELECT empno, ename, sal, ROW_NUMBER() OVER (ORDER BY sal DESC) as row_num
            FROM EMP ) 
      WHERE row_num <= 3;
      
      -- 8
      SELECT * FROM employees e
      WHERE sal = (SELECT MIN(sal) FROM employees WHERE deptno = e.deptno);
      
      -- 9
      SELECT * FROM employees e
      WHERE sal > (SELECT AVG(sal) FROM employees WHERE deptno = e.deptno);
      
      -- 10
      SELECT * FROM employees WHERE job = 'Analyst';
      
      -- 11
      SELECT * FROM employees e
      WHERE sal > ALL (SELECT sal FROM employees WHERE job = e.job AND empno <> e.empno);
      
      
      -- 12
      SELECT *
      FROM (SELECT empno, ename, sal, ROWNUM as rnum
            FROM emp
            WHERE ROWNUM <= 5)
      WHERE rnum >= 2;
      ```

      >   1.   一些聚合函数：<span style="color:red">注意`WHERE`子句一般不能使用聚合函数</span>。
      >
      >        1.   `NVL`:
      >             *   用于处理空值（NULL）。如果第一个表达式的值为 NULL，则返回第二个表达式的值，否则返回第一个表达式的值。
      >             *   示例：`SELECT NVL(column_name, 'Default_Value') FROM table_name;`
      >        2.   `MAX`:
      >             *   用于返回某列的最大值。
      >             *   示例：`SELECT MAX(column_name) FROM table_name;`
      >        3.   `MIN`:
      >             *   用于返回某列的最小值。
      >             *   示例：`SELECT MIN(column_name) FROM table_name;`
      >        4.   `COUNT`:
      >             *   用于计算满足指定条件的行数。
      >             *   示例：`SELECT COUNT(*) FROM table_name WHERE condition;`
      >        5.   `AVG`:
      >             *   用于计算某列的平均值。
      >             *   示例：`SELECT AVG(column_name) FROM table_name;`
      >        6.   `SUM`:
      >             *   用于计算某列值的总和。
      >             *   示例：`SELECT SUM(column_name) FROM table_name;`
      >
      >   2.   `any`与`all`
      >
      >        1.   `ALL`:
      >             *   `ALL` 关键字用于比较一个值和子查询返回的所有值，如果所有值都满足条件，则返回 `TRUE`；否则返回 `FALSE`。
      >             *   示例：`SELECT column_name FROM table_name WHERE column_name > ALL (SELECT another_column FROM another_table);`
      >        2.   `ANY`/`SOME`:
      >             *   `ANY` 或 `SOME` 关键字用于比较一个值和子查询返回的任何值，只要有一个值满足条件，就返回 `TRUE`；否则返回 `FALSE`。
      >             *   示例：`SELECT column_name FROM table_name WHERE column_name > ANY (SELECT another_column FROM another_table);`
      >
      >        3.   这两个关键字通常用于配合比较运算符，如 `>、<、=、>=、<=` 等。
      >
      >   3.   `DESC`降序排序、`ASC`升序排序。

2.   能够利用分析函数完成要求的分组查询，例如利用 `ROW_NUMBER ( )` `OVER (partition by id1 order by id2 desc)`实现一组数据按照指定的字段进行分割成组，然后组内按照某个字段排序编号。

     >   1.   `OVER` 子句是在 Oracle SQL 中用于指定分析函数（Analytic Functions）的窗口范围的一种方式。
     >
     >        ```sql
     >        analytic_function() OVER (
     >          [PARTITION BY partition_expression, ... ]
     >          ORDER BY sort_expression [ASC | DESC], ...
     >          windowing_clause
     >        )
     >        /*
     >        analytic_function 是要使用的分析函数，如 SUM(), AVG(), ROW_NUMBER() 等。
     >        PARTITION BY 子句可用于将结果集划分为多个分区，每个分区内的计算是独立的。
     >        ORDER BY 子句定义了分析函数计算的排序规则。
     >        windowing_clause 定义了窗口范围，常见的有 ROWS BETWEEN ... AND ... 和 RANGE BETWEEN ... AND ...。
     >        */
     >        ```
     >
     >   2.   `ROW_NUMBER()` 函数为查询结果集中的每一行分配一个唯一的整数值，该值是根据指定的排序规则确定的。
     >
     >        ```sql
     >        SELECT
     >          column1,
     >          column2,
     >          ROW_NUMBER() OVER (ORDER BY column1) AS row_num
     >        FROM your_table;
     >        ```
     >
     >   3.   `RANK()` 函数为查询结果集中的每一行分配一个排名值，具有相同的值的行将共享相同的排名，并且下一个排名将按照跳过相同排名的行数进行分配。
     >
     >        ```sql
     >        SELECT
     >          column1,
     >          column2,
     >          RANK() OVER (ORDER BY column1) AS rank_value
     >        FROM your_table;
     >        ```
     >
     >   4.   `DENSE_RANK()` 函数类似于 `RANK()`，但不会跳过相同排名的行，即具有相同值的行将共享相同的排名，下一个排名将始终递增。
     >
     >        ```sql
     >        SELECT
     >          column1,
     >          column2,
     >          DENSE_RANK() OVER (ORDER BY column1) AS dense_rank_value
     >        FROM your_table;
     >        ```

     1.   查询各部门工资排名位于前三名的员工信息。
     2.   查询工资低于 2000 元的员工姓名和部门，并显示符合条件员工总数。




### 数据库建模工具 PowerDesigner

#### 需掌握的知识

1.   掌握数据库常见的规范性要求。

2.   掌握 power designer 中 `CDM`、`PDM `基本含义，知晓什么是逆向工程。

#### 需具备的能力

1.   能够熟练使用 `pd`，针对跟定用户需求进行数据库建模。（项目实践报告中考核）

### 序列、视图和游标

#### 需掌握的知识

1.   掌握序列的语法定义，`curval `和 `nextval `两个伪列的含义。

     >   1.    在 Oracle 数据库中，序列（Sequence）是一种用于生成唯一数值的对象。序列通常用于生成主键值，确保在表中插入唯一的标识符。
     >   2.   创建序列后，可以使用 `NEXTVAL` 和 `CURRVAL` 两个伪列获取序列的下一个值和当前值。
     >   3.   首先引用序列必须先使用 `NextVal`，然后使用 `Currval`，否则出错;每次使用`NextVal`时，Oracle 会根据创建参数产生新的伪列，新的伪列值被赋予 `CurrVal`。查询 `CurrVal `不会立生新的序列值。多用户会话使用同一序列值，保持增量且唯一，不会重复。

     ```sql
     -- 格式
     CREATE SEQUENCE sequence_name
       [INCREMENT BY n]
       [START WITH n]
       [MAXVALUE n | NOMAXVALUE]
       [MINVALUE n | NOMINVALUE]
       [CYCLE | NOCYCLE]
       [CACHE n | NOCACHE];
     /*
     sequence_name：序列的名称。
     INCREMENT BY n：指定每次增加的步长，默认为 1。
     START WITH n：指定序列的起始值，默认为 1。
     MAXVALUE n | NOMAXVALUE：指定序列的最大值，或者使用 NOMAXVALUE 表示没有最大值。
     MINVALUE n | NOMINVALUE：指定序列的最小值，或者使用 NOMINVALUE 表示没有最小值。
     CYCLE | NOCYCLE：指定序列达到最大值后是否循环，默认为 NOCYCLE。
     CACHE n | NOCACHE：指定是否缓存序列值，默认为 NOCACHE。
     */
     
     -- 创建序列
     CREATE SEQUENCE emp_seq
       INCREMENT BY 1
       START WITH 1
       MAXVALUE 1000
       NOCYCLE
       CACHE 10;
     
     -- 获取下一个值
     SELECT emp_seq.NEXTVAL FROM dual;
     
     -- 获取当前值
     SELECT emp_seq.CURRVAL FROM dual;
     ```

2.   掌握由游标的语法定义、游标的常见属性`%ISOPEN`、`%FOUND`、`%NOTFOUND`、`%ROWCOUNT`

     >1.   游标（`Cursor`）用于对查询结果集进行迭代处理。
     >2.   对于非查询语句，如修改、删除操作，则由ORACLE 系统自动地为这些操作设置游标并创建其工作区，这些由系统隐含创建的游标称为隐性游标，隐性游标的名字为`SQL`，这是由ORACLE 系统定义的。对于隐性游标的操作，如定义、打开、取值及关闭操作，都由ORACLE 系统自动地完成，无需用户进行处理。用户只能通过隐式游标的相关属性，来完成相应的操作。
     >3.   常见属性：
     >     1.   `%ISOPEN`：判断游标是否处于打开状态（`TRUE `或 `FALSE`）。
     >     2.   `%FOUND`：判断最后一次 `FETCH` 操作是否成功找到一行数据（`TRUE `或 `FALSE`）。
     >     3.   `%NOTFOUND`：判断最后一次 `FETCH` 操作是否未找到数据（`TRUE `或 `FALSE`）。
     >     4.   `%ROWCOUNT`：获取当前游标位置的行号。

     ```sql
     DECLARE
        CURSOR cursor_name IS
         SELECT column1, column2, ...
         FROM your_table
         WHERE your_condition;
     
       -- 声明用于存储查询结果的变量(employees.first_name%TYPE 是数据类型引用，表示变量类型与employees表的first_name列的数据类型相同)
       variable1 datatype;
       variable2 datatype;
       ...
     
     BEGIN
       -- 打开游标
       OPEN cursor_name;
     
       -- 使用游标
       LOOP
         FETCH cursor_name INTO variable1, variable2, ...;
         EXIT WHEN cursor_name%NOTFOUND;
     
         -- 在此处进行处理
         -- ...
     
       END LOOP;
     
       -- 关闭游标
       CLOSE cursor_name;
     
     END;
     ```

     ```sql
     -- 显示游标+loop循环
     declare
     vno number(5);
     vname varchar2(20);
     cursor c is select empno,ename from emp;
     begin
        open c;
           loop
               fetch c into vno,vname;
               exit when c%notfound;
               dbms_output.put_line(vno||'   '||vname);  	-- || 用于拼接字符串
           end loop;
        close c;
     end;
     
     -- 显示游标+for循环
     打印emp表中的员工编号和员工姓名：
     declare
     vno number(10);
     vname varchar2(20);
     cursor c is select empno,ename from emp;
     begin
         open c;
            fetch c into vno,vname; 
            while c%found loop
               dbms_output.put_line(vno||'  '||vname);
               fetch  c into vno,vname;   //这句话是为了使最后游标找不到值，而能够跳出循环
            end loop; 
         close c;
     end;
     
     -- 显示游标+while循环
     打印emp表中的员工编号和员工姓名：
     declare
     i emp%rowtype;
     cursor c is select empno,ename from emp;
     begin
        for i in c loop
            dbms_output.put_line(i.empno||'  '||i.ename);
        end loop;
     end;
     
     -- 隐性游标(查看更新了几条数据)
     declare
     begin
         update emp set deptno=11 where deptno=10;     
         if sql%notfound then
         dbms_output.put_line('没有找到该条数据');
         else
         dbms_output.put_line('更新了'||sql%rowcount||'数据');
         end if;
     end;
     ```

3.   掌握游标的使用规范（`open`、`fetch`、`close`）

     >   1.   `OPEN `： 打开游标，将查询结果集放入内存，准备开始遍历。
     >   2.   `FETCH `： 获取游标当前指向的行，将数据存储到变量中。
     >   3.   `CLOSE `： 关闭游标，释放相关资源。

4.   掌握视图的定义，多表视图的组成。

     >   1.   多表视图是基于多个表的查询结果构建的视图。在多表视图中，可以通过连接操作来获取来自多个表的数据。
     >   2.   所谓视图是由`select`子查询语句定义的一个虚表。
     >   3.   `WITH CHECK OPTION` 是用于定义视图时的一个选项。它确保在插入或更新数据时，只有满足视图定义中指定的条件的数据才能通过视图进行修改。
     >   4.   视图是由 `select `子查询语句定义的一个逻辑表。视图中不会保存有数据。但可以通过视图操作数据库中数据，例如`INSERT INTO my_view (column1, column2) VALUES ('value1', 'value2')`。

     ```sql
     -- 格式
     CREATE [OR REPLACE] [FORCE|NOFORCE] VIEW 视图名
     AS
     SELECT 查询语句
     WITH READ ONLY; -- 只读
     /*
     CREATE VIEW: 表示创建一个视图。
     OR REPLACE: 表示如果同名的视图已经存在，则会被替换。
     FORCE|NOFORCE: 可选项，用于指定创建视图时是否强制依赖于底层表的存在。FORCE 表示强制依赖，NOFORCE 表示不强制依赖。
     AS: 表示关键字，用于引导后面的查询语句，即视图的定义。
     WITH READ ONLY: 可选项，表示该视图是只读的，不能用于执行更新操作。如果不希望通过视图进行数据修改，可以使用该选项。
     */
     
     -- 创建视图
     CREATE OR REPLACE FORCE VIEW emp_summary
     AS
     SELECT emp_id, emp_name, department, salary
     FROM employee
     WHERE salary > 50000
     
     -- 查询
     SELECT * FROM emp_summary;
     
     -- 多表视图
     CREATE VIEW multi_table_view AS
     SELECT employee_id, employee_name, department_name
     FROM employees
     JOIN departments ON employees.department_id = departments.department_id;
     ```

5.   (补充)同义词：同义词 `synonym `用于定义数据库对象别名，可隐藏对象真实名称信息，也可以缩短具有模式的长对象名,或者使对象名更容易被理解。和视图的功能类似实质上就是一种映射关系。

     ```sql
     -- 创建同义词:public表示公共，不写表示private
     CREATE [OR REPLACE][PUBLIC] SYNONYM synonym_name
     FOR [schema.]object;
     
     -- 删除同义词
     DROP [PUBLIC] SYNONYM synonym_name
     ```

     

#### 需具备的能力

1.   能够按照用户给定要求创建一个整数序列，能够用于对表插入数据时作为自增主键。

     ```sql
     -- 创建
     CREATE SEQUENCE user_defined_seq
       INCREMENT BY 1
       START WITH 1
       MAXVALUE 999999999
       NOCYCLE
       NOCACHE;
       
     -- 使用
     INSERT INTO your_table (id, column1, column2)
     VALUES (user_defined_seq.NEXTVAL, 'value1', 'value2');
     
     ```

2.   能够定义一个游标，实现对用户表的访问并输出信息。例如，输入雇员编号，输出`emp `表员工信息。

     ```sql
     DECLARE
       -- 定义变量用于接收用户输入的雇员编号
       v_empno NUMBER;
     
       -- 定义游标
       CURSOR emp_cursor (p_empno NUMBER) IS
         SELECT empno, ename, job, sal
         FROM emp
         WHERE empno = p_empno;
     
       -- 定义变量用于存储查询结果
       v_emp_info emp_cursor%ROWTYPE; -- %ROWTYPE 表示使用该游标的查询结果的行结构。
     
     BEGIN
       -- 用户输入雇员编号
       v_empno := &input_empno; -- & 表示输入变量，可以根据实际情况修改获取用户输入的方式
     
       -- 打开游标
       OPEN emp_cursor(v_empno);
     
       -- 获取查询结果
       FETCH emp_cursor INTO v_emp_info;
     
       -- 判断是否有查询结果
       IF emp_cursor%FOUND THEN
         -- 输出员工信息
         DBMS_OUTPUT.PUT_LINE('Employee Number: ' || v_emp_info.empno);
         DBMS_OUTPUT.PUT_LINE('Employee Name: ' || v_emp_info.ename);
         DBMS_OUTPUT.PUT_LINE('Job: ' || v_emp_info.job);
         DBMS_OUTPUT.PUT_LINE('Salary: ' || v_emp_info.sal);
       ELSE
         -- 没有查询到结果
         DBMS_OUTPUT.PUT_LINE('Employee not found for Employee Number: ' || v_empno);
       END IF;
     
       -- 关闭游标
       CLOSE emp_cursor;
     END;
     /  -- PL/SQL中，斜杠(/)通常用于执行或运行之前已经定义好的PL/SQL块或语句。
     ```

3.   能够按照要求创建一个用户视图。

4.   一些权限补充：

     >   1.   操作视图权限(含`alter`、`drop`、`create`)：`grant create view to xxx`。
     >   2.   操作序列权限(含`alter`、`drop`、`create`)：`grant create sequence to xxx`。





### PL/SQL 编程

#### 需掌握的知识

1.   掌握 `PL/SQL` 编程额基本语法、语句和异常处理。

     >   1.   基本语法：
     >
     >        1.   块结构：PL/SQL 代码通常包含在块中，一个块以 `DECLARE` 开始，以 `END;` 结束。块中可以包含声明、执行语句和异常处理。
     >
     >            ```sql
     >            DECLARE
     >               -- 声明部分
     >            BEGIN
     >               -- 执行语句部分
     >            EXCEPTION
     >               -- 异常处理部分
     >            END;
     >            ```
     >
     >        2.    变量声明：使用 `DECLARE` 部分声明变量。
     >
     >             ```sql
     >             DECLARE
     >                variable_name datatype;
     >             ```
     >
     >        3.   赋值语句：使用 `:=` 运算符进行赋值。<span style="color:red">获取用户输入`user_id:= &id`,即使用`&`</span>。
     >
     >             ```sql
     >             variable_name := value;
     >             ```
     >
     >   2.   基本语句：
     >
     >        1.   条件语句（IF-THEN-ELSE）：
     >
     >            ```sql
     >            IF condition THEN
     >               -- 如果条件成立的代码
     >            ELSE
     >               -- 如果条件不成立的代码
     >            END IF;
     >            ```
     >
     >        2.   循环语句（LOOP）：
     >
     >             ```sql
     >             LOOP
     >                -- 循环体内的代码
     >             END LOOP;
     >             ```
     >
     >        3.   FOR LOOP：
     >
     >             ```sql
     >             FOR variable_name IN [reverse] lower_bound..upper_bound LOOP
     >                -- 循环体内的代码
     >             END LOOP;
     >             ```
     >
     >   3.   `case`语句：
     >
     >        1.   第一种使用方式：
     >
     >             ```sql
     >             CASE
     >                WHEN condition1 THEN result1
     >                WHEN condition2 THEN result2
     >                ...
     >                ELSE default_result
     >             END AS alias_name
     >             ```
     >
     >             ```sql
     >             SELECT
     >               product_name,
     >               CASE
     >                 WHEN quantity > 10 THEN 'High Demand'
     >                 WHEN quantity > 5 THEN 'Moderate Demand'
     >                 ELSE 'Low Demand'
     >               END AS demand_level
     >             FROM
     >               products;
     >             ```
     >
     >        2.   第二种使用方式：
     >
     >             ```sql
     >             CASE
     >                WHEN column_name = value1 THEN result1
     >                WHEN column_name = value2 THEN result2
     >                ...
     >                ELSE default_result
     >             END case;
     >             ```
     >
     >             ```sql
     >             begin
     >             	case
     >             	...
     >             	end case;
     >             end;
     >             ```
     >
     >   4.   判断语句
     >
     >        1.   `if`：
     >
     >             ```sql
     >             IF condition1 THEN
     >             	...
     >             ELSIF condition2 THEN
     >             	...
     >             ELSE
     >             	...
     >             END IF;
     >             ```
     >
     >        2.   `exist()`判断语句是否查询到，有则为`true`。
     >
     >             ```sql
     >             IF EXISTS (SELECT 1 FROM stu WHERE student_id = p_student_id) THEN
     >             ...
     >             end if;
     >             ```
     >
     >        3.   `when`:
     >
     >             ```sql
     >             -- 1
     >             WHEN condition1 THEN
     >                  ...
     >                        
     >             -- 2
     >             exit when condition1
     >             ```
     >
     >             
     >
     >   5.   异常处理：通过 `EXCEPTION` 部分实现。可以捕获特定的异常并处理，也可以使用 `OTHERS` 处理未指定的异常。
     >
     >        ```sql
     >        BEGIN
     >           -- 代码
     >        EXCEPTION
     >           WHEN exception1 THEN
     >              -- 处理 exception1 的代码
     >           WHEN exception2 THEN
     >              -- 处理 exception2 的代码
     >           WHEN OTHERS THEN
     >              -- 处理其他异常的代码
     >        END;
     >        ```

2.   掌握常见的系统异常类型，例如 `NO_DATA_FOUND`、`DUP_VAL_ON_INDEX` 等含义。

     >   1.  ` NO_DATA_FOUND`：当 SELECT 语句未找到任何数据时抛出的异常。
     >
     >       ```sql
     >       DECLARE
     >          my_value NUMBER;
     >       BEGIN
     >          SELECT salary INTO my_value FROM employees WHERE employee_id = 1000;
     >          DBMS_OUTPUT.PUT_LINE('Salary: ' || my_value);
     >       EXCEPTION
     >          WHEN NO_DATA_FOUND THEN
     >             DBMS_OUTPUT.PUT_LINE('Employee not found.');
     >       END;
     >       ```
     >
     >   2.   `TOO_MANY_ROWS`：当 SELECT 语句返回多行数据时抛出的异常。
     >
     >       ```sql
     >       DECLARE
     >          my_value NUMBER;
     >       BEGIN
     >          SELECT salary INTO my_value FROM employees WHERE department_id = 10;
     >          DBMS_OUTPUT.PUT_LINE('Salary: ' || my_value);
     >       EXCEPTION
     >          WHEN TOO_MANY_ROWS THEN
     >             DBMS_OUTPUT.PUT_LINE('Multiple employees found.');
     >       END;
     >       ```
     >
     >   3.  `DUP_VAL_ON_INDEX`：当试图在唯一索引上插入重复值时抛出的异常。
     >
     >       ```sql
     >       DECLARE
     >          duplicate_value EXCEPTION;
     >          PRAGMA EXCEPTION_INIT(duplicate_value, -1);
     >       BEGIN
     >          INSERT INTO employees (employee_id, first_name, last_name)
     >          VALUES (100, 'John', 'Doe');
     >       EXCEPTION
     >          WHEN duplicate_value THEN
     >             DBMS_OUTPUT.PUT_LINE('Duplicate employee ID.');
     >       END;
     >       ```
     >
     >   4.  `ZERO_DIVIDE`：当试图除以零时抛出的异常。
     >
     >       ```sql
     >       DECLARE
     >          result NUMBER;
     >       BEGIN
     >          result := 10 / 0;
     >       EXCEPTION
     >          WHEN ZERO_DIVIDE THEN
     >             DBMS_OUTPUT.PUT_LINE('Cannot divide by zero.');
     >       END;
     >       ```

3.   掌握过程、函数、触发器的定义语法，知晓行级触发器和语句及触发器的区别。

     >   1.   存储过程：
     >
     >        1.   创建和运行格式
     >
     >             ```sql
     >             -- 创建
     >             CREATE [OR REPLACE] PROCEDURE procedure_name (parameter1 datatype, parameter2 datatype, ...) IS
     >                -- 声明变量和常量等
     >             BEGIN
     >                -- 存储过程的逻辑代码
     >
     >                -- 可以包含数据操作、控制结构、异常处理等
     >
     >             EXCEPTION
     >                -- 异常处理部分，可选
     >                WHEN OTHERS THEN
     >                   -- 处理其他异常的代码
     >
     >             END;
     >
     >             -- 运行
     >             / -- 默认运行上一个代码块
     >             execute/exec procedure_name (parameter1 datatype, parameter2 datatype, ...) -- 执行指定
     >
     >             -- 删除
     >             DROP PROCEDURE procedure_name;
     >             ```
     >
     >        2.   举例说明：表见下面触发器举例部分
     >
     >             ```sql
     >             -- 创建存储过程:修改指定用户密码
     >             CREATE [OR REPLACE] PROCEDURE reset_pwd(user_name users.user_name%type, user_pwd users.pwd%type) IS
     >             BEGIN
     >                 update users set pwd = user_pwd where user_name = user_name;
     >             end;
     >        
     >             ```
     >
     >   2.   函数：
     >
     >        1.   创建和运行：
     >
     >             ```sql
     >             -- 创建
     >             CREATE [OR REPLACE] FUNCTION function_name (parameter1 datatype, parameter2 datatype, ...) RETURN return_datatype IS
     >                -- 声明变量和常量等
     >                v_result return_datatype;
     >             
     >             BEGIN
     >                	-- 函数的逻辑代码
     >             
     >             	-- 可以包含数据操作、控制结构、异常处理等
     >             
     >             	RETURN v_result;  -- 返回结果
     >             EXCEPTION
     >                   -- 异常处理部分，可选
     >                   WHEN OTHERS THEN
     >                   -- 处理其他异常的代码
     >                   RETURN NULL;  -- 或者返回其他默认值
     >             END;
     >             
     >              -- 运行
     >             / -- 默认运行上一个代码块
     >             execute/exec procedure_name (parameter1 datatype, parameter2 datatype, ...)  -- 执行指定
     >             -- 此外还可以直接在select中使用
     >             
     >             -- 删除
     >             DROP FUNCTION procedure_name;
     >
     >        2.   举例说明：获取某个用户的密码。
     >
     >             ```sql
     >             create [or replace] function GetPwd(tmp_name IN Users.UserName%type)
     >              	Return Users.UserPwd%type
     >                 IS
     >                 OutPwd Users.UserPwd%type;
     >             begin
     >                 select UserPwd
     >                           into OutPwd
     >                 from Users
     >                 where UserName = "|| tmp_name ||";
     >                 DBMS_OUTPUT.PUT_LINE('密码是:'||OutPwd)
     >              return OutPwd;
     >             end;
     >             
     >             execute/exec GetPwd('fish')
     >
     >   3.   触发器：
     >
     >        1.   创建和运行：
     >
     >             ```sql
     >             -- 创建
     >             CREATE [OR REPLACE] TRIGGER trigger_name
     >             {BEFORE  | AFTER | INSTEAD OF} -- 触发时机(view中是instead of替换原来的视图操作语句)
     >             {INSERT  | UPDATE  | DELETE} -- 触发的事件
     >             [OF column [, column …] -- 触发字段
     >                                                                                   ON table_name -- 目标表
     >             [REFERENCING OLD AS old NEW AS new] -- 可选，用于引用旧值和新值
     >             [FOR EACH ROW] -- 指定触发器的执行频率
     >            [WHEN] -- 触发条件
     >             [FOLLOWS other_trigger] -- 指定触发顺序
     >            DECLARE
     >                -- 触发器的PL/SQL代码
     >            BEGIN
     >                -- 触发器的PL/SQL代码
     >             END;
     >             /
     >
     >             -- 删除
     >             DROP TRIGGER trigger_name
     >
     >             -- 启用/禁用触发器
     >             ALTER TRIGGER your_trigger_name ENABLE/DISABLE
     >             ```
     >
     >        2.   `REFERENCING OLD` 和 `REFERENCING NEW` 的含义不同，具体取决于触发器是行级还是语句级触发器。对于行级触发器，`REFERENCING OLD` 子句允许引用更新或删除之前行中的值，`REFERENCING NEW` 子句允许引用已插入或更新的值。在 `BEFORE` 和 `AFTER` 触发器中可以引用 `OLD` 和 `NEW` 行。`REFERENCING NEW` 子句允许在插入或更新操作发生之前在 `BEFORE` 触发器中修改新行
     >
     >        3.   在使用前还需了解<span style="color:red">行级触发器</span>两个伪记录变量`NEW`和`OLD`。
     >
     >             1.   `:old `操作之前，是记录变量，使用形式：`:old.字段名`。`:new` 操作之后，是记录变量，使用形式：`:new.字段名`。
     >                       2.   `:NEW` 和:`OLD`使用方法和意义，`new` 只出现在`insert`和`update`时，`old`只出现在`update`和`delete`时。在`insert`时`new`表示新插入的行数据，`update`时`new`表示要替换的新数据、`old`表示要被更改的原来的数据行，`delete`时`old`表示要被删除的数据。
     >             3.   `begin`前面出现的`new`，`old`不加冒号，`begin`和`end`之间出现的`new`和`old`都要在前面加上`:`。
     >
     >                  4.   举例说明：创建自增主键
     >
     >             ```sql
     >             -- 创建自增序列作为自增主键
     >             
     >             CREATE SEQUENCE pk_auto
     >              increment by 1
     >                 start with 1
     >              maxvalue 99999
     >                 nominvalue
     >                 nocycle
     >                 nocache
     >             
     >             -- 创建表
     >            CREATE TABLE users
     >             (
     >                 user_id   number(8) default pk_auto.nextval primary key,
     >                                                                                                                                                   pwd       VARCHAR2(20),
     >                 user_name varchar2(20)
     >             );
     >             
     >             -- 创建触发器
     >             CREATE OR REPLACE TRIGGER auto_insert
     >                 BEFORE INSERT ON USERS
     >                 FOR EACH ROW
     >                                                                                   BEGIN
     >                 SELECT pk_auto.NEXTVAL   -- 获取序列值并替换插入的新值中的user
     >                 INTO :new.user_id
     >                 FROM dual;
     >             END;
     >             /
     >             
     >             -- 插入数据
     >                                                                         insert into users(pwd, user_name)
     >             values ('fish', 'fish')
     >             ```
     
4.   了解替代触发器的本质，了解系统事件触发器。

     >   1.   本质：替代触发器的本质是在用户执行 `DML `操作时，触发器会在操作发生之前（`BEFORE`）或之后（`AFTER`）代替默认的数据库操作。它允许开发人员在执行 `DML `操作时定义自定义的逻辑，而不是使用数据库默认的行为。
     >   2.   系统事件触发器是一种特殊类型的触发器，它与数据库的系统事件相关联。这些触发器是在数据库级别上定义的，与特定表或视图无关。系统事件触发器可以用于捕获数据库级别的事件，例如数据库启动或关闭、DDL 语句的执行等。
     >   3.   常见误区：
     >        1.   触发器可以看做一种特殊的存储过程。
     >        2.   触发器被事件触发。
     >        3.   触发器不接收参数，且无法被显示调用。带有`for each row`是行级触发器。
     >   4.   行触发对触发事件影响的每一行执行触发器。语句触发对于触发事件只能触发一次，而且不能访问受触发器影响的每一行的值。

5.   掌握包的有规范和定义组成，了解常见数据包 `DBMS_OUTPUT` 等。

     >   1.   在 Oracle 中，包是一种封装数据库对象的方式，通常包含了过程、函数、变量、常量和游标等。包的主要目的是将相关的功能和数据组织在一起，提高代码的可维护性和重用性。包分为两个主要部分：包规范（Specification）和包体（Body）。
     >
     >   2.   包规范： 包规范定义了包中公共的接口，包含了声明过程、函数、变量、常量等的信息，但不包含具体的实现。
     >
     >        ```sql
     >        CREATE OR REPLACE PACKAGE my_package IS
     >          PROCEDURE my_procedure(p_param1 NUMBER);
     >          FUNCTION my_function(p_param2 VARCHAR2) RETURN NUMBER;
     >          -- 其他声明
     >        END my_package;
     >        /
     >        ```
     >
     >   3.   包体（Body）： 包体包含了包规范中声明的过程和函数的具体实现，以及其他私有的变量和过程等。
     >
     >        ```sql
     >        CREATE OR REPLACE PACKAGE BODY my_package IS
     >          PROCEDURE my_procedure(p_param1 NUMBER) IS
     >          BEGIN
     >            -- 具体实现
     >            NULL;
     >          END my_procedure;
     >          
     >          FUNCTION my_function(p_param2 VARCHAR2) RETURN NUMBER IS
     >          BEGIN
     >            -- 具体实现
     >            RETURN 0;
     >          END my_function;
     >          -- 其他实现
     >        END my_package;
     >        /
     >        ```
     >
     >   4.   `DBMS_OUTPUT` 是 Oracle 提供的一个用于向客户端输出消息的包，通常在调试过程中使用。通过 `DBMS_OUTPUT.PUT_LINE` 可以在包体中输出调试信息，然后通过客户端工具（如 SQL*Plus）的设置来查看这些信息。请注意，为了使用 `DBMS_OUTPUT`，需要在客户端工具中启用输出`SET SERVEROUTPUT ON`。

6.   补充一些权限

     >   1.   操作触发器权限(含`alter`、`drop`、`create`)：`grant create trigger to xxx`。
     >   2.   操作存储过程权限(含`alter`、`drop`、`create`)：`grant create produce to xxx`。



### 需具备的能力

1.   能够熟练编写 `PL/SQL` 程序，定义常量、变量。

     ```sql
     -- 定义常量
     DECLARE
        constant_name CONSTANT datatype := value;
     
     -- 定义变量
     DECLARE
     variable_name datatype;
     ```

2.   能够针对用户要求进行异常处理。例如，在给定用户编号情况下查询 `emp `表，<span style="color:red">定义用户自定义异常</span>或使用 `RAISE_APPLICATION_ERROR `抛出异常，保证程序的正确流程。

     >   1.   使用异常处理机制来捕获和处理程序中可能出现的异常。
     >   2.   `PRAGMA EXCEPTION_INIT(CUSTOM_EXCEPTION, code)`:设置自定义异常的错误代码。当然此前需要先自定义一个异常`CUSTOM_EXCEPTION`。
     >   3.   `RAISE customize_exp `：抛出自定义异常。
     >   4.   `RAISE_APPLICATION_ERROR(error_code, error_message)`:抛出自定义应用程序错误的函数。
     >        1.   `error_code` 是一个 3 位整数，用于标识自定义错误。错误代码必须在范围 -20000 到 -20999 之间，以避免与 Oracle 内部错误代码冲突。
     >        2.   `error_message` 是一个字符串，用于描述自定义错误的详细信息。
     >   5.   以下是一个示例，其中根据给定的用户编号查询 `emp `表，并在找不到用户时抛出自定义异常。

     ```sql
     DECLARE
        v_emp_name employees.first_name%TYPE;
        v_emp_id employees.employee_id%TYPE := &user_id;  -- 用户输入的员工编号
     
        -- 自定义异常
        CUSTOM_EXCEPTION EXCEPTION;
        -- PRAGMA EXCEPTION_INIT(CUSTOM_EXCEPTION, -20001); 设置异常代码
     BEGIN
        -- 使用 SELECT INTO 语句查询员工姓名
        SELECT first_name INTO v_emp_name FROM employees WHERE employee_id = v_emp_id;
     
        -- 如果找到员工，则输出员工姓名
        DBMS_OUTPUT.PUT_LINE('Employee Name: ' || v_emp_name);
     
     EXCEPTION
        WHEN NO_DATA_FOUND THEN
           -- 当没有找到数据时抛出自定义异常
           RAISE_APPLICATION_ERROR(-20001, 'Employee with ID ' || v_emp_id || ' not found.');
           -- 另一种方式
           RAISE CUSTOM_EXCEPTION; -- 抛出自定义异常
     
        WHEN OTHERS THEN
           -- 捕获其他异常并输出错误信息
           DBMS_OUTPUT.PUT_LINE('An error occurred: ' || SQLERRM);
     END;
     /
     ```

3.   能够运用`%type`、`%rowtype` 定义变量，并且运用在 `PL/SQL` 编程中。

     >   1.   `%TYPE` 用于定义变量的数据类型，该数据类型与指定列的数据类型相匹配。例如：
     >
     >        ```sql
     >        DECLARE
     >           emp_salary employees.salary%TYPE;
     >        BEGIN
     >           -- 这里的 emp_salary 变量的数据类型与 employees 表的 salary 列相匹配
     >           SELECT salary INTO emp_salary FROM employees WHERE employee_id = 100;
     >           DBMS_OUTPUT.PUT_LINE('Employee Salary: ' || emp_salary);
     >        END;
     >        /
     >        ```
     >
     >   2.   `%ROWTYPE` 用于定义变量，该变量的数据类型与指定表的一行记录相匹配。例如：
     >
     >        ```sql
     >        DECLARE
     >           emp_record employees%ROWTYPE;
     >        BEGIN
     >           -- 这里的 emp_record 变量的数据类型与 employees 表的一行记录相匹配
     >           SELECT * INTO emp_record FROM employees WHERE employee_id = 100;
     >           DBMS_OUTPUT.PUT_LINE('Employee Name: ' || emp_record.first_name || ' ' || emp_record.last_name);
     >        END;
     >        /
     >        ```

4.   能够定义过程、函数实现对 `emp `表密码重置、工资查询等，定义触发器实现对 `emp`表修改时，在特定条件下触发，例如修改工资低于原工资时进行信息输出提醒或者记录到其他表中。

     ```sql
     -- 创建过程
     CREATE OR REPLACE PROCEDURE ResetPassword(
         p_emp_id IN emp.emp_id%TYPE,
         p_new_password IN VARCHAR2
     ) AS
     BEGIN
       UPDATE emp
       SET password = p_new_password
       WHERE emp_id = p_emp_id;
       
       COMMIT;
       DBMS_OUTPUT.PUT_LINE('Password reset successfully.');
     END;
     /
     
     
     -- 创建函数
     CREATE OR REPLACE FUNCTION GetSalary(
         p_emp_id IN emp.emp_id%TYPE
     ) RETURN NUMBER AS
       v_salary NUMBER;
     BEGIN
       SELECT salary INTO v_salary
       FROM emp
       WHERE emp_id = p_emp_id;
     
       RETURN v_salary;
     END;
     /
     
     
     -- 创建触发器
     CREATE OR REPLACE TRIGGER SalaryUpdateTrigger
     BEFORE UPDATE OF salary ON emp
     FOR EACH ROW
     DECLARE
       v_old_salary NUMBER;
     BEGIN
       -- 获取原工资
       v_old_salary := NVL(:OLD.salary, 0);
     
       -- 如果新工资低于原工资，输出信息
       IF :NEW.salary < v_old_salary THEN
         DBMS_OUTPUT.PUT_LINE('Warning: New salary is lower than the original salary.');
       END IF;
     END;
     /
     ```

     >   `COMMIT` 是在数据库中提交当前事务的操作。在 Oracle 数据库中，所有的 SQL 语句默认都在一个事务中执行，但是并不会立即将修改的数据写入数据库，而是将这些修改放在一个临时的存储区域（称为回滚段）。



### 其他

#### 需掌握的知识

1.   掌握 `dual `表的使用；

     >   1.   `dual`是一个虚拟表，用来构成`select`的语法规则，oracle保证`dual`里面永远只有一条记录。可以用它来做很多事情。
     >   2.   `DUAL` 是 Oracle 数据库中的一个系统表，通常用于执行一些与数据无关的计算，例如获取当前日期、执行数学计算等。它只有一列 `DUMMY`。
     >   3.   例如此前使用序列实现自增主键时创建一个触发器，其中就使用到`dual`。

2.   掌握 `rowid`、`rownum `伪列的定义与使用。

     >   1.   `rowid`: 用于唯一标识表中的行，它是行的物理地址标识。每个 `rowid` 都是唯一的。例如：
     >
     >        ```sql
     >        SELECT empno, ename, rowid
     >        FROM emp
     >        WHERE empno = 7369;
     >        ```
     >
     >   2.   `rownum`: 用于给查询结果集的行添加行号。请注意，`rownum` 是在查询结果集返回给用户之前进行计算的。例如：
     >
     >        ```sql
     >        SELECT empno, ename, sal, ROWNUM
     >        FROM emp
     >        WHERE ROWNUM <= 5;
     >        ```

3.   知悉 `ADO.NET`、`JDBC`、`ODBC `数据访问接口含义。

     >   1.   `ADO.NET`: 是 Microsoft 的一组用于访问和操作数据的技术，主要用于` .NET `平台。
     >
     >   2.   `JDBC` (Java Database Connectivity): 是 Java 语言访问关系数据库的应用程序接口。
     >
     >   3.   `ODBC` (Open Database Connectivity): 是一个标准的数据库访问接口，允许应用程序使用 SQL 查询方式来访问数据库。

4.   了解 `imp`、`exp `与 `impdp`、`expdp `的区别。

     >   1.  `imp` (Import) 和 `exp` (Export) 是 Oracle 数据库的传统工具，用于导入和导出数据库对象和数据。<span style="color:red">服务端、客户端均可用</span>
     >   2.  `impdp` (Data Pump Import) 和 `expdp` (Data Pump Export) 是 Oracle 数据库的数据泵工具，提供更高级、更灵活的导入导出功能，支持并行处理等特性。<span style="color:red">仅服务端可用</span>

5.   了解闪回的基本原理。

#### 需具备的能力

1.   能够运用高级语言通过数据接口完成项目开发。（项目实践中考核）

2.   能够运用导入导出工具实现数据库的导入导出。