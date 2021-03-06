import json
import os
import sys

from jupyter_client.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory

from os.path import dirname,abspath

from shutil import copy as file_copy

kernel_json = {"argv":[sys.executable,"-m","jupyter_polymake_wrapper", "-f", "{connection_file}"],
 "display_name":"polymake",
 "language":"polymake",
 "codemirror_mode":"polymake", # note that this does not exist yet
 "env":{"PS1": "$"}
}

def install_my_kernel_spec(user=True):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        path_of_file = dirname( abspath(__file__) ) + "/resources/"
        filenames=[ "Detector.js", "three.js", "kernel.js"  ]
        filenames_renderer=[ "CanvasRenderer.js", "Projector.js" ]
        filenames_control=[ "TrackballControls.js" ]
        for i in filenames:
            file_copy(path_of_file + i, td )
        os.mkdir( td + "renderers", mode=755 )
        for i in filenames_renderer:
            file_copy(path_of_file + "renderers/" + i, td + "renderers" )
        os.mkdir( td + "controls", mode=755 )
        for i in filenames_control:
            file_copy(path_of_file + "controls/" + i, td + "controls" )
        file_copy(path_of_file + "logo-32x32.png", td )
        file_copy(path_of_file + "logo-64x64.png", td )
        print('Installing IPython kernel spec')
        install_kernel_spec(td, 'polymake', user=user, replace=True)

def main(argv=None):
    install_my_kernel_spec()

if __name__ == '__main__':
    main()
