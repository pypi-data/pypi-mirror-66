from subprocess import Popen
from . import glb
import os

def start():
    # out = open(glb.get_path('out.log'), 'ab')
    # err = open(glb.get_path('err.log'), 'ab')
    Popen(["exam_proctor_daemon"], stdout=out, stderr=err)
    # os.spawnl(os.P_DETACH, "exam_proctor_daemon")

