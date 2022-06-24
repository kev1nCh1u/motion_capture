import os
import sys
sys.path.append(os.getcwd())
from lib.kevin.kevincv import *

###################################################################################
# if main
###################################################################################
if __name__ == '__main__':
    gp = GenPoint()

    gp.a = [14.414906327500171, 22.34505201771049, 449.62576160776894]
    gp.b = [96.13160683183148, 55.10663416683474, 478.5723029681971]
    gp.c = [47.43867422337718, 71.66474800800661, 461.57418427997044]
    gp.dis = [79,57,82]

    ans = gp.solve_fsolve()
    print(ans)