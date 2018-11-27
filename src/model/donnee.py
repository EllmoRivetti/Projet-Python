import os
import os.path 
from src.tools import Tools 
import json
import sys
import src

#TODO make the data files path relative to a data folder. 

class Donnee:
    DATA_FOLDER = 'data'

    def __init__(self, url, file_name, keys, key_aliases, parent_class, critical_keys='all', size='undefined', archive_name='none', archive_path=[]):
        self.url            = url
        self.file_name      = file_name
        self.keys           = keys
        self.key_aliases    = key_aliases
        self.critical_keys  = critical_keys
        if critical_keys == 'all':
            self.critical_keys = self.keys
        self.size           = size
        self.compressed     = not archive_name == 'none'
        self.archive_name   = archive_name
        self.archive_path   = archive_path
        self.parent_class   = parent_class
        
        self.set_up()

    def set_up(self):
        print('Setting up', self.parent_class)
        if not os.path.isfile(os.path.join(Donnee.DATA_FOLDER, self.file_name)):
            print('File ' + str(self.file_name) + ' not found on disk.')
            if self.archive_name == 'none':
                print("Directly downloadign file " + str(self.file_name))
                Tools.download_file(self.url, os.path.join(Donnee.DATA_FOLDER, self.file_name))
            else:
                print("Downloading archive " + str(self.archive_name))
                Tools.download_file(self.url, self.archive_name)
                print("Extracting archive " + str(self.file_name))
                Tools.extract_file_from_archive(self.file_name, self.archive_name, self.archive_path, Donnee.DATA_FOLDER)
                
        f = Tools.open_file(self.file_name, Donnee.DATA_FOLDER, self.archive_name, self.archive_path)
        
        try:
            self.read_json_data_from_file(f)
            print("Succesfully read data from " + str(self.file_name))
        except:
            print("You don't have the data file ", self.file_name, " or this file is corrupted. Do you agree to download this file (Approximative size: ", self.size, " ? (yes/no)")
            download = (str(input()).lower() == "yes")
            if not download:
                print("Exiting..")
                exit()
            else:
                Tools.download_file(self.url, os.path.join(Donnee.DATA_FOLDER, self.file_name))
                f = Tools.open_file(os.path.join(Donnee.DATA_FOLDER, self.file_name), self.archive_name, self.archive_path)
                self.read_json_data_from_file(f)
        print('#########################\n')

    def read_json_data_from_file(self, f):
        constructor = None
        RAW_FILE_JSON = json.loads(''.join(f.readlines()))
        # i = 0
        ignores = 0
        for raw_line in RAW_FILE_JSON:
            # Tools.global_progress_bar(i, len(RAW_FILE_JSON))
            # i+=1
            line = raw_line
            if 'fields' in raw_line:
                line = raw_line['fields']

            all_critical_keys_in_entry = True
            for critical_key in self.critical_keys:
                if not critical_key in line.keys():
                    all_critical_keys_in_entry = False

            if all_critical_keys_in_entry:

                if self.parent_class == "departement":
                    constructor = src.model.departement.Departement
                elif self.parent_class == "region":
                    constructor = src.model.region.Region
                elif self.parent_class == "perte":
                    constructor = src.model.perte.Perte
                elif self.parent_class == "gare":
                    constructor = src.model.gare.Gare
                    
                instance = constructor()
                
                for key, value in line.items():
                    if key in self.keys:
                        index_key = self.keys.index(key)
                        alias = self.key_aliases[index_key]
                        try:
                            setattr(instance, alias, int(value))
                        except ValueError:
                            setattr(instance, alias, value)
                        except TypeError:
                            setattr(instance, alias, value)
            else:
                ignores += 1
        # print(ignores, "/", len(RAW_FILE_JSON), "rows have been ignored since they didn't contain all the required fields.")
