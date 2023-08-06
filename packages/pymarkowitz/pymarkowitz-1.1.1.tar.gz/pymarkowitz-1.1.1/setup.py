from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pymarkowitz',
      version='1.1.1',
      description='pymarkowitz',
      url='https://github.com/johnsoong216/pymarkowitz',
      download_url='https://github.com/johnsoong216/pymarkowitz/archive/v1.0.tar.gz',
      author='johnsoong216',
      author_email='johnsoong216@hotmail.com',
      license='MIT',
      keywords=['portfolio-optimization', 'finance', 'mean-variance-optimization'],
      install_requires=["numpy", "pandas", "pandas-datareader", "sklearn", "seaborn", "plotly", "matplotlib", "bt"],
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            "Intended Audience :: Financial and Insurance Industry",
            "Intended Audience :: Education"
      ],
      zip_safe=False)


