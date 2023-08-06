import numbers
import warnings
from copy import deepcopy
from abc import ABC, abstractmethod

import torch
import SimpleITK as sitk

from ..utils import is_image_dict, nib_to_sitk, sitk_to_nib
from .. import TypeData, TYPE


class Transform(ABC):
    """Abstract class for all TorchIO transforms.

    All classes used to transform a sample from an
    :py:class:`~torchio.ImagesDataset` should subclass it.
    All subclasses should overwrite
    :py:meth:`torchio.tranforms.Transform.apply_transform`,
    which takes a sample, applies some transformation and returns the result.

    Args:
        p: Probability that this transform will be applied.
    """
    def __init__(self, p: float = 1):
        self.probability = self.parse_probability(p)

    def __call__(self, sample: dict):
        """Transform a sample and return the result."""
        self.parse_sample(sample)
        if torch.rand(1).item() > self.probability:
            return sample
        sample = deepcopy(sample)
        sample = self.apply_transform(sample)
        return sample

    @abstractmethod
    def apply_transform(self, sample: dict):
        raise NotImplementedError

    @staticmethod
    def parse_probability(probability: float) -> float:
        is_number = isinstance(probability, numbers.Number)
        if not (is_number and 0 <= probability <= 1):
            message = (
                'Probability must be a number in [0, 1],'
                f' not {probability}'
            )
            raise ValueError(message)
        return probability

    @staticmethod
    def parse_sample(sample: dict) -> None:
        images_found = False
        type_in_dict = False
        for image_dict in sample.values():
            if not is_image_dict(image_dict):
                continue
            images_found = True
            if TYPE in image_dict:
                type_in_dict = True
            if images_found and type_in_dict:
                break
        if not images_found:
            warnings.warn(
                'No image dicts found in sample.'
                f' Sample keys: {sample.keys()}'
            )

    @staticmethod
    def nib_to_sitk(data: TypeData, affine: TypeData):
        return nib_to_sitk(data, affine)

    @staticmethod
    def sitk_to_nib(image: sitk.Image):
        return sitk_to_nib(image)
