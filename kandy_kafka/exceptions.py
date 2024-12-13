class HostsFileNotFound(Exception):
    """
    Exception raised when the hosts configuration file is not found
    """

    pass


class HostsFileHasWrongSyntax(Exception):
    """
    Exception raised when the hosts configuration file has incorrect syntax or missing required fields
    """

    pass
