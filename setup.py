import setuptools

setuptools.setup(
    name='iftttie',
    version='0.8',
    author='Pavel Perestoronin',
    author_email='eigenein@gmail.com',
    description='Yet another home assistant',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eigenein/iftttie',
    packages=setuptools.find_packages(exclude=['tests']),
    package_data={
        '': ['*'],
    },
    python_requires='>=3.7',
    install_requires=[
        'aiohttp',
        'aiohttp_jinja2',
        'click',
        'loguru',
        'pygal',
        'ujson',
        'aiohttp-sse-client',
        'argon2_cffi',
        'aioping',
    ],
    extras_require={
        'dev': ['pip-tools', 'isort', 'ipython', 'twine', 'flake8'],
    },
    entry_points={
        'console_scripts': [
            'iftttie = iftttie.__main__:main',
            'iftttie.utils = iftttie.utils:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
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
