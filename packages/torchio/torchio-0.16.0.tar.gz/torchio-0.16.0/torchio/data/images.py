import warnings
import collections
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Sequence,
    Optional,
    Callable,
)
import torch
from torch.utils.data import Dataset
import numpy as np
from ..utils import get_stem
from ..torchio import DATA, AFFINE, TYPE, PATH, STEM, TypePath
from .io import read_image, write_image


class Image:
    r"""Class to store information about an image.

    Args:
        path: Path to a file that can be read by
            :mod:`SimpleITK` or :mod:`nibabel` or to a directory containing
            DICOM files.
        type_: Type of image, such as :attr:`torchio.INTENSITY` or
            :attr:`torchio.LABEL`. This will be used by the transforms to
            decide whether to apply an operation, or which interpolation to use
            when resampling.
        **kwargs: Items that will be added to image dictionary within the
            subject sample.
    """

    def __init__(self, path: TypePath, type_: str, **kwargs):
        self.path = self._parse_path(path)
        self.type = type_
        self.__dict__.update(kwargs)

    @staticmethod
    def _parse_path(path: TypePath) -> Path:
        try:
            path = Path(path).expanduser()
        except TypeError:
            message = f'Conversion to path not possible for variable: {path}'
            raise TypeError(message)
        if not (path.is_file() or path.is_dir()):  # might be a dir with DICOM
            raise FileNotFoundError(f'File not found: {path}')
        return path

    def load(self, check_nans: bool = True) -> Tuple[torch.Tensor, np.ndarray]:
        r"""Load the image from disk.

        The file is expected to be monomodal and 3D. A channels dimension is
        added to the tensor.

        Args:
            check_nans: If ``True``, issues a warning if NaNs are found
                in the image

        Returns:
            Tuple containing a 4D data tensor of size
            :math:`(1, D_{in}, H_{in}, W_{in})`
            and a 2D 4x4 affine matrix
        """
        tensor, affine = read_image(self.path)
        tensor = tensor.unsqueeze(0)  # add channels dimension
        if check_nans and torch.isnan(tensor).any():
            warnings.warn(f'NaNs found in file "{self.path}"')
        return tensor, affine


class Subject(dict):
    """Class to store information about the images corresponding to a subject.

    Args:
        *args: If provided, a dictionary of items.
        **kwargs: Items that will be added to the subject sample.

    Example:

        >>> import torchio
        >>> from torchio import Image, Subject
        >>> # One way:
        >>> subject = Subject(
        ...     one_image=Image('path_to_image.nii.gz, torchio.INTENSITY),
        ...     a_segmentation=Image('path_to_seg.nii.gz, torchio.LABEL),
        ...     age=45,
        ...     name='John Doe',
        ...     hospital='Hospital Juan Negrín',
        ... )
        >>> # If you want to create the mapping before, or have spaces in the keys:
        >>> subject_dict = {
        ...     'one image': Image('path_to_image.nii.gz, torchio.INTENSITY),
        ...     'a segmentation': Image('path_to_seg.nii.gz, torchio.LABEL),
        ...     'age': 45,
        ...     'name': 'John Doe',
        ...     'hospital': 'Hospital Juan Negrín',
        ... }
        >>> Subject(subject_dict)

    """

    def __init__(self, *args, **kwargs: Dict[str, Any]):
        if args:
            if len(args) == 1 and isinstance(args[0], dict):
                kwargs.update(args[0])
            else:
                message = (
                    'Only one dictionary as positional argument is allowed')
                raise ValueError(message)
        super().__init__(**kwargs)
        self.images = [
            (k, v) for (k, v) in self.items()
            if isinstance(v, Image)
        ]
        self._parse_images(self.images)

    def __repr__(self):
        string = (
            f'{self.__class__.__name__}'
            f'(Keys: {tuple(self.keys())}; images: {len(self.images)})'
        )
        return string

    @staticmethod
    def _parse_images(images: List[Tuple[str, Image]]) -> None:
        # Check that it's not empty
        if not images:
            raise ValueError('A subject without images cannot be created')


