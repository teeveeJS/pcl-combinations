def valid_file_name(s):
    """Check if the input string follows the guidelines of a valid filename"""
    disallowed = ["\'", "\"", "~", "#", "%", "&", "*", "{", "}", "\\", ":", \
                  "<", ">", "?", "/", "|", ".", ",", ";"]
    if len(s) == 0 or len(s) > 50:
        return False
    # prohibit hidden files. also takes care of _vti_
    if s[0] == "_":
        return False
    for c in s:
        if c in disallowed:
            return False
    # bunch of other checks that i'll ignore
    return True
