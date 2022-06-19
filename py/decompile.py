"""
creation: January 5, 2021?

Mass decompiles .class files in a .jar
You need to unzip the jar, then
`python3 decompile.py [path to decompiler (I used cfr)] [unzipped jar folder] [target folder]`
"""

import os
from pathlib import Path
import subprocess
import sys

CFR = Path(sys.argv[1])
frompath = Path(sys.argv[2])
topath = Path(sys.argv[32])

for p, _, fs in os.walk(frompath):
    rp = Path(p).relative_to(frompath)
    np = topath.joinpath(rp)

    if not os.path.isdir(np): os.mkdir(np)
    
    for f in fs:
        oldf = Path(p).joinpath(f)
        if oldf.suffix != '.class': continue
        newf = Path(np).joinpath(f).with_suffix('.java')

        sub = subprocess.run(['java', '-jar', str(CFR), oldf], stdout=subprocess.PIPE)
        with open(newf, mode='wb') as w:
            w.write(sub.stdout)
        