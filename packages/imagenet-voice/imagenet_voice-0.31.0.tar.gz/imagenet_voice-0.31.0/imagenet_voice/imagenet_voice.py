import glob
import os
import progressbar
import random as rand
import wavio

import numpy as np


def __download_dataset():
    confirmation = input("Estimated download size: 2 GB\nAre you sure you want to download this dataset? (y/n) ")
    if "y" in confirmation.lower():
        print("Cloning from https://github.com/CharlesAverill/ImageNet-Voice.git ...")
        os.system("git clone https://github.com/CharlesAverill/ImageNet-Voice.git")
        os.system("mv ./ImageNet-Voice/inv_data ./")
        os.system("rm -r ImageNet-Voice")


def __load_wavs_in_dir(directory):
    """
    :param directory: Directory to load from
    :return: List of NumPy arrays of wav data in directory, shape (num_samples, num_channels)
    """
    output = []
    for fn in glob.glob(directory + "/*.wav"):
        data = wavio.read(fn).data
        output.append(data)
    return output


def load_classes(classes: list, progress: bool = False, download_data=True):
    """
    :param classes: A list of the desired classes to be loaded
    :param progress: Whether or not to display a progressbar
    :param download_data: Whether or not to download the dataset
    :return: A NumPy array containing NumPy arrays of data loaded with wavio
    """
    if download_data:
        __download_dataset()

    could_not_load = []
    output = []

    bar = None
    count = 1

    if progress:
        bar = progressbar.ProgressBar(max_value=len(classes))
        bar.start()

    for label in classes:
        try:
            wavs = __load_wavs_in_dir(label)
            output.extend(wavs)
        except Exception as e:
            could_not_load.append(label)
        if bar:
            bar.update(count)
            count += 1
    if len(could_not_load) > 0:
        print("Could not load:", could_not_load)
    return np.array(output)


def load_n(n: int, random: bool = False, progress: bool = False, download_data=True):
    """
    :param n: Number of classes to be loaded
    :param random: Whether or not to load random classes
    :param progress: Whether or not to display a progressbar
    :param download_data: Whether or not to download the dataset
    :return: A NumPy array containing NumPy arrays of data loaded with wavio
    """
    if download_data:
        __download_dataset()

    output = []
    could_not_load = []
    directories = [x[0] for x in os.walk("./inv_data/") if "/inv_data/." not in x[0] and len(x[0]) > 11]
    directories.sort()

    bar = None

    if progress:
        bar = progressbar.ProgressBar(max_value=n)
        bar.start()

    if random:
        for i in range(n):
            temp_dir = rand.choice(directories)
            directories.remove(temp_dir)
            try:
                wavs = __load_wavs_in_dir(temp_dir)
                output.extend(wavs)
            except Exception as e:
                could_not_load.append(temp_dir)
            if bar:
                bar.update(i)
    else:
        for i in range(n):
            temp_dir = directories[i]
            try:
                wavs = __load_wavs_in_dir(temp_dir)
                output.extend(wavs)
            except Exception as e:
                could_not_load.append(temp_dir)
            if bar:
                bar.update(i)
    if len(could_not_load) > 0:
        print("Could not load:", could_not_load)
    return np.array(output)


def load(progress: bool = False, download_data=True):
    """
    :param progress: Whether or not to display a progressbar
    :param download_data: Whether or not to download the dataset
    :return: A NumPy array containing NumPy arrays of data loaded with wavio
    """
    if download_data:
        __download_dataset()

    output = []
    could_not_load = []
    directories = [x[0] for x in os.walk("./inv_data/")]

    bar = None
    count = 1

    if progress:
        bar = progressbar.ProgressBar(max_value=len(directories))
        bar.start()

    for directory in directories:
        try:
            wavs = __load_wavs_in_dir(directory)
            output.extend(wavs)
        except Exception as e:
            could_not_load.append(directory)
        if bar:
            bar.update(count)
            count += 1
    if len(could_not_load) > 0:
        print("Could not load:", could_not_load)
    return np.array(output)

