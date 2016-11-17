from pyspark.sql import SparkSession
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from numpy.linalg import eigh

import sys

def preparePlot(xticks, yticks, figsize=(10.5, 6), hideLabels=False, gridColor='#999999',
                gridWidth=1.0):
    """Template for generating the plot layout."""
    plt.close()
    fig, ax = plt.subplots(figsize=figsize, facecolor='white', edgecolor='white')
    ax.axes.tick_params(labelcolor='#999999', labelsize='10')
    for axis, ticks in [(ax.get_xaxis(), xticks), (ax.get_yaxis(), yticks)]:
        axis.set_ticks_position('none')
        axis.set_ticks(ticks)
        axis.label.set_color('#999999')
        if hideLabels: axis.set_ticklabels([])
    plt.grid(color=gridColor, linewidth=gridWidth, linestyle='-')
    map(lambda position: ax.spines[position].set_visible(False), ['bottom', 'top', 'left', 'right'])
    return fig, ax

def pca(data, k=2):
    """Computes the top `k` principal components, corresponding scores, and all eigenvalues.

    Note:
        All eigenvalues should be returned in sorted order (largest to smallest). `eigh` returns
        each eigenvectors as a column.  This function should also return eigenvectors as columns.

    Args:
        data (RDD of np.ndarray): An `RDD` consisting of NumPy arrays.
        k (int): The number of principal components to return.

    Returns:
        tuple of (np.ndarray, RDD of np.ndarray, np.ndarray): A tuple of (eigenvectors, `RDD` of
            scores, eigenvalues).  Eigenvectors is a multi-dimensional array where the number of
            rows equals the length of the arrays in the input `RDD` and the number of columns equals
            `k`.  The `RDD` of scores has the same number of rows as `data` and consists of arrays
            of length `k`.  Eigenvalues is an array of length d (the number of features).
    """
    covAuto = estimateCovariance(data)
    eigVals, eigVecs = eigh(covAuto)
    # Use np.argsort to find the top eigenvector based on the largest eigenvalue
    indsAscending = np.argsort(eigVals)
    inds = indsAscending[::-1]
    # Return the `k` principal components, `k` scores, and all eigenvalues
    topComponents = np.array([eigVecs[:, j] for j in inds[0:k]]).T
    scores = data.map(lambda obs: np.dot(obs, topComponents))
    sortedEigVals = np.array([eigVals[c] for c in inds[:]])
    return (topComponents, scores, sortedEigVals)

def estimateCovariance(data):
    """Compute the covariance matrix for a given rdd.

    Note:
        The multi-dimensional covariance array should be calculated using outer products.  Don't
        forget to normalize the data by first subtracting the mean.

    Args:
        data (RDD of np.ndarray):  An `RDD` consisting of NumPy arrays.

    Returns:
        np.ndarray: A multi-dimensional array where the number of rows and columns both equal the
            length of the arrays in the input `RDD`.
    """
    n = data.count() + .0
    featuresMean = data.sum() / n
    dataZeroMean = data.map(lambda obs: obs - featuresMean)
    dataCov = (dataZeroMean
                 .map(lambda obs: np.outer(obs, obs))
                 .sum() / n
                )
    return dataCov

def parse(line):
    """Parse the raw data into a (`tuple`, `np.ndarray`) pair.

    Note:
        You should store the pixel coordinates as a tuple of two ints and the elements of the pixel intensity
        time series as an np.ndarray of floats.

    Args:
        line (str): A string representing an observation.  Elements are separated by spaces.  The
            first two elements represent the coordinates of the pixel, and the rest of the elements
            represent the pixel intensity over time.

    Returns:
        tuple of tuple, np.ndarray: A (coordinate, pixel intensity array) `tuple` where coordinate is
            a `tuple` containing two values and the pixel intensity is stored in an NumPy array
            which contains 240 values.
    """
    lineSplit = line.split(' ')
    point = (int(lineSplit[0]), int(lineSplit[1]))
    intensityArray = np.array(lineSplit[2:]).astype(np.float)
    return (point, intensityArray)

