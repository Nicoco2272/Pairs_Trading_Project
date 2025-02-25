import statsmodels.tsa.vector_ar.vecm as vecm

def prueba_johansen(data):

    X = data.dropna()

    johansen_test = vecm.coint_johansen(X, det_order=0, k_ar_diff=1)

    print("\n Eigenvalue Statistics:", johansen_test.lr1)
    print("Trace Statistics:", johansen_test.lr2)
    print("Eigenvalues:", johansen_test.eig)
    print("Eigenvectors:")
    print(johansen_test.evec)

    spread_model = johansen_test.evec[:, 0]
    print(f"\nNuestro modelo de spread es:\n u_t = {spread_model[0]:.5f} * x_t {spread_model[1]: .5f} * y_t")


