from sioux import remote_pipeline

p = remote_pipeline.RemotePipeline()

doc = p.doc('George Washington fought in the war.')

# get POS view and NER view
pos_view = p.get_pos(doc)
ner_view = p.get_ner_conll(doc)

# find NER constituents that are labeled PER (label from NER view)
per_list = []
for ner in ner_view:
    if ner['label'] == 'PER':
        per_list.append(ner)


matching_list = []

# For each of the constituents that is labeled PER,
# check if it is followed by constituent that is labeled VBD (label from POS view)

for per in per_list:
    for pos in pos_view:
        if pos['label'] == "VBD" and pos['start'] == per['end']:
            matching_list.append((per['tokens'], pos['tokens']))
            break

print(matching_list)
