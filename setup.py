import setuptools

setuptools.setup(
    name='iftttie',
    version='0.1',
    author='Pavel Perestoronin',
    author_email='eigenein@gmail.com',
    description="Because I don't like Home assistant…",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eigenein/iftttie',
    packages=setuptools.find_packages(exclude=['tests']),
    python_requires='>=3.7',
    install_requires=[
        'aiohttp',
    ],
    extras_require={},
    entry_points={
        'console_scripts': ['iftttie = iftttie:main'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Home Automation',
    ],
    zip_safe=True,
)
