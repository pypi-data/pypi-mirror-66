#!C:\Users\samueld\anaconda3\envs\archetypal\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'archetypal==1.3.0','console_scripts','archetypal'
__requires__ = 'archetypal==1.3.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('archetypal==1.3.0', 'console_scripts', 'archetypal')()
    )
