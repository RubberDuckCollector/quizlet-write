import matplotlib.pyplot as plt

def make_line_graph():
    # this is a line graph of x versus y
    plt.plot([1, 2, 3, 4], [12, 3, 123, 3214])
    plt.ylabel("some measuremetn")
    plt.xlabel("some time")
    plt.savefig("testimg.pdf", bbox_inches="tight")
    # .show() frees the plot from memory, so saving the fig after doing so will result in a blank white file
    plt.show()
    plt.close()


def main():
    make_line_graph()


if __name__ == "__main__":
    main()
