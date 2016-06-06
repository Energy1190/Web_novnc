from setuptools import setup, find_packages

version = '0.0.1'
name = 'web_novnc'

setup(name=name,
      version=version,
      description='web_novnc',
      long_description='web_novnc',
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4"
        ],
      keywords='noVNC',
      license='LGPLv3',
      url="https://github.com/Energy1190/Web_novnc",

      packages=['web_novnc'],
      include_package_data=True,
      install_requires=['websockify'],
      zip_safe=False,
    )