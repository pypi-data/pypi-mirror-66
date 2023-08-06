"""A collection of utility functions for internal use by the apdft project"""


def flatten(l: list):
    """
    Accepts a list containing one or more nested lists and returns a flattened copy.

    Parameters
    ----------
    l: list
        A list containing one or more lists. Can contain zero lists but there's no point

    Returns
    -------
    list
        A flattened version of the original list, no matter how deep. String elements
        are preserved as to not spread them out into individual characters.
    """
    new_list = []
    for i in l:
        if isinstance(i, list):
            new_list.extend(flatten(i))
        else:
            new_list.append(i)

    return new_list


def get_pdfs_in_dir(dir: str, disable_sorting: bool = False):
    import os

    """
    Retrieves a list of all '.pdf' files found under the given directory.

    Parameters
    ----------
    dir: str
        An absolute or relative path to a directory containing '.pdf' files.

    Returns
    -------
    list
        A list of absolute file paths to each '.pdf' file under the directory tree,
        sorted alphanumerically by filename.
    """
    names_in_dir = os.listdir(dir)
    abs_paths_in_dir = [os.path.join(dir, name) for name in names_in_dir]

    found_pdfs = []
    for path in abs_paths_in_dir:
        if os.path.isdir(path):
            found_pdfs.append(get_pdfs_in_dir(path))
        else:
            _, ext = os.path.splitext(path)
            if ext == ".pdf":
                found_pdfs.append(path)

    found_pdfs = flatten(found_pdfs)
    if not disable_sorting:
        found_pdfs = sorted(found_pdfs, key=lambda path: os.path.basename(path))
    return found_pdfs
