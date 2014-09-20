#import experiments
#import chemicals
#import functions
#import organelles
#import proteins

from glob import glob
from os.path import basename
moduleList = glob("biohex/bitLibrary/*.py")
for module in [basename(i)[:-3] for i in moduleList]:
    exec ("import " + module)