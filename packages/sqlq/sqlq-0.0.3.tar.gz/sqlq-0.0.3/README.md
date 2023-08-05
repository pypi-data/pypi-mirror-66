# Sqlite3 Execution Queue

<badges>[![version](https://img.shields.io/pypi/v/sqlq.svg)](https://pypi.org/project/sqlq/)
[![license](https://img.shields.io/pypi/l/sqlq.svg)](https://pypi.org/project/sqlq/)
[![pyversions](https://img.shields.io/pypi/pyversions/sqlq.svg)](https://pypi.org/project/sqlq/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>A thread safe queue worker that executes SQL for multi-threaded applications.</i>

# Hierarchy

```
sqlqueue
'---- SqlQueue()
    |---- sql()
    |---- _sql()
    |---- commit()
    '---- stop()
```

# Example

## python
```python
from sqlq import *

# specify the db file, relative or absolute path
sqlqueue = SqlQueue(r"db.db")


# run benchmark
# this example shows how sqlq is used
# SQL should not be executed frequently
# see next example for sqlq usage
r = (1, 5, 10, 50, 100, 200)
r = (50,)
for l in r:
    tw = ThreadWrapper(threading.Semaphore(l))
    starttime = time.time()
    for i in range(l):
        def job(i):
            sqlqueue._sql(threading.get_ident(), "INSERT INTO test VALUES (?);", (str(i),))
        tw.add(job, args=args(i))
    tw.wait()
    p(l, (time.time()-starttime)/l, time.time()-starttime)
    # p(sql.sql("SELECT * FROM test;"))
    tw = ThreadWrapper(threading.Semaphore(l))
    starttime = time.time()
    for i in range(l):
        def job(i):
            sqlqueue._sql(threading.get_ident(), f"DELETE FROM test WHERE a = ?;", (str(i),))
        tw.add(job, args=args(i))
    tw.wait()
    p(l, (time.time()-starttime)/l, time.time()-starttime)


    starttime = time.time()
    for i in range(l):
        sqlqueue.sql("INSERT INTO test VALUES (?);", (str(i),))
    p(l, (time.time()-starttime)/l, time.time()-starttime)
    # p(sql.sql("SELECT * FROM test;"))
    starttime = time.time()
    for i in range(l):
        sqlqueue.sql(f"DELETE FROM test WHERE a = ?;", (str(i),))
    p(l, (time.time()-starttime)/l, time.time()-starttime)
    p()
    sqlqueue.commit()


# SQL execution modes
SqlQueue().sql("SELECT * FROM table;")
SqlQueue().sql("INSERT INTO table VALUES (?);", (0,))
SqlQueue().sql("INSERT INTO table VALUES (?);", ((0,),(0,)))
SqlQueue().sql('''
CREATE TABLE "tablea" ("a" TEXT);
DELETE TABLE "table";
''')
```
