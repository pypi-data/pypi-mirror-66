from typing import Dict, Any
import collections

def deep_dict_merge(
    d1: Dict[Any,Any],
    d2: Dict[Any,Any], 
    add_keys = True
) -> Dict[Any, Any]:
    d1 = d1.copy()

    if not add_keys:
        dict_shared_keys = [k for k in set(d1).intersection(set(d2))]
        d2 = {
            x : d2[x] for x in dict_shared_keys
        }
    
    for k, v in d2.items():
        if (k in d1 and 
            isinstance(d1[k], dict) and
            isinstance(d2[k], collections.Mapping)):
            d1[k] = deep_dict_merge(d1[k], d2[k], add_keys=add_keys)
        else:
            d1[k] = d2[k]

    return d1
