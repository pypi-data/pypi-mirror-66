# coding=utf-8

import setuptools

versiyon = '0.0.56'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='surk',
    version=versiyon,
    description='Surk dilini derleyip çalıştırmak üzere hazırlanıp dağıtılan program.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Emre ŞURK',
    author_email='emre.surk@gmail.com',
    packages=setuptools.find_packages(),
    scripts=['bin/surk'],
    # scripts=['surk/__main__.py'],
    install_requires=[],  # external packages as dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


# python3 setup.py sdist bdist_wheel
# twine upload dist/*
# pip3 uninstall surk && pip3 install surk && surk -y

# rm dist/* && sleep 1 && python3 setup.py sdist bdist_wheel && twine upload dist/* && sleep 5 && pip3 install surk --upgrade --no-cache-dir && surk -y

# python3 setup.py sdist && twine upload dist/*
# pip3 uninstall surk && pip3 install surk && surk -y
