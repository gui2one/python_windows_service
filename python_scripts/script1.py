import json
import sys
from  pathlib import Path

src_file_path = Path(sys.argv[1])
dst_file_path = Path(sys.argv[2]) 


data : str = ""
with open(src_file_path, "r") as f:
    data = f.read()
with open(dst_file_path, "w") as f:
    json_data = json.loads(data)
    json_data["hello"] = "world"
    f.write(json.dumps(json_data, indent=4))
