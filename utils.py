import os
import sys

def get_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.join(os.path.dirname(sys.executable), "laudo_sars_cov")
    else:
        # The application is not frozen
        datadir = "laudo_sars_cov"
    return os.path.join(datadir, filename)