class ImagesDataset(Dataset):
    """Base TorchIO dataset.

    :class:`~torchio.data.images.ImagesDataset`
    is a reader of 3D medical images that directly
    inherits from :class:`torch.utils.data.Dataset`.
    It can be used with a :class:`torch.utils.data.DataLoader`
    for efficient loading and augmentation.
    It receives a list of subjects, where each subject is an instance of
    :class:`~torchio.data.images.Subject` containing instances of
    :class:`~torchio.data.images.Image`.
    The file format must be compatible with `NiBabel`_ or `SimpleITK`_ readers.
    It can also be a directory containing
    `DICOM`_ files.

    Indexing an :class:`~torchio.data.images.ImagesDataset` returns a
    Python dictionary with the data corresponding to the queried subject.
    The keys in the dictionary are the names of the images passed to that
    subject, for example ``('t1', 't2', 'segmentation')``.

    The value corresponding to each image name is another dictionary
    ``image_dict`` with information about the image.
    The data is stored in ``image_dict[torchio.IMAGE]``,
    and the corresponding `affine matrix`_
    is in ``image_dict[torchio.AFFINE]``:

        >>> sample = images_dataset[0]
        >>> sample.keys()
        dict_keys(['image', 'label'])
        >>> image_dict = sample['image']
        >>> image_dict[torchio.DATA].shape
        torch.Size([1, 176, 256, 256])
        >>> image_dict[torchio.AFFINE]
        array([[   0.03,    1.13,   -0.08,  -88.54],
               [   0.06,    0.08,    0.95, -129.66],
               [   1.18,   -0.06,   -0.11,  -67.15],
               [   0.  ,    0.  ,    0.  ,    1.  ]])

    Args:
        subjects: Sequence of instances of
            :class:`~torchio.data.images.Subject`.
        transform: An instance of :py:class:`torchio.transforms.Transform`
            that will be applied to each sample.
        check_nans: If ``True``, issues a warning if NaNs are found
            in the image.
        load_image_data: If ``False``, image data and affine will not be loaded.
            These fields will be set to ``None`` in the sample. This can be
            used to quickly iterate over the samples to retrieve e.g. the
            images paths. If ``True``, transform must be ``None``.

    .. _NiBabel: https://nipy.org/nibabel/#nibabel
    .. _SimpleITK: https://itk.org/Wiki/ITK/FAQ#What_3D_file_formats_can_ITK_import_and_export.3F
    .. _DICOM: https://www.dicomstandard.org/
    .. _affine matrix: https://nipy.org/nibabel/coordinate_systems.html

    """

    def __init__(
            self,
            subjects: Sequence[Subject],
            transform: Optional[Callable] = None,
            check_nans: bool = True,
            load_image_data: bool = True,
            ):
        self._parse_subjects_list(subjects)
        self.subjects = subjects
        self._transform: Optional[Callable]
        self.set_transform(transform)
        self.check_nans = check_nans
        self._load_image_data: bool
        self.set_load_image_data(load_image_data)

    def __len__(self):
        return len(self.subjects)

    def __getitem__(self, index: int) -> dict:
        if not isinstance(index, int):
            raise ValueError(f'Index "{index}" must be int, not {type(index)}')
        subject = self.subjects[index]
        sample = self.get_sample_dict_from_subject(subject)

        # Apply transform (this is usually the bottleneck)
        if self._transform is not None:
            sample = self._transform(sample)
        return sample

    def get_sample_dict_from_subject(self, subject: Subject):
        """Create a dictionary of dictionaries with subject information.

        Args:
            subject: Instance of :py:class:`~torchio.data.images.Subject`.
        """
        subject_sample = {}
        for (key, value) in subject.items():
            if isinstance(value, Image):
                subject_sample[key] = self.get_image_dict_from_image(value)
            else:
                subject_sample[key] = value
        return subject_sample

    def get_image_dict_from_image(self, image: Image):
        """Create a dictionary with image information.

        Args:
            image: Instance of :py:class:`~torchio.data.images.Image`.

        Return:
            Dictionary with keys
            :py:attr:`torchio.DATA`,
            :py:attr:`torchio.AFFINE`,
            :py:attr:`torchio.TYPE`,
            :py:attr:`torchio.PATH` and
            :py:attr:`torchio.STEM`.
        """
        if self._load_image_data:
            tensor, affine = image.load(check_nans=self.check_nans)
        else:
            tensor = affine = None
        image_dict = {
            DATA: tensor,
            AFFINE: affine,
            TYPE: image.type,
            PATH: str(image.path),
            STEM: get_stem(image.path),
        }
        return image_dict

    def set_transform(self, transform: Optional[Callable]) -> None:
        """Set the :attr:`transform` attribute.

        Args:
            transform: An instance of :py:class:`torchio.transforms.Transform`.
        """
        if transform is not None and not callable(transform):
            raise ValueError(
                f'The transform must be a callable object, not {transform}')
        self._transform = transform

    @staticmethod
    def _parse_subjects_list(subjects_list: Sequence[Subject]) -> None:
        # Check that it's list or tuple
        if not isinstance(subjects_list, collections.abc.Sequence):
            raise TypeError(
                f'Subject list must be a sequence, not {type(subjects_list)}')

        # Check that it's not empty
        if not subjects_list:
            raise ValueError('Subjects list is empty')

        # Check each element
        for subject in subjects_list:
            if not isinstance(subject, Subject):
                message = (
                    'Subjects list must contain instances of torchio.Subject,'
                    f' not "{type(subject)}"'
                )
                raise TypeError(message)

    @classmethod
    def save_sample(
            cls,
            sample: Dict[str, dict],
            output_paths_dict: Dict[str, TypePath],
            ) -> None:
        for key, output_path in output_paths_dict.items():
            tensor = sample[key][DATA][0]  # remove channels dim
            affine = sample[key][AFFINE]
            write_image(tensor, affine, output_path)

    def set_load_image_data(self, load_image_data: bool):
        if not load_image_data and self._transform is not None:
            message = (
                'Load data cannot be set to False if transform is not None.'
                f'Current transform is {self._transform}')
            raise ValueError(message)
        self._load_image_data = load_image_data
