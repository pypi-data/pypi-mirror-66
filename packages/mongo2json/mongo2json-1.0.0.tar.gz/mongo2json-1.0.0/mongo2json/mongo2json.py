import orjson

from mongo2json import cleaner


def loads(dirty_json_string: str) -> list or dict:
    valid_json_string = cleaner.clean(string=dirty_json_string)
    return orjson.loads(valid_json_string)
