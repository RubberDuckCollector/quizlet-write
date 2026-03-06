import matplotlib.pyplot as plt

x_axes = [[1, 2, 3, 4], [1, 2], [1]]
y_axes = [[100.0, 100.0, 67.0, 50.0], [100.0, 50.0], [100.0]]

plt.figure(figsize=(8, 5))

# Use zip to pair up the sublists

for i, (x, y) in enumerate(zip(x_axes, y_axes)):
    plt.plot(x, y)

plt.show()

# for i, (x_data, y_data) in enumerate(zip(x_axes, y_axes)):
#     plt.plot(x_data, y_data, label=f'Round {i + 1}', marker='o')  # i think the dots make it more readable across a larger graph

# plt.grid(color = 'grey', linestyle = '-', linewidth = 0.3)

# plt.plot(x_axes, y_axes)
# plt.title(f"Consistency line graph for session starting at {p_start_time}\nPath to cards: {sys.argv[1]}")
# plt.xlabel("# Cards answered")
# plt.ylabel("% Accuracy")
# # plt.ylim(0, 100)  # y axis goes from 0 to 100
# if min_each_round == max_each_round:
#     min_each_round -= 2
# plt.ylim(min_each_round, max_each_round)  # y axis graduates from min percentage achieved to highest percentage achieved
# # MAXIMUM RECURSION DEPTH EXCEEDED ERROR IS HERE
# # TODO: put everything inside if not p_args.test: into its own function
# plt.legend(loc="upper left")  # force the key to appear on the graph, "best" means that matplotlib will put it in the least obtrusive area using its own judgement
# plt.xticks([i for i in range(1, P_NUM_CARDS + 1, 2)])
# # plt.yticks([i for i in range(0, 101, 1)])  # full y axis
# plt.yticks(range(int(p_min_each_round), int(p_max_each_round) + 2, 2))  # only the relevant parts of the graph
# plt.gca().xaxis.set_ticks_position('both')  # puts the x and y axes on the right and top of the graphs, increases readablilty for long graphs
# plt.gca().tick_params(axis='x', labeltop=True, rotation=90)  # enable x axis numbers on the right side of the graph as well as the left, also rotates those numbers by 90 degrees to make them readable
# plt.gca().yaxis.set_ticks_position('both')
# plt.gca().tick_params(axis='y', labelright=True)  # enable y axis numbers on the top of the graph as well as the bottom
# my_modules.plotting.saving_graph()
# # bbox_inches = "tight" removes the bug of the title going offscreen if it's too long
# # https://stackoverflow.com/a/59372013
# plt.savefig(f"{p_this_sessions_dir}/line-graph.pdf", bbox_inches = "tight")
