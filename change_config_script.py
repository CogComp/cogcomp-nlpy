import configparser
import codecs
import os
from sioux import download

config = configparser.ConfigParser()
file_path = os.path.expanduser("~{0}.sioux{0}".format(os.path.sep)) + "config.cfg"

os.remove(file_path)
download.recover_model_config()

with codecs.open(file_path, mode='r', encoding='utf-8') as f:
    config.read_string(f.read())
config['remote_pipeline_setting']['api'] = "http://austen.cs.illinois.edu:PORT"
with codecs.open(file_path, mode='w', encoding='utf-8') as f:
    config.write(f)
