import pymysql

from src.database import mysql_config


class Mysql():
    def __init__(self):
        self.cursor = self.connect()

    def connect(self):
        con = pymysql.connect(**mysql_config["test"])
        con.autocommit(1)
        return con.cursor()

    def close(self):
        self.cursor.close()

    def run(self, temp):
        if "command" not in temp or "table" not in temp:
            return False
        if temp["command"] == "insert":
            return self.insert(temp)
        elif temp["command"] == "update":
            return self.update(temp)
        elif temp["command"] == "select":
            return self.select(temp)
        elif temp["command"] == "delete":
            return self.delete(temp)
        else:
            return False

    def select(self, temp):
        sql = "SELECT "
        contents = temp.get("content", [])
        if contents:
            for content in contents:
                sql += "`" + content + "`" + ", "
            sql = sql.rstrip(", ")
        else:
            sql += "*"
        sql += " FROM `" + temp.get("table") + "` "

        if "key" in temp:
            sql += "WHERE "
            conditions = []
            for k, i in temp.get("key").items():
                conditions.append("`" + k + "` = %s")
            sql += " AND ".join(conditions)
        self.cursor.execute(sql, tuple(temp.get("key", {}).values()))
        return self.cursor.fetchall()

    def insert(self, temp):
        sql = "INSERT INTO `" + temp.get("table") + "` "
        columns = []
        values = []
        for k, v in temp.get("key").items():
            columns.append("`" + k + "`")
            values.append("%s")

        sql += "(" + ", ".join(columns) + ")"
        sql += " VALUES (" + ", ".join(values) + ")"

        data = tuple(temp.get("key").values())

        self.cursor.execute(sql, data)

    def update(self, temp):
        sql = "UPDATE `" + temp.get("table") + "` SET "
        updates = []
        for k, v in temp.get("values").items():
            updates.append("`" + k + "` = %s")
        sql += ", ".join(updates)

        if "key" in temp:
            sql += " WHERE "
            conditions = []
            for k, i in temp.get("key").items():
                conditions.append("`" + k + "` = %s")
            sql += " AND ".join(conditions)

        values = tuple(temp.get("values").values())
        key_values = tuple(temp.get("key").values())
        self.cursor.execute(sql, values + key_values)

    def delete(self, temp):
        sql = "DELETE FROM `" + temp.get("table") + "`"
        if "key" in temp:
            sql += " WHERE "
            conditions = []
            for k, i in temp.get("key").items():
                conditions.append("`" + k + "` = %s")
            sql += " AND ".join(conditions)

        key_values = tuple(temp.get("key").values())
        self.cursor.execute(sql, key_values)


if __name__ == '__main__':
    a = Mysql(
    )
    temp = {
        "table": "machines_overview",
        "command": "delete",
        "content": ["machine"],
        "key": {"machine": "test"},
        "values": {"app_ids": 703}
    }
    result = a.run(temp)
    print(result)
    a.close()
