import vim
from omnipytent import *


@task
def build(ctx):
    BANG('pyinstaller', '--onefile', '--uac-admin', 'src/deploy.py')
