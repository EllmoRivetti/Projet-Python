class Donnee:
    def __init__(self, url, file_name, keys, key_aliases, critical_keys='all', size='undefined', archive_name='none', archive_path=[]):
        self.url = url
        self.file_name = file_name
        self.keys = keys
        self.key_aliases = key_aliases
        self.critical_keys = critical_keys
        if critical_keys == 'all':
            self.critical_keys = data_keys
        self.size = size
        self.compressed = not archive_name == 'none'
        self.archive_name = archive_name
        self.archive_path = archive_path

    def set_up(self):
        if os.path.isfile(self.file_name):
            print('File ' + str(self.file_name) + ' not found on disk.')
        if download and not os.path.isfile(self.file_name):
            Tools.download_file(self.url, self.file_name)

        f = Tools.open_file(self.file_name, self.compressed_file_name, self.path)
        try:
            print(file_name)
            self.read_json_data_from_file(f)
        except:
            print("You don't have the data file ", self.file_name, " or this file is corrupted. Do you agree to download this file (Approximative size: ", self.size, " ? (yes/no)")
            download = (str(input()).lower() == "yes")
            if not download:
                print("Exiting..")
                exit()
            else:
                Tools.download_file(self.url, self.file_name)
                f = Tools.open_file(self.file_name, self.compressed_file_name, self.path)
                self.read_json_data_from_file(f)

    def read_json_data_from_file(f):
    RAW_FILE_JSON = json.loads(''.join(f.readlines()))
    for raw_line in RAW_FILE_JSON:
        line = raw_line
        if 'fields' in raw_line:
            line = raw_line['fields']

        l = dict()
        all_critical_keys_in_entry = True
        for critical_key in self.critical_keys:
            if not critical_key in line.keys():
                all_critical_keys_in_entry = False

        if all_critical_keys_in_entry:
            for key, value in line.items():
                if key in self.keys:
                    index_key = self.keys.index(key)
                    alias = self.key_aliases[index_key]
                    try:
                        l[alias] = int(value)
                    except ValueError:
                        l[alias] = value
                    except TypeError:
                        l[alias] = value 
            DATA[CURRENT_DATA_NAME].append(l)