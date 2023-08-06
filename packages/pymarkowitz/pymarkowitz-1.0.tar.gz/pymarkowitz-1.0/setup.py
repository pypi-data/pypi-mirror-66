from setuptools import setup

setup(name='pymarkowitz',
      version='1.0',
      description='pymarkowitz',
      url='https://github.com/johnsoong216/pymarkowitz',
      download_url='https://github.com/johnsoong216/pymarkowitz/archive/v1.0.tar.gz',
      author='johnsoong216',
      author_email='johnsoong216@hotmail.com',
      license='MIT',
      keywords=['portfolio-optimization', 'finance', 'mean-variance-optimization'],
      install_requires=["numpy", "pandas", "pandas-datareader", "sklearn", "seaborn", "plotly", "matplotlib"],
      zip_safe=False)

