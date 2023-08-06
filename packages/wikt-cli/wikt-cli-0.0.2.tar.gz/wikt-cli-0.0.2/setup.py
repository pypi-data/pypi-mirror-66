from setuptools import setup, find_packages

setup(
    name='wikt-cli',
    version='0.0.2',
    description='An English Wiktionary frontend for CLI.',
    long_description=open('./README.md').read(),
    long_description_content_type='text/markdown',
    keywords='wiktionary dictionary cli',
    license='MIT',
    url='https://git.sr.ht/~fkfd/wikt-cli',
    author='fakefred',
    author_email='fkfd@macaw.me',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wikt=wikt.__main__:main'
        ]
    },
    python_requires='>=3.5',
    install_requires=['wiktionaryparser', 'colored'],
    project_urls={
        'LiberaPay': 'https://liberapay.com/fakefred/donate'
    }
)
