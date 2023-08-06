# mongo2json

Converts mongo shell JSON output to a valid JSON or a Python object

#### Installation:

`pip install mongo2json`

#### Usage: 
```
import mongo2json

data = mongo2json.loads(open('mongo_export.json').read())
```

### Warning! Current implementation is slow as hell!