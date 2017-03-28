#! /usr/bin/env python

import time
import os
from sioux import pipeliner

input_string = "We are using a long sentence to check if the running time will be changed significantly."

def test_init(output_file):
    start_time = time.time()
    reload(pipeliner)
    end_time = time.time()
    result = "Time for setting up pipeline and jvm with default configuration: {0}\n".format(end_time-start_time)
    output_file.write(result)

    start_time = time.time()
    doc = pipeliner.doc("Hello world, I'am Guan.")
    end_time = time.time()
    output_file.write("Time for creating new text annotation: {0}\n".format(end_time-start_time))

    start_time = time.time()
    for i in range(10):
        doc = pipeliner.doc("Hello world, I'am Guan.")
    end_time = time.time()
    output_file.write("Average time for re-creating same text annotation: {0}\n".format((end_time-start_time)/10.0)) 

def test_get_views(output_file,input_string, times):
    time_escaped = []
    for i in range(10):
        time_escaped.append(0)
    for i in range(times):
        doc = pipeliner.doc(input_string)
        start_time = time.time()
        pipeliner.get_pos(doc)
        time_escaped[0] += time.time() - start_time

        start_time = time.time()
        pipeliner.get_lemma(doc)
        time_escaped[1] += time.time() - start_time

        start_time = time.time()
        pipeliner.get_ner_conll(doc)
        time_escaped[2] += time.time() - start_time

        start_time = time.time()
        pipeliner.get_ner_ontonotes(doc)
        time_escaped[3] += time.time() - start_time

        start_time = time.time()
        pipeliner.get_stanford_parse(doc)
        time_escaped[4] += time.time() - start_time

        start_time = time.time()
        pipeliner.get_shallow_parse(doc)
        time_escaped[5] += time.time() - start_time

        start_time = time.time()
        pipeliner.get_dependency_parse(doc)
        time_escaped[6] += time.time() - start_time

        start_time = time.time()
        #pipeliner.get_quantities(doc)
        time_escaped[7] += time.time() - start_time

        start_time = time.time()
        pipeliner.get_srl_verb(doc)
        time_escaped[8] += time.time() - start_time

        start_time = time.time()
        pipeliner.get_srl_nom(doc)
        time_escaped[9] += time.time() - start_time

    for i in range(10):
        time_escaped[i] = time_escaped[i] * 1.0 / times

    output_file.write("Average time for getting views in following order: (1)pos, (2)lemma, (3)ner_conll, (4)ner_ontonotes, (5)stanford_parse, (6)shallow_parse, (7)dependency_parse, (8)quantities, (9)srl_verb, (10)srl_nom\n")
    output_file.write("Average time for 1:{0}, 2:{1}, 3:{2}, 4:{3}, 5:{4}, 6:{5}, 7:{6}, 8:{7}, 9:{8}, 10:{9}\n".format(time_escaped[0],time_escaped[1],time_escaped[2],time_escaped[3],time_escaped[4],time_escaped[5],time_escaped[6],time_escaped[7],time_escaped[8],time_escaped[9]))

def test(output_file,input_string):
    output_file.write("Measure time for setting up environment:\n")
    test_init(output_file)
    output_file.write("Measure time for initializing each view (passing unrelated text to get function of each view):\n")
    test_get_views(output_file, "Hello world.", 1)
    output_file.write("Using string: {0}\n".format(input_string))
    output_file.write("Measure time for getting different views for the first time:\n")
    test_get_views(output_file, input_string, 1)
    output_file.write("Measure time for getting different views for text has been processed (same text, different text annotation instance):\n")
    test_get_views(output_file, input_string, 10)

if __name__ == '__main__':
    output_file = open('time_tracking.txt', 'w')
    os.system("cp sioux/config/web_pipeline.cfg sioux/config/pipeline.cfg")
    output_file.write("testing web approach ...\n")
    test(output_file, input_string)
    os.system("cp sioux/config/jnius_pipeline.cfg sioux/config/pipeline.cfg") 
    output_file.write("\ntesting local approach ...\n")
    test(output_file, input_string)
    os.system("cp sioux/config/web_pipeline.cfg sioux/config/pipeline.cfg")
    output_file.close()
