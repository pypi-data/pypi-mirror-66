# greece-utils
A set of common but yet useful generic tools

### Examples:
##### Convert SQL database table to CSV file
Implement recursive mapping of all foreign key tables (join of all related tables)
```
>>> from utils.toolset import SqlCsv
>>> my_object = SqlCsv(engine, session)
>>> my_object.to_csv("my_table_name", "path/to/file.csv", map_foreign_key_tables=True)
```

##### Find files in directory
```
from utils.sys import find_file
```
* Look for file extension in current directory
```
>>> find_file(".py")
```

* Look for file name(s) in specific directory
```
>>> find_file("filename", "/path/to/valid/directory")
```

* Look for multiple file names/extension in current directory
```
>>> list(set([item for item in find_file(ext) for ext in ["filename", ".py"]]))
```

##### Log
* Print standard output error to log file
```
>>> from utils.sys import StreamToLogger
>>> import logging
>>> log = StreamToLogger(logging.getLogger('STDERR'), name=log_name, log_level=logging.ERROR)
>>> sys.stderr = log
```