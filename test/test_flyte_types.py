# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
"""Tests for types that the Flyte tasks return."""

from dataclasses import dataclass

import flyte
import pytest
from flyte.io import File

import mriqc_flyte.env


# Types
@dataclass(frozen=True)
class FileStr:
    file: File
    string: str


@dataclass
class FileStrListFile:
    fstr: FileStr
    listfile: list[File]


# Tasks
@mriqc_flyte.env.anat_env.task
async def filestr(fs: FileStr) -> FileStr:
    return fs


@mriqc_flyte.env.anat_env.task
async def filestr_listfile(f: FileStrListFile) -> FileStrListFile:
    return f


@mriqc_flyte.env.anat_env.task
async def file_none(f: File | None) -> File | None:
    return f


@mriqc_flyte.env.anat_env.task
async def listfile(lf: list[File]) -> list[File]:
    return lf


@mriqc_flyte.env.anat_env.task
async def dict_str_float(d: dict[str, float]) -> dict[str, float]:
    return d


# Tests
@pytest.fixture
def sample_file() -> File:
    with open("tmpfile.txt", "a") as f:
        f.write("File content\n")

    return File(path="tmpfile.txt")


## FileStr dataclass
@pytest.mark.asyncio
async def test_dataclass_filestr_direct(sample_file):
    """Frozen dataclass "FileStr" can be used as an input and return type,
    while running directly."""
    fs = FileStr(sample_file, "testString")

    assert isinstance(await filestr(fs), FileStr)


@pytest.mark.asyncio
async def test_dataclass_filestr_flyterun(sample_file):
    """Frozen dataclass "FileStr" can be used as an input and return type,
    while runnign through flyte.run()."""
    fs = FileStr(sample_file, "testString")

    run = flyte.run(filestr, fs)

    assert isinstance(run.outputs()[0], FileStr)


## FileStrListFile dataclass
@pytest.mark.asyncio
async def test_dataclass_filestrlistfile_direct(sample_file):
    """Dataclass "FileStrListFile" can be used as an input and return type,
    while running directly."""
    fs = FileStr(sample_file, "testString")

    dc = FileStrListFile(fs, [sample_file, sample_file])

    assert isinstance(await filestr_listfile(dc), FileStrListFile)


@pytest.mark.asyncio
async def test_dataclass_filestrlistfile_flyterun(sample_file):
    """Dataclass "FileStrListFile" can be used as an input and return type,
    while running thorugh flyte.run()."""
    fs = FileStr(sample_file, "testString")

    dc = FileStrListFile(fs, [sample_file, sample_file])

    run = flyte.run(filestr_listfile, dc)

    assert isinstance(run.outputs()[0], FileStrListFile)


## File | None
@pytest.mark.asyncio
async def test_dataclass_filenone_file_direct(sample_file):
    """File | None can be used as an input and return type (sending a file)
    while running directly."""
    assert isinstance(await file_none(sample_file), File)


@pytest.mark.asyncio
async def test_dataclass_filenone_none_direct():
    """File | None can be used as an input and return type (sending nothing)
    while running directly."""
    assert isinstance(await file_none(None), File | None)


@pytest.mark.asyncio
async def test_dataclass_filenone_file_flyterun(sample_file):
    """File | None can be used as an input and return type (sending a file)
    while running through flyte.run()."""
    run = flyte.run(file_none, sample_file)

    assert isinstance(run.outputs()[0], File)


@pytest.mark.asyncio
async def test_dataclass_filenone_none_flyterun():
    """File | None can be used as an input and return type (sending nothing)
    while running through flyte.run()."""
    run = flyte.run(file_none, None)

    assert isinstance(run.outputs()[0], File | None)


## list[File]
@pytest.mark.asyncio
async def test_dataclass_listfile_direct(sample_file):
    """list[File] can be used as an input and return type while running directly."""
    assert isinstance(await listfile([sample_file, sample_file]), list)


@pytest.mark.asyncio
async def test_dataclass_listfile_flyterun(sample_file):
    """list[File] can be used as an input and return type while running flyte.run()."""
    run = flyte.run(listfile, [sample_file, sample_file])

    assert isinstance(run.outputs()[0], list)


## dict[str, float]
@pytest.mark.asyncio
async def test_dataclass_dictstrfloat_direct():
    """dict[str, float] can be used as an input and return type while running directly."""
    d = {"a": 1.2, "b": 5.4}
    assert isinstance(await dict_str_float(d), dict)


@pytest.mark.asyncio
async def test_dataclass_dictstrfloat_flyterun():
    """dict[str, float] can be used as an input and return type while running flyte.run()."""
    d = {"a": 1.2, "b": 5.4}
    run = flyte.run(dict_str_float, d)
    assert isinstance(run.outputs()[0], dict)
