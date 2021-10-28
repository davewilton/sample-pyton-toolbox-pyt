import sys
from unittest.mock import Mock, MagicMock


def pytest_addoption(parser):
    """
    Commandline options for tests
    """
    parser.addoption(
        '--nomock',
        action='store_true',
        help='Do not use the arcpy mock - use arcpy'
    )


def pytest_configure(config):
    if not config.getoption('--nomock'):
        # Import our arcpy_mock module
        # This can provide the behavior we want to the necessary
        # arcpy methods.

        import arcpy_mock
        arcpy_mock.enable()
