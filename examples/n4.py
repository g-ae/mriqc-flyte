import subprocess

from flyte.io import File

from mriqc_flyte.env import anat_env


@anat_env.task(cache="auto")
async def n4(in_file: File) -> File:
    local_path = await in_file.download()

    print(local_path)

    # fmt: off
    cmd = [
        "N4BiasFieldCorrection",
        "-d", "3",
        "-i", local_path,
        "-o", "/work/test.nii.gz",
    ]

    # fmt: on
    subprocess.run(cmd, check=True)

    out_file = await File.from_local("/work/test.nii.gz")
    return out_file


@anat_env.task
async def print_local_path(in_file: File) -> None:
    print("Remote path:", in_file.path)
    local_path = await in_file.download()
    print("Local path:", local_path)


@anat_env.task
async def main(in_file: File) -> None:
    n4_outfile = await n4(in_file)
    await print_local_path(n4_outfile)
