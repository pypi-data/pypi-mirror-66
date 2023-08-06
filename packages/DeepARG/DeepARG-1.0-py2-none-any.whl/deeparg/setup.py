from setuptools import setup, find_packages

setup(
    name='DeepARG',
    version='2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'BioPython',
        'ete3',
        'h5py',
        'tqdm',
        'pandas',
        'networkx'
    ],
    entry_points='''
        [console_scripts]
        deeparg=GeneTools.entry:cli
    ''',
)
