import setuptools


#try:
#    from setuptools import setup, find_packages
#except ImportError:
#    from distils.core import setup, find_packages



setuptools.setup(
    name="MCRLLM",
    version="0.0.71",
    author="Ryan Gosselin",
    author_email="ryan.gosselin@usherbrooke.ca",
    packages=["MCRLLM"],
    description="MCRLLM: Multivariate Curve Resolution by Log-Likelihood Maximization",
    long_description="MCRLLM: Multivariate Curve Resolution by Log-Likelihood Maximization.\
    \n\nX = CS\
    \nwhere\
    \nX(nxk): Spectroscopic data where n spectra acquired over k energy levels\
    \nC(nxa): Composition map based on a MCRLLM components\
    \nS(axk): Spectra of the a components as computed by MCRLLM\
    \n\n# Method first presented in\
    \nLavoie F.B., Braidy N. and Gosselin R. (2016) Including Noise Characteristics in MCR to improve Mapping and Component Extraction from Spectral Images, Chemometrics and Intelligent Laboratory Systems, 153, 40-50.\
    \n\n# Input data\
    \nAlgorithm is designed to treat 2D data X(nxk) where n spectra acquired over k energy levels.\
    \nA 3D spectral image X(n1,n2,k) can be reshaped to a 2D matrix X(n1xn2,k) prior to MCRLLM analysis. Composition maps can then be obtained by reshaping C(n1xn2,a) into 2D chemical maps C(n1,n2,a).\
    \n# Input and output arguments\
    \nMCRLLM requires 4 inputs :\
    \n 1. X data\
    \n 2. Number of MCRLLM components to compute (nb_c)\
    \n 3. Method of initialization:\
    \n      -'Kmeans': Kmeans\
    \n      -'NFindr': N-FINDR\
    \n      -'ATGP': Automatic Target Generation Process\
    \n      -'FIPPI': Fast Iterative Pixel Purity Index\
    \n 4. Number of MCRLLM iterations.\
    \n# Example\
    \n#Compute MCRLLM on X using 7 components.\
    \n\n#First obtain X data. Spectroscopic data is available in the zip file of this Pypi module (data_EELS.txt). It represents EELS (Electron Energy Loss Spectroscopy). This data consists of 100 spectra acquired over 2048 energy levels.\
    \n\nimport MCRLLM as mcrllm\
    \nimport matplotlib.pyplot as plt\
    \nimport numpy as np\
    \n\nX = np.loadtxt('data_EELS.txt', delimiter=',')\
    \n\nnb_c = 7\
    \ndecomposition = mcrllm(X,nb_c,init = 'Kmeans', nb_iter=20)\
    \nC = decomposition.C\
    \nS = decomposition.S\
    \nplt.figure();plt.plot(S.T)\
    \nplt.figure();plt.plot(C)\
    \n# Compatibility\
    \nMCRLLM tested on Python 3.7 using the following modules:\
    \nNumpy 1.17.2\
    \nScipy 1.3.1\
    \nSklearn 0.21.3\
    \nPysptools 0.15.0\
    \nTqdm 4.36.1",
    long_description_content_type="text/markdown",
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)