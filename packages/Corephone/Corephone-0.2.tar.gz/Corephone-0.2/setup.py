from setuptools import setup

def readme():
    with open('README.md') as readme_file:
        README = readme_file.read()
    return README

setup(
    name='Corephone',
    version='0.2',
    description='Useful tools to work with phonetic algorithm in Python',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/SJamii/Phonetic-Algorithm",
    author="Shafayat Jamil",
    author_email="shafayatiuc@gmail.com",
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["Corephone"],
    include_package_data=True,
)
