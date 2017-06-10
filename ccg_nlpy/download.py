import codecs
import configparser
import logging
import os
import platform
import subprocess
import six

logger = logging.getLogger(__name__)

MODEL_FOLDER = "model_{}"
CONFIG_FILENAME = "config.cfg"
DEFAULT_CONFIG_ROOT_DIRECTORY = "~{0}.ccg_nlpy{0}".format(os.path.sep)
DEFAULT_CONFIG_VERSION = "3.1.15"
MAVEN_COMMAND = "mvn dependency:copy-dependencies -DoutputDirectory={} -Dsilent=True"
POM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.cogcomp</groupId>
    <artifactId>ccg_nlpy-pipeline-dependencies</artifactId>
    <version>1.0-SNAPSHOT</version>

    <repositories>
        <repository>
            <id>CogcompSoftware</id>
            <name>CogcompSoftware</name>
            <url>http://cogcomp.cs.illinois.edu/m2repo/</url>
        </repository>
    </repositories>

    <dependencies>
        <dependency>
            <groupId>edu.illinois.cs.cogcomp</groupId>
            <artifactId>illinois-nlp-pipeline</artifactId>
            <version>##VERSION##</version>
        </dependency>
    </dependencies>

</project>
"""


def _shell_argument():
    """Identify if the current platform is a Windows installation."""
    return 'windows' in platform.system().lower()


def _parse_default_config(root_directory, args=None):
    """Parse default configuration for model_download"""

    default_config_file = os.path.join(root_directory, CONFIG_FILENAME)
    package_config_file = os.path.dirname(os.path.realpath(__file__)) + '/config/pipeline.cfg'

    config = configparser.ConfigParser()
    if os.path.exists(default_config_file):
        with codecs.open(default_config_file, mode='r', encoding='utf-8') as f:
            config.read_string(f.read())
    else:
        with codecs.open(package_config_file,mode='r',encoding='utf-8') as f:
            config.read_string(f.read())

    if 'model_download' not in config:
        config['model_download'] = {}

    if args is not None and args.version is not None:
        version = args.version
    elif 'version' not in config['model_download']:
        version = DEFAULT_CONFIG_VERSION
    else:
        version = config['model_download']['version']

    config['model_download']['version'] = version

    return (config, default_config_file)


def _check_maven_installed():
    """Method to check if maven is installed and on the classpath"""

    try:
        output = subprocess.check_output(
            ["mvn", "--version"], shell=_shell_argument())
        logger.debug(output)
    except Exception:
        logger.error(
            'Maven installation not found!\n\
            Please install Apache Maven and add it to the classpath.',
            exc_info=True)
        raise


def _create_or_update_pom_file(file_path, version):
    """
    Create the pom.xml file needed for maven to download dependencies.
    """

    logger.info("Creating pom file")

    if six.PY2:
        # Python 2 - Write as a binary file and replace newline on windows
        # to universal newline.
        with open(file_path, 'wb') as file:
            pom_data = POM_TEMPLATE.replace("##VERSION##", version)
            pom_data = pom_data.replace('\r\n', '\n')
            file.write(pom_data)
    else:
        # Python 3 - use newline as \n always. Maven does not work otherwise.
        with open(file_path, "w", newline='\n') as file:
            pom_data = POM_TEMPLATE.replace("##VERSION##", version)
            file.write(pom_data)


def _download_jars(model_directory, config_directory, version):
    """
    Download Jars into the model_directory parameter

    Note: This method invokes maven internally to download dependencies.
    """

    if not os.path.exists(model_directory):
        os.makedirs(model_directory)

    logger.info('Root Directory = {}'.format(config_directory))
    logger.info('Model Directory = {}'.format(model_directory))

    try:
        command = MAVEN_COMMAND.format(model_directory)
        logger.debug(command)

        command_parts = command.split()
        proc = subprocess.Popen(
            command_parts,
            cwd=config_directory,
            stdout=subprocess.PIPE,
            shell=_shell_argument())

        # Calling proc.communicate() waits for the subprocess to complete.
        output, _ = proc.communicate()
        logger.info(output)
    except Exception:
        logger.error('Error while downloading jar files.', exc_info=True)
        raise

def recover_model_config():
    """
    Function to recover the model config if user accidentally deleted it
    """
    try:
        root_directory = get_root_directory()
        default_config, config_file_path = _parse_default_config(root_directory)
    
        with codecs.open(config_file_path, mode='w', encoding='utf-8') as file:
            default_config.write(file)
    except:
        logger.error("Error while recovering model config.", exc_info=True)


def get_root_directory():
    """Get the root config/model directory"""

    root_directory = os.path.expanduser(DEFAULT_CONFIG_ROOT_DIRECTORY)

    if not os.path.exists(root_directory):
        os.makedirs(root_directory)

    return root_directory


def get_model_path():
    """Returns the path of the JAR models."""

    root_directory = get_root_directory()
    default_config, _ = _parse_default_config(root_directory)
    version = default_config['model_download']['version']

    return os.path.join(root_directory, MODEL_FOLDER.format(version))


def main(args):
    """Default handler function"""

    logger.info("Starting download")
    try:
        _check_maven_installed()

        # Get default config along with args override.
        root_directory = get_root_directory()
        (config, config_file_path) = _parse_default_config(
            root_directory, args)
        version = config['model_download']['version']

        # Create/Update POM file.
        pom_file_path = os.path.join(root_directory, "pom.xml")
        logger.info(pom_file_path)
        _create_or_update_pom_file(pom_file_path, version)

        # Download model jars according to the version specified.
        jar_directory = os.path.join(root_directory,
                                     MODEL_FOLDER.format(version))
        _download_jars(jar_directory, root_directory, version)

        # Write the updated config file if download was successful.
        with codecs.open(config_file_path, mode='w', encoding='utf-8') as file:
            config.write(file)

        logger.info("Model download successful.")
    except Exception:
        logger.exception("Download failed.", exc_info=True)
