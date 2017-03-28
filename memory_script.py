#! /usr/bin/env python

from memory_profiler import profile
import os
from sioux import pipeliner

input_string = "This is the last sentence to be tested for measuring the memory usage."

f = open("memory_tracking.txt", "w")

def test_init_helper():
    for i in range(10):
        doc = pipeliner.doc("Hello world, I am Guan.")

@profile(stream=f)
def test_init():
    reload(pipeliner)
    pipeliner.doc("Hello world, I am Guan")
    test_init_helper()

@profile(stream=f)
def test_get_views(input_string):
    doc = pipeliner.doc(input_string)
    pipeliner.get_pos(doc)
    pipeliner.get_lemma(doc)
    pipeliner.get_ner_conll(doc)
    pipeliner.get_ner_ontonotes(doc)
    pipeliner.get_stanford_parse(doc)
    pipeliner.get_shallow_parse(doc)
    pipeliner.get_dependency_parse(doc)
    pipeliner.get_srl_nom(doc)
    pipeliner.get_srl_verb(doc)
    #pipeliner.get_quantities(doc)


def test():
    print("Measure time for setting up environment:\n")
    test_init()
    test_get_views("Hello world.")
    test_get_views(input_string)
    test_get_views(input_string)

if __name__ == '__main__':
    os.system("cp sioux/config/web_pipeline.cfg sioux/config/pipeline.cfg")
    os.system("cp sioux/config/jnius_pipeline.cfg sioux/config/pipeline.cfg") 
    print("testing memory usage for local approach ...\n")
    test()
    os.system("cp sioux/config/web_pipeline.cfg sioux/config/pipeline.cfg")
    #output_file.close()


