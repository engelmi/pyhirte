from distutils.core import setup

setup(
    name='pyhirte',
    packages=['pyhirte'],
    version='0.1.0',
    license='GNU',
    description='Python SDK for Hirte',
    author='Michael Engel',
    author_email='mengel@redhat.com',
    url='https://github.com/engelmi/pyhirte',
    download_url='',
    keywords=['Hirte', 'systemd', 'D-Bus', 'multi-node'],
    install_requires=[
        'dasbus>=1.7',
        'vext>=0.7.6',
        'vext.gi>=0.7.4',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: multi-node controller',
        'License :: OSI Approved :: GNU License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
