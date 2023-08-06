import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='xlogger',
    version='0.0.2',
    packages=setuptools.find_packages(),
    url='https://github.com/deadlyedge/xlogger',
    author='xdream',
    author_email='xdream@gmail.com',
    description='a fast, no dependencies log colorizer. with style formatter.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=(
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License'
    )
)
