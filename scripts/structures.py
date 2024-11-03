def parse_coffee_info_dict(c_struct: dict) -> list:
    entries = []
    for key, val in c_struct.items():
        entry={}
        entry['Varietal'] = key
        entry['Species'] = c_struct[key]['species'].title()
        m = zip(c_struct[key]['headers'], c_struct[key]['values'])
        ag = zip(c_struct[key]['agro_headers'], c_struct[key]['agro_values'])
        bg = zip(c_struct[key]['background_headers'], c_struct[key]['background_values'])

        for v in m:
            entry[v[0]] = v[1]
        for v in ag:
            entry[v[0]] = v[1]
        for v in bg:
            entry[v[0]] = v[1]

        entries.append(entry)

    return entries