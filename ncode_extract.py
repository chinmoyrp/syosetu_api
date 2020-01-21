import json
from os import walk

(_, _, json_files) = next(walk('json'))

ncode_dict = {}
for jf in json_files:
    with open('json/{}'.format(jf), 'r', encoding='utf-8') as f:
        try:
            novel_data = json.load(f)
            ncode_list = []
            for nd in novel_data[1:]:
                ncode_list.append(nd['ncode'].lower())
            year = jf.split('.')[0].split('_')[0]
            try:
                ncode_list.extend(ncode_dict[year])
            except KeyError:
                pass
            ncode_dict[year] = ncode_list
        except json.decoder.JSONDecodeError:
            print("Skipping", jf)
            pass
            

with open('ncodes.json', 'w', encoding='utf-8') as nf:
    json.dump(ncode_dict, nf, ensure_ascii=False, indent=1) 
