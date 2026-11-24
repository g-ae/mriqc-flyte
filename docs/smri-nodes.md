# sMRI node table (anatMRIQC)
Only <mark>MapNode</mark> is `ComputeIQMs.tpms_std2t1w`

## Start
|Sub-workflow|Node name|Interface class|Package|External program|Inputs|
|---|---|---|---|---|---|
|-|inputnode|<mark>IdentityInterface</mark>|nipype|-|-|
|-|conform|ConformImage|mriqc|-|inputnode|

## SynthStrip
|Sub-workflow|Node name|Interface class|Package|External program|Inputs|
|---|---|---|---|---|---|
|synthstrip_wf|inputnode|<mark>IdentityInterface</mark>|nipype|-|conform|
|synthstrip_wf|pre_clip|IntensityClip|niworkflows|-|synthstrip_wf.inputnode|
|synthstrip_wf|pre_n4|N4BiasFieldCorrection|nipype|N4BiasFieldCorrection|synthstrip_wf.pre_clip|
|synthstrip_wf|synthstrip|SynthStrip|mriqc|synthstrip|synthstrip_wf.pre_n4|
|synthstrip_wf|post_n4|N4BiasFieldCorrection|nipype|N4BiasFieldCorrection|synthstrip_wf.pre_clip, synthstrip_wf.synthstrip|
|synthstrip_wf|final_masked|ApplyMask|niworkflows|-|synthstrip_wf.synthstrip, synthstrip_wf.post_n4|
|synthstrip_wf|outputnode|<mark>IdentityInterface</mark>|nipype|-|synthstrip_wf.synthstrip, synthstrip_wf.final_masked, synthstrip_wf.post_n4|

## SpatialNormalization
|Sub-workflow|Node name|Interface class|Package|External program|Inputs|
|---|---|---|---|---|---|
|SpatialNormalization|inputnode|<mark>IdentityInterface</mark>|nipype|-|synthstrip_wf.outputnode, inputnode|
|SpatialNormalization|SpatialNormalization|SpatialNormalizationRPT|niworkflows|-|SpatialNormalization.inputnode|
|SpatialNormalization|tpms_std2t1w|FixHeaderApplyTransforms|niworkflows|-|SpatialNormalization.SpatialNormalization|
|SpatialNormalization|outputnode|<mark>IdentityInterface</mark>|nipype|-|SpatialNormalization.SpatialNormalization, SpatialNormalization.tpms_std2t1w|

## HeadMaskWorkflow
|Sub-workflow|Node name|Interface class|Package|External program|Inputs|
|---|---|---|---|---|---|
|HeadMaskWorkflow|inputnode|<mark>IdentityInterface</mark>|nipype|-|synthstrip_wf.outputnode, SpatialNormalization.outputnode|
|HeadMaskWorkflow|Enhance|<mark>Function</mark>|mriqc|-|HeadMaskWorkflow.inputnode|
|HeadMaskWorkflow|Grad|<mark>Function</mark>|mriqc|-|HeadMaskWorkflow.inputnode, HeadMaskWorkflow.Enhance|
|HeadMaskWorkflow|GradientThreshold|<mark>Function</mark>|mriqc|-|HeadMaskWorkflow.inputnode, HeadMaskWorkflow.Grad|
|HeadMaskWorkflow|apply_mask|ApplyMask|niworkflows|-|HeadMaskWorkflow.inputnode, HeadMaskWorkflow.Enhance|
|HeadMaskWorkflow|outputnode|<mark>IdentityInterface</mark>|nipype|-|HeadMaskWorkflow.GradientThreshold, HeadMaskWorkflow.apply_mask|

