import setuptools

def readme():
    with open('README.md') as f:
        README=f.read()
    return README

setuptools.setup(

    name='Feature Selction-Ranking Algorithms',
    version='1.0.0',
    author='Lakshajyoti Paul',
    author_email='lakshajyotipaul777@gmail.com',
    license='MIT',
    description='A Feature Selection and Feature ranking Package that can be used to select and rank features in datasets',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['fsfr']
)
