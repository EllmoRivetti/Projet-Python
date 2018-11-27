import sys
import urllib.request
import zipfile
import os 
import unicodedata



class Tools:
    CURRENTLY_DOWNLOADED_FILE = None
    percentage = 0

    @staticmethod
    def global_progress_bar(blocks_transfered, total_size):
        if blocks_transfered % int(total_size / 100) == 0:
            progress_bar_size = 20
            done_percentage = (blocks_transfered/total_size) * 100
            sys.stdout.write("Computing losses by regions and departements... ")
            sys.stdout.write("[")
            for i in range(progress_bar_size):
                if i < done_percentage/100*progress_bar_size:
                    sys.stdout.write("-")
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("] - ")
            sys.stdout.write(str(done_percentage).split('.')[0])
            sys.stdout.write("% \r")

    @staticmethod
    def strip_accents(text):
        """
        Strip accents from input String.

        :param text: The input string.
        :type text: String.

        :returns: The processed String.
        :rtype: String.
        https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
        """
        try:
            text = unicode(text, 'utf-8')
        except (TypeError, NameError): # unicode is a default on python 3 
            pass
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return str(text).replace('-', ' ') # replaces '-' by spaces for pseudo conventional naming

    @staticmethod
    def progress_bar(blocks_transfered, block_size, total_size):
        # the progress bar might be buggy because of bad websites that do not provide packet size in html headers
        size = 20
        done_percentage = (blocks_transfered * block_size/total_size) * 100
        
        if not Tools.percentage == done_percentage:
            Tools.percentage = done_percentage
            sys.stdout.write("\rPlease be patient while the data files are being downloaded ")
            sys.stdout.write("[")
            for i in range(size):
                if i < done_percentage/100*size:
                    sys.stdout.write("-")
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("] - ")
            sys.stdout.write(str(done_percentage).split('.')[0])
            sys.stdout.write("%")
            if done_percentage == 100:
                Tools.percentage = 0
                print('\n')

    @staticmethod
    def download_file(url, file_name):
        # response = urllib.request.urlopen(url)
        # html = response.read()
        # binfile = open(filename, "wb")
        # binfile.write(html)
        # binfile.close()
        Tools.CURRENTLY_DOWNLOADED_FILE = file_name
        urllib.request.urlretrieve(url, file_name, Tools.progress_bar)
        Tools.CURRENTLY_DOWNLOADED_FILE = None


    @staticmethod
    def extract_file_from_archive(file_name, archive_name, archive_path, directory_name=''):
        archive = zipfile.ZipFile(archive_name, 'r')
        path = []
        path.extend(archive_path)
        path.append(file_name)
        path_to_file = os.path.join(*path)
        path_to_file = path_to_file.replace('\\', '/')
        file = archive.open(path_to_file)
        with open(os.path.join(directory_name, file_name), 'wb') as destination_file:
            for line in file.readlines():
                destination_file.write(line)

    @staticmethod
    def open_file(file_name, directory_name='', archive_name='', path_in_archive=[]):
        try:
            return open(os.path.abspath(os.path.join(directory_name, file_name)))
        except:
            archive = zipfile.ZipFile(archive_name, 'r')
            path = []
            path.extend(path_in_archive)
            path.append(file_name)
            path_to_file = os.path.join(*path)
            path_to_file = path_to_file.replace('\\', '/')

            file = archive.open(path_to_file)
            with open(file_name, 'wb+') as f:
                for line in file.readlines():
                    f.write(line)
