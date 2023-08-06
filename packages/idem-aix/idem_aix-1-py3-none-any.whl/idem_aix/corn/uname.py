import os


async def load_uname(hub):
    """
    Verify that idem-aix is running on AIX
    """
    (
        hub.corn.CORN.kernel,
        hub.corn.CORN.nodename,
        hub.corn.CORN.kernelrelease,
        hub.corn.CORN.kernelversion,
        _,
    ) = os.uname()
    assert hub.corn.CORN.kernel == "AIX", "idem-AIX is only intended for AIX systems"

    # Hard coded grains for AIX systems
    hub.corn.CORN.os_family = hub.corn.CORN.os = "AIX"
    hub.corn.CORN.osmanufacturer = "International Business Machines Corporation"
    hub.corn.CORN.ps = "/usr/bin/ps auxww"
