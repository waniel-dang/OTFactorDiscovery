import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

from .loss import *

def etgw(L: Loss, x_init, y_init, lr, epsilon=0.001, max_iter = 1000): 
    """
    Explicit Twisted Gradient Descent (ETGD)

    This function implements the ETGD algorithm from
    Essid, Tabak, and Trigila (2019). 
    Notably, the optimization here is: 

            min_x max_y L(x, y)

    Inputs: 
        - L: the loss function, should take x and y as arguments
        - x_init: the initial value of x
        - y_init: the initial value of y
        - lr: the learning rate
        - epsilon: the stopping criterion
        - max_iter: the maximum number of iterations
    
    Outputs: 
        - x: the final value of x
        - y: the final value of y
        - x_list: a list of all x values
        - y_list: a list of all y values
    """
    # set initial values 
    x = x_init
    y = y_init
    # initialize lists to store values
    x_list = [x]
    y_list = [y]
    gradient_norm = [np.linalg.norm(L.gradient(x, y, as_numpy=True))]
    # initialize iteration counter
    i = 0
    # iterate until convergence
    while i < max_iter: 
        grad_L = L.gradient(x, y)
        x = x - lr * grad_L[0]
        y = y + lr * grad_L[1]
        x_list.append(x)
        y_list.append(y)
        gradient_norm.append(np.linalg.norm(L.gradient(x, y, as_numpy=True)))
        if gradient_norm[-1] < epsilon:
            break
        i += 1
    return x, y, x_list, y_list, gradient_norm

def itgw(L: Loss, x_init, y_init, lr, epsilon=0.001, max_iter = 1000):
    """ 
    Implicit Twisted Gradient Descent (ITGD)

    This function implements the ITGD algorithm from
    Essid, Tabak, and Trigila (2019).
    Notably, the optimization here is: 

            min_x max_y L(x, y)
    
    Different from the explicit version, the implicit version 
    attempts to leverage the gradient at the next iteration. 
    Since computing the gradient of the next point is difficult,
    we instead use gradient and hessian of the current point to 
    approximate it. 

    Inputs: 
        - L: the loss function, should take x and y as arguments
        - x_init: the initial value of x
        - y_init: the initial value of y
        - lr: the learning rate
        - epsilon: the stopping criterion
        - max_iter: the maximum number of iterations
    """
    # set initial values 
    x = x_init
    y = y_init
    # initialize lists to store values
    x_list = [x]
    y_list = [y]
    gradient_norm = [np.linalg.norm(L.gradient(x, y, as_numpy=True))]
    # initialize iteration counter
    i = 0
    # iterate until convergence
    while i < max_iter: 
        grad_L = L.gradient(x, y, as_numpy=True)
        hess_L = L.hessian(x, y, as_numpy=True)
        z = np.array([x, y]) - lr * np.linalg.inv(np.array([[1, 0], [0, -1]]) + lr * hess_L) @ grad_L
        x = z[0]
        y = z[1]
        x_list.append(x)
        y_list.append(y)
        gradient_norm.append(np.linalg.norm(L.gradient(x, y, as_numpy=True)))
        if gradient_norm[-1] < epsilon:
            break
        i += 1
    return x, y, x_list, y_list, gradient_norm


def plot_3D(f, x_list = None, y_list = None, grid = [[-50, 50], [-50, 50]], fineness = 0.2): 
    """
    Code adapted from Chapter 12 of "Python Programming and Numerical Methods" by Kong, Siauw, and Bayen. 
    Link: https://pythonnumericalmethods.berkeley.edu/notebooks/chapter12.02-3D-Plotting.html    

    Inputs: 
        - f: the function to plot
        - x_list: a list of x values to plot on the function surface
        - y_list: a list of y values to plot on the function surface
        - grid: the domain of the function
        - fineness: the fineness of the mesh grid
    """
    # set-up 3D plot
    fig = plt.figure(figsize = (12,10))
    ax = plt.axes(projection='3d')
    # define the domain of the function
    x = np.arange(grid[0][0], grid[0][1], fineness)
    y = np.arange(grid[1][0], grid[1][1], fineness)
    # generate the mesh grid for the function
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    surf = ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)
    # visualize the function
    ax.set_xlabel('x', labelpad=20)
    ax.set_ylabel('y', labelpad=20)
    ax.set_zlabel('z', labelpad=20)
    fig.colorbar(surf, shrink=0.5, aspect=8)
    # visualize the path of the optimization algorithm if provided
    if x_list is not None and y_list is not None:
        x_arr = np.array(x_list)
        y_arr = np.array(y_list)
        ax.plot(x_arr, y_arr, zs = f(x_arr, y_arr), zdir = 'z', marker = 'o', color = 'r', linewidth = 2)
    plt.show()

def vis_gradient(y_list, y_axis_title = "Gradient Norm", x_axis_title = "Iteration", x_list = None): 
    """
    Visualize the gradient norm over iterations of an optimization procedure, in order to determine convergence. 

    Inputs: 
        - y_list: a list of gradient norms per iteration. 
        - y_axis_title: the title of the y-axis
        - x_axis_title: the title of the x-axis
        - x_list: a list of iteration numbers.
    """
    if x_list is None: 
        x_list = np.arange(len(y_list))
    y_list = np.array(y_list)
    plt.plot(x_list, y_list)
    plt.xlabel(x_axis_title)
    plt.ylabel(y_axis_title)
    plt.show()