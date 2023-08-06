import datetime
import os
import subprocess 
import errno
import sys
from email.parser import Parser


def main():
    print "Setting up Maya..."

    maya_info = get_package_info("conductor.maya")
    if not  maya_info:
        sys.stderr.write("conductor.maya is not installed")
        sys.exit(1)

        
    core_info = get_package_info("conductor.core")
    if not core_info:
        sys.stderr.write("conductor.core is not installed")
        sys.exit(1)

    mod_dir=None
    try:
        mod_dir = get_maya_modules_dir()
    except OSError as ex:
        print ex
        sys.stderr.write(ex.message)
        sys.stdout.write("Can't access any module directory.\n")
        sys.stdout.write("Please note the following information and then consult docs.conductortech.com and search 'setup_maya'.\n")
        
    mod_file = write_module_file(core_info, maya_info, mod_dir)
    sys.stdout.write("Wrote module file: {}.\n".format(mod_file))
    msg= """
Thanks for installing Conductor-Maya!
The next time you run Maya you can load the Conductor plugin from the Plugin Manager. 
Windows->Settings/Preferences->Plug-in Manager.
Once loaded, you'll see a Conductor menu in the main menu bar, where you can configure a submission.

For more info, visit https://docs.conductortech.com and search for setup_maya. 
    """
    sys.stdout.write(msg)
    sys.exit(0)
    
def write_module_file(core_info, maya_info, modules_directory=None):

    paths = list(set([core_info[0],maya_info[0]]))
    python_paths = ":".join(paths)
    maya_mod_path = os.path.join(maya_info[0], "conductor", "maya")
    content = "+ conductor {} {}\n".format(maya_info[1], maya_mod_path)
    content += "PYTHONPATH +={}\n".format(python_paths)

    module_file = None
    if modules_directory:
        module_file = os.path.join(modules_directory,"conductor.mod" )
        with open(module_file, "w") as fobj:
            fobj.write(content)
    else:
        sys.stdout.write(content)
        
    return module_file

def get_maya_modules_dir():
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

    mod_dir = os.path.join(app_dir,  "modules")
    ensure_directory(mod_dir)
    return mod_dir


def ensure_directory(directory):
    try:
        os.makedirs(directory)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise

def get_package_info(name):
    p = subprocess.Popen(["pip", "show", name ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")

    data = Parser().parsestr(output)
    if "Location" in data:
        return (data["Location"], data.get("Version")) 
