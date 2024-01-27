#
# b u g . p y
#

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import BboxImage

if __name__ == '__main__':
    fig,ax = plt.subplots()

    txt = ax.text(0.5, 0.5, "test", size=30, ha="center", color="w")
    ax.add_artist(
        BboxImage(txt.get_window_extent, data=np.arange(256).reshape((1, -1))))

    plt.show()