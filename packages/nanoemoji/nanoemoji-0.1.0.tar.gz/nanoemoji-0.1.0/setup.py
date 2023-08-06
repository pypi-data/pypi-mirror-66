# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

setup(
    name="nanoemoji",
    use_scm_version={"write_to": "src/nanoemoji/_version.py"},
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={"console_scripts": ["nanoemoji=nanoemoji.nanoemoji:main"]},
    setup_requires=["setuptools_scm"],
    install_requires=[
        "absl-py>=0.9.0",
        "CairoSVG>=2.4.2",
        "fonttools>=4.8.1",
        "fs==2.4.11",
        "lxml>=4.0",
        "picosvg>=0.3.3",
        "regex>=2020.4.4",
        "skia-pathops>=0.3",
        "ufo2ft>=2.13.0",
        "ufoLib2>=0.6.2",
    ],
    # metadata to display on PyPI
    author="Rod S",
    author_email="rsheeter@google.com",
    description=("Exploratory utility for color fonts"),
)
