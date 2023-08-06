import logging
import re
import shutil

log = logging.getLogger(__name__)


async def load_meminfo(hub):
    """
    Return the memory information for AIX systems
    """
    hub.corn.CORN.mem_total = 0

    prtconf = shutil.which("prtconf")
    if prtconf:
        ret = await hub.exec.cmd.run([prtconf, "-m"])
        hub.corn.CORN.mem_total = int(ret.stdout.strip().split()[2])
    else:
        log.error("Could not find `prtconf` binary in $PATH")


async def load_swapinfo(hub):
    hub.corn.CORN.swap_total = 0

    swap = shutil.which("swap")
    if swap:
        # allocated = 688128 blocks used = 2664 blocks free = 685464 blocks
        ret = await hub.exec.cmd.run([swap, "-s"])
        match = re.search(
            "blocks\s+used\s+=\s+(\d+)\s+blocks\s+free\s+=\s+(\d+)\s+blocks",
            ret.stdout.strip(),
        )
        if match:
            hub.corn.CORN.swap_total = (int(match.group(1)) + int(match.group(2))) * 4
    else:
        log.error("Could not find `swap` binary in $PATH")
