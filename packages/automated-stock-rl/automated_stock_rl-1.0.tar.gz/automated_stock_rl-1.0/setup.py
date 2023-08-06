from setuptools import setup
from setuptools import find_packages
setup(
    name='automated_stock_rl',
    version='1.0',
    description='Automated Stock Reinforcement Learning',
    long_description=open('README.md').read(),
    author='Noah Weber',
    author_email='noahweber53@ygmail.com',
    url='https://github.com/noahweber1/automated_stock_rl',
    download_url='https://github.com/noahweber1/automated_stock_rl',
    install_requires=['time',
                      'random',
                      'chainer',
                      'copy',
                      'pandas',
                      'numpy','matplotlib'],
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
