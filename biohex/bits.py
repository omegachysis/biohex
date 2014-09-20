
import random
import life

from bitLibrary.chemicals import *
from bitLibrary.experiments import *
from bitLibrary.functions import *
from bitLibrary.organelles import *
from bitLibrary.proteins import *

from bitLibrary import functions

from glob import glob
from os.path import basename
moduleList = glob("biohex/bitLibrary/*.py")
for module in [basename(i)[:-3] for i in moduleList]:
    if module != "functions":
        exec ("from bitLibrary." + module + " import *")