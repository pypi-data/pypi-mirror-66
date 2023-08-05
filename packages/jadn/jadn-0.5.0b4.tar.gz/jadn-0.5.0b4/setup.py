import setuptools
with open('README.rst', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='jadn',
    version='0.5.0b4',
    author='David Kemp',
    author_email='dk190a@gmail.com',
    description='JADN schema tools',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/davaya/jadn-software',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
    python_requires='>=3.4',
    install_requires=['jsonschema'],
)