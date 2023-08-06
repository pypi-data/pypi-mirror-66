#-*- coding:utf-8 -*-
 
#############################################
# File Name: setup.py
# Author: Frank Lee
# Mail: frankleecsz@gmail.com
# Created Time: 2020-01-18
#############################################
 
 
from setuptools import setup, find_packages
 
setup(
  name = "teny",
  version = "0.1.3",
  keywords = ["pip", "dnn", "DeepLearning", "MachineLearning"],
  description = "dnn framework",
  long_description = "simple deep learning framework in numpy for demo.",
  license = "MIT Licence",
 
  url = "https://github.com/FrankLeeC/MachineLearning/teny",
  author = "FrankLee",
  author_email = "frankleecsz@gmail.com",
 
  packages = find_packages(),
  include_package_data = True,
  platforms = "any",
  install_requires = ['numpy']
)