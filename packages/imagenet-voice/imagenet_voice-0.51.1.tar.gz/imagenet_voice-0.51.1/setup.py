import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='imagenet_voice',
    version='0.51.1',
    scripts=['./imagenet_voice/__init__.py'],
    author="Charles Averill",
    author_email="charlesaverill20@gmail.com",
    description="A collection of synthetic audio files containing spoken labels from ImageNet",
    long_description=long_description,
    install_requires=['progressbar2', 'wavio', 'numpy'],
    long_description_content_type="text/markdown",
    url="https://github.com/CharlesAverill/ImageNet-Voice/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
