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
    package_config_file = os.path.dirname(os.path.realpath(__file__)) + '/config/pipeline.cfg'
    config_file = package_config_file
    models_downloaded = os.path.exists(download.get_model_path())

    config = configparser.ConfigParser()

    # if model folder does not exist, then user hasn't download jars yet, use config file in the package
    # the config file in the package will use pipeline server instead of local pipeline
    default_config_file = os.path.join(download.get_root_directory(), CONFIG_FILENAME)
    if models_downloaded:
        default_config_file = os.path.join(download.get_root_directory(), CONFIG_FILENAME)
        config_file = default_config_file
    else:
        logger.warn('Models not found, using pipeline web server. To use pipeline locally, please refer the documentation for downloading models.')

    with codecs.open(config_file,mode='r',encoding='utf-8') as f:
        config.read_string(f.read())
    return config, models_downloaded

def get_user_config(file_name):
    global user_config_file
    if file_name is not None and os.path.exists(file_name):
        models_downloaded = os.path.exists(download.get_model_path())
        config = configparser.ConfigParser()
        user_config_file = file_name
        with codecs.open(user_config_file,mode='r',encoding='utf-8') as f:
            config.read_string(f.read())

        # check this for edge case where using server is off in user config but models haven't downloaded (impossible to set up local pipeline)
        if config['pipeline_setting']['use_pipeline_server'] == 'false' and models_downloaded == False:
            config['pipeline_setting']['use_pipeline_server'] = 'true'

        return config, models_downloaded
    else:
        logger.warn('User config file not found, initializing pipeline with default config file.')
        return get_current_config()

def change_temporary_config(config, models_downloaded, enable_views, disable_views, use_server, server_api):
    # Common section that can be changed in both package config and default config
    # (only section that can be changed in package config)
    if server_api is not None:
        config['pipeline_server']['api'] = server_api

    # Sections that can be changed if config is not read from config file in package
    # (models_downloaded will be False if and only if config is not read from config file in package)
    if models_downloaded == True:
        if disable_views is not None:
            for view in disable_views:
                if view in config['views_setting']:
                    config['views_setting'][view] = 'false'
        if enable_views is not None:
            for view in enable_views:
                if view in config['views_setting']:
                    config['views_setting'][view] = 'true'
        if use_server is not None:
            if use_server == False:
                config['pipeline_setting']['use_pipeline_server'] = 'false'
            elif use_server == True:
                config['pipeline_setting']['use_pipeline_server'] = 'true'
    else:
        if use_server == False:
            logger.warn('Tried to use local pipeline while models have not been downloaded, turn on using pipeline web server')
    return log_current_config(config)

def set_current_config(config):
    if user_config_file is None:
        logger.error('Could not overwrite config file if user has not previous provide one.')
    else:
        with codecs.open(user_config_file, mode='w', encoding='utf-8') as file:
            config.write(file)
        logger.info('Config file has been updated.')
    

def log_current_config(config):
    if config['pipeline_setting']['use_pipeline_server'] == 'true':
        logger.info('Using pipeline web server with API: {0}'.format(config['pipeline_server']['api']))
        return None
    else:
        enabled_views = []
        for view_setting in config.items('views_setting'):
            if view_setting[1] == 'true':
                enabled_views.append(view_setting[0].upper())
        logger.info('Using local pipeline with following views enabled: {0}'.format(enabled_views))
        return enabled_views

def view_enabled(config, view_name):
    # because server will have all views enabled
    if config['pipeline_setting']['use_pipeline_server'] == 'false':
        # return false only when view not found or indeed disabled
        if view_name not in config['views_setting'] or config['views_setting'][view_name] == 'false':
            return False
    return True
