'''
Following Ani's naming converntion.
Although technically, this is a wrapper for class BasicAnnotatorService, the return type of PipelineFactory
'''
from text_annotation import TextAnnotation

class CgPipeline:
    '''
        This class is the wrapper on Pipeline Factory using jnius.
        It has a constructor to set up the pipeline given configuration
        And a run_pipeline function to preprocess a given text with the pipeline

    '''

    # Optimally, user could pass in a set of string "views" rather than a path to config file
    # such that this class can either process the future text using web server
    # or create a (wrapper of)basic annotator service as the Java code does
    # if some conditions are satisfied (ex. user provides the path to the nlp jar)
    def __init__(self, jar_paths = None, config_file = None):
        # the Java object used in preprocessing
        self.pipeline = None

        # store the python version of class TextAnnotation
        self.text_annotation = None

        if jar_paths != None:
            # import jnius in constructor such that the JVM will be set up only when pipeline is created
            # initialize environment for starting JVM
            try:
                # This is an alternative way to avoid changing configuration while JVM is running
                #       also need to consider VM detachment
                import jnius_config
                jnius_config.add_options("-Xms4G",'-Xmx4G')
                for jar_path in jar_paths:
                    jnius_config.add_classpath(jar_path)
            except:
                print "warning; try to change JVM config when JVM is running"
            finally:
                from jnius import autoclass

            PipelineFactory = autoclass('edu.illinois.cs.cogcomp.nlp.pipeline.IllinoisPipelineFactory')

            if config_file != None:
                # Build pipeline based on provided config
                ResourceManager = autoclass('edu.illinois.cs.cogcomp.core.utilities.configuration.ResourceManager')
                userConfig = ResourceManager(config_file)
                self.pipeline = PipelineFactory.buildPipeline(userConfig)
            else:
                # Build based on default config
                self.pipeline = PipelineFactory.buildPipeline()
        else:
            # this else statement can be the entry of pipeline with web server
            self.pipeline = "this could be a connection between web server"

    def run_pipeline(self, text = "Hello World"):
        # clear up storage when pipeline is run
        self.text_annotation = None

        if self.pipeline != None:
            text_annotation_java = self.pipeline.createAnnotatedTextAnnotation("", "", text)
            from jnius import autoclass

            # Convert Text Annotation into JSON format
            SerializationHelper = autoclass('edu.illinois.cs.cogcomp.core.utilities.SerializationHelper')
            jsonTaStr = SerializationHelper.serializeToJson(text_annotation_java, True)
            self.text_annotation = TextAnnotation(text_annotation_java, jsonTaStr)
        else:
            # entry for web server
            self.text_annotation = None

        return self.text_annotation
