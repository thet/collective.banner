from setuptools import setup, find_packages

version = '1.0dev'

setup(
    name='collective.banner',
    version=version,
    description="Add-on for having Collections' results presented as a nice carousel",
    long_description=open("README.rst").read() + "\n" + open("CHANGES.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone zope collection carousel',
    author='Johannes Raggam',
    author_email='raggam-nl@adm.at',
    url='https://github.com/thet/collective.banner',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.portlet.collection',
    ],
    extras_require={'test': [
        'Products.PloneTestCase',
        'collective.testcaselayer'
    ]},
    entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
    """,
)
