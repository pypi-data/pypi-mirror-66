import logging
import re
import shutil

log = logging.getLogger(__name__)


async def load_machine_id(hub):
    lsattr = shutil.which("lsattr")

    if lsattr:
        ret = await hub.exec.cmd.run([lsattr, "-El", "sys0"])
        match = re.search(r"(?im)^\s*os_uuid\s+(\S+)\s+(.*)", ret.stdout)
        if match and len(match.groups()) >= 1:
            hub.corn.CORN.machine_id = match.group(1)
    else:
        log.error("The `lsattr` binary was not found in $PATH")
