"""Functions that uncompress gzipped base64 content and write them to file."""

import base64
import gzip
import os
import shutil

gz_file = 'temp.{0}.gz'
file = 'temp.{0}'
mode_write = 'wb'
mode_read = 'rb'
default_encoding = 'UTF-8'


def uncompressed_base64(gz_content, extension, encoding='{0}'.format(default_encoding)):
    """Uncompress a gzip-compressed file content or encoded content to plain base64 text mode.

        The gz_content argument can be an actual gzip compressed file content string to be 
        decompressed as a file and the file to be a base64 content.

        The extension argument is a file extension which is compressed to gzip.
        
        The encoding argument is a file encoding format which is used at compression to gzip.
        It is defaults to UTF-8

        This function will return a plain base64 string of a compressed file.

        """
    # Converting gzip compressed file data into binary
    binary_data = base64.b64decode(gz_content)
    # De compressing binary data to bytes stream
    decompressed_content = gzip.decompress(binary_data)
    # Creating a temp gzip file
    temp_gz_file = gzip.GzipFile(gz_file.format(extension), mode_write)
    temp_gz_file.write(decompressed_content)
    temp_gz_file.close()

    # Opening gzip file to extract it's content
    with gzip.open(gz_file.format(extension), mode_read) as f_in:
        # Opening new file to write gzip extracted content
        with open(file.format(extension), mode_write) as f_out:
            shutil.copyfileobj(f_in, f_out)

    file_content = open(file.format(extension), mode_read).read()
    b64_string = base64.b64encode(file_content)

    os.remove(gz_file.format(extension))
    os.remove(file.format(extension))

    return b64_string.decode(encoding)


def write_to_file(gz_content, file_name, extension):
    """Uncompress a gzip-compressed file content or encoded content to original file.

            The gz_content argument can be an actual gzip compressed file content string to be
            decompressed as a file.

            The file_name argument is a free file name which is used to write the file on file system.

            The extension argument is a file extension which is compressed to gzip.

            """
    file_name = file_name + '.{0}'
    binary_data = base64.b64decode(gz_content)
    # De compressing binary data to bytes stream
    decompressed_content = gzip.decompress(binary_data)
    # Creating a temp gzip file
    temp_gz_file = gzip.GzipFile(gz_file.format(extension), mode_write)
    temp_gz_file.write(decompressed_content)
    temp_gz_file.close()

    # Opening gzip file to extract it's content
    with gzip.open(gz_file.format(extension), mode_read) as f_in:
        # Opening new file to write gzip extracted content
        with open(file_name.format(extension), mode_write) as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(gz_file.format(extension))
