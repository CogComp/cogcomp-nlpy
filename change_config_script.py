import configparser
import codecs
import os
from sioux import download

# Get absolute path to config file in root directory
config = configparser.ConfigParser()
file_path = os.path.expanduser("~{0}.sioux{0}".format(os.path.sep)) + "config.cfg"

# Remove the config file and restore it such that it is consistent with the DEFAULT version in download.py
os.remove(file_path)
download.recover_model_config()

with codecs.open(file_path, mode='r', encoding='utf-8') as f:
    config.read_string(f.read())

# Change specific setting in config file
# You should change PORT such that the tests are run in unlimited port
config['remote_pipeline_setting']['api'] = "http://austen.cs.illinois.edu:PORT"

with codecs.open(file_path, mode='w', encoding='utf-8') as f:
    config.write(f)
