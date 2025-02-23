from dataclasses import dataclass
from dataclasses_json import dataclass_json
import os
import sys

CONFIG_FILE_NAME = "config.json"


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    

@dataclass_json
@dataclass
class Config:
    file_to_convert : str
    target_file : str
    
def get_config_path() -> str:
    print(__file__)
    return f"{BASE_DIR}/{CONFIG_FILE_NAME}"
    
