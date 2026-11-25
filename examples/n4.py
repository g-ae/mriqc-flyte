import subprocess
from pathlib import Path

from flyte.io import File

from mriqc_flyte.env import anat_env


@anat_env.task(cache="auto")
async def n4(in_file: File, work_dir: Path) -> File:
    local_path = await in_file.download()
    print(local_path)

    work_dir = work_dir / "n4"
    work_dir.mkdir(parents=True, exist_ok=True)

    file_uri = work_dir / "test.nii.gz"

    # fmt: off
    cmd = [
        "N4BiasFieldCorrection",
        "-d", "3",
        "-i", local_path,
        "-o", file_uri,
    ]

    # fmt: on
    subprocess.run(cmd, check=True)

    out_file = await File.from_local(file_uri)
    return out_file


@anat_env.task
async def print_local_path(in_file: File) -> None:
    print("Remote path:", in_file.path)
    local_path = await in_file.download()
    print("Local path:", local_path)


@anat_env.task
async def main(in_file: File, work_dir: str = "/work") -> None:
    work = Path(work_dir) / "mriqc_flyte"
    n4_outfile = await n4(in_file, work)
    await print_local_path(n4_outfile)
