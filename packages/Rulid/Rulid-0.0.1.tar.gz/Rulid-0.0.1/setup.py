from distutils.core import setup

setup(
    name="Rulid",
    py_modules=["rulid"],
    entry_points={"console_scripts": ["slowloris=rulid:main"]},
    version="0.0.1",
    description="Build system and package manager for Rust",
    author="Gokberk Yaltirakli",
    author_email="opensource@gkbrk.com",
    url="https://github.com/gkbrk/rulid",
    keywords=["rust", "build", "package"],
    license="GPL-3",
)
