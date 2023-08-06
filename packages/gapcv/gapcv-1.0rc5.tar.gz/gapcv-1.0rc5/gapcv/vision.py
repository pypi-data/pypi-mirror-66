"""
Copyright(c), Google, LLC (Andrew Ferlitsch)
Copyright(c), Virtualdvid (David Molina)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import ast
import csv
import datetime
import gc
import hashlib
import json
import multiprocessing as mp
import os
import random
import threading
import time
from typing import List, Tuple

import cv2
import h5py
import imutils
import numpy as np
import requests
from tqdm import tqdm

# Import pillow for Python image manipulation for GIF and JP2K
from PIL import Image as PILImage


NORMAL_POS = 0
NORMAL_ZERO = 1
NORMAL_STD = 2
GRAYSCALE = cv2.IMREAD_GRAYSCALE
COLOR = cv2.IMREAD_COLOR

class BareMetal(object):
    """ Data Preprocessing of Images
    """

    ## Utils
    def _final_transformation_of_pixels(self, collections, counts, labels, option=True):
        # perform final transformations of pixels in the collection
        _labels = []
        _collections = []
        for key in collections:
            # empty collection
            if not counts[key]:
                continue
            if not self._stream and collections[key]:
                _collections.append(self._pixel_transform(collections[key]))
            else:
                _collections.append(np.asarray([]))
            if option:
                _labels.append(np.asarray(labels[key][:counts[key]]))
            else:
                _labels.append(np.asarray([labels[key] for _ in range(counts[key])]))
        return _labels, _collections

    def _load_dataset(self):
        """Load a dataset

        Returns:
            collections {list[np.ndarray]} -- list of images
            labels (list[int]) -- list of labels
            classes {list[str]} -- list of classes
            errors {str} -- exception
            elapsed {float} -- time elapsed
        """

        # Create the HDF5 file
        if self._store:
            self._create_hdf5()
        # no storage
        else:
            self._hf = None

        # dataset is in memory
        if isinstance(self._dataset, np.ndarray):
            collections, labels, classes, errors, elapsed = self._load_memory()
        elif isinstance(self._dataset, list):
            # non-empty dataset
            if self._dataset:
                # dataset is in memory
                if isinstance(self._dataset[0], np.ndarray):
                    collections, labels, classes, errors, elapsed = self._load_memory()
                # load from in-memory list
                else:
                    collections, labels, classes, errors, elapsed = self._load_list()
            else:
                collections = []
                labels = []
                classes = []
                errors = []
                elapsed = 0
        # load from CSV file
        elif self._dataset.endswith('.csv'):
            if self._dataset.startswith(('http://', 'https://')):
                response = requests.get(self._dataset, timeout=10, stream=True)
                if response.status_code == 200:
                    self._response_decoded = response.iter_lines(decode_unicode=True)
                    self._remote = True
                else:
                    raise OSError('CSV file not found at url location: {}'.format(self._dataset))
            elif not os.path.exists(self._dataset):
                raise OSError('CSV file does not exist: {}'.format(self._dataset))
            collections, labels, classes, errors, elapsed = self._load_csv()
        # load from json file
        elif self._dataset.endswith('.json'):
            if self._dataset.startswith(('http://', 'https://')):
                response = requests.get(self._dataset, timeout=10, stream=True)
                if response.status_code == 200:
                    self._response_decoded = response.iter_lines(decode_unicode=True)
                    self._remote = True
                else:
                    raise OSError('JSON file not found at url location: {}'.format(self._dataset))
            elif not os.path.exists(self._dataset):
                raise OSError('JSON file does not exist: {}'.format(self._dataset))
            collections, labels, classes, errors, elapsed = self._load_json()
        # load from directory
        else:
            if not os.path.isdir(self._dataset):
                raise OSError('Directory does not exist: {}'.format(self._dataset))

            if self._stream_ff:
                collections, labels, classes, errors, elapsed = self._load_directory_streaming(
                    self._dataset
                )
            else:
                collections, labels, classes, errors, elapsed = self._load_directory()

        if self._store:
            self._classes = classes
            self._errors = errors
            self._time = elapsed
            self._end_hdf5()

        # tell garbage collector to free any unused memory
        gc.collect()

        return collections, labels, classes, errors, elapsed

    def _load_directory(self):
        """ Load a Directory based dataset, where the toplevel subdirectories are the classes.

        Returns:
            collections {list[np.ndarray], None} -- list of images or None if streaming
            labels (list[int]) -- list of labels
            classes {list[str]} -- list of classes
            errors {str} -- exception
            elapsed {float} -- time elapsed
        """

        collections = []
        labels = []
        classes = {}
        errors = []
        total_elapsed = 0
        n_label = 0
        dset = None
        pool = None

        self._count = 0

        # Get the list (generator) of the subdirectories of the parent directory of the dataset
        subdirs = sorted(os.scandir(self._dataset), key=lambda e: e.name)
        cwd = os.getcwd()
        os.chdir(self._dataset)

        # concurrent processing of subdirectories of images
        if self._mp > 1:
            pool = mp.Pool(self._mp)
            results = []

        with tqdm(subdirs, postfix='Getting ready...', disable=self._disable) as pbar:
            for subdir in pbar:
                # skip entries that are not subdirectories or hidden directories (start with dot)
                if not subdir.is_dir() or subdir.name.startswith(('.', '_')):
                    continue
                files = os.listdir(subdir.name)
                if not files:
                    continue

                classes[subdir.name] = n_label

                pbar.postfix = 'Processing label: {}'.format(subdir.name)

                if pool:
                    results.append(
                        pool.apply_async(
                            self._pool_directory,
                            (subdir.name, files, n_label)
                        )
                    )
                else:
                    os.chdir(subdir.name)
                    if self._stream:
                        dset = self._init_stream_hdf5(subdir.name, len(files))

                    collection, names, types, sizes, shapes, errors, elapsed = self._load_images(files, dset)

                    if not self._stream:
                        # Accumulate the collections
                        collections.append(collection)
                        # Accumulate the labels
                        label_acum = len(collection)
                        labels.append(np.asarray([n_label for _ in range(label_acum)]))
                        self._count += label_acum
                    else:
                        self._count += len(files) - len(errors)

                    # Write collection to HDF5 storage
                    if self._store:
                        self._write_group_hdf5(
                            subdir.name,
                            collection,
                            n_label,
                            elapsed,
                            names,
                            types,
                            sizes,
                            shapes,
                            dset
                        )

                    # maintain total time to process
                    total_elapsed += elapsed
                    os.chdir('..')

                # increment the mapping of class name to label
                n_label += 1

        os.chdir(cwd)

        if pool:
            pool.close()
            pool.join()
            for result in results:
                params = result.get()
                collections.append(params[0])
                errors.append(params[5])
                n_label = params[7]
                label_params = len(params[0])
                labels.append(np.asarray([n_label for _ in range(label_params)]))
                self._count += label_params
                total_elapsed += int(params[6])

        if self._stream:
            collections = None

        return collections, labels, classes, errors, total_elapsed

    def _load_directory_streaming(self, dataset: str):
        """ Loads images from a directory

        Arguments:
            dataset {str} -- directory path

        Returns:
            collections {list[np.ndarray]} -- list of images
            labels (list[int]) -- list of labels
            classes {list[str]} -- list of classes
            errors {None} -- exception
            elapsed {None} -- time elapsed
        """

        collection = []
        labels = []
        classes = {}

        self._image_label = []

        for i, folder in enumerate(os.scandir(dataset)):
            if folder.is_dir() or not folder.name.startswith(('.', '_')):
                classes[folder.name] = i
                for image in os.scandir(folder.path):
                    collection.append(image.path)
                    labels.append(i)
                    self._image_label.append((image.path, i))

        return collection, labels, classes, None, None

    def _pool_directory(self, subdir, files, n_label):
        """ Work in Progress """

        dset = None
        if self._stream:
            dset = self._init_stream_hdf5(subdir, len(files))

        os.chdir(subdir)
        collection, names, types, sizes, shapes, errors, elapsed = self._load_images(files, dset)

        label = None
        if not self._stream:
            # Accumulate the labels
            label_acum = len(collection)
            label = np.asarray([n_label for _ in range(label_acum)])

        # Write collection to HDF5 storage
        if self._store:
            self._write_group_hdf5(
                subdir,
                collection,
                n_label,
                elapsed,
                names,
                types,
                sizes,
                shapes,
                dset
            )

        os.chdir('../')
        return collection, names, types, sizes, shapes, errors, elapsed, label

    def _load_memory(self):
        """load a dataset from in-memory

        Returns:
            _collections {list[np.ndarray], None} -- list of images or None if streaming
            _labels (list[int]) -- list of labels
            classes {list[str]} -- list of classes
            errors {str} -- exception
            elapsed {float} -- time elapsed
        """

        start_time = time.time()

        errors = []
        collections, labels, classes, counts, names, types, sizes, shapes, dset, d_index = self._init_labels()

        with tqdm(self._dataset, postfix='Getting ready...', disable=self._disable) as pbar:
            for index, image in enumerate(pbar):
                label = self._labels[index]

                pbar.postfix = 'Processing: {}'.format(label)

                # load image from remote location
                image, shape, size, name, _type, error = self._load_image_memory(image)

                if image is not None:
                    if self._stream:
                        d_index[label] = self._pixel_transform_stream(
                            image,
                            dset[label],
                            d_index[label]
                        )
                    else:
                        # append each in-memory image into a list
                        collections[label].append(image)

                    # append the metadata for each image into a list
                    names[label].append(bytes(name, 'utf-8'))
                    types[label].append(bytes(_type, 'utf-8'))
                    sizes[label].append(size)
                    shapes[label].append(shape)
                else:
                    errors.append(error)
                    counts[label] -= 1

        # perform final transformations of pixels in the collection
        _labels, _collections = self._final_transformation_of_pixels(
            collections,
            counts,
            labels
        )

        elapsed = time.time() - start_time

        # Write collection to HDF5 storage
        if self._store:
            # Create dataset group
            for i, collection in enumerate(_collections):
                n_label = _labels[i][0]
                if n_label not in dset:
                    label = list(classes.keys())[list(classes.values()).index(n_label)]
                else:
                    label = n_label
                self._write_group_hdf5(
                    str(label),
                    collection,
                    n_label,
                    elapsed,
                    names[label],
                    types[label],
                    sizes[label],
                    shapes[label],
                    dset[label]
                )

        # subtract final count of images the number that did not process
        self._count -= len(errors)

        if self._stream:
            _collections = None
        return  _collections, _labels, classes, errors, elapsed

    def _load_list(self):
        """ Read a dataset from in-memory

        Returns:
            _collections {list[np.ndarray], None} -- list of images or None if streaming
            _labels (list[int]) -- list of labels
            classes {list[str]} -- list of classes
            errors {str} -- exception
            elapsed {float} -- time elapsed
        """

        start_time = time.time()

        verbosity_nparray = False
        if isinstance(self._dataset[0], str):
            if self._dataset[0].startswith(('http:', 'https:')):
                function = self._load_image_remote
            else:
                function = self._load_image_disk
        elif isinstance(self._dataset[0], np.ndarray):
            function = self._load_image_memory
            verbosity_nparray = True

        errors = []
        collections, labels, classes, counts, names, types, sizes, shapes, dset, d_index = self._init_labels()

        with tqdm(self._dataset, postfix='Getting ready...', disable=self._disable) as pbar:
            for index, image in enumerate(pbar):
                label = self._labels[index]

                if verbosity_nparray:
                    print_image = index
                else:
                    print_image = image

                pbar.postfix = 'Processing image: {} label: {}'.format(print_image, label)

                # load image from remote location
                image, shape, size, name, _type, error = function(image)

                if image is not None:
                    if self._stream:
                        d_index[label] = self._pixel_transform_stream(
                            image,
                            dset[label],
                            d_index[label]
                        )
                    else:
                        # append each in-memory image into a list
                        collections[label].append(image)

                    # append the metadata for each image into a list
                    names[label].append(bytes(name, 'utf-8'))
                    types[label].append(bytes(_type, 'utf-8'))
                    sizes[label].append(size)
                    shapes[label].append(shape)
                else:
                    errors.append(error)
                    counts[label] -= 1

        # perform final transformations of pixels in the collection
        _labels, _collections = self._final_transformation_of_pixels(
            collections,
            counts,
            labels
        )

        elapsed = time.time() - start_time

        # Write collection to HDF5 storage
        if self._store:
            # Create dataset group
            for i, collection in enumerate(_collections):
                n_label = _labels[i][0]
                if n_label not in dset:
                    label = list(classes.keys())[list(classes.values()).index(n_label)]
                else:
                    label = n_label
                self._write_group_hdf5(
                    str(label),
                    collection,
                    n_label,
                    elapsed,
                    names[label],
                    types[label],
                    sizes[label],
                    shapes[label],
                    dset[label]
                )

        # subtract final count of images the number that did not process
        self._count -= len(errors)

        if self._stream:
            _collections = None
        return  _collections, _labels, classes, errors, elapsed

    def _load_csv(self):
        """ Read a dataset from a CSV file

        Returns:
            _collections {list[np.ndarray], None} -- list of images or None if streaming
            _labels (list[int]) -- list of labels
            classes {list[str]} -- list of classes
            errors {str} -- exception
            elapsed {float} -- time elapsed
        """

        # Argument Checks
        if self._image_col is None:
            raise AttributeError('Config setting image_col not set')
        if self._label_col is None:
            raise AttributeError('Config setting label_col not set')
        if self._image_col == self._label_col:
            raise ValueError('Image and Label column cannot be the same value')

        start_time = time.time()

        collections = {}
        labels = {}
        counts = {}
        names = {}
        types = {}
        sizes = {}
        shapes = {}
        classes = {}
        dset = {}
        d_index = {}
        errors = []
        is_memory = False

        csv.field_size_limit(100000000)

        if not self._remote:
            csvf = open(self._dataset, newline='')
            reader = csv.reader(csvf, delimiter=self._col_sep)
        else:
            reader = csv.reader(self._response_decoded)

        # check for header
        if self._header:
            try:
                next(reader)
            except:
                raise EOFError('Header expected, but CSV file is empty')

        # prepass
        self._count = 0
        first_row = True
        n_label = 0
        for row in reader:
            if first_row:
                if self._label_col >= len(row):
                    raise IndexError('Label column index not valid for CSV file')
                if self._image_col >= len(row):
                    raise IndexError('Index column index not valid for CSV file')
                first_row = False
            label = row[self._label_col]
            if label in counts:
                counts[label] += 1
            else:
                counts[label] = 1
                collections[label] = []
                names[label] = []
                types[label] = []
                sizes[label] = []
                shapes[label] = []
                labels[label] = n_label
                classes[label] = n_label
                n_label += 1
            self._count += 1

        for label in counts:
            if self._stream:
                dset[label] = self._init_stream_hdf5(str(label), counts[label])
            else:
                dset[label] = None
            d_index[label] = 0

        if not self._remote:
            # parse
            csvf.seek(0)
        else:
            response = requests.get(self._dataset, timeout=10, stream=True)
            self._response_decoded = response.iter_lines(decode_unicode=True)
            reader = csv.reader(self._response_decoded)

        if self._header:
            next(reader)

        first_row = True
        with tqdm(reader, postfix='Getting ready...', disable=self._disable) as pbar:
            for row in pbar:

                try:
                    image = row[self._image_col]
                    label = row[self._label_col]
                except Exception as error:
                    errors.append(error)
                    counts[label] -= 1
                    continue

                pbar.postfix = 'Processing image: {} label: {}'.format(image, label)

                if first_row:
                    first_row = False
                    try:
                        # load image from memory
                        ast.literal_eval(image)
                        is_memory = True
                        function = self._load_image_memory
                    except:
                        # load image from remote location
                        if image.startswith(('http:', 'https:')):
                            function = self._load_image_remote
                        else:
                            # load image from local disk
                            function = self._load_image_disk

                if is_memory:
                    image = ast.literal_eval(image)
                    image = np.asarray([np.asarray(img).astype(self._dtype) for img in image])

                image, shape, size, name, _type, error = function(image)

                # append each in-memory image into a list
                if image is not None:
                    if self._stream:
                        d_index[label] = self._pixel_transform_stream(
                            image,
                            dset[label],
                            d_index[label]
                        )
                    else:
                        # append each in-memory image into a list
                        collections[label].append(image)
                    # append the metadata for each image into a list
                    names[label].append(bytes(name, 'utf-8'))
                    types[label].append(bytes(_type, 'utf-8'))
                    sizes[label].append(size)
                    shapes[label].append(shape)
                else:
                    errors.append(error)
                    counts[label] -= 1

        if not self._remote:
            csvf.close()

        # perform final transformations of pixels in the collection
        _labels, _collections = self._final_transformation_of_pixels(
            collections,
            counts,
            labels,
            option=False
        )

        elapsed = time.time() - start_time

        # Write collection to HDF5 storage
        if self._store:
            # Create dataset group
            for i, collection in enumerate(_collections):
                n_label = _labels[i][0]
                if n_label not in dset:
                    label = list(classes.keys())[list(classes.values()).index(n_label)]
                else:
                    label = n_label
                self._write_group_hdf5(
                    str(label),
                    collection,
                    n_label,
                    elapsed,
                    names[label],
                    types[label],
                    sizes[label],
                    shapes[label],
                    dset[label]
                )

        # subtract final count of images the number that did not process
        self._count -= len(errors)

        if self._stream:
            _collections = None
        return  _collections, _labels, classes, errors, elapsed

    def _load_json(self):
        """ Read a dataset from a JSON file

        Returns:
            _collections {list[np.ndarray], None} -- list of images or None if streaming
            _labels (list[int]) -- list of labels
            classes {list[str]} -- list of classes
            errors {str} -- exception
            elapsed {float} -- time elapsed

        Format:
            [
                { image_key: image_path, label_key: label },
                { image_key: image_path, label_key: label },
            ]
        """

        # Argument Checks
        if self._image_key is None:
            raise AttributeError('Config setting image_key not set')
        if self._label_key is None:
            raise AttributeError('Config setting label_key not set')
        if self._image_key == self._label_key:
            raise ValueError('Image and Label key cannot be the same value')

        start_time = time.time()

        collections = {}
        labels = {}
        counts = {}
        names = {}
        types = {}
        sizes = {}
        shapes = {}
        classes = {}
        dset = {}
        d_index = {}
        errors = []
        is_memory = False

        if not self._remote:
            jsonf = open(self._dataset)
            try:
                data = json.load(jsonf)
            except:
                raise OSError('Invalid Format for JSON file')
        else:
            for item in self._response_decoded:
                data = json.loads(item)

        # Prepass
        first = True
        self._count = 0
        n_label = 0
        for entry in data:
            if first:
                try:
                    entry[self._label_key]
                except:
                    raise IndexError('Label key not found in JSON file')
                try:
                    image = entry[self._image_key]
                except:
                    raise IndexError('Image key not found in JSON file')

                try:
                    # load image from memory
                    ast.literal_eval(image)
                    is_memory = True
                    function = self._load_image_memory
                except:
                    # load image from remote location
                    if image.startswith(('http:', 'https:')):
                        function = self._load_image_remote
                    else:
                        # load image from local disk
                        function = self._load_image_disk
                first = False

            label = entry[self._label_key]
            if label in counts:
                counts[label] += 1
            else:
                counts[label] = 1
                collections[label] = []
                names[label] = []
                types[label] = []
                sizes[label] = []
                shapes[label] = []
                labels[label] = n_label
                classes[label] = n_label
                n_label += 1
            self._count += 1

        for label in counts:
            if self._stream:
                dset[label] = self._init_stream_hdf5(str(label), counts[label])
            else:
                dset[label] = None
            d_index[label] = 0

        with tqdm(data, postfix='Getting ready...', disable=self._disable) as pbar:
            for entry in pbar:

                image = entry[self._image_key]
                label = entry[self._label_key]

                pbar.postfix = 'Processing: image: {} label: {}'.format(image, label)

                if is_memory:
                    image = ast.literal_eval(image)
                    image = np.asarray([np.asarray(img).astype(self._dtype) for img in image])

                image, shape, size, name, _type, error = function(image)

                # append each in-memory image into a list
                if image is not None:
                    if self._stream:
                        d_index[label] = self._pixel_transform_stream(
                            image,
                            dset[label],
                            d_index[label]
                        )
                    else:
                        # append each in-memory image into a list
                        collections[label].append(image)
                    # append the metadata for each image into a list
                    names[label].append(bytes(name, 'utf-8'))
                    types[label].append(bytes(_type, 'utf-8'))
                    sizes[label].append(size)
                    shapes[label].append(shape)
                else:
                    errors.append(error)
                    counts[label] -= 1

        if not self._remote:
            jsonf.close()

        # perform final transformations of pixels in the collection
        _labels, _collections = self._final_transformation_of_pixels(
            collections,
            counts,
            labels,
            option=False
        )

        elapsed = time.time() - start_time

        # Write collection to HDF5 storage
        if self._store:
            # Create dataset group
            for i, collection in enumerate(_collections):
                n_label = _labels[i][0]
                if n_label not in dset:
                    label = list(classes.keys())[list(classes.values()).index(n_label)]
                else:
                    label = n_label
                self._write_group_hdf5(
                    str(label),
                    collection,
                    n_label,
                    elapsed,
                    names[label],
                    types[label],
                    sizes[label],
                    shapes[label],
                    dset[label]
                )

        # subtract final count of images the number that did not process
        self._count -= len(errors)

        if self._stream:
            _collections = None
        return  _collections, _labels, classes, errors, elapsed

    def _load_images(self, files, dset):
        """ Load a collection of images

        Arguments:
            files {list[strings] or numpy array of matrixes} -- list of file paths of images
                on-disk, or remote images, or in-memory images.
            dset {HDF5 handle} -- HDF5 handle to dataset

        Returns:
            tuple -- (
                machine learning ready data, image names, image types,
                image shapes, image sizes, processing errors, processing time
            )
        """

        start_time = time.time()

        collection = []
        names = []
        types = []
        sizes = []
        shapes = []
        errors = []
        d_index = 0

        # TODO is it necesary evaluate files when this funtion is just used
        # for _load_directory()?
        verbosity_nparray = False
        if isinstance(files[0], str):
            if files[0].startswith(('http:', 'https:')):
                function = self._load_image_remote
            else:
                function = self._load_image_disk
        elif isinstance(files[0], np.ndarray):
            function = self._load_image_memory
            verbosity_nparray = True

        cleaner_control = []
        with tqdm(files, postfix='Getting ready...', disable=self._disable) as pbar:
            for index, item in enumerate(pbar):
                with open(item, 'rb') as f:
                    filehash = hashlib.md5(f.read()).hexdigest()
                if filehash not in cleaner_control:
                    cleaner_control.append(filehash)
                else:
                    continue

                if verbosity_nparray:
                    print_image = index
                else:
                    print_image = item

                pbar.postfix = 'Processing image: {}'.format(print_image)

                image, shape, size, name, _type, error = function(item)

                if image is not None:
                    if self._stream:
                        d_index = self._pixel_transform_stream(image, dset, d_index)
                    else:
                        # append each in-memory image into a list
                        collection.append(image)
                    # append the metadata for each image into a list
                    names.append(bytes(name, 'utf-8'))
                    types.append(bytes(_type, 'utf-8'))
                    sizes.append(size)
                    shapes.append(shape)
                else:
                    errors.append(error)

        if not self._stream and collection:
            collection = self._pixel_transform(collection)

        elapsed = time.time() - start_time

        return collection, names, types, sizes, shapes, errors, elapsed

    def _load_image_disk(self, file: str):
        """ Loads an image from disk

        Arguments:
            file {str} -- a file path to an image

        Returns:
            numpy matrix -- a processed image (or vector if flattened)
        """

        # retain original file information
        basename = os.path.splitext(os.path.basename(file))
        name = basename[0]
        _type = basename[1][1:].lower()
        try:
            size = os.path.getsize(file)
        except Exception as error:
            return None, None, None, '', '', error

        try:
            if _type in ('gif', 'jp2', 'jpx', 'j2k'):
                image = PILImage.open(file)
                if self._colorspace == GRAYSCALE:
                    image = image.convert('L')
                else:
                    image = image.convert('RGB')
                image = np.array(image)
            elif _type in ('jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff'):
                # keep 16bpp formats as 16bpp
                if self._16bpp:
                    image = cv2.imread(file, cv2.IMREAD_UNCHANGED)
                    if self._colorspace == COLOR:
                        # convert grayscale to color
                        if image.ndim == 2:
                            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                        else:
                            image = np.asarray(image)
                    else:
                        # convert color to grayscale
                        if image.ndim == 3:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        else:
                            image = np.asarray(image)
                # 8bpp
                else:
                    image = cv2.imread(file, self._colorspace)
            else:
                return None, None, None, '', '', 'Not a supported type: {}'.format(_type)

            # retain the original shape
            shape = image.shape

        except Exception as error:
            return None, None, None, '', '', error

        if self._stream_ff:
            return image
        else:
            return image, shape, size, name, _type, None

    def _load_image_remote(self, url: str):
        """Loads an image from a remote location

        Arguments:
            url {str} -- url where the image is stored

        Returns:
            image {np.ndarray} -- image loaded
            shape {tuple} -- (width, height)
            size {int} -- image size on Disk
            name {str} -- image name
            _type = {str} -- image extension
            {exception, None} -- error raised
        """

        try:
            response = requests.get(url, timeout=10)
        except Exception as error:
            return None, None, None, '', '', error

        # read in the image data
        data = np.frombuffer(response.content, np.uint8)
        # retain the original size
        size = len(data)
        # retain original image information
        temp_img_name = url.split('/')[-1]
        basename = os.path.splitext(temp_img_name)
        name = basename[0]
        _type = basename[1][1:].lower()

        # decode the image
        try:
            image = cv2.imdecode(data, self._colorspace)
        except Exception as error:
            return None, None, None, '', '', error

        # retain the original shape
        shape = image.shape

        return image, shape, size, name, _type, None

    def _load_image_memory(self, image: np.ndarray):
        """ Loads an image from memory

        Arguments:
            image {np.ndarray} -- image loaded in memory

        Returns:
            image {np.ndarray} -- image loaded
            shape {tuple} -- (width, height)
            size {int} -- image size on Disk
            name {str} -- image name
            _type = {str} -- image extension
            {exception, None} -- error raised
        """

        # retain the original shape
        try:
            shape = image.shape
        except Exception as error:
            return None, None, None, '', '', error

        # retain original image information
        name = ''
        _type = ''
        # assume each element is a float32
        size = shape[0] * 4
        if image.ndim > 1:
            size *= shape[1] * 4
        if image.ndim > 2:
            size *= shape[2] * 4

        # Special Case: Image already flattened
        if image.ndim == 1:
            return image, shape, size, name, _type, None

        try:
            #  Grayscale conversion
            if self._colorspace == GRAYSCALE:
                # single channel (assume grayscale)
                if image.ndim != 2:
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            # Color Conversion
            elif self._colorspace == COLOR:
                if image.ndim != 3:
                    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        except Exception as error:
            return None, None, None, '', '', error

        return image, shape, size, name, _type, None

    def _pixel_transform(self, collection):
        """ Perform pixel transformations across collection.

        Arguments:
            collection {list} -- A collection of partially preprocessed images

        Returns:
            collection {
                list[np.ndarray],
                np.ndarray,
                None
            } -- list of images, image or None if streaming
        """

        try:
            if self._flatten:
                # flatten into 1D vector and resize
                collection = [cv2.resize(
                    image,
                    self._resize,
                    interpolation=cv2.INTER_AREA
                ).flatten() for image in collection]
            else:
                # resize each image to the target size (e.g., 50x50)
                collection = [self._gray_expand_dim(
                    cv2.resize(
                        image,
                        self._resize,
                        interpolation=cv2.INTER_AREA
                    )
                ) for image in collection]
        except:
            return None

        # calculate the bits per pixel of the original data
        bpp = collection[0].itemsize * 8

        # once the collection is assembled, convert the list to a multi-dimensional numpy array
        collection = np.asarray(collection).astype(self._dtype)

        return self._pixel_normalize(collection, bpp)

    def _pixel_transform_stream(self, image, dset, index: int):
        """Perform pixel transformations for single image which is then streamed into storage

        Arguments:
            image {np.ndarray} -- image to resize
            dset {class} -- HDF5 handle to dataset
            index {int} -- index in sequence

        Returns:
            {np.ndarray, int) -- an image or an index
        """

        try:
            if self._flatten:
                # flatten into 1D vector
                image = cv2.resize(
                    image,
                    self._resize,
                    interpolation=cv2.INTER_AREA
                ).flatten()
            else:
                # resize each image to the target size (e.g., 50x50)
                image = cv2.resize(
                    image,
                    self._resize,
                    interpolation=cv2.INTER_AREA
                )
        except:
            return None

        image = self._gray_expand_dim(image)

        # calculate the bits per pixel of the original data
        bpp = image.itemsize * 8

        image = self._pixel_normalize(image.astype(self._dtype), bpp)

        if self._stream_ff:
            return image
        else:
            # load image array into dataset
            dset[index, :] = image
            return index + 1

    def _pixel_normalize(self, image_or_collection, bpp: int):
        """Normalize collection or image

        Arguments:
            image_or_collection {
                np.ndarray,
                list
            } -- the collection or image to normalize in np.ndarray
            bpp {int} -- bits per pixel

        Returns:
            {np.ndarray, list} -- image or normalized collection
        """

        # Do not normalize if requesting to keep data in original integer bits per pixel (bpp)
        if self._dtype not in (np.uint8, np.int8, np.uint16, np.int16):
            # original pixel data is 8 bits per pixel
            if bpp == 8:
                if self._norm == NORMAL_POS:
                    image_or_collection /= 255.0
                elif self._norm == NORMAL_ZERO:
                    image_or_collection = image_or_collection / 127.5 - 1
                elif self._norm == NORMAL_STD:
                    image_or_collection = (
                        image_or_collection - np.mean(image_or_collection)
                    ) / np.std(image_or_collection)
            # original pixel data is 16 pixel
            elif bpp == 16:
                if self._norm == NORMAL_POS:
                    image_or_collection /= 65535.0
                elif self._norm == NORMAL_ZERO:
                    image_or_collection = image_or_collection / 32767.5 - 1
                elif self._norm == NORMAL_STD:
                    image_or_collection = (
                        image_or_collection - np.mean(image_or_collection)
                    ) / np.std(image_or_collection)

        return image_or_collection

    def _create_hdf5(self):
        """Create the HDF5 file and add toplevel metadata
        """

        if self._name:
            self._hf = h5py.File(os.path.join(self._dir, self._name + '.h5'), 'w')
        else:
            self._hf = h5py.File(os.path.join(self._dir, self._dataset + '.h5'), 'w')

        # Dataset Attributes
        if self._name:
            self._hf.attrs['name'] = self._name
        else:
            self._hf.attrs['name'] = str(self._dataset)
        self._hf.attrs['author'] = self._author
        self._hf.attrs['source'] = self._src
        self._hf.attrs['description'] = self._desc
        self._hf.attrs['license'] = self._license
        self._hf.attrs['date'] = str(datetime.datetime.now())
        self._hf.attrs['dtype'] = str(self._dtype)

        if self._colorspace == COLOR:
            self._hf.attrs['channel'] = str(['R', 'G', 'B'])
        else:
            self._hf.attrs['channel'] = str(['K'])

    def _end_hdf5(self):
        """Finish storing to HDF5 and update remaining metadata
        """

        self._hf.attrs['count'] = self._count
        self._hf.attrs['time'] = self._time
        self._hf.attrs['shape'] = self._shape
        self._hf.attrs['class'] = str(self._classes)
        self._hf.attrs['color'] = self._colorspace

        # only store the number of failures, not the failures themselves
        self._hf.attrs['fail'] = len(self._errors)

        self._hf.close()
        self._hf = None

    def _init_stream_hdf5(self, name: str, nelem: int):
        """init streaming from a h5 file

        Arguments:
            name {str} -- group name
            nelem {int} -- number of elements

        Returns:
            dset {HDF5 handle} -- HDF5 handle to dataset
        """

        self._group = self._hf.create_group(name) # Create dataset group
        self._groups.append(name)
        if self._colorspace == GRAYSCALE:
            if self._flatten:
                shape = (self._resize[0] * self._resize[1],)
            else:
                # switch to height, width (resize is reversed for cv2
                shape = (self._resize[1], self._resize[0])
            if self._expand_dim:
                # switch to height, width (resize is reversed for cv2
                shape = (self._resize[1], self._resize[0], 1)
        else:
            if self._flatten:
                shape = (self._resize[0] * self._resize[1] * 3,)
            else:
                # switch to height, width (resize is reversed for cv2
                shape = (self._resize[1], self._resize[0], 3)

        shape = ((nelem,) + shape)
        if self._dtype == np.uint8:
            dtype = 'i1'
        elif self._dtype == np.uint16:
            dtype = 'i2'
        elif self._dtype == np.float16:
            dtype = 'f2'
        elif self._dtype == np.float32:
            dtype = 'f4'
        elif self._dtype == np.float64:
            dtype = 'f8'
        else:
            dtype = 'i1'
        return self._group.create_dataset('data', shape, dtype=dtype)

    def _write_group_hdf5(self, group: str, collection, label: int, elapsed: float,
                          names, types, sizes, shapes, dset):
        """Write a collection and metadata to HDF5 file

        Arguments:
            group {str} -- name of collection
            collection {np.ndarray} -- collection of preprocessed image data
            label {int} -- the label for the entire collection (if labels is None)
            elapsed {float} -- the elapsed time to process in seconds
            names {list[str]} -- the original image file names
            types {list[str]} -- the original image file types
            sizes {list[int]} -- the original image file sizes
            shapes {list[tuple]} -- the original image shapes
            dset {HDF5 handle} -- HDF5 handle to dataset
        """

        if not self._stream:
            # Create dataset group
            group = self._hf.create_group(group)

            # Create dataset attributes
            dset = group.create_dataset('data', data=collection)
            dset.attrs['count'] = len(collection)
        else:
            dset.attrs['count'] = len(sizes)

        dset.attrs['label'] = label
        dset.attrs['time'] = elapsed

        # Create individual original image attributes
        try:
            dset.attrs['name'] = names
            dset.attrs['type'] = types
            dset.attrs['size'] = sizes
            dset.attrs['shape'] = shapes
        except Exception as error:
            # maybe too large
            pass

    def _init_labels(self):
        """Initialize variables for multi-class labels
        """

        classes = {}
        collections = {}
        labels = {}
        counts = {}
        names = {}
        types = {}
        shapes = {}
        sizes = {}
        dset = {}
        d_index = {}

        # initialize the collections
        self._count = len(self._dataset)
        if isinstance(self._labels, (list, np.ndarray)):
            if len(self._labels) != self._count:
                raise AttributeError('Number of labels does not match number of images')

            for label in self._labels:
                if label in counts:
                    counts[label] += 1
                else:
                    collections[label] = []
                    counts[label] = 1
                    names[label] = []
                    types[label] = []
                    sizes[label] = []
                    shapes[label] = []

            n_label = 0
            for label in collections:
                if isinstance(label, int):
                    classes[str(label)] = n_label
                else:
                    classes[label] = n_label
                labels[label] = [n_label for _ in range(counts[label])]
                n_label += 1

                if self._stream:
                    dset[label] = self._init_stream_hdf5(str(label), counts[label])
                else:
                    dset[label] = None
                d_index[label] = 0
        else:
            n_label = 0
            classes = {str(self._labels) : n_label}
            self._labels = [n_label for label in range(self._count)]
            collections[n_label] = []
            labels[n_label] = self._labels
            names[n_label] = []
            types[n_label] = []
            sizes[n_label] = []
            shapes[n_label] = []
            counts[n_label] = self._count

            if self._stream:
                dset[n_label] = self._init_stream_hdf5('unnamed', self._count)
            else:
                dset[n_label] = None
            d_index[n_label] = 0

        return collections, labels, classes, counts, names, types, sizes, shapes, dset, d_index

    # UNUSED method
    def _process_image(self, image, resize: Tuple[int, int], flatten: bool = False):
        """ Lowest level processing of an raw pixel data. [UNUSED]

        Arguments:
            image {numpy matrix} -- raw pixel data as 2D (grayscale) or 3D (color) matrix.
            resize {tuple(height, width)} -- scale (downsample or upsample)
                                             image to a specifid height, width.

        Keyword Arguments:
            flatten {bool} -- whether to flatten the image into a 1D vector or not.
                              (default: {False})

        Returns:
            image {np.ndarray} -- a processed image (or vector if flattened).
        """

        # resize each image to the target size (e.g., 50x50) and flatten into 1D vector
        if flatten:
            return cv2.resize(image, resize, interpolation=cv2.INTER_AREA).flatten()
        # resize each image to the target size (e.g., 50x50)
        else:
            return cv2.resize(image, resize, interpolation=cv2.INTER_AREA)


    def _gray_expand_dim(self, image):
        if self._colorspace == GRAYSCALE and self._expand_dim:
            if image.ndim == 2:
                image = np.expand_dims(image, axis=-1)
        return image


    ### Image Augmentation ###

    def _augmentation(self, image):
        """ select a random augmentation

        Arguments:
            image {numpy matrix} -- raw pixel data as 2D (grayscale) or 3D (color) matrix.

        Returns:
            function -- selected random augmentation
        """

        function = random.choice(self._augment)

        return function(image)

    def _rotate_image(self, image):
        """ rotate the image

        Arguments:
            image {np.ndarray} -- raw pixel data as 2D (grayscale) or 3D (color) matrix.

        Returns:
            {np.ndarray} -- image rotated
        """

        degree = random.randint(self._rotate[0], self._rotate[1])

        # operation not supported in float16
        if self._dtype == np.float16:
            image = image.astype(np.float32)

        # rotate the image
        rotated = imutils.rotate_bound(image, degree)

        # resize back to expected dimensions
        if degree not in (0, 90, 180, 270, -90, -180, -270):
            # resize takes only height x width
            shape = (image.shape[0], image.shape[1])
            rotated = cv2.resize(rotated, shape, interpolation=cv2.INTER_AREA)

        if self._dtype == np.float16:
            return rotated.astype(np.float16)

        rotated = self._gray_expand_dim(rotated)
        return rotated

    def _edge_image(self, image):
        """ edge the image

        Arguments:
            image {np.ndarray} -- raw pixel data as 2D (grayscale) or 3D (color) matrix.

        Returns:
            {np.ndarray} -- image edged
        """

        if self.dtype in (np.uint8, np.uint16):
            gray = cv2.GaussianBlur(image, (3, 3), 0)
            edged = cv2.Canny(gray, 20, 100)
        else:
            edged = image

        edged = self._gray_expand_dim(edged)
        return edged

    def _flip_image(self, image):
        """ flip the image

        Arguments:
            image {np.ndarray} -- raw pixel data as 2D (grayscale) or 3D (color) matrix.

        Returns:
            {np.ndarray} -- image flipped
        """

        # operation not supported as float16
        if self._dtype == np.float16:
            image = image.astype(np.float32)

        if self._horizontal:
            flip = cv2.flip(image, 1) # flip image horizontally
        if self._vertical:
            flip = cv2.flip(image, 0) # flip image
        if self._dtype == np.float16:
            return flip.astype(np.float16)

        flip = self._gray_expand_dim(flip)
        return flip

    def _zoom_image(self, image):
        """ zoom the image

        Arguments:
            image {np.ndarray} -- raw pixel data as 2D (grayscale) or 3D (color) matrix.

        Returns:
            {np.ndarray} -- image zoomed
        """

        # operation not supported as float16
        if self._dtype == np.float16:
            image = image.astype(np.float32)

        old_height, old_width = image.shape[:2]
        image = cv2.resize(
            image,
            (int(self._zoom*old_width), int(self._zoom*old_height)),
            interpolation=cv2.INTER_CUBIC
        )
        new_height, new_width = image.shape[:2]

        y_new = int(new_height/2)
        x_new = int(new_width/2)
        h_old = int(old_height/2)
        w_old = int(old_width/2)

        zoom_img = image[
            y_new-h_old:y_new+h_old,
            x_new-w_old:x_new+w_old
        ]

        if self._dtype == np.float16:
            return zoom_img.astype(np.float16)

        zoom_img = self._gray_expand_dim(zoom_img)
        return zoom_img

    def _denoise_image(self, image):
        """ denoise the image

        Arguments:
            image {np.ndarray} -- raw pixel data as 2D (grayscale) or 3D (color) matrix.

        Returns:
            {np.ndarray} -- image denoiseed
        """

        if self.dtype in (np.uint8, np.uint16):
            denoise = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        else:
            denoise = image

        denoise = self._gray_expand_dim(denoise)
        return denoise

    def _brightness_contrast_image(self, image):
        """ brightness & contrast the image

        Arguments:
            image {np.ndarray} -- raw pixel data as 2D (grayscale) or 3D (color) matrix.

        Returns:
            {np.ndarray} -- image contrasted
        """

        # operation not supported as float16
        if self._dtype == np.float16:
            image = image.astype(np.float32)

        brightness_contrast = cv2.convertScaleAbs(
            image,
            alpha=self._contrast,
            beta=self._brightness
        )
        if self._dtype == np.float16:
            return brightness_contrast.astype(np.float16)

        brightness_contrast = self._gray_expand_dim(brightness_contrast)
        return brightness_contrast


class Images(BareMetal):
    """Base (super) for classifying a group of images
    """

    def __init__(self, name: str = 'unnamed', images=None, labels=None, _dir: str = './',
                 ehandler=None, config=[], augment=[]):
        """ Constructor

        Keyword Arguments:
            name {str} -- name of the dataset (default: {'unnamed'})
            images {str or numpy array} -- location of images (default: {None})
            labels {list or int} -- the image labels (default: {None})
            _dir {str} -- directory to store HDF5 file (default: {'./'})
            ehandler {callback function} -- callback for asynchronous
                                            processing (default: {None})
            config {list} -- configuration settings (default: {[]})
            augment {list} -- augmentation settings (default: {[]})
        """

        ### Argument Validation ###

        self.name = name

        if labels is None:
            if isinstance(images, (list, np.ndarray)):
                raise TypeError('Labels expected when images are a list or numpy array')
        else:
            if isinstance(labels, np.ndarray):
                if labels.size == 0:
                    raise AttributeError('Array must be > 0 for labels')
                if labels.dtype not in ('int8', 'int16', 'int32', 'uint8', 'uint16', 'uint32'):
                    raise TypeError('Array values must be integers for labels')
            elif isinstance(labels, list):
                if not labels:
                    raise AttributeError('List must be > 0 for labels')
                if not isinstance(labels[0], (int, str)):
                    raise TypeError('List values must be integers or strings for labels')
            elif isinstance(labels, int):
                pass
            elif isinstance(labels, str):
                pass
            else:
                raise TypeError('List, Numpy, integer or string expected for labels')
        self._labels = labels

        self.dir = _dir

        if ehandler:
            if isinstance(ehandler, tuple):
                if not callable(ehandler[0]):
                    raise TypeError('Function expected for ehandler')
            elif not callable(ehandler):
                raise TypeError('Function expected for ehandler')

        self._data = None
        self._groups = []
        self._ehandler = ehandler
        self._resize = (128, 128)
        self._flatten = False
        self._colorspace = COLOR
        self._expand_dim = False
        self._dtype = np.float32
        self._norm = NORMAL_POS
        self._author = ''
        self._desc = ''
        self._src = ''
        self._license = ''
        self._header = False
        self._image_col = None
        self._label_col = None
        self._col_sep = ','
        self._image_key = None
        self._label_key = None
        self._store = False
        self._stream = False
        self._stream_ff = False
        self._classes = None
        self._time = 0
        self._errors = []
        self._shape = (0,)
        self._count = 0
        self._16bpp = False
        self._hf = None
        self._verbose = False
        self._disable = True
        self._duplicate = False
        self._mp = 1            # parallel processing threads

        self._split = 0.8       # percentage of split between train / test
        self._seed = 0          # seed for random shuffle of data
        self._train = None      # indexes for training set
        self._trainsz = 0       # size of training set
        self._test = None       # indexes for test set
        self._val = None        # indexes for validation set
        self._next = 0          # next item in training set
        self._nlabels = None    # number of labels in the collection
        self._minisz = 0        # (mini) batch size

        self._remote = False

        if config:
            if not isinstance(config, list):
                raise TypeError('List expected for config settings')
            else:
                for setting in config:
                    if setting.startswith('resize='):
                        param = setting.split('=')[1]
                        try:
                            toks = param.split(',')
                            if toks[0][0] == '(':
                                toks[0] = toks[0][1:]
                                toks[1] = toks[1][:-1]
                            # openCV resizes as (width, height)
                            self._resize = (int(toks[1]), int(toks[0]))
                            if self._resize[0] <= 0 or self._resize[1] <= 0:
                                raise AttributeError('Height and width must be > 0 for resize')
                        except:
                            raise AttributeError('Tuple(int,int) expected for resize')
                    elif setting.startswith(('norm=', 'normalization=')):
                        param = setting.split('=')[1]
                        if param == 'pos':
                            self._norm = NORMAL_POS
                        elif param == 'zero':
                            self._norm = NORMAL_ZERO
                        elif param == 'std':
                            self._norm = NORMAL_STD
                        else:
                            raise AttributeError('pos, zero or std expected for norm(alization)')
                    elif setting.startswith('image_col='):
                        try:
                            self._image_col = int(setting.split('=')[1])
                            if self._image_col < 0:
                                raise AttributeError('Value must be >= 0 for image_col')
                        except:
                            raise AttributeError('Integer expected for image_col')
                    elif setting.startswith('label_col='):
                        try:
                            self._label_col = int(setting.split('=')[1])
                            if self._label_col < 0:
                                raise AttributeError('Value must be >= 0 for label_col')
                        except:
                            raise AttributeError('Integer expected for label_col')
                    elif setting.startswith('sep='):
                        self._col_sep = setting.split('=')[1]
                        if not self._col_sep:
                            raise AttributeError('Character sequence expected for sep')
                    elif setting.startswith('image_key='):
                        self._image_key = setting.split('=')[1]
                        if not self._image_key:
                            raise AttributeError('String expected for image_key')
                    elif setting.startswith('label_key='):
                        self._label_key = setting.split('=')[1]
                        if not self._label_key:
                            raise AttributeError('String expected for label_key')
                    elif setting.startswith('author='):
                        self._author = setting.split('=')[1]
                    elif setting.startswith('desc='):
                        self._desc = setting.split('=')[1]
                    elif setting.startswith('src='):
                        self._src = setting.split('=')[1]
                    elif setting.startswith('license='):
                        self._license = setting.split('=')[1]
                    elif setting.startswith('mp='):
                        val = setting.split('=')[1]
                        if not val:
                            raise AttributeError('Integer expected for mp')
                        try:
                            self._mp = int(val)
                        except:
                            raise AttributeError('Integer expected for mp')
                    elif setting == 'verbose':
                        self._disable = False
                    elif setting in ('gray', 'grayscale'):
                        self._colorspace = GRAYSCALE
                    elif setting == 'gray-expand_dim':
                        self._colorspace = GRAYSCALE
                        self._expand_dim = True
                    elif setting in ('flat', 'flatten'):
                        self._flatten = True
                    elif setting == 'uint8':
                        self._dtype = np.uint8
                    elif setting == 'uint16':
                        self._dtype = np.uint16
                    elif setting == 'float16':
                        self._dtype = np.float16
                    elif setting == 'float32':
                        self._dtype = np.float32
                    elif setting == 'float64':
                        self._dtype = np.float64
                    elif setting == 'header':
                        self._header = True
                    elif setting == 'store':
                        self._store = True
                    elif setting == 'stream':
                        self._stream = True
                        # stream implies store
                        self._store = True
                    elif setting == '_stream_ff':
                        self._stream_ff = True
                    elif setting == '16bpp':
                        self._16bpp = True
                    elif setting == 'duplicate':
                        self._duplicate = True
                    else:
                        raise AttributeError('Config setting not recognized: {}'.format(setting))

        ### Image Augmentation - Argument Validation ###

        self._rotate = []
        self._flip = None
        self._horizontal = False
        self._vertical = False
        self._zoom = None
        self._augment = []
        self._brightness = 0
        self._contrast = 1.0
        self._toggle = True

        if augment is not None:
            if not isinstance(augment, list):
                raise TypeError('List expected for augment settings')
            else:
                for setting in augment:
                    if setting.startswith('flip='):
                        self._flip = setting.split('=')[1]
                        if not self._flip or self._flip not in ('horizontal', 'vertical', 'both'):
                            raise AttributeError('horizontal, vertical, or both expected for flip')
                        if self._flip in ('horizontal', 'both'):
                            self._horizontal = True
                        if self._flip in ('vertical', 'both'):
                            self._vertical = True
                        self._augment.append(self._flip_image)
                    elif setting.startswith('zoom='):
                        self._zoom = setting.split('=')[1]
                        if not self._zoom:
                            raise AttributeError('integer or float >= 0 expected for zoom')
                        try:
                            self._zoom = ast.literal_eval(self._zoom)
                            if self._zoom < 0:
                                raise AttributeError('Value must be >= 0 for zoom')
                        except:
                            raise AttributeError('integer or float >= 0 expected for zoom')
                        self._zoom += 1
                        self._augment.append(self._zoom_image)
                    elif setting.startswith('rotate='):
                        args = setting.split('=')[1]
                        if not args:
                            raise AttributeError('Missing value for rotate')
                        rotate_range = args.split(',')
                        if len(rotate_range) != 2:
                            raise AttributeError('Degree range expected for rotate')
                        try:
                            min_rotate = int(rotate_range[0])
                            self._rotate.append(min_rotate)
                            max_rotate = int(rotate_range[1])
                            self._rotate.append(max_rotate)
                        except:
                            raise AttributeError('Degree range not an integer')
                        if min_rotate <= -360 or max_rotate >= 360:
                            raise AttributeError('Degree range must be between -360 and 360')
                        self._augment.append(self._rotate_image)
                    elif setting.startswith(('brightness=', 'contrast=')):
                        option = setting.split('=')
                        if option[0] == 'contrast':
                            if not option[1]:
                                raise AttributeError('Missing value for contrast')
                            try:
                                self._contrast = float(option[1])
                                if self._contrast < 1.0 or self._contrast > 3.0:
                                    raise AttributeError(
                                        "Contrast range must be between 1.0 and 3.0"
                                    )
                            except:
                                raise AttributeError('Contrast range not a float')
                        if option[0] == 'brightness':
                            if not option[1]:
                                raise AttributeError('Missing value for brightness')
                            try:
                                self._brightness = ast.literal_eval(option[1])
                                if self._brightness < 0 or self._brightness > 100:
                                    raise AttributeError(
                                        "Brightness range must be between 0 and 100"
                                    )
                            except:
                                raise AttributeError('Brightness range not an integer or float')
                        self._augment.append(self._brightness_contrast_image)
                    elif setting == 'edge':
                        self._augment.append(self._edge_image)
                    elif setting == 'denoise':
                        self._augment.append(self._denoise_image)
                    else:
                        raise AttributeError('Augment setting not recognized: {}'.format(setting))

        # Make Empty Images collection
        if images is None:
            return
        self._dataset = images

        # shape is set to the resize
        self._shape = (self._resize[1], self._resize[0])

        # Process the dataset synchronously
        if ehandler is None:
            self._process()
        # Process the dataset asynchronously
        else:
            # no parameters
            if not isinstance(self._async, tuple):
                thread = threading.Thread(target=self._async, args=())
            else:
                thread = threading.Thread(target=self._async, args=(ehandler[1:], ))
            thread.start()

    def _process(self):
        """Process the Dataset
        """

        try:
            self._data, self._labels, self._classes, self._errors, self._time = self._load_dataset()
        except Exception as error:
            if self._hf:
                self._hf.close()
            raise error

    def _async(self):
        """Asynchronous processing of the collection
        """

        self._process()
        # signal user defined event handler when processing is done
        if isinstance(self._ehandler, tuple):
            self._ehandler[0](self, self._ehandler[1:])
        else:
            self._ehandler(self)

    ### Methods ###

    def load(self, name: str = 'unnamed', _dir: str = None):
        """ Load a Collection of Images
        """

        if name is None:
            raise ValueError("Name parameter cannot be None")
        if not isinstance(name, str):
            raise TypeError('String expected for collection name')
        self._name = name

        if _dir is not None:
            if not isinstance(_dir, str):
                raise TypeError('String expected for directory name')
            self.dir = _dir

        # unnecessary self._dir gets the value './' when images = Images()
        # added exception if images = Images(_dir=None)
        # if self._dir is None:
        #     self._dir = "./"

        # Read the preprocessed dataset from the HD5 file
        self._data = []
        self._labels = []
        self._groups = []
        with h5py.File(os.path.join(self._dir, self._name + '.h5'), 'r') as self._hf:
            # Dataset Attributes
            self._name = self._hf.attrs['name']
            self._author = self._hf.attrs['author']
            self._src = self._hf.attrs['source']
            self._desc = self._hf.attrs['description']
            self._license = self._hf.attrs['license']
            self._date = self._hf.attrs['date']
            self._shape = tuple(self._hf.attrs['shape'])
            self._channel = self._hf.attrs['channel']
            self._count = self._hf.attrs['count']
            self._time = self._hf.attrs['time']
            self._classes = ast.literal_eval(self._hf.attrs['class'])
            dtype = self._hf.attrs['dtype']
            if dtype == "<class 'numpy.float64'>":
                self._dtype = np.float64
            elif dtype == "<class 'numpy.float32'>":
                self._dtype = np.float32
            elif dtype == "<class 'numpy.float16'>":
                self._dtype = np.float16
            elif dtype == "<class 'numpy.uint16'>":
                self._dtype = np.uint16
            elif dtype == "<class 'numpy.uint8'>":
                self._dtype = np.uint8
            self._colorspace = self._hf.attrs['color']

            self._errors = [_ for _ in range(self._hf.attrs['fail'])]

            self._resize = self._shape

            # Groups
            for group in self._hf:
                dset = self._hf[group]
                try:
                    count = dset['data'].attrs['count']
                except:
                    # empty dataset
                    continue
                # will stream from HDF5 instead of memory when feeding
                if not self._stream:
                    data = dset['data'][:count]
                    self._data.append(data)
                label = dset['data'].attrs['label']
                self._labels.append(np.asarray([label for _ in range(count)]))
                self._groups.append(group)

            # TODO: group attributes

        # leave HDF5 open when streaming
        if self._stream:
            self._hf = h5py.File(os.path.join(self._dir, self._name + '.h5'), 'r')

    def store(self, name: str = 'unnamed', _dir: str = None):
        """Load a Collection of Images

        Keyword Arguments:
            name {str} -- image HDF5 name (default: {'unnamed'})
            _dir {str} -- directory where to save HDF5 file (default: {None})
        """

        if name is None:
            raise ValueError("Name parameter cannot be None")
        if not isinstance(name, str):
            raise TypeError('String expected for collection name')
        self._name = name

        if _dir is not None:
            if not isinstance(_dir, str):
                raise TypeError('String expected for directory name')
            self.dir = _dir

        self._create_hdf5()

        for n_label in range(len(self._data)):
            collection = self._data[n_label]
            for key, value in self._classes.items():
                if value == n_label:
                    name = key
            names = None
            types = None
            sizes = None
            shapes = None
            self._write_group_hdf5(
                name,
                collection,
                n_label,
                0,
                names,
                types,
                sizes,
                shapes,
                None
            )
        self._end_hdf5()

    ### Properties ###

    @property
    def name(self):
        """Getter for the dataset (collection) name
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Setter for the dataset (collection) name
        """
        if name and not isinstance(name, str):
            raise TypeError('String expected for collection name')
        self._name = name

    @property
    def images(self):
        """Getter for the list of processed images
        """
        return self._data

    @property
    def labels(self):
        """Getter for image labels (classification)
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Setter for image labels (classification)
        """
        self._labels = labels

    @property
    def dir(self):
        """Getter for the image directory
        """
        return self._dir

    @dir.setter
    def dir(self, _dir: str):
        """Setter for image directory

        Arguments:
            _dir {str} -- directory path
        """
        # value must be a string
        if _dir is not None:
            if not isinstance(_dir, str):
                raise TypeError('String expected for image storage path')
            if not _dir.endswith("/"):
                _dir += "/"
            self._dir = _dir
        self._dir = _dir
        try:
            os.makedirs(self._dir, exist_ok=True)
        except:
            raise TypeError('String expected for image storage path')

    @property
    def time(self):
        """Getter for the processing time
        """
        return self._time

    @property
    def elapsed(self):
        """Getter for elapsed time in hh:mm:ss format for the processing time
        """
        return time.strftime("%H:%M:%S", time.gmtime(self._time))

    @property
    def fail(self):
        """Getter for the number of images that failed processing
        """
        if self._errors:
            return len(self._errors)
        return 0

    @property
    def errors(self):
        """Getter for the list of errors reported
        """
        return self._errors

    @property
    def classes(self):
        """Getter for list of mapping of class names to labels (integers)
        """
        return self._classes

    @property
    def dtype(self):
        """Getter for the datatype of pixel data
        """
        return self._dtype

    @property
    def shape(self):
        """Shape of the dataset
        """
        return self._shape

    @property
    def count(self):
        """Total number of images
        """
        return self._count

    @property
    def author(self):
        """Getter for the dataset (collection) author / copyright
        """
        return self._author

    @property
    def src(self):
        """Getter for the dataset (collection) source
        """
        return self._src

    @property
    def desc(self):
        """Getter for the dataset (collection) description
        """
        return self._desc

    @property
    def license(self):
        """Getter for the dataset (collection) license
        """
        return self._license

    ### Overrides ###

    def __len__(self):
        """Override the len() operator - return the number of collections
        """
        if self._data is None:
            return 0
        return len(self._data)

    def __not__(self):
        """Override the not operator - return whether there are any collections
        """
        if self._data is None:
            return False
        return True

    def __getitem__(self, index_x: int):
        """Override the index operator - return the collection at the corresponding index

        Arguments:
            index_x {int} -- [description]

        Returns:
            [type] -- [description]
        """
        if not isinstance(index_x, int):
            raise TypeError('Index must be an integer')
        if index_x > len(self):
            raise IndexError('Index out of range for Images')
        return self._data[index_x]

    def __iadd__(self, image):
        """Override the += operator - add an image to the collection

        Arguments:
            image {np.ndarray} -- image to add in dataset

        Returns:
            self -- [description]
        """
        if image is None:
            return self

        # Add single image
        if isinstance(image, Image):
            pass # TODO
        # Add a collection of images
        elif isinstance(image, Images):
            # Validity Checks
            if self._shape != image._shape:
                raise AttributeError('Collections must be of the same shape to add')
            if self._dtype != image._dtype:
                raise AttributeError('Collections must be of the sample pixel data type to add')
            if self._colorspace != image._colorspace:
                raise AttributeError('Collections must be of the same color space to add')

            # merge the counts
            self._count += image._count
            self._errors.append(image._errors)
            self._time += image._time

            # merge metadata
            if self._author != image._author:
                self._author += ',' + image._author
            if self._desc != image._desc:
                self._desc += ',' + image._desc
            if self._src != image._src:
                self._src += ',' + image._src
            if self._license != image._license:
                self._license += ',' + image._license

            # merge the classes
            for i_label in image._classes:
                match = False
                for j_label in self._classes:
                    # same class
                    if i_label == j_label:
                        match = True
                        ix = image._classes[i_label]
                        jx = self._classes[j_label]
                        self._data[jx] = np.concatenate(
                            (self._data[jx], image._data[ix]),
                            axis=0
                        )
                        self._labels[jx] = np.concatenate(
                            (self._labels[jx], image._labels[ix]),
                            axis=0
                        )
                        break
                if not match:
                    ix = image._classes[i_label]
                    n_label = len(self._classes)
                    self._classes[i_label] = n_label
                    self._data.append(image._data[ix])
                    self._labels.append(np.asarray([n_label for _ in range(len(image._data[ix]))]))
        else:
            raise TypeError('Image(s) expected for image')

        return self

    ### Feeders ###

    @property
    def split(self):
        """Getter for return a split training set
        """

        if self._stream:
            raise AttributeError('Split incompatible in stream mode')

        # Training set not already split, so split it
        if self._train is None:
            self.split = (1 - self._split)

        # Construct the train and test lists
        X_train = []
        Y_train = []
        X_test = []
        Y_test = []
        X_val = []
        Y_val = []

        # use the shuffled indices to assemble the train data
        for ix, index in self._train:
            X_train.append(self._data[ix][index])
            Y_train.append(self._labels[ix][0])

        # assemble the test (holdout) data
        for ix, index in self._test:
            X_test.append(self._data[ix][index])
            Y_test.append(self._labels[ix][0])

        # assemble the validation data
        val_validator = False
        if self._val:
            val_validator = True
            for ix, index in self._val:
                X_val.append(self._data[ix][index])
                Y_val.append(self._labels[ix][0])

        # calculate the number of labels in the training set
        if self._nlabels == None:
            if len(Y_test) > 0:
                self._nlabels = max(np.max(Y_train), np.max(Y_test)) + 1
            else:
                self._nlabels = np.max(Y_train) + 1

        # convert from list to numpy array
        X_train = np.asarray(X_train)
        X_test = np.asarray(X_test)
        if val_validator:
            X_val = np.asarray(X_val)
        # data was not normalized prior, normalize now during feeding
        # TODO: There is no way to set the float data type
        if self.dtype == np.uint8:
            X_train = (X_train / 255.0).astype(np.float32)
            X_test = (X_test / 255.0).astype(np.float32)
            if val_validator:
                X_val = (X_val / 255.0).astype(np.float32)
        elif self.dtype == np.uint16:
            X_train = (X_train / 65535.0).astype(np.float32)
            X_test = (X_test / 65535.0).astype(np.float32)
            if val_validator:
                X_val = (X_val / 65535.0).astype(np.float32)

        if len(self._test) > 0:
            # labels already one-hot encoded
            if isinstance(Y_train[0], np.ndarray):
                if val_validator:
                    return (
                        X_train,
                        X_val,
                        X_test,
                        np.asarray(Y_train),
                        np.asarray(Y_val),
                        np.asarray(Y_test)
                    )
                else:
                    return X_train, X_test, np.asarray(Y_train), np.asarray(Y_test)
            # one-hot encode the labels
            else:
                if val_validator:
                    return (
                        X_train,
                        X_val,
                        X_test,
                        self._one_hot(np.asarray(Y_train), self._nlabels),
                        self._one_hot(np.asarray(Y_val), self._nlabels),
                        self._one_hot(np.asarray(Y_test), self._nlabels)
                    )
                else:
                    return (
                        X_train,
                        X_test,
                        self._one_hot(np.asarray(Y_train), self._nlabels),
                        self._one_hot(np.asarray(Y_test), self._nlabels)
                    )
        else:
            # Calculate the number of labels as a sequence starting from 0
            if val_validator:
                return (
                    X_train,
                    X_val,
                    None,
                    self._one_hot(np.asarray(Y_train), self._nlabels),
                    self._one_hot(np.asarray(Y_val), self._nlabels),
                    None
                )
            else:
                return X_train, None, self._one_hot(np.asarray(Y_train), self._nlabels), None

    @split.setter
    def split(self, percent):
        """Set the split for training/test and create a randomized i

        Arguments:
            percent {
                float,
                list[float],
                tuple(float)
            } -- split and seed (optional)

        Dex
            Collections =>
                Indices (split and shuffled)
                    |
                    V
        """

        if isinstance(percent, tuple):
            if len(percent) != 2:
                raise AttributeError('Split setter must be percent, seed')
            self._seed = percent[1]
            if not isinstance(self._seed, int):
                raise TypeError('Seed parameter must be an integer')
            percent = percent[0]

        val_percent = 0
        if isinstance(percent, list):
            if len(percent) != 2:
                raise AttributeError('Percent must either be for test or test and eval')
            val_percent = percent[1]
            percent = percent[0]
            if not isinstance(val_percent, float):
                raise TypeError('Valuation Percent must be float')
        if not isinstance(percent, float) and percent != 0:
            raise TypeError('Float expected for percent')
        if percent < 0 or percent >= 1:
            raise ValueError("Percent parameter must be between 0 and 1")
        if val_percent < 0 or val_percent >= 1:
            raise ValueError("Valuation percent parameter must be between 0 and 1")

        if self._labels is None:
            raise AttributeError('No image data')

        # open HDF5 for streaming when feeding
        if self._stream and self._hf is None:
            self._hf = h5py.File(os.path.join(self._dir, self._name + '.h5'), 'r')

        self._split = (1 - percent)

        self._train = []
        self._test = []
        self._val = []
        random.seed(self._seed)
        for ix, collection in enumerate(self._labels):
            # create a randomized index to the images in this collection, where each entry is:
            # (index of collection, index within collection)
            l = len(collection)
            indices = [(ix, _) for _ in range(l)]
            random.shuffle(indices)

            # calculate the pivot point for the split
            pivot = max(int(self._split * l), 1)

            # if validation, calculate pivot for validation split
            if val_percent > 0:
                v_pivot = int(val_percent * pivot)
                # split train and validation
                self._train += indices[:v_pivot]
                self._val += indices[v_pivot:pivot]
            # split training only
            else:
                self._train += indices[:pivot]

            # split test
            self._test += indices[pivot:]

        # random shuffle the flattened training indices
        random.shuffle(self._train)

        # initialize the next iterator
        self._trainsz = len(self._train)
        self._next = 0

    def _one_hot(self, Y, C=0):
        """ Convert Vector to one-hot encoding """
        if C == 0:
            # Calculate the number of labels in Y
            C = len(np.max(Y)) + 1
        Y = np.eye(C)[Y.reshape(-1)].astype(np.uint8)
        return Y

    def _verify_normalization(self, image):
        # pre-normalized
        if self.dtype == np.uint8:
            image = (image / 255.0).astype(np.float32)
        elif self.dtype == np.uint16:
            image = (image / 65535.0).astype(np.float32)
        # else already normalized
        return image

    @property
    def minibatch(self):
        """Return a generator for the next mini batch
        """
        # mini-batch was not set, implicitly set it
        if self._minisz == 0:
            self.minibatch = 32

        # Mini-batch, return a batch on each iteration
        while True:

            # reshuffle the training data after an entire pass
            if self._next >= self._trainsz:
                random.shuffle(self._train)
                self._next = 0

            x_batch = []
            y_batch = []
            for _ in range(self._next, min(self._next + self._minisz, self._trainsz)):
                ix, iy = self._train[_]
                label = self._labels[ix][iy]
                # streaming
                if self._stream:
                    data = self._hf[self._groups[ix]]['data'][iy]
                # in-memory
                else:
                    data = self._data[ix][iy]
                x_batch.append(self._verify_normalization(data))
                y_batch.append(label)

                # if augmentation, feed a second augmented version of the image
                if self._augment:
                    image = self._augmentation(data)
                    x_batch.append(self._verify_normalization(image))
                    y_batch.append(label)

            self._next += self._minisz
            yield np.asarray(x_batch), self._one_hot(np.asarray(y_batch), self._nlabels)

    @minibatch.setter
    def minibatch(self, batch_size: int):
        """Generator for creating mini-batches

        Arguments:
            batch_size {int} -- batche size to load data in training
        """
        if not isinstance(batch_size, int):
            raise TypeError('Integer expected for mini batch size')

        if batch_size <= 0:
            raise ValueError("Batch size must be > 0")

        # Training set not already split, so split it
        if self._train is None:
            self.split = (1 - self._split)

        if batch_size < 2 or batch_size >= self._trainsz:
            raise ValueError("Mini batch size is out of range")

        # half the batch size when augmenting
        if self._augment:
            batch_size //= 2

        self._minisz = batch_size
        self._nlabels = len(self._classes)

    @property
    def stream_from_folder(self):
        """Returns images preprocessed from folders
        """
        image_label = self._image_label
        while image_label:
            total_images = len(image_label)
            if total_images < self._stream_batch:
                self._stream_batch = total_images
            images_batch = random.sample(image_label, self._stream_batch)
            x_batch = []
            y_batch = []
            for i, item in enumerate(images_batch, 1):
                file = item[0]
                image_label.remove(item)
                if not isinstance(file, str):
                    raise ValueError('image path must be a string')
                image = self._load_image_disk(file)
                if self._augment and (i % 2) == 0:
                    ## augment just half of the data set
                    image = self._augmentation(image)

                ## resize image
                image = self._pixel_transform_stream(image)

                x_batch.append(image)

            yield np.asarray(x_batch), self._one_hot(np.asarray(y_batch), self._nlabels)

    @stream_from_folder.setter
    def stream_from_folder(self, batch_size: int):
        """Setup batch size of images to load from folders
        """
        if not isinstance(batch_size, int):
            raise TypeError('Integer expected for mini batch size')

        if batch_size <= 0:
            raise ValueError("Batch size must be > 0")

        if batch_size < 1 or batch_size > self._image_label:
            raise ValueError("Mini batch size is out of range")

        self._stream_batch = batch_size
        self._nlabels = len(self._classes)

    @property
    def stratify(self):
        """Return a generator for the next stratified mini batch
        """

        # stratify was not set, implicitly set it
        if self._minisz == 0:
            self.stratify = 32

        while True:
            # Mini-batch, return a batch on each iteration
            x_batch = []
            y_batch = []
            n = 0
            while n < self._minisz:
                for ix, collection in enumerate(self._train):
                    iy = random.randint(0, len(collection))
                    label = self._labels[ix]
                    # streaming
                    if self._stream:
                        data = self._hf[self._groups[ix]]['data'][iy]
                    # in-memory
                    else:
                        data = self._data[ix][iy]
                    x_batch.append(self._verify_normalization(data))
                    y_batch.append(label)
                    n += 1

                    # if augmenting, send a second augmented version of the image
                    if self._augment:
                        image = self._augmentation(data)
                        x_batch.append(self._verify_normalization(image))
                        y_batch.append(label)

            yield np.asarray(x_batch), self._one_hot(np.asarray(y_batch), self._nlabels)

    @stratify.setter
    def stratify(self, batch_size: int):
        """Generator for creating stratify mini-batches
        """
        if isinstance(batch_size, int):
            batch_size = tuple([batch_size])

        if not isinstance(batch_size, tuple) or len(batch_size) > 3:
            raise AttributeError('Stratify setter must be batch_size, percent[,seed]')

        self._minisz = batch_size[0]
        if not isinstance(self._minisz, int):
            raise TypeError('Integer expected for mini batch size')
        if self._minisz <= 0:
            raise ValueError("Batch size must be > 0")

        if len(batch_size) > 1:
            percent = batch_size[1]
            if not isinstance(percent, float) and percent != 0:
                raise TypeError('Float expected for percent')
            if percent < 0 or percent >= 1:
                raise ValueError('Percent parameter must be between 0 and 1')
        else:
            percent = (1 - self._split)

        if len(batch_size) > 2:
            self._seed = batch_size[2]
            if not isinstance(self._seed, int):
                raise TypeError('Seed parameter must be an integer')

        if self._labels is None:
            raise AttributeError('No image data')

        if self._minisz < len(self._labels):
            raise ValueError('Batch size too small')

        self._split = (1 - percent)

        self._nlabels = len(self._classes)

        self._train = []
        self._test = []
        random.seed(self._seed)
        for ix, collection in enumerate(self._labels):
            l = len(collection)
            indices = [_ for _ in range(l)]
            random.shuffle(indices)

            # calculate the pivot point for the split
            pivot = max(int(self._split * l), 1)

            # split the collection
            self._train.append(indices[:pivot])
            self._test.append(indices[pivot:])

            # make a one-hot encoding for the labels
            self._labels[ix] = ix

        #self._labels = self._one_hot(np.asarray(self._labels), self._nlabels)

        # open HDF5 for streaming when feeding
        if self._stream and self._hf is None:
            self._hf = h5py.File(os.path.join(self._dir, self._name + '.h5'), 'r')

    @property
    def test(self):
        """Return the test data
        """
        # Training set not already split, so split it
        if self._train is None:
            self.split = (1 - self._split)

        X_test = []
        Y_test = []
        for ix, index in self._test:
            if self._stream:
                X_test.append(self._hf[self._groups[ix]]['data'][index])
            else:
                X_test.append(self._data[ix][index])
            Y_test.append(self._labels[ix][0])

        # calculate the number of labels in the training set
        if self._nlabels == None:
            self._nlabels = np.max(Y_test) + 1

        # convert from list to numpy array
        X_test = np.asarray(X_test)
        # data was not normalized prior, normalize now during feeding
        # TODO: There is no way to set the float data type
        if self.dtype == np.uint8:
            X_test = (X_test / 255.0).astype(np.float32)
        elif self.dtype == np.uint16:
            X_test = (X_test / 65535.0).astype(np.float32)

        # labels already one-hot encoded
        if isinstance(Y_test[0], np.ndarray):
            return X_test, np.asarray(Y_test)
        # one-hot encode the labels
        else:
            return X_test, self._one_hot(np.asarray(Y_test), self._nlabels)

    def __next__(self):
        """Iterate through the training set (single image at a time)
        """

        # Training set not already split, so split it
        if self._train is None:
            self.split = (1 - self._split)

        # Create one-hot encoded labels
        if self._nlabels is None:
            self._nlabels = len(self._classes)
            for ix, labels in enumerate(self._labels):
                self._labels[ix] = np.zeros(self._nlabels).astype(np.uint8)
                self._labels[ix][ix] = 1

        # End of training set
        if self._next >= self._trainsz:
            # Reshuffle the training data for the next round
            random.shuffle(self._train)
            self._next = 0
            return None, None

        # Get index of next item in training set
        ix, iy = self._train[self._next]

        # pre-normalize: normalize as being feed
        label = self._labels[ix]
        if self._stream:
            image = self._hf[self._groups[ix]]['data'][iy]
        else:
            image = self._data[ix][iy]
        if self.dtype == np.uint8:
            image = (image / 255.0).astype(np.float32)
        elif self.dtype == np.uint16:
            image = (image / 65535.0).astype(np.float32)

        # if augment, return original image, and then augmented version
        if self._augment:
            if self._toggle:
                image = self._augmentation(image)
                self._toggle = False
                return image, label
            else:
                self._toggle = True

        # advance to next image
        self._next += 1
        return image, label

    ### Transforms ###

    @property
    def flatten(self):
        """dummy property
        """
        return None

    @flatten.setter
    def flatten(self, flatten: bool):
        """(Un)Flatten the Image Data

        Arguments:
            flatten {bool} -- True to flat images arrays
        """
        if not isinstance(flatten, bool):
            raise TypeError('Boolean expected for flatten')
        if not self:
            return
        if flatten == True:
            # Already Flattened
            if self._data[0].ndim == 2:
                return
            collections = []
            for collection in self._data:
                _collection = []
                for image in collection:
                    _collection.append(image.flatten())
                collections.append(np.asarray(_collection))
            self._data = collections
        else:
            # Not Flattened
            if self._data[0].ndim != 2:
                return
            if self._resize != None:
                if self._colorspace == COLOR:
                    resize = (self._resize[0], self._resize[1], 3)
                else:
                    resize = (self._resize[0], self._resize[1])
            collections = []
            for collection in self._data:
                shape = (len(collection),) + resize
                collections.append(collection.reshape(shape))
            self._data = collections

    @property
    def resize(self):
        """dummy property
        """
        return None

    @resize.setter
    def resize(self, resize: Tuple[int, int]):
        """Resize the Image Data

        Arguments:
            resize {tuple(int)} -- (height, width)
        """

        # Argument Validation
        if not isinstance(resize, tuple):
            raise TypeError('Tuple expected for resize')
        if len(resize) != 2:
            raise AttributeError('Tuple for resize must be in form (height, width)')
        if not isinstance(resize[0], int) or not isinstance(resize[1], int):
            raise TypeError('Integer expected for height and width in resize')
        if resize[0] <= 0 or resize[1] <= 0:
            raise ValueError('height and width must > 0 in resize')

        # There are no images
        if not self:
            return

        # Data is flatten, so let's unflatten it first
        if self._data[0].ndim == 2:
            self.flatten = False

        # openCV uses width, height
        self._resize = (resize[1], resize[0])
        self._shape = (resize[0], resize[1])

        collections = []
        for collection in self._data:
            images = []
            for image in collection:
                images.append(
                    cv2.resize(
                        image,
                        self._resize,
                        interpolation=cv2.INTER_AREA
                    )
                )
            collections.append(np.asarray(images))
        self._data = collections

    @property
    def gray(self):
        """dummy property
        """
        return None

    @gray.setter
    def gray(self, gray):
        """Grayscale the Image Data

        Arguments:
            gray {
                tuple(bool),
                list(bool),
                bool
            } -- True for gray, (True, True) to expand dimention for gray images
        """
        expand_dim = False
        if isinstance(gray, (tuple, list)):
            if len(gray) != 2:
                raise AttributeError("gray and expand_dim setter must be (bool, bool)")
            for item in gray:
                if not isinstance(item, bool):
                    raise AttributeError("gray and expand_dim setter must be bool")
            expand_dim = gray[1]
            gray = gray[0]
        elif not isinstance(gray, bool):
            raise AttributeError("gray and expand_dim setter must be bool")

        if gray and self._colorspace != GRAYSCALE:
            self._colorspace = GRAYSCALE
            collections = []
            for collection in self._data:
                images = []
                for image in collection:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    if expand_dim:
                        image = np.expand_dims(image, axis=-1)
                    images.append(image)
                collections.append(np.asarray(images))
            self._data = collections

class Image(object):
    """work in progress"""
    def __init__(self):
        """ """
        pass
        # TODO
