import matplotlib.pyplot as plt
import numpy as np
import pandas

Z = np.array([[0,1,1,0],
     [0,0,1,0],
     [0,1,0,1],
     [1,0,1,1]])


def plt_color_mesh(data=Z):
    fig, ax0 = plt.subplots(1, 1)
    
    c = ax0.pcolor(data)
    ax0.set_title('default: no edges')
    
    fig.tight_layout()
    plt.show()

plt_color_mesh(Z)