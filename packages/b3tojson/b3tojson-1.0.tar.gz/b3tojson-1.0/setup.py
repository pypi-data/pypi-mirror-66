import os
import sys

import setuptools
import versioneer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))  # noqa

setuptools.setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass()
)
