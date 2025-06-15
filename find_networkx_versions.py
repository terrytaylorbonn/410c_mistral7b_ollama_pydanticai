# Temporary script to find the latest compatible networkx version for the current Python
import pkg_resources
import sys

try:
    import pip._internal as pip_internal
except ImportError:
    import pip as pip_internal

from subprocess import check_output

# Get all available versions of networkx
output = check_output([sys.executable, '-m', 'pip', 'index', 'versions', 'networkx'])
print(output.decode())
