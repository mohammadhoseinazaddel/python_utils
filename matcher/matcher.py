import types
def matcher(input_text, patterns=None, splitter=None, end_string=""):
    """ This function finds pattern strings in input_text and returns a dict of wanted parts.

    Args:
        input_text (str): String to be parsed.
        patterns (list of dicts): A list of dicts that shows rules of splitting. dicts have 3 keys.
        "string" that show the word to be looked for.
        "wanted_delta" that show which parts of split list are wanted.
        "splitter" that show the string that line should be split with.
        splitter (str or None): String that lines of input_text are going to be split with.
        end_string (str): String that defines end of a section.

    Returns:
        List of dict or int: List of dicts if successful, ErrorCodes.ERROR_HELPER_MATCHER otherwise.
    """
    if patterns is None:
        patterns = []
    result = []
    per_res = dict()
    for line in input_text.splitlines():
        for pattern in patterns:
            if line.strip().startswith(str(pattern["string"]).strip()):
                if "splitter" in pattern:
                    splitter_string = pattern["splitter"]
                else:
                    splitter_string = splitter
                if splitter_string is None:
                    bits = line.split()
                else:
                    bits = line.split(splitter_string)
                if isinstance(pattern["wanted_delta"], types.ListType):
                    per_res[pattern["string"]] = []
                    for index in pattern["wanted_delta"]:
                        per_res[pattern["string"]].append(bits[index].strip())
                elif pattern["wanted_delta"] == 'all':
                    per_res[pattern["string"]] = line.split(pattern["string"])[-1].strip()
                else:
                    per_res[pattern["string"]] = bits[pattern["wanted_delta"]].strip()
                break

        if end_string in line:
            result.append(per_res)
            per_res = {}
    return result


def convert_tuple_to_pattern_dict(pattern):
    """Converts a list of tuple to a list of dicts. output dicts has a format like
       {"string":tuple[0], "wanted_delta":tuple[1], "splitter":tuple[2]}

    Args:
        pattern (list of tuples): List to be converted.

    Returns:
        List or int: List of dicts if successful, ErrorCodes.ERROR_HELPER_CONVERT_TUPLE otherwise.
    """
    patterns = []
    pattern_dict = {}
    for tuple_info in pattern:
        pattern_dict["string"] = tuple_info[0]
        pattern_dict["wanted_delta"] = tuple_info[1]
        if len(tuple_info) == 3:
            pattern_dict["splitter"] = tuple_info[2]
        patterns.append(pattern_dict)
        pattern_dict = {}
    return patterns


prc_cout = "Adapter #0" \
           "Enclosure Device ID: 12" \
           "Slot Number: 0" \
           "Drive's position: DiskGroup: 0, Span: 0, Arm: 0" \
           "Enclosure position: 1" \
           "Device Id: 13" \
           "WWN: 5002538e403e1157" \
           "Last Predictive Failure Event Seq Number: 0" \
           "PD Type: SATA" \
           "Raw Size: 238.474 GB [0x1dcf32b0 Sectors]" \
           "Non Coerced Size: 237.974 GB [0x1dbf32b0 Sectors]" \
           "Firmware state: Online, Spun Up" \
           "SAS Address(0): 0x5003048020ca19c0" \
           "Connected Port Number: 0(path0) " \
           "Inquiry Data: S42VNF0K516979R     Samsung SSD 860 PRO 256GB               RVM01B6Q" \
           "Device Speed: 6.0Gb/s " \
           "Link Speed: 12.0Gb/s " \
           "Media Type: Solid State Device" \
           "Drive:  Not Certified" \
           "Drive Temperature :21C (69.80 F)" \
           "Drive has flagged a S.M.A.R.T alert : No"

parse_ret = matcher(prc_cout,
                    convert_tuple_to_pattern_dict(
                        [
                            ("Enclosure Device ID", -1),
                            ("Slot Number", -1),
                            ("Enclosure position", -1),
                            ("Device Id", -1),
                            ("PD Type", -1),
                            ("Raw Size", -1),
                            ("Firmware state", -1),
                            ("Inquiry Data", -1),
                            ("Foreign State", -1),
                            ("Link Speed", -1),
                            ("Media Type", -1),
                            ("WWN", -1)
                        ]
                    ), ":",
                    "Drive has flagged a S.M.A.R.T alert")
