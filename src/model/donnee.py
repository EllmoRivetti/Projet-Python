class Donnee:
    def __init__(self, url, file_name, keys, key_aliases, critical_keys='all', size='undefined', compressed=False):
        self.url = url
        self.file_name = file_name
        self.keys = keys
        self.key_aliases = key_aliases
        self.critical_keys = critical_keys
        if critical_keys == 'all':
            self.critical_keys = data_keys
        self.size = size
        self.compressed = compressed