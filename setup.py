# noqa: D100
from pathlib import Path

import setuptools

from ims_envista.version import __version__

# Read the README file content using pathlib and a context manager
long_description = Path("README.md").read_text(encoding="utf-8").strip()

setuptools.setup(name="ims_envista",
                 version=__version__,
                 long_description_content_type="text/markdown",
                 description="Israel Meteorological Service Envista API wrapper package",
                 long_description=long_description,
                 author="Guy Khmelnitsky",
                 author_email="guykhmel@gmail.com",
                 url="https://github.com/GuyKh/py-ims-envista",
                 packages=setuptools.find_packages(),
                 python_requires=">=3.10",
                 install_requires=["aiohttp", "async_timeout"],
                 license="MIT License",
                 zip_safe=False,
                 keywords=["ims","weatheril","Israel Meteorological Service","Meteorological Service","weather"],
                 classifiers=[    "Intended Audience :: Developers",
                            "Topic :: Software Development :: Build Tools",
                            "License :: OSI Approved :: MIT License",
                            "Programming Language :: Python :: 3.10",
                            "Programming Language :: Python :: 3.11",
                            "Programming Language :: Python :: 3.12",
                            "Natural Language :: English",
                            "Operating System :: OS Independent"])
