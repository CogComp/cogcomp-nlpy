import configparser
import codecs
import logging
import os
import sys

from . import download

logger = logging.getLogger(__name__)

CONFIG_FILENAME = 'config.cfg'
user_config_file = None

def get_current_config():
    """
    Function to get configuration for setting up pipeline.
    If the models have been downloaded, the function will (restore and) load configuration from '~/.ccg_nlpy/config.cfg.'
    Otherwise, it will load from 'pipeline.cfg' in the package

    @return: config, a ConfigParser instance with loaded configuration
             models_downloaded, True if models have been downloaded, False otherwise.

    """
    package_config_file = os.path.dirname(os.path.realpath(__file__)) + '/config/pipeline.cfg'
    config_file = package_config_file
    models_downloaded = os.path.exists(download.get_model_path())

    config = configparser.ConfigParser()

    # if model folder does not exist, then user hasn't download jars yet, use config file in the package
    # the config file in the package will use pipeline server instead of local pipeline
    default_config_file = os.path.join(download.get_root_directory(), CONFIG_FILENAME)
    if models_downloaded:
        default_config_file = os.path.join(download.get_root_directory(), CONFIG_FILENAME)
        if os.path.exists(default_config_file) is False:
            download.recover_model_config()
        config_file = default_config_file
    else:
        logger.warn('Models not found. To use pipeline locally, please refer the documentation for downloading models.')

    with codecs.open(config_file,mode='r',encoding='utf-8') as f:
        config.read_string(f.read())
    return config, models_downloaded

def get_user_config(file_name):
    """
    Function to get configuration for setting up pipeline from file that user provides.
    If the file does not exist, it will call function 'get_current_config()' and return its result

    @param: file_name, the file name of custom config file
    @return: config, a ConfigParser instance with loaded configuration
             models_downloaded, True if models have been downloaded, False otherwise
    """
    global user_config_file
    if file_name is not None and os.path.exists(file_name):
        models_downloaded = os.path.exists(download.get_model_path())
        config = configparser.ConfigParser()
        user_config_file = file_name
        with codecs.open(user_config_file,mode='r',encoding='utf-8') as f:
            config.read_string(f.read())
        return config, models_downloaded
    else:
        logger.warn('User config file not found, initializing pipeline with default config file.')
        return get_current_config()

def change_temporary_config(config, models_downloaded, use_server, server_api):
    """
    Function to change configuration temporarily. In other words, it only changes values in the ConfigParser provided as parameter.

    @param: config, the ConfigParser instance to be made changes on
            models_downloaded, Boolean to indicate if models have been downloaded
            enable_views, List of strings to indicate views to be enabled
            disable_views, List of strings to indicate views to be disabled (enable_views has higher priority)
            use_server, Boolean to indicate if using remote server
            server_api, the address of the server, including port number
    @return: List of names of enabled view if use_server is False, None otherwise
    """
    if server_api is not None:
        config['remote_pipeline_setting']['api'] = server_api

    log_current_config(config, use_server)

def set_current_config(config):
    """
    Function to write the current configuration to file if the configuration was loaded from custom config file

    @param: config, the ConfigParser instance to be written to file
    """
    if user_config_file is None:
        logger.error('Could not overwrite config file if user has not previous provide one.')
    else:
        with codecs.open(user_config_file, mode='w', encoding='utf-8') as file:
            config.write(file)
        logger.info('Config file has been updated.')
    

def log_current_config(config, use_server):
    """
    Function to log current configuration

    @param: config, the ConfigParser instance to be logged
            use_server, Boolean to indicate if using remote server
    """
    if use_server:
        logger.info('Using pipeline web server with API: {0}'.format(config['remote_pipeline_setting']['api']))
    else:
        logger.info('Using local pipeline')
