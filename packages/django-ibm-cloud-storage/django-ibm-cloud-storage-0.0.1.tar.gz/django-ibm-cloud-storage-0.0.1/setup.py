 #!/usr/bin/env python3
 # -*- coding: utf-8 -*- 
from setuptools import setup, find_packages

setup(name='django-ibm-cloud-storage',
      version='0.0.1',
      description="Connect IBM Cloud Object storage",
      packages=find_packages(),
      keywords='IBM Cloud, storage',
      author='ThomasIBM',
      author_email='guojial@cn.ibm.com',
      license="Apache License, Version 2.0",
      url='https://github.com/ThomasIBM/django-ibm-cloud-storage',
      include_package_data=True,
      zip_safe=False,
)