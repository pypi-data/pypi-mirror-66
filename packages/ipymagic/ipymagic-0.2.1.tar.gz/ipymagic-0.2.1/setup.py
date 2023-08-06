"""
@author: Youngju Jaden Kim
"""

from setuptools import setup, find_packages


__version__ = '0.2.1'


# Package Description

package_name = 'ipymagic'
package_version = __version__
short_desc = 'Useful tools for Data Scentists'
package_source = '{name}-{version}.tar.gz'.format(
    name=package_name,
    version=package_version,
)
git_url = 'https://github.com/pydemia/ipymagic'
doc_url = 'https://ipymagic.readthedocs.io/en/latest/index.html'
license_str = 'MIT License'



required_packages = [
    'ipython >=7.12.0',
]


setup(
    name=package_name,
    version=package_version,
    description="run python with virtualenv in 'ipython'",
    long_description=short_desc,  # long_desc,
    python_requires='>= 3.5',
    url=doc_url,
    download_url=git_url,
    author='Youngju Jaden Kim',
    author_email='pydemia@gmail.com',
    license=license_str,
    classifiers=[
        # How Mature: 3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        ],
    packages=find_packages(exclude=[
        'contrib',
        # 'docs',
        'tests',
    ]),
    install_requires=required_packages,
    include_package_data=True,
    data_files=[
        # like `jupyter nbextension install --sys-prefix`
        ("share/jupyter/nbextensions/ipymagic", [
            "ipymagic/static/index.js",
        ]),
        # like `jupyter nbextension enable --sys-prefix`
        ("etc/jupyter/nbconfig/notebook.d", [
            "jupyter-config/nbconfig/notebook.d/ipymagic.json"
        ]),
        # like `jupyter serverextension enable --sys-prefix`
        ("etc/jupyter/jupyter_notebook_config.d", [
            "jupyter-config/jupyter_notebook_config.d/ipymagic.json"
        ])
    ],
    zip_safe=False,
    # package_data={package_name: ['*.js', '*.json']},
)
