import numpy as np

def calc_laplacian(adj_mat):
    # Calculate the row sum of the adjacency matrix
    # ... the row sum is the (out) degree of the node
    rowsum = adj_mat.sum(axis=1)
    # Construct a degree matrix
    # ... the degree matrix is a diagnal matrix of node degree
    # ... (D = diag(d))
    degree_matrix = np.diag(np.array(rowsum))
    # The Laplacian is defined as 
    # ... the degree matrix minus the adjacency matrix
    # ... (L = D - M)
    laplacian = degree_matrix - adj_mat
    return laplacian

# return the Fiedler value to show strong connection of the array
def fiedler(adj_mat):
    '''
    Return the fiedler value, the second smallest
    eigenvalue of the Laplacian.
    Done by constructing a degree matrix from the 
    adjacency matrix and calculating the Laplacian
    and its eigenvalues.
    '''
    laplacian = calc_laplacian(adj_mat)

    # Calculate the eigenvalues of the Laplacian
    e_values, _ = np.linalg.eig(laplacian)
    # Sort the eigenvalues
    sorted_e_values = sorted(e_values)
    # The Fiedler value is the second smallest eigenvalue of the Laplacian
    return sorted_e_values[1]

# return the Fiedler value to show strong connection of the array
def fiedler_vector(adj_mat):
    '''
    Return the fiedler value, the second smallest
    eigenvalue of the Laplacian.
    Done by constructing a degree matrix from the 
    adjacency matrix and calculating the Laplacian
    and its eigenvalues.
    '''
    laplacian = calc_laplacian(adj_mat)

    # Calculate the eigenvalues of the Laplacian
    e_values, e_vectors = np.linalg.eig(laplacian)
    # Sort the eigenvalues
    sorted_e_values = sorted(list(zip(e_values, e_vectors)),key=lambda o: o[0])
    # The Fiedler value is the second smallest eigenvalue of the Laplacian
    return sorted_e_values[1][1]

def normalized_fiedler(adj_mat):
    '''
    Extends above 
    ... but does so with the normalized adj and Laplacian
    A_n = D^(-1/2) * A * D^(-1/2)
    L = I - A_n
    '''

    # Calculate the row sum of the adjacency matrix
    # ... the row sum is the (out) degree of the node
    rowsum = adj_mat.sum(axis=1)
    # Construct a degree matrix to the power (-1/2)
    # ... the degree matrix is a diagnal matrix of node degree
    # ... (D = diag(d))
    handle_zeros = [0 if e == 0 else e ** (-1/2) for e in rowsum]
    degree_matrix_neg_1_2 = np.diag(np.array(handle_zeros))
    # A_n = D^(-1/2) * A * D^(-1/2)
    norm_adj_mat = np.matmul(degree_matrix_neg_1_2, np.matmul(adj_mat, degree_matrix_neg_1_2))
    # L = I - A_n
    norm_laplacian = np.identity(len(adj_mat)) - norm_adj_mat

    # Calculate the eigenvalues of the Laplacian
    e_values, _ = np.linalg.eig(norm_laplacian)
    # Sort the eigenvalues
    sorted_e_values = sorted(e_values)
    # The Fiedler value is the second smallest eigenvalue of the Laplacian
    return sorted_e_values[1]


def effective_resistance(g,u,v):
    # Reff(e) = (δa − δb)^T * L^+ * (δa − δb).
    size = len(g)
    d_a = np.zeros(size)
    d_a[u] = 1.0
    d_b = np.zeros(size)
    d_b[v] = 1.0
    l_plus = np.linalg.pinv(calc_laplacian(g)) 
    return np.dot((d_a - d_b).T,l_plus.dot((d_a - d_b)))

def leverage_score(g,u,v):
    # ;e = w(a,b) * Reff(e)
    return g[u][v] * effective_resistance(g,u,v)