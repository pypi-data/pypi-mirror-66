from setuptools import setup, find_packages

setup(
    name='DeepARG',
    version='1.0',
    author='Gustavo Arango',
    packages=find_packages(
        exclude=(".git", "data")
    ),
    include_package_data=True,
    package_data={},
    install_requires=[
        'BioPython',
        'ete3',
        'tqdm',
        'numpy==1.10.4',
        'scipy==0.16.1',
        'nolearn==0.6',
        'lasagne==0.1',
        'scikit-learn==0.19.1',
        'theano==0.8.2',
        'requests',
        'wget'
    ],
    python_requires="==2.7.16",
    entry_points='''
        [console_scripts]
        deeparg=deeparg.entry:main
    ''',
)
