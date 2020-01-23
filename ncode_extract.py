import json
from os import walk

#(_, _, json_files) = next(walk('json'))

#ncode_dict = {}
#for jf in json_files:
    #with open('json/{}'.format(jf), 'r', encoding='utf-8') as f:
        #try:
            #novel_data = json.load(f)
            #ncode_list = []
            #for nd in novel_data[1:]:
                #ncode_list.append(nd['ncode'].lower())
            #year = jf.split('.')[0].split('_')[0]
            #try:
                #ncode_list.extend(ncode_dict[year])
            #except KeyError:
                #pass
            #ncode_dict[year] = ncode_list
        #except json.decoder.JSONDecodeError:
            #print("Skipping", jf)
            #pass
            

#with open('ncodes.json', 'w', encoding='utf-8') as nf:
    #json.dump(ncode_dict, nf, ensure_ascii=False, indent=1) 
with open('crawler/ncodes.json', 'r', encoding='utf-8') as f:
        novel_data = json.load(f)
        ncode_list = []
        data_2018 = set(novel_data["2018"])
        with open('ncodes.2018') as sf:
            for line in sf:
                ncode_list.append(line.strip())
        
        ncode_list = set(ncode_list)
        remaining = data_2018 - ncode_list
        print(len(remaining))
        remaining = list(remaining)
        #for date in range(2004, 2016):
            #ncode_list.extend(novel_data[str(date)])
            #print("key:", date, "coutnt", len(novel_data[str(date)]))
sublist = [remaining[x:x+10000] for x in range(0, len(remaining), 10000)]
for s in sublist:
    print(len(s))
with open('ncodes-2018.json', 'w', encoding='utf-8') as nf:
    dict_ = {}
    for i in range(1, 10):
        dict_["2018.%d"%i] = sublist[i-1]
        print(len(dict_["2018.%d"%i]), i)
    json.dump(dict_, nf, ensure_ascii=False, indent=1)
