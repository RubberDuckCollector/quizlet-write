import matplotlib.pyplot as plt
import numpy as np

def make_line_graph():
    # importing package

    # create data
    x = [1,2,3,4,5]
    y = [3,3,3,3,3]

    # plot lines
    plt.plot(x, y, label = "line 1", linestyle="-")
    plt.plot(y, x, label = "line 2", linestyle="--")
    plt.plot(x, np.sin(x), label = "curve 1", linestyle="-.")
    plt.plot(x, np.cos(x), label = "curve 2", linestyle=":")
    plt.legend()
    plt.show()


def main():
    make_line_graph()


if __name__ == "__main__":
    main()
