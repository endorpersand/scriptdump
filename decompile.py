import os
from pathlib import Path
import subprocess

frompath = Path('./OptiFine_1.16.4_HD_U_G5/net/optifine')
topath = Path('./de')

for p, _, fs in os.walk(frompath):
    rp = Path(p).relative_to(frompath)
    np = topath.joinpath(rp)

    if not os.path.isdir(np): os.mkdir(np)
    
    for f in fs:
        oldf = Path(p).joinpath(f)
        if oldf.suffix != '.class': continue
        newf = Path(np).joinpath(f).with_suffix('.java')

        sub = subprocess.run(['java', '-jar', 'cfr-0.150.jar', oldf], stdout=subprocess.PIPE)
        with open(newf, mode='wb') as w:
            w.write(sub.stdout)
        