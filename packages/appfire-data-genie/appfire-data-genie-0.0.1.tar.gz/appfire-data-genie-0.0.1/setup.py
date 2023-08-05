#
#  Copyright (c) 2020 Appfire Technologies, Inc.
#  All rights reserved.
#  This software is licensed under the provisions of the "Bob Swift Atlassian Add-ons EULA"
#  (https://bobswift.atlassian.net/wiki/x/WoDXBQ) as well as under the provisions of
#  the "Standard EULA" from the "Atlassian Marketplace Terms of Use" as a "Marketplace Product"
#  (http://www.atlassian.com/licensing/marketplace/termsofuse).
#  See the LICENSE file for more details.
#

"""Setup script for create-appfire-app"""

import os.path
from setuptools import setup

# # The directory containing this file
# HERE = os.path.abspath(os.path.dirname(__file__))
#
# # README file contents
# with open(os.path.join(HERE, "README.md")) as fid:
#     README = fid.read()
#
# # setup()
setup(
    name="appfire-data-genie",
    version="0.0.1",
    description="Generates random data for Appfire P2 apps",
    long_description="Generates random data for Appfire P2 apps",
    long_description_content_type="text/plain",
    url="",
    author="Lava Kumar Dukanam",
    author_email="lavakumar.dukanam@appfire.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["adg"],
    include_package_data=True,
    install_requires=[
       "click", "jaydebeapi", "questionary"
    ],
    entry_points={"console_scripts": ["adg=adg.execute:process"]},
)
