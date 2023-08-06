import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='vincenty-cuda-nns',
    version='0.2.2',
    author='Serhii Hulko',
    author_email='felytic@gmail.com',
    description='Nearest neighbor search on Earth\'s surface with a GPU',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/eos-vision/vincenty-cuda-nns',
    packages=['vincenty_cuda_nns'],
    install_requires=[
        'numba==0.48.0',
        'cuda-friendly-vincenty==0.1.2',
        'numpy==1.18.2',
    ],
    license='GPLv3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: '
        'GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
    ],
)
