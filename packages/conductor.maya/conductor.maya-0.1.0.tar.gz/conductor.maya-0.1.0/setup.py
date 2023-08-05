#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This setup.py file was originally templated from https://github.com/navdeep-G/setup.py

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import fileinput
import glob
import io
import os
import sys
from shutil import rmtree

import setuptools
from pip._internal.utils import misc
from setuptools.command.install import install

NAME = "conductor.maya"
DESCRIPTION = "Maya plugin for Conductor's client tools"
URL = "https://github.com/AtomicConductor/conductor-maya"
EMAIL = "info@conductortech.com"
AUTHOR = "conductor"
REQUIRES_PYTHON = "~=2.7"
VERSION = ""  # version will be populated by __version__.py file

REQUIRED = [
    "conductor.core>=0.1.1,<1.0.0"
    ]

# Optional packages/functionality
EXTRAS = {}


here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except IOError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace(
        "-", "_").replace(" ", "_").replace(".", os.sep)
    with open(os.path.join(here, "src", project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


def get_maya_app_dir():
    """Get Maya app dir from standard locations, unless overridden."""
    app_dir = os.environ.get("MAYA_APP_DIR")
    if not app_dir:
        home = os.path.expanduser("~")
        platform = sys.platform
        if platform == "darwin":
            tail = "Library/Preferences/Autodesk/maya"
        elif platform in ["win32", "msys", "cygwin"]:
            tail = "Documents\maya"
        else:  # linux
            tail = "maya"
        app_dir = os.path.join(home, tail)
    return app_dir


def added_by_us(line):
    return  line.strip().startswith("MAYA_MODULE_PATH") and "conductor/maya" in line  
 

def pypath_exists(line, install_dir):
    return line.strip().startswith("PYTHONPATH") and install_dir in line
 

class UploadCommand(setuptools.Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel distribution…")
        os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system(
            'twine upload --repository-url "https://test.pypi.org/legacy" dist/*')

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


class InstallWithVersionedModuleFile(install):
    """Write the module file with the version."""

    def run(self):
        if not self.dry_run:
            self.write_mod_file()
        install.run(self)
        if not self.dry_run:
            try:
                self.write_maya_env_files()
            except BaseException:
                pass

    def write_mod_file(self):
        target_path = os.path.join(self.build_lib, "conductor", "maya")
        with open(os.path.join(target_path, "conductor.mod"), "w") as fobj:
            fobj.write("+ conductor {} .\n".format(about["__version__"]))

    @staticmethod
    def write_maya_env_files():
        """
        if running under virtualenv then always use the sitepackages dir
        user and target flags are ignored.
        otherwise target takes precedence.
        if not in a virtualenv and no user or target flag set
        then use sitepackages
        This is, to the best of my knowledge, how pip determines
        where to put things.
        """
        install_path = misc.site_packages
        if not misc.running_under_virtualenv:
            if "-t" in sys.argv or "--target" in sys.argv:
                index = next(i for (i, a) in enumerate(sys.argv)
                             if a == "-t" or a == "--target")
                install_path = os.path.abspath(sys.argv[index+1])
            elif "--user" in sys.argv:
                install_path = misc.user_site

        mod_path = os.path.join(install_path, "conductor", "maya")
 
        app_dir = get_maya_app_dir()
        needs_pypath = True
        if os.path.isdir(app_dir):
            for env_file in glob.glob("{}/**/Maya.env".format(app_dir)):
                for line in fileinput.input(env_file, inplace=1):
                    if needs_pypath and pypath_exists(line, install_path):
                        needs_pypath=False
                    if added_by_us(line):
                        pass
                    else:
                        print line,

                with open(env_file, "a") as fobj:
                    fobj.write(
                        "\nMAYA_MODULE_PATH = $MAYA_MODULE_PATH:{}\n".format(mod_path))
                    if needs_pypath:
                        fobj.write("PYTHONPATH = $PYTHONPATH:{}\n".format(install_path))


setuptools.setup(
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
    ],
    cmdclass={"upload": UploadCommand,
              "install": InstallWithVersionedModuleFile},
    description=DESCRIPTION,
    extras_require=EXTRAS,
    install_requires=REQUIRED,
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=NAME,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    version=about["__version__"],
    zip_safe=False,
    package_data={
        NAME: [
            "plug-ins/*.py",
            "icons/*.*",
            "scripts/*.mel",
            "scripts/*.py",
        ]
    },
)
