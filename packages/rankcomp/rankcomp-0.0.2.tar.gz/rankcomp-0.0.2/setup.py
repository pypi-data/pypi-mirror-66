#!/bin/python

import os
import setuptools
import rankcomp

this_dir=os.getcwd()
pj=lambda *path: os.path.abspath(os.path.join(*path))
#if not os.path.exists(pj(this_dir,"rankcomp/setting.py")):
    

##read file
read_file=lambda file_name: open(pj(this_dir,file_name),"r").read()
##get relation
read_req=lambda file_name: [line.strip() for line in read_file(file_name).splitlines() if not line.startswith("#")]

setuptools.setup(
    name="rankcomp",
    version="0.0.2",
    python_requires='>=3.6',
    description="high fided extraction of differential expression genes without considering the batch effects",
    long_description=read_file("README.md"),
    #long_description_content_typ="text/markdown",
    author="Terminator Jun",
    author_email="2300869361@qq.com",
    url="https://github.com/SpiderClub/haipproxy",
    install_requires=read_req("rankcomp/needed_packages.txt"),
    license="MIT",
    packages=setuptools.find_packages(),
    #packages=["os","numpy","time","scipy","pandas","matplotlib","statsmodels","fisher","sklearn"],
    keywords=["rank","DEG","batch-effect","rankcomp"],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent",
    ], 

)

