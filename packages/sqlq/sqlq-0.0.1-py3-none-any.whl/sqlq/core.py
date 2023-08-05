import queue
import sqlite3
from omnitools import *
from threadwrapper import *
from filehandling import join_path, abs_cwd


__ALL__ = ["SqlQueue"]


class SqlQueue(object):
    def worker(self, db) -> None:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        db.execute("PRAGMA locking_mode=EXCLUSIVE;")
        timeout = 0
        while not self.terminate:
            if self.sqlq.qsize() > 0 and not self.do_commit:
                tid, sql, data = self.sqlq.get()
                self.exc_result[tid] = self.__exc(db, sql, data)
                self.sqlq.task_done()
                timeout = 0
            else:
                if (timeout > self.timeout_commit or self.do_commit) and len(self.exc_result) == 0:
                    conn.commit()
                    self.do_commit = False
                    timeout = 0
                else:
                    timeout += 1
            time.sleep(1/1000)
        db.execute("PRAGMA locking_mode=NORMAL;")
        conn.close()

    def __exc(self, db: sqlite3.Cursor, sql: str, data: tuple) -> list_or_tuple:
        mode = ""
        try:
            if sql.endswith(";"):
                sql = sql[:-1]
            mode = ""
            if len(data) != 0:
                if isinstance(data[0], tuple):
                    mode = "many"
                else:
                    mode = "data"
            elif len(sql.split(";")) > 1:
                mode = "script"
            else:
                mode = "sql"
            if mode == "many":
                db.executemany(sql, data)
            elif mode == "data":
                db.execute(sql, data)
            elif mode == "sql":
                db.execute(sql)
            elif mode == "script":
                db.executescript(sql)
            result = [dict(row) for row in db.fetchall()]
            return result
        except Exception as e:
            p(f"error: [{mode}] {sql}(", data, f") due to {e}")
            info = debug_info()
            p(info[0])
            return info

    def commit(self):
        self.do_commit = True
        while self.do_commit:
            time.sleep(1/1000)

    def stop(self):
        self.terminate = True

    def __init__(self, db: str, timeout_commit: int = 1000) -> None:
        if not os.path.isabs(db):
            db = join_path(abs_cwd(depth=2), db)
        self.do_commit = False
        self.terminate = False
        self.timeout_commit = timeout_commit
        self.exc_result = {}
        self.sqlq = queue.Queue()
        self.sqlq_worker = threading.Thread(target=self.worker, args=(db,))
        self.sqlq_worker.daemon = True
        self.sqlq_worker.start()
        self.functions = dict(sql=self.sql)

    def _sql(self, tid: int, sql: str, data: tuple = ()) -> list:
        self.sqlq.put([tid, sql, data])
        while tid not in self.exc_result:
            time.sleep(1/1000)
            continue
        try:
            return self.exc_result[tid]
        finally:
            self.exc_result.pop(tid)

    def sql(self, sql: str, data: tuple = (), result: Any = None, key: Any = None) -> list:
        if result is None:
            result = {}
        key = key or 0

        def job(sql: str, data: tuple) -> list:
            return self._sql(threading.get_ident(), sql, data)

        threadwrapper = ThreadWrapper(threading.Semaphore(1))
        threadwrapper.add(job=job, args=args(sql, data), result=result, key=key)
        threadwrapper.wait()
        return result[key]


