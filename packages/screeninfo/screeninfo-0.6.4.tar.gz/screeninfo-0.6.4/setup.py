from distutils.core import setup

setup(
    name="screeninfo",
    packages=["screeninfo", "screeninfo.enumerators"],
    version="0.6.4",
    description="Fetch location and size of physical screens.",
    author="rr-",
    author_email="rr-@sakuya.pl",
    url="https://github.com/rr-/screeninfo",
    keywords=["screen", "monitor", "desktop"],
    classifiers=[],
    install_requires=[
        "dataclasses",
        'Cython ; platform_system=="darwin"',
        'pyobjus ; platform_system=="darwin"',
    ],
)
