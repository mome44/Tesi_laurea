Ranking
In paper 4 there is the search for the optimal value of the ranking that is able to obtain the best performances. More specifically they selected the rank that was able to explain 90% of the variance in the weight matrices. 

Matrices can be decomposed into eigen values and eigenvectors according to the singular value decomposition.  SVD.

Let's suppose they have a dimension d. So theoretically they should have d eigenvalues λ. 

When we do the SVD the middle matrix (Sigma) which contains the singular values ordered by importance (size). 

The singular values are the square root of the eigenvalues, so in order to compute which ranking explains 90 percent of the matrix one should have that the sum of the square of the first r squared singular values (eigenvalues) is equal greater to 0.9 multiplied by the total sum. 

Since the first ones are the most relevant even small r can cover up to 40% of the whole variance. 

**So this variance is not the probabilistic variance.**

Trego23i!



