import os
import zlib
import time
import flask
import sqlite3

from pathlib import Path

DB = Path("./Data/Visits.db")


with sqlite3.connect(DB) as conn:
    Tables = list(conn.execute("""
                        SELECT
                            name
                        FROM
                            sqlite_master
                        WHERE
                            type ='table' AND
                            name NOT LIKE 'sqlite_%';
                        """))
    if ("VISITS",) not in Tables:
        conn.execute("""
            CREATE TABLE VISITS(
                    VISITID     INT     PRIMARY KEY NOT NULL,
                    TIME        INT                 NOT NULL,
                    USERID      INT                 NOT NULL
                );""")


def LogVisit(req: flask.Request):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "Insert into VISITS values(?,?,?)", (
                int.from_bytes(os.urandom(4), 'big'),
                int(time.time()),
                zlib.crc32(req.remote_addr.encode())
            )
        )
