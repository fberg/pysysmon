from setuptools import setup

setup(name='PySysMon',
      description='System monitoring application writting in Python',
      version='0.1',
      url='https://github.com/fberg/pysysmon',
      author='Franz Berger',
      license='GPL-3',
      packages=[
          'pysysmon',
          'pysysmon.monitors'
      ],
      scripts=['bin/pysysmon'],
      install_requires=[
      ]
)
