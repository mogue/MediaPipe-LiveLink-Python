from distutils.core import setup

setup(
    # Application name:
    name="MediaPipe-LiveLink-Python",
    
    # Version number (initial):
    version="0.1.0",
    
    # Application author details:
    author="mogue",
    author_email="name@addr.ess",
    
    # Packages
    packages=["src"],
    
    # Include additional files into the package
    include_package_data=True,
    
    # Details
    url="http://pypi.python.org/pypi/MyApplication_v010/",
    
    # license="LICENSE.txt",
    description="WebCam MediaPipe to LiveLink data.",
    
    long_description=open("README.md").read(),
    
    # Dependent packages (distributions)
    install_requires=[
        "numpy",
        "opencv-python",
        "mediapipe",
        "scipy",
    ],
)