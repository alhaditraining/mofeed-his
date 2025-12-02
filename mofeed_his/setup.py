from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="mofeed_his",
    version="0.0.1",
    description="Al-Mofeed Hospital Information System",
    author="Al-Mofeed HIS Team",
    author_email="info@mofeed-his.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
