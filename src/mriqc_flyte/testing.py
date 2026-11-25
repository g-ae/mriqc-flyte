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
"""Comparators (images, masks, IQM files) and the baseline loader"""

import os
from pathlib import Path

from nipype.interfaces.base.support import InterfaceResult
from nipype.utils.filemanip import loadpkl
from traits.trait_base import _Undefined


def baseline_node(run: int, subworkflow: str, node: str) -> dict:
    prefix = os.getenv("MRIQC_FLYTE_BASELINE", "/baseline")

    base_path = Path(prefix) / f"run-{run}" / "work" / "mriqc_wf" / "anatMRIQC" / subworkflow
    glob_results = list(base_path.glob(f"*/{node}/result_{node}.pklz"))

    if len(glob_results) == 0:
        raise Exception(f"Results file not found with baseline '{prefix}'")

    result: InterfaceResult = loadpkl(glob_results[0])
    # inputs = dict
    # outputs = N4BiasFieldCorrectionOutputSpec

    # inputs with paths: input_image
    # outputs with paths: output_image, bias_image

    if not isinstance(result.outputs.output_image, _Undefined):
        result.outputs.output_image = Path(
            result.outputs.output_image.replace("/baseline", prefix)
        )
    if not isinstance(result.outputs.bias_image, _Undefined):
        result.outputs.bias_image = Path(result.outputs.bias_image.replace("/baseline", prefix))

    return {
        "inputs": result.inputs,
        "outputs": {
            "output_image": result.outputs.output_image,
            "bias_image": result.outputs.bias_image,
        },
    }
