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

def storcli_matcher(all_disk_attributes_list, wanted_attributes_list):
    """

    Args:
        all_disk_attributes_list: contains all disks' information
        wanted_attributes_list: the keys that wanted to extract from all_disk_attributes_list

    Returns:
        list of extracted values each element of this list contain extracted features that wanted

    """
    all_disks_data = []
    for che_attr in all_disk_attributes_list:
        found_attrs = {}
        for attr in wanted_attributes_list:
            found_attrs[attr] = che_attr[attr]
        all_disks_data.append(copy.deepcopy(found_attrs))
        found_attrs.clear()
    return all_disks_data


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


prc_storcli_out = {
"Controllers":[
{
	"Command Status" : {
		"CLI Version" : "007.0606.0000.0000 Mar 20, 2018",
		"Operating system" : "Linux 5.4.52-HPDS",
		"Controller" : 0,
		"Status" : "Success",
		"Description" : "Show Drive Information Succeeded."
	},
	"Response Data" : {
		"Drive /c0/e12/s0" : [
			{
				"EID:Slt" : "12:0",
				"DID" : 13,
				"State" : "Onln",
				"DG" : 0,
				"Size" : "237.968 GB",
				"Intf" : "SATA",
				"Med" : "SSD",
				"SED" : "N",
				"PI" : "N",
				"SeSz" : "512B",
				"Model" : "Samsung SSD 860 PRO 256GB",
				"Sp" : "U",
				"Type" : "-"
			}
		],
		"Drive /c0/e12/s0 - Detailed Information" :   {
			"Drive /c0/e12/s0 State" : {
				"Shield Counter" : 0,
				"Media Error Count" : 0,
				"Other Error Count" : 0,
				"Drive Temperature" : " 21C (69.80 F)",
				"Predictive Failure Count" : 0,
				"S.M.A.R.T alert flagged by drive" : "No"
			},
			"Drive /c0/e12/s0 Device attributes" : {
				"SN" : "S42VNF0K516979R",
				"Manufacturer Id" : "ATA     ",
				"Model Number" : "Samsung SSD 860 PRO 256GB",
				"NAND Vendor" : "NA",
				"WWN" : "5002538e403e1157",
				"Firmware Revision" : "RVM01B6Q",
				"Raw size" : "238.474 GB [0x1dcf32b0 Sectors]",
				"Coerced size" : "237.968 GB [0x1dbf0000 Sectors]",
				"Non Coerced size" : "237.974 GB [0x1dbf32b0 Sectors]",
				"Device Speed" : "6.0Gb/s",
				"Link Speed" : "12.0Gb/s",
				"NCQ setting" : "Enabled",
				"Write Cache" : "N/A",
				"Logical Sector Size" : "512B",
				"Physical Sector Size" : "512B",
				"Connector Name" : "Port 0 - 3 "
			},
			"Drive /c0/e12/s0 Policies/Settings" : {
				"Drive position" : "DriveGroup:0, Span:0, Row:0",
				"Enclosure position" : "1",
				"Connected Port Number" : "0(path0) ",
				"Sequence Number" : 2,
				"Commissioned Spare" : "No",
				"Emergency Spare" : "No",
				"Last Predictive Failure Event Sequence Number" : 0,
				"Successful diagnostics completion on" : "N/A",
				"SED Capable" : "No",
				"SED Enabled" : "No",
				"Secured" : "No",
				"Cryptographic Erase Capable" : "No",
				"Locked" : "No",
				"Needs EKM Attention" : "No",
				"PI Eligible" : "No",
				"Certified" : "No",
				"Wide Port Capable" : "No",
				"Port Information" : [
					{
						"Port" : 0,
						"Status" : "Active",
						"Linkspeed" : "12.0Gb/s",
						"SAS address" : "0x5003048020ca19c0"
					}
				]
			},
			"Inquiry Data" : "40 00 ff 3f 37 c8 10 00 00 00 00 00 3f 00 00 00 00 00 00 00 34 53 56 32 46 4e 4b 30 31 35 39 36 39 37 20 52 20 20 20 20 00 00 00 00 00 00 56 52 30 4d 42 31 51 36 61 53 73 6d 6e 75 20 67 53 53 20 44 36 38 20 30 52 50 20 4f 35 32 47 36 20 42 20 20 20 20 20 20 20 20 20 20 20 20 20 20 01 80 01 40 00 2f 00 40 00 02 00 02 07 00 ff 3f 10 00 3f 00 10 fc fb 00 01 01 ff ff ff 0f 00 00 07 00 "
		}
        
        
 parse_ret = helper.storcli_matcher(prc_storcli_out,
                                           ["Enclosure Device ID", "Slot Number", "Enclosure position", "DID",
                                            "Intf", "Raw size", "Firmware Revision", "SN", "DG",
                                            "Link Speed", "Med", "WWN"]
                                           )
 
