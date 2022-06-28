def kind_key_finder(resp):
    """
    use to extract all keys and values from json even in list and dict values
    """
    all_of_all_key_val = {}
    dict_keys = []
    list_keys = []

    normal_keys = [dict_keys.append(key) if isinstance(resp[key], dict)
                   else list_keys.append(key) if isinstance(resp[key], list)
                   else key for key in resp.keys()]

    for key in normal_keys:
        if key != None:
            all_of_all_key_val[key] = resp[key]

    if len(dict_keys) != 0:
        for dict_key in dict_keys:
            all_of_all_key_val.update(kind_key_finder(resp[dict_key]))

    if len(list_keys) != 0:
        for list_key in list_keys:
            for dict_key_val in resp[list_key]:
                all_of_all_key_val.update(kind_key_finder(dict_key_val))
    return all_of_all_key_val
