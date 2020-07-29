from pathlib import Path

from clld.web.assets import environment

import tppsr


environment.append_path(
    Path(tppsr.__file__).parent.joinpath('static').as_posix(),
    url='/tppsr:static/')
environment.load_path = list(reversed(environment.load_path))