def rescale(ts):
    """Take a np.ndarray and return the standardized array by subtracting and dividing by the mean.

    Note:
        You should first subtract the mean and then divide by the mean.

    Args:
        ts (np.ndarray): Time series data (`np.float`) representing pixel intensity.

    Returns:
        np.ndarray: The times series adjusted by subtracting the mean and dividing by the mean.
    """
    mean = ts.mean() + .0
    return (ts - mean) / mean

def polarTransform(scale, img):
    """Convert points from cartesian to polar coordinates and map to colors."""
    from matplotlib.colors import hsv_to_rgb

    img = np.asarray(img)
    dims = img.shape

    phi = ((np.arctan2(-img[0], -img[1]) + np.pi/2) % (np.pi*2)) / (2 * np.pi)
    rho = np.sqrt(img[0]**2 + img[1]**2)
    saturation = np.ones((dims[1], dims[2]))

    out = hsv_to_rgb(np.dstack((phi, saturation, scale * rho)))

    return np.clip(out * scale, 0, 1)

usePC1 = int(sys.argv[1])-1
usePC2 = int(sys.argv[2])-1
nComponents = usePC2 + 1

spark = SparkSession\
    .builder.config("spark.port.maxRetries", "100")\
    .appName("SparkFish")\
    .getOrCreate()

sc = spark.sparkContext

#The input file is located at:
inputFile = '/cvmfs/softdrive.nl/maithilk/pbs-course-data/neuro.txt'
lines = sc.textFile(inputFile)

# Check that everything loaded properly
assert len(lines.first()) == 1397
assert lines.count() == 46460


rawData = lines.map(parse)
rawData.cache()
entry = rawData.first()
#print 'Length of movie is {0} seconds'.format(len(entry[1]))


#print ('DEBUG!!')
#print rawData.count()

# print 'Number of pixels in movie is {0:,}'.format(rawData.count())


mn = rawData.flatMap(lambda (_, intensities): intensities).min()
mx = rawData.flatMap(lambda (_, intensities): intensities).max()

#print mn, mx

scaledData = rawData.mapValues(lambda v: rescale(v))
mnScaled = scaledData.map(lambda (k, v): v).map(lambda v: min(v)).min()
mxScaled = scaledData.map(lambda (k, v): v).map(lambda v: max(v)).max()
#print mnScaled, mxScaled

# #### We now have a preprocessed dataset with $\scriptsize n = 46460$ pixels and $\scriptsize d = 240$ seconds of time series data for each pixel.  We can interpret the pixels as our observations and each pixel value in the time series as a feature.  We would like to find patterns in brain activity during this time series, and we expect to find correlations over time.  We can thus use PCA to find a more compact representation of our data and allow us to visualize it.
#
# #### Use the `pca` function from Part (2a) to perform PCA on the preprocessed neuroscience data with $\scriptsize k = 3$, resulting in a new low-dimensional 46460 by 3 dataset.  The `pca` function takes an RDD of arrays, but `data` is an RDD of key-value pairs, so you'll need to extract the values.

componentsScaled, scaledScores, eigenvaluesScaled = pca(
    scaledData.map(lambda (_, intensities): intensities), nComponents)


# #### **Visualization 7: Top two components as images**
# #### Now, we'll view the scores for the top two component as images.  Note that we reshape the vectors by the dimensions of the original image, 230 x 202.
# #### These graphs map the values for the single component to a grayscale image.  This provides us with a visual representation which we can use to see the overall structure of the zebrafish brain and to identify where high and low values occur.  However, using this representation, there is a substantial amount of useful information that is difficult to interpret.  In the next visualization, we'll see how we can improve interpretability by combining the two principal components into a single image using a color mapping.

# In[39]:

scoresScaled = np.vstack(scaledScores.collect())
imagesScaled = []
for i in range(nComponents):
    imageIScaled = scoresScaled[:,i].reshape(230, 202).T
    imagesScaled.append(imageIScaled)


# Use the same transformation on the image data
# Try changing the first parameter to lower values
brainmap = polarTransform(2.0, [imagesScaled[usePC1], imagesScaled[usePC2]])

# generate layout and plot data
fig, ax = preparePlot(np.arange(0, 10, 1), np.arange(0, 10, 1), figsize=(9.0, 7.2), hideLabels=True)
ax.grid(False)
image = plt.imshow(brainmap,interpolation='nearest', aspect='auto')
plt.savefig('PC%d-%d.png'%(usePC1+1,usePC2+1))
