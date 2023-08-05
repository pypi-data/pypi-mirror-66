from setuptools import setup


def get_file(fn):
    with open(fn) as fp:
        return fp.read()

setup(
    name='pyOnvif',
    version="1.1",
    description='Simple Onvif camera client',
    long_description=(
        get_file('README.rst') + '\n\n' + get_file('HISTORY.rst')
    ),
    author="Pekka Jäppinen",
    maintainer="Petri Savolainen",
    url='https://github.com/koodaamo/pyOnvif',
    install_requires=[],
    extras_require={
        'discovery':  ["WSDiscovery"]
    },
    packages=[
        'pyonvif',
    ],
    include_package_data=True,
    license="GPLv3",
    zip_safe=False,
    keywords='onvif',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points = {'console_scripts': ['pyonvif=pyonvif.cmdline:command']}
)
