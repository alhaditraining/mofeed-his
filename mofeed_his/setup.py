"""
Setup script for mofeed_his Frappe app.
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="mofeed_his",
    version="0.0.1",
    description="Hospital Information System for clinics, medical centers, and hospitals in Iraq. Built on ERPNext + Healthcare.",
    author="Al-Mofeed HIS Team",
    author_email="info@mofeed-his.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.10",
)