## AirMaskWorkflow
|Sub-workflow|Node name|Interface class|Package|External program|Inputs|
|---|---|---|---|---|---|
|AirMaskWorkflow|inputnode|<mark>IdentityInterface</mark>|nipype|-|conform, synthstrip_wf.outputnode, HeadMaskWorkflow.outputnode, SpatialNormalization.outputnode|
|AirMaskWorkflow|RotationMask|RotationMask|mriqc|-|AirMaskWorkflow.inputnode|
|AirMaskWorkflow|ArtifactMask|ArtifactMask|mriqc|-|AirMaskWorkflow.inputnode|
|AirMaskWorkflow|outputnode|<mark>IdentityInterface</mark>|nipype|-|AirMaskWorkflow.RotationMask, AirMaskWorkflow.ArtifactMask|

## brain_tissue_segmentation
|Sub-workflow|Node name|Interface class|Package|External program|Inputs|
|---|---|---|---|---|---|
|brain_tissue_segmentation|inputnode|<mark>IdentityInterface</mark>|nipype|-|synthstrip_wf.outputnode, SpatialNormalization.outputnode, HeadMaskWorkflow.outputnode|
|brain_tissue_segmentation|format_tpm_names|<mark>Function</mark>|mriqc|-|brain_tissue_segmentation.inputnode|
|brain_tissue_segmentation|segmentation|Atropos|nipype|Atropos|brain_tissue_segmentation.inputnode, brain_tissue_segmentation.format_tpm_names|
|brain_tissue_segmentation|outputnode|<mark>IdentityInterface</mark>|nipype|-|brain_tissue_segmentation.segmentation|

## ComputeIQMs
|Sub-workflow|Node name|Interface class|Package|External program|Inputs|
|---|---|---|---|---|---|
|ComputeIQMs|inputnode|<mark>IdentityInterface</mark>|nipype|-|inputnode, conform, synthstrip_wf.outputnode, SpatialNormalization.outputnode, brain_tissue_segmentation.outputnode, HeadMaskWorkflow.outputnode, AirMaskWorkflow.outputnode|
|ComputeIQMs|provenance|AddProvenance|mriqc|-|ComputeIQMs.inputnode|
|ComputeIQMs|smoothness|FWHMx|nipype|afni|ComputeIQMs.inputnode|
|ComputeIQMs|harmonize|Harmonize|mriqc|-|ComputeIQMs.inputnode|
|ComputeIQMs|ComputeQI2|ComputeQI2|mriqc|-|ComputeIQMs.inputnode|
|ComputeIQMs|measures|StructuralQC|mriqc|-|ComputeIQMs.inputnode, ComputeIQMs.smoothness, ComputeIQMs.harmonize|
|ComputeIQMs|datasink|IQMFileSink|mriqc|-|ComputeIQMs.inputnode, ComputeIQMs.provenance, ComputeIQMs.ComputeQI2, ComputeIQMs.measures|
|ComputeIQMs|outputnode|<mark>IdentityInterface</mark>|nipype|-|ComputeIQMs.ComputeQI2, ComputeIQMs.datasink|

## anat_report_wf
|Sub-workflow|Node name|Interface class|Package|External program|Inputs|
|---|---|---|---|---|---|
|anat_report_wf|inputnode|<mark>IdentityInterface</mark>|nipype|-|inputnode, conform, synthstrip.outputnode, SpatialNormalization.outputnode, brain_tissue_segmentation.outputnode, HeadMaskWorkflow.outputnode, AirMaskWorkflow.outputnode, ComputeIQMs.outputnode.outputnode|
|anat_report_wf|PlotMosaicZoomed|PlotMosaic|nireports|-|anat_report_wf.inputnode|
|anat_report_wf|PlotMosaicNoise|PlotMosaic|nireports|-|anat_report_wf.inputnode|
|anat_report_wf|ds_report_zoomed|DerivativesDataSink|mriqc|-|anat_report_wf.inputnode, anat_report_wf.PlotMosaicZoomed|
|anat_report_wf|ds_report_background|DerivativesDataSink|mriqc|-|anat_report_wf.inputnode, anat_report_wf.PlotMosaicNoise|

## End
|Sub-workflow|Node name|Interface class|Package|External program|Inputs|
|---|---|---|---|---|---|
|-|outputnode|<mark>IdentityInterface</mark>|nipype|-|ComputeIQMs.outputnode|