import setuptools

setuptools.setup(
    name="paiktj",
    version="0.0.4",
    # license='MIT',
    author="paiktj",
    author_email="paiktj@snu.ac.kr",
    description="custom for me",
    long_description=open('README.md').read(),
    # url="github url 등",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)

'''
import setuptools

setuptools.setup(
    name="패키지 이름",
    version="버전",
    license='MIT',
    author="패키지 제작자 이름",
    author_email="패키지 제작자 이메일",
    description="패키지 요약",
    long_description=open('README.md').read(),
    url="github url 등",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)

pip install setuptools wheel
python -m pip install --user --upgrade setuptools wheel
python setup.py sdist bdist_wheel
dist 폴더 밑에 .tar.gz 파일과 .whl 파일이 생성되면 성공
pip install twine
python -m twine upload dist/*
'''
