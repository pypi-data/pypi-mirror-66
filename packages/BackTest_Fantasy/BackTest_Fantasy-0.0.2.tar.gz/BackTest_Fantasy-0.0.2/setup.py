
from setuptools import setup

setup(
    name='BackTest_Fantasy',
    packages=['BackTest'],
    description="BackTest",
    version='0.0.2',
    author='Fantasy',
    author_email='toubiana.nathan@gmail.com',
    keywords=['machine-learning', 'scikit-learn', 'training-time'],
    tests_require=[
    'pytest',
    'pytest-cov',
    'pytest-sugar'
    ],
    package_data={
    # include json and pkl files
    '': ['*.json', 'models/*.pkl', 'models/*.json'],
    },
    include_package_data=True,
    python_requires='>=3'
    )