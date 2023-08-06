import setuptools

import qcrop

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = [line.strip() for line in fh]

setuptools.setup(
    name="qcrop",
    version=qcrop.__version__,
    author=qcrop.__author__,
    author_email="gregory@millasseau.fr",
    description="A basic PyQt image cropping tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gregseth/qcrop",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Multimedia :: Graphics"
    ],
    entry_points={
        'console_scripts': [
            'qcrop = qcrop.__main__:main'
        ]
    }
)
