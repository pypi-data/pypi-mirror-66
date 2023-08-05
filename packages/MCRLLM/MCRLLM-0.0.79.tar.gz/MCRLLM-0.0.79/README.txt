MCRLLM
Multivariate Curve Resolution by Log-Likelihood Maximization

Available at www.pypi.org


X = CS
where
X(nxk): Spectroscopic data where n spectra acquired over k energy levels
C(nxa): Composition map based on a MCRLLM components
S(axk): Spectra of the a components as computed by MCRLLM


METHOD FIRST PRESENTED IN
Lavoie F.B., Braidy N. and Gosselin R. (2016) Including Noise Characteristics in MCR to improve Mapping and Component Extraction from Spectral Images, Chemometrics and Intelligent Laboratory Systems, 153, 40-50.


INPUT DATA
Algorithm is designed to treat 2D data X(nxk) where n spectra acquired over k energy levels.
A 3D spectral image X(n1,n2,k) can be reshaped to a 2D matrix X(n1xn2,k) prior to MCRLLM analysis. Composition maps can then be obtained by reshaping C(n1xn2,a) into 2D chemical maps C(n1,n2,a).


INPUT ARGUMENTS
MCRLLM requires 4 inputs :
1. X data
2. Number of MCRLLM components to compute
3. Method of initialization:
'Kmeans': Kmeans
'NFindr': N-FINDR
'ATGP': Automatic Target Generation Process
'FIPPI': Fast Iterative Pixel Purity Index
4. Number of MCRLLM iterations


EXAMPLES
Two full examples, along with datasets, are provided in 'Download Files'.
Please refer to 'MCRLLM_example.pdf' for full details.
- Example 1: 1D spectral linescan of EELS data.
- Example 2: 2D spectral image of XPS data.


COMPATIBILITY
MCRLLM tested on Python 3.7 using the following modules:
- Numpy 1.17.2
- Scipy 1.3.1
- Sklearn 0.21.3
- Pysptools 0.15.0
- Tqdm 4.36.1


CONTACT INFO
Ryan Gosselin, Université de Sherbrooke, ryan.gosselin@usherbrooke.ca




-- Ryan Gosselin, April 15th, 2020