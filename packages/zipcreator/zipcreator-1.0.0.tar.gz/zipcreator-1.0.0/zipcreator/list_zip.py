import zipfile


def create(files, destination, compression=zipfile.ZIP_DEFLATED):
    """
    Create the zipfile located at the given destination with the files specified.

    :param files: List of files as strings
    :param destination: path and filename of desired zip destination
    :param compression: Compression format for zip handler
    """
    zip_handler = zipfile.ZipFile(destination, 'w', compression)
    if len(files) > 1:
        for f in files:
            zip_handler.write(f)
    zip_handler.close()
