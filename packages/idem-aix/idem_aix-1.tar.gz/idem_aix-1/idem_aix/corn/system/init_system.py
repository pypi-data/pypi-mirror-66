import shutil


async def load_init(hub):
    if shutil.which("rc"):
        hub.corn.CORN.init = "rc"
    else:
        hub.corn.CORN.init = "unknown"
