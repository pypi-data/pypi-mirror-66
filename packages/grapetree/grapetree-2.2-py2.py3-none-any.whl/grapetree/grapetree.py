#!/usr/bin/env python

# Copyright Zhemin Zhou, Martin Sergeant, Nabil-Fareed Alikhan & Mark Achtman (2017)
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but without
# any warranty; without even the implied warranty of merchantability or fitness
# for a particular purpose. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Web interface of GrapTree, which is a program for phylogenetic analysis.

GrapeTree is an integral part of EnteroBase and we advise that you use GrapeTree
through EnteroBase for the best results. However, many people have asked for a
stand-alone GrapeTree version that they could use offline or integrate into the
other applications.

The stand-alone version emulates the EnteroBase version through a lightweight
webserver running on your local computer.  You will be interacting with the
program as you would in EnteroBase; through a web browser.
"""
from __future__ import print_function, absolute_import

try:
    from .module import app
    from .module.MSTrees import backend, add_args
except :
    from module import app
    from module.MSTrees import backend, add_args
    
import threading
import webbrowser
import traceback
import argparse
import os, sys, shutil
import multiprocessing


__licence__ = 'GPLv3'
__author__ = 'EnteroBase development team'
__author_email__ = 'zhemin.zhou@warwick.ac.uk'

epi = "Licence: " + __licence__ + " by " + __author__ + \
    " <" + __author_email__ + ">"


def open_browser(PORT):
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s' % PORT)
    thread = threading.Timer(0.5, _open_browser)
    thread.start()


def main() :
    if len(sys.argv) > 1 :
        print (backend(**add_args()))
    else :
        try:
            desc = __doc__.split('\n\n')[1].strip()
            parser = argparse.ArgumentParser(description=desc, epilog=epi)
            args = parser.parse_args()
            open_browser(app.config.get('PORT'))
            app.run(port=app.config.get('PORT'))
            sys.exit(0)
        except KeyboardInterrupt as e:  # Ctrl-C
            raise e
        except SystemExit as e:  # sys.exit()
            raise e
        else :
            print ('ERROR, UNEXPECTED EXCEPTION')
            print (str(e))
            traceback.print_exc()
            os._exit(1)

if __name__ == "__main__":
    #from module import views
    #views.sendToMicroReact(debug='debug')
    multiprocessing.freeze_support()
    main()
