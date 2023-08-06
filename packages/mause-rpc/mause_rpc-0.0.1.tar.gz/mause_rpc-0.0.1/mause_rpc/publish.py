from pathlib import Path

from poetry_publish.publish import poetry_publish

import mause_rpc


def publish():
    poetry_publish(
        package_root=Path(mause_rpc.__file__).parent.parent,
        version=mause_rpc.__version__,
    )
