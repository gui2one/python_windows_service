import json
import sys
from  pathlib import Path
import logging
if len(sys.argv) != 3:
    print("Usage: python script1.py <src_file_path> <dst_file_path>")
    sys.exit(0)
src_file_path = Path(sys.argv[1])
dst_file_path = Path(sys.argv[2]) 

logger = logging.getLogger(__name__)

logging.basicConfig(filename='script1.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

src_json_data = json.loads(src_file_path.read_text())

logger.info(f"src_json_data: {src_json_data}")