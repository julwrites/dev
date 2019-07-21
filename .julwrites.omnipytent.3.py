import vim
from omnipytent import *


@task
def gather(ctx):
    BANG('python', 'gather.py')


@task
def scatter(ctx):
    BANG('python', 'scatter.py')
