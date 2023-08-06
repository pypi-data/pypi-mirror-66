from setuptools import setup
from setuptools import find_packages
setup(
    name='ml_automated_123',
    version='1.0',
    description='Automated machine learning',
    long_description=open('README.md').read(),
    author='Noah Weber',
    author_email='noahweber53@ygmail.com',
    url='https://github.com/noahweber1/ml_automated_123',
    download_url='https://github.com/noahweber1/ml_automated_123',
    install_requires=['hyperopt>=0.2',
                      'networkx>=2.1',
                      'numpy>=1.17',
                      'pandas>=0.24',
                      'scikit-learn>=0.22',
                      'xgboost>=0.9'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    keywords='Auto_ML',
    packages=find_packages()
)
