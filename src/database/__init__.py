import json


def init():
    url = "doc/database/conf.json"
    with open(url, "r") as f:
        result = f.read()
    result = json.loads(result)
    return result


_conf = init()
mysql_config = _conf.get("mysql", {})
redis_config = _conf.get("mysql", {})
mongodb_config = _conf.get("mysql", {})
