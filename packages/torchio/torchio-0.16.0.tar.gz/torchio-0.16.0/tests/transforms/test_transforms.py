#!/usr/bin/env python

import numpy as np
from torchio import INTENSITY
from torchio.transforms import (
    Lambda,
    RandomFlip,
    RandomBlur,
    RandomSwap,
    RandomNoise,
    RandomBiasField,
    RandomElasticDeformation,
    RandomAffine,
    RandomMotion,
    RandomSpike,
    RandomGhosting,
    RescaleIntensity,
    Resample,
    ZNormalization,
    HistogramStandardization,
    Pad,
    Crop,
    ToCanonical,
    CropOrPad,
    OneOf,
    Compose,
)
from ..utils import TorchioTestCase


class TestTransforms(TorchioTestCase):
    """Tests for all transforms."""

    def test_transforms(self):
        landmarks_dict = dict(
            t1=np.linspace(0, 100, 13),
            t2=np.linspace(0, 100, 13),
        )
        transforms = (
            CropOrPad((9, 21, 30)),
            ToCanonical(),
            Resample((1, 1.1, 1.25)),
            RandomFlip(axes=(0, 1, 2), flip_probability=1),
            RandomMotion(),
            RandomGhosting(axes=(0, 1, 2)),
            RandomSpike(),
            RandomNoise(),
            RandomBlur(),
            RandomSwap(patch_size=2, num_iterations=5),
            Lambda(lambda x: 1.5 * x, types_to_apply=INTENSITY),
            RandomBiasField(),
            RescaleIntensity((0, 1)),
            ZNormalization(masking_method='label'),
            HistogramStandardization(landmarks_dict=landmarks_dict),
            RandomElasticDeformation(max_displacement=1),
            RandomAffine(),
            OneOf({RandomAffine(): 3, RandomElasticDeformation(): 1}),
            Pad((1, 2, 3, 0, 5, 6), padding_mode='constant', fill=3),
            Crop((3, 2, 8, 0, 1, 4)),
        )
        transform = Compose(transforms)
        transformed = transform(self.sample)
