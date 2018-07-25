# CogComp-NLPy
[![Build Status](https://semaphoreci.com/api/v1/projects/dc68ab4d-d1b7-4405-adca-b0c6af2e1aa0/1223617/badge.svg)](https://semaphoreci.com/danyaljj/sioux-2)

Run NLP tools such as Part-of-Speech tagging, Chunking, Named Entity Recognition, etc on your documents in Python with ease and breeze!

## Installation


1. Make sure [you have "pip" on your system](https://pip.pypa.io/en/stable/installing/). 
2. Make sure you have installed Cython:

```bash
pip install cython
```

3. Install:

```bash
pip install ccg_nlpy
```    

4. Enjoy!

Here is the project page at [PyPI website](https://pypi.python.org/pypi/ccg-nlpy).

## Support

The package is compatible with Python 2.6+ and Python 3.3+. We highly recommend using Python 3.3+

This package uses ```utf-8``` encoding.
In Python 2.6+, all strings are stored as ```unicode``` objects.
In Python 3.3+, all strings are stored as ```str``` objects.


## Getting Started 
Here is a sample usage showing how easily you run our system:

```python
from ccg_nlpy import remote_pipeline

pipeline = remote_pipeline.RemotePipeline()
doc = pipeline.doc("Hello, how are you. I am doing fine")
print(doc.get_lemma) # will produce (hello Hello) (, ,) (how how) (be are) (you you) (. .) (i I) (be am) (do doing) (fine fine)
print(doc.get_pos) # will produce (UH Hello) (, ,) (WRB how) (VBP are) (PRP you) (. .) (PRP I) (VBP am) (VBG doing) (JJ fine)
```

The default/easy usage has some restrictions as will deliniate in the next section. See the next section to 

**Api Docs:** Here is the [API docs](http://cogcomp.cs.illinois.edu/software/doc/ccg_nlpy/pipeliner.m.html) of our `Pipeliner` module.

## Structure
This tool enables you accesss [CogComp pipeline](https://github.com/CogComp/cogcomp-nlp/tree/master/pipeline) in different forms. The figure below summarizes these approaches:

![](https://user-images.githubusercontent.com/2441454/27004781-963ae9e0-4ddd-11e7-9864-b96a52df062b.png)


The figure above gives a summary of possible usages, as well as their pros and cons. Next we will go through each item and elaborate: 

### Remote Pipeline 
In this setting, you can send annotation requests to a remote machine. Hence there is not much memory burden on your local machine. Instead all the heavy-lifting is on the remote server.

**Default remote server:**  This is the default setting. The requests are sent to our remote server, hence requires a network connection. This option is here to demonstrate how things work, but it is not a viable solution for your big experiments since we limit the number of queries to our server (current limit is *100 queries a day*). If you are a busy nlp user, you should use any of the other options.

**Starting your own (remote) server:** If you have a big (remote) machine, this is probably a good option for you. 
You'll have to read the instructions on how to install the pipeline server in the [pipeline project documentation](https://github.com/CogComp/cogcomp-nlp/tree/master/pipeline#using-pipeline-webserver). In summary: 

1. Clone our  [CogComp-NLP](https://github.com/CogComp/cogcomp-nlp/) java project.
2. Run `pipeline/scripts/runWebserver.sh` to start the server. 
3. When you see `Server:xxx - Started @xxxxxms`, the server is up and running: 
  
After making sure that the server is running, we can make python call to it: 

```python
from ccg_nlpy import remote_pipeline
pipeline = remote_pipeline.RemotePipeline(server_api='http://www.fancyUrlName.com:8080') 
# constructor declaration: RemotePipeline(server_api = None, file_name = None)
# "server_api" is the address of the server as string. An example: http://www.fancyUrlName.com:8080
# "file_name" is the config file used to set up pipeline (optional), please refer the latter section for more details
```

**Note:** This tool is based on CogComp's [pipeline project](https://github.com/CogComp/cogcomp-nlp/tree/master/pipeline>). Essentially annotator included in the pipeline should be accessible here. 
 
### Local Pipeline 

In this setting, the system will download the trained models and files required to run the pipeline locally. Since everything is run on your machine, it will probably require a lot of memory (the amount depends on which annotations you use). If you have a single big machine (i.e. memory > 15GB) for your expeirments, this is probably a good option for you.
Local pipeline also gives you the functionality to work with pre-tokenized text.

To download the models, run the following command:
```bash
python -m ccg_nlpy download
```

This will download model files into your home directly under `~/.ccg_nlpy/`.

**Note:** Note that downloading the models require you to have Maven installed on your machine. If you don't, [here are some guidelines on how to install it](https://maven.apache.org/install.html). 

In the local pipeline annotators are loaded lazily; i.e. they are not loaded until you call them for the first time. 

```python 
from ccg_nlpy import local_pipeline
pipeline = local_pipeline.LocalPipeline() 
# constructor declaration: LocalPipeline()
```

To run on pre-tokenized text, the document is represented as a list of (sentences) list of tokens. The argument ```pretokenized=True``` needs to be passed to the ```pipeline.doc``` function.
```
from ccg_nlpy import local_pipeline
pipeline = local_pipeline.LocalPipeline()

document = [ ["Hi", "!"], ["How", "are", "you", "?"] ]
doc = pipeline.doc(document, pretokenized=True)
```

#### Frequent Issues: 
 - To use the pipelne locally you have to make sure you have set `JAVA_HOME` variable. In MacOS, you can verify it with `echo "$JAVA_HOME"`. If it is not set, you can `export JAVA_HOME=$(/usr/libexec/java_home)`. 
 - If you are using Java version > 8, you are likely to receive an error that looks like the following:  ```
 ERROR:ccg_nlpy.local_pipeline:Error calling dlopen(b'/Library/Java/JavaVirtualMachines/jdk-10.0.1.jdk/Contents/Home/jre/lib/server/libjvm.dylib': b'dlopen(/Library/Java/JavaVirtualMachines/jdk-10.0.1.jdk/Contents/Home/jre/lib/server/libjvm.dylib, 10): image not found' ```
To solve this, you have to [install Java-8 on your machine](https://gist.github.com/JeOam/a926dbb5145c4d0789c1) and direct your commandline to it: ```export JAVA_HOME=`/user/libexec/java_home -v 1.8` ```. 
 

### Setting from Configuration file 

You can set settings on how to run CogComp-NLPy via a local option too, rather than setting it programmatically.
Here is how to: 

```python 
from ccg_nlpy import remote_pipeline
pipeline = remote_pipeline.RemotePipeline(file_name = 'path_to_custom_config_file')
```
   
The default keys and values are specified below. If you want to use custom config file, please provide a file in similar format.


```bash
[remote_pipeline_setting]
api = ADDRESS_OF_THE_SERVER # example: http://fancyUrlName.com:8080
```    

### System failures

System failures are part of any software system. Upon some certain outputs (e.g. receiving error 500 from remote pipeline),
we return `None` in the output of call. When processing big documents it might make sense to check take care of
this explicitly:

```python
d = ... # docuemnt
p = ... # pipeline
doc = p.doc(d)
if doc is not None:
    # do sth with it
    ner_view = doc.get_ner_conll
```

## Questions/Suggestions/Comments 

Use comments or pull requests. 

