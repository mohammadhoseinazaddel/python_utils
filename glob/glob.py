from glob import glib

def file_folder_finder(folder_path, word_or_globy_regex, is_folder=False):
    """

    Args:
        folder_path: the path to find
        word_or_globy_regex: use *word if you want endwith the word or word* start with it
        is_folder: if you only just want find folders

    Returns:
        list of matched files

    """
    complete_path = folder_path + word_or_globy_regex
    if is_folder:
        complete_path += "/"
    return glob(complete_path)
  
  
