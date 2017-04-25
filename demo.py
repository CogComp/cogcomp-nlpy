from sioux import remote_pipeline

p = remote_pipeline.RemotePipeline()

doc = p.doc('George Washington fought in the war.')

# get POS view and NER view
pos = p.get_pos(doc)
ner = p.get_ner_conll(doc)

# get the list of constituents from each view
pos_cons = pos.get_cons()
ner_cons = ner.get_cons()

# find NER constituents that are labeled PER (label from NER view)
per_index_list = []
for ner_index in range(len(ner_cons)):
    if ner_cons[ner_index]['label'] == 'PER':
        per_index_list.append(ner_index)


matching_list = []

# For each of the constituents that is labeled PER,
# check if it is followed by constituent that is labeled VBD (label from POS view)

pos_index = 0 # keep the index out of the loop such that each POS constituent will only be checked once
for per_index in per_index_list:
    per_end_token_index = ner_cons[per_index]['end']
    while pos_index < len(pos_cons):
        if pos_cons[pos_index]['label'] == "VBD" and pos_cons[pos_index]['start'] == per_end_token_index:

            # put the matching pairs into matching_list as tuple
            # get_cons(key='token') will return a list of constituents in terms of corresponding tokens
            matching_list.append((ner.get_cons(key='token')[per_index], pos.get_cons(key='token')[pos_index]))
            pos_index += 1
            break
        elif pos_cons[pos_index]['start'] > per_end_token_index:
            break
        else:
            pos_index += 1

print(matching_list)
