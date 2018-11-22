import sys
import urllib.request
import zipfile
import os 

class Tools:

    @staticmethod
    def progress_bar(blocks_transfered, block_size, total_size):

        size = 20
        done_percentage = (blocks_transfered * block_size/total_size) * 100
        os.system("cls") 
        sys.stdout.flush()
        sys.stdout.write("Please be patient while the data files are being downloaded \n")
        sys.stdout.write("[")
        for i in range(size):
            if i < done_percentage/100*size:
                sys.stdout.write("-")
            else:
                sys.stdout.write(" ")
        sys.stdout.write("] - ")
        sys.stdout.write(str(done_percentage).split('.')[0])
        sys.stdout.write("%")
        sys.stdout.write("\n (the progress bar might be buggy)")

        # print(blocks_transfered * block_size)
        # print(block_size)
        # print(total_size)

    @staticmethod
    def download_file(url, file_name):
        # response = urllib.request.urlopen(url)
        # html = response.read()
        # binfile = open(filename, "wb")
        # binfile.write(html)
        # binfile.close()
        urllib.request.urlretrieve(url, file_name, Tools.progress_bar)


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
