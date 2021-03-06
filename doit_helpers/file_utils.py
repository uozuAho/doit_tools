import fnmatch
import os


def find(path, patterns, exclude_patterns=[], search_subdirs=False):
    """ Return a list of files under the given path that match any
        of the given patterns, and doesn't match any of the exclude
        patterns. Uses Unix filename patterns (fnmatch). Searches
        all subdirectories by default.

        @param patterns:
            Filename pattern(s) to match. Can be a string or a list
            of strings.

        @param exclude_patterns:
            Filename pattern(s) to exclude from search results. Can
            be a string of list of strings.
    """
    # convert patterns to lists if they are not already
    if type(patterns) is not list:
        patterns = [patterns]
    if type(exclude_patterns) is not list:
        exclude_patterns = [exclude_patterns]

    # find all paths that match the include pattern(s)
    matches = []
    if search_subdirs:
        for root, dirnames, filenames in os.walk(path):
            for filename in filenames:
                for pattern in patterns:
                    if fnmatch.fnmatch(filename, pattern):
                        matches.append(os.path.join(root, filename))
    elif os.path.exists(path):
        for item in os.listdir(path):
            item = os.path.join(path, item)
            if os.path.isfile(item):
                for pattern in patterns:
                    if fnmatch.fnmatch(item, pattern):
                        matches.append(item)

    # remove any paths that match the exclude pattern(s)
    def is_excluded(filename):
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(filename, pattern):
                return True
        return False

    return [x for x in matches if not is_excluded(x)]
