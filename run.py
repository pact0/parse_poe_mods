import pandas as pd
import json
import re
from tqdm import tqdm
  

def main():
    f = open('./_PoeStatBasedItemListingRecord__202303092021.json')
    data = json.load(f)
    data = data["select * from \"PoeStatBasedItemListingRecord\" where \"league\" = 'Sanctum'"]
    
    f2 = open('res_full.json')
    mods = json.load(f2)
    
    f = open('./poec_lang.us.json')
    translations = json.load(f)
    
    bases = []
    for a, b in translations["base"].items():
        bases.append(b)
    
    len(bases)
    
    mods = []
    for a, b in translations["mod"].items():
        mods.append(b)
    len(mods)
    
    
    additional_records = ["price"]
    cools = mods
    cools.extend(bases)
    cools.extend(additional_records)
    
    
    base_item = {col: 0 for col in cools}
    
    # print the dictionary
    print(len(base_item))
    
    
    df = pd.DataFrame()
    fdsf = pd.DataFrame([base_item])
    df = pd.concat([df, fdsf], ignore_index=True)
    
    
    reg = r'/(\d+\.?(?:\d+)?)/g'
    reg = r'\d+\.?\d?'
    
    
    def parse_explicit_mods(mods):
        res = {}
        for mod in mods:
            matched_numbers = re.search(reg, mod)
    
            name = re.sub(reg, "#", mod)
            values = []
    
            for match in re.finditer(reg, mod):
                a = match.group()
                if '.' in a:
                    a = float(a)
                else:
                    a = int(a)
                values.append(a)
    
            res[name] = {"values": values}
        return res
    counter = 0
    for item in tqdm(data):
        temp_item = base_item.copy()
        temp_item["price"] = item["noteValue"]
    
        try:
            if item["baseType"].find("Cluster Jewel") != -1 or item["baseType"].find("Watcher") != -1 or item["baseType"].find("Thief's Trinket") != -1:
                continue
            explicitMods = item["explicitMods"]
            implicitMods = item["implicitMods"]
            craftedMods = item["craftedMods"]
    
            b = explicitMods.strip('{}').split(',')
            a = [s.strip('"') for s in b]
            parsed_mods = parse_explicit_mods(a)
            # print("paars",parsed_mods)
    
            all_mods_for_this_base = mods[item["baseType"]]["mods"]
            base = mods[item["baseType"]]["base"]
            temp_item[base] = 1
            # print(all_mods_for_this_base)
    
            for mod, vals in parsed_mods.items():
                v = vals["values"]
                mod_values = all_mods_for_this_base[mod]
                min_mod = mod_values["min"]
                max_mod = mod_values["max"]
    
                if len(v) > 0:
                    normalized = v[len(v)-1] / max_mod
                else:
                    normalized = 1
                
                temp_item[mod] = normalized
    
                #print(mod, min_mod, max_mod, normalized)
        except:
            counter = counter + 1
        
        dfdf = pd.DataFrame([temp_item])
        df = pd.concat([df, dfdf], ignore_index=True)
            #print("crash", item, mod, v, mod_values,counter)
    print(counter)

main()
