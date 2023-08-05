from setuptools import setup

setup(
    name = 'sphinx-osgeocn-theme',
    version = '0.1.0',
    author = 'OSGeo CN',
    author_email= '486936@qq.com',
    url="https://github.com/osgeocn/sphinx-osgeocn-theme",
    docs_url="https://github.com/osgeocn/sphinx-osgeocn-theme/",
    description='Sphinx Bootstrap4 Theme of OSGeo China Chapter Documents',
    py_modules = ['sphinx_osgeocn_theme'],
    packages = ['themes'],
    include_package_data=True,
    license= 'MIT License',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        "Topic :: Internet",
        "Topic :: Software Development :: Documentation"
    ],
)

