import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
from IPython.display import Image, display

from Primitives.map import Map
from Primitives.node import Node

# color pool for coloring different agents,
# if number of agents is more than number of colors here
# then it will just cycle through these colors
pallet = [
    "#DF4003",  # red
    "#1998FF",  # blue
    "#9437FF",  # purple
    "#00FDFF",  # cyan
    "#00F900",  # green
    "#FF9300",  # orange
    "#FFFB00",  # yellow
    "#FF40FF",  # magenta
    "#C29B3B",  # brownish
    "#FF8AD8",  # pinky
    "#F0B81E",  # ginger
    "#32473B",  # greyish
    "#393C47",  # actual grey
    "#160000",  # black, indicator that we are out of colors
]


def animate_solutions(map: Map, node: Node, *, show=True, wall_color='#2776B3'):
    fpe = 15  # frames per one edge passing to smooth out animation

    fig, ax = plt.subplots()
    plt.tight_layout()
    fig.subplots_adjust(0.01, 0, 0.99, 1, 0, 0)
    ax.axis([0, map.width, 0, map.height + 0.5])
 
    ax.set_axis_off()
    ax.set_aspect("equal")

    for (y, x), cell in np.ndenumerate(map.cells):
        if cell:  # cell is not traversable
            block = Rectangle((x, y), 1, 1, color=wall_color)
            ax.add_patch(block)

    time_label = ax.text(0, map.height + 0.3, "t = 0",
                         color="#000000", fontsize=17, fontdict={'fontname':'Chalkboard'})

    agents = []

    def init():
        for i, solution in enumerate(node.solutions):
            x, y = solution.get_point_at(0)
            agent = Circle((x + 0.5, y + 0.5), radius=0.3,
                           color=pallet[i % len(pallet)])
            _ = ax.add_patch(agent)
            agents.append(agent)

    def update(time):
        for agent, solution in zip(agents, node.solutions):
            now, past = np.modf(time)  # decimal and integer part
            future = np.ceil(time)

            x0, y0 = solution.get_point_at(int(past))
            x1, y1 = solution.get_point_at(int(future))

            x = x0 + now * (x1 - x0)
            y = y0 + now * (y1 - y0)

            agent.center = x + 0.5, y + 0.5
            time_label.set_text(f"t = {past}")

    # this is some stuff .....
    frames = np.zeros(node.time * fpe * 2 + fpe)
    for f in range(node.time * fpe * 2 + fpe):
        cell = f // fpe
        if cell % 2 == 0:
            frames[f] = cell // 2
        else:
            frames[f] = f / fpe - cell // 2 - 1

    # back to normal
    ax.invert_yaxis()
    movie = animation.FuncAnimation(
        fig, update, init_func=init,
        frames=frames, interval=40
    )

    dumpname = "./tmp/current_animation.gif"
    movie.save(dumpname)  # type: ignore
    if show:
        display(Image(filename=dumpname))
    plt.close(fig)
    return dumpname
