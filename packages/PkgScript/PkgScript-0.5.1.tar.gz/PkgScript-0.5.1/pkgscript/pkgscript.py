#!/usr/bin/env python

"""pkgscript.py

    Python module that allows a packaged module to run properly as a script.

    Calling this function in a packaged module (running as a script) will
    import the script's parent package(s),
    allowing the script to import other modules from the same package family
    (using either explicit relative or absolute import statements).

    !!! This function must be called before any package-sibling imports !!!

    Examples:

        ### Milo.mod_script.py
        import pkgscript
        # Only call function if module is being run as a script
        if (__name__ == "__main__") and (__package__ is None):
            pkgscript.import_parent_packages("Milo", globals())
        from Milo.version import __version__
        from .version import __version__    # same as previous line

        ### top_pkg.sub_pkg.sub_sub_pkg.mod_script.py
        import pkgscript
        # Only call function if module is being run as a script
        if (__name__ == "__main__") and (__package__ is None):
            pkgscript.import_parent_packages(
                "top_pkg.sub_pkg.sub_sub_pkg", globals())
        # Import top_pkg.sub_pkg.other_module
        from top_pkg.sub_pkg import other_module
        from .. import other_module    # same as previous line
        from ...sub_pkg import other_module    # same as previous line

        ### ALS.Milo.mod_script.py
        import pkgscript
        # Only call function if module is being run as a script
        if (__name__ == "__main__") and (__package__ is None):
            pkgscript.import_parent_packages("als.milo", globals())
        from als.milo import __version__, __date__
        from . import __version__, __date__    # same as previous line

    This software is adapted from helpful code posted by @vaultah
        (https://gist.github.com/vaultah/d63cb4c86be2774377aa674b009f759a)
        in response to a question on Stack Overflow
        (https://stackoverflow.com/a/28154841/9639441)

    Copyright (c) 2018, 2020, Padraic Shafer

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""

__copyright__ = "Copyright 2018, Padraic Shafer"
__credits__ = ["Padraic Shafer", "vaultah"]
__license__ = "The MIT License (MIT)"
__maintainer__ = "Padraic Shafer"
__email__ = "PShafer@lbl.gov"
__status__ = "Development"

import os
import importlib


def import_parent_packages(abs_package_name, global_dict):
    """ Import all parent packages when module is run as script

        *) Allows script to import "sibling" modules from package family
            (using either explicit relative or absolute import statements)

        abs_package_name: Absolute package name of script's parent directory
        global_dict: Calling script should pass `globals()`

        RETURNS: None

        !!! Side Effects !!!
            *) Sets __package__ to abs_package_name
            *) Adds parent directory of top-level package to *system path*
            *) Imports __package__

    """
    # __package__ defaults to None for module run as script
    global_dict["__package__"] = abs_package_name
    package_levels = len(abs_package_name.split('.'))

    # Start from script directory, recursively go up to top-level directory
    script_dir = os.path.dirname(global_dict["__file__"])
    package_parent_dir = os.path.abspath(script_dir)
    for i in range(package_levels):
        package_parent_dir = os.path.dirname(package_parent_dir)

    # Local package can override an installed package (e.g., for development)
    os.sys.path.insert(0, package_parent_dir)
    global_dict[abs_package_name] = importlib.import_module(abs_package_name)

    return
