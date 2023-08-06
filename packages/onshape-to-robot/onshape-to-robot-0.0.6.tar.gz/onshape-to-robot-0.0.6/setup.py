import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="onshape-to-robot",
    version="0.0.6",
    author="Rhoban team",
    author_email="team@rhoban.com",
    description="Converting OnShape assembly to robot definition (SDF or URDF) through OnShape API ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rhoban/onshape-to-robot/",
    packages=setuptools.find_packages(),
    scripts=['bin/onshape-to-robot', 'bin/onshape-to-robot-bullet'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy", "pybullet", "requests", "commentjson", "colorama", "numpy-stl"
    ],
    python_requires='>=3.6',
)
