from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="mofeed_his",
    version="0.0.1",
    description="Hospital Information System for clinics and hospitals in Iraq",
    author="Al-Mofeed",
    author_email="info@mofeed.iq",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
