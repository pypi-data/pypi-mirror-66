import shutil


async def load_techlevel(hub):
    oslevel = shutil.which("oslevel")
    if oslevel:
        hub.corn.CORN.osrelease_techlevel = (
            await hub.exec.cmd.run([oslevel, "-r"])
        ).stdout.strip()


async def load_os(hub):
    release_info = lambda osrelease: tuple(
        int(x) if x.strip().isdigit() else x for x in osrelease.split(".")
    )

    oslevel = shutil.which("oslevel")
    uname = shutil.which("uname")
    if oslevel:
        hub.corn.CORN.osrelease = (await hub.exec.cmd.run(oslevel)).stdout.strip()
        hub.corn.CORN.osrelease_info = release_info(hub.corn.CORN.osrelease)
        hub.corn.CORN.osmajorrelease = hub.corn.CORN.osrelease_info[0]
        if uname:
            hub.corn.CORN.osfullname = (await hub.exec.cmd.run(uname)).stdout.strip()
            hub.corn.CORN.osfinger = (
                f"{hub.corn.CORN.osfullname}-{hub.corn.CORN.osmajorrelease}"
            )
    hub.corn.CORN.oscodename = "unknown"


async def load_build(hub):
    hub.corn.CORN.osbuild = "unknown"
    bootinfo = shutil.which("bootinfo")
    if bootinfo:
        ret = await hub.exec.cmd.run([bootinfo, "-m"])
        hub.corn.CORN.osbuild = ret.stdout.strip()
