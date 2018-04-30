import copy
from math import sqrt

from matplotlib.pyplot import ylim
from matplotlib.pyplot import xlim

import matplotlib.path as mpath
import matplotlib.patches as mpatches

Path = mpath.Path

from ccg_nlpy import TextAnnotation
# from bokeh.plotting import *

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class TextVizualization():
    @classmethod
    def get_len(cls, t):
        return max(len(t['tokens']), len(t['label']))

    @classmethod
    def do(cls, ta, view_name):

        constituents1 = ta.get_view(view_name).cons_list
        constituents2 = copy.deepcopy(constituents1)

        # for i, c in enumerate(constituents1):
        #     c["idx"] = i

        relations1 = ta.get_view(view_name).relation_array
        # print(relations1)

        # indices_covered = []
        # for c in constituents:
        #     indices_covered += range(c['start'], c['end'])
        # print(indices_covered)
        tokens = ta.get_view(view_name).tokens
        # print(constituents1)
        # print(tokens)

        constituents = []
        old_to_new_index_map = {}
        for i, t in enumerate(tokens):
            # check if there are any constituents covering this token
            selected_c = None
            added = False
            selected_idx = None
            for j, c in enumerate(constituents1):
                if(i == c['start']): # and i < c['end']
                    selected_c = c
                    selected_idx = j

                if (i >= c['start'] and i < c['end']):
                    added = True

            if(selected_c is not None):
                constituents.append(selected_c)
                print(selected_idx)
                old_to_new_index_map[selected_idx] = len(old_to_new_index_map)

            if(not added):
                token = {}
                token['start'] = i
                token['end'] = i + 1
                token['label'] = ""
                token['tokens'] = t
                constituents.append(token)


        # print("constituents1 : " + str(len(constituents1)))
        # print("old_to_new_index_map: " + str(len(old_to_new_index_map)))
        #
        # assert len(old_to_new_index_map) == len(constituents1)

        figscale = 10

        fig1 = plt.figure(figsize=(figscale * 2, figscale * 1), facecolor='white', edgecolor='black')
        ax1 = fig1.add_subplot(111, aspect='equal')

        offset = [0]
        for t in constituents:
            offset.append(offset[-1] + cls.get_len(t) + 1.2)

        height = 0.08

        for i, node in enumerate(constituents):
            scale = 0.039
            x = scale * offset[i]

            y = -height / 2
            width = scale * cls.get_len(node)

            # if(len(node['label']) > 0 ):
                # patch = ax1.add_patch(
                #     patches.Rectangle((x, y), width, 0.15, alpha=0.1, facecolor='red', label='Label')
                # )

            center_x = x + width / 2
            center_y = 0.0

            # if("idx" in node):
            node["x"] = center_x

            plt.text(center_x, center_y, node['label'], ha="center", fontsize=figscale,
            bbox = dict(alpha=0.1, facecolor='red', edgecolor='none', boxstyle='round')
                     )
            plt.text(center_x, center_y - height, node['tokens'], ha="center", fontsize=figscale)


        for r in relations1:
            start = r["srcConstituent"]
            end = r["targetConstituent"]
            start_new_idx = old_to_new_index_map[start]
            print(end)
            print("end_new_idx: " + str(len(old_to_new_index_map)))
            end_new_idx = old_to_new_index_map[end]
            start_x = constituents[start_new_idx]["x"]
            # print(end_new_idx)
            constituents[end_new_idx]
            end_x = constituents[end_new_idx]["x"]
            pp1 = mpatches.PathPatch(
                Path([(start_x, height), ((start_x + end_x)/2, 1*sqrt(abs(end_x - start_x))), (end_x, height)],
                     [Path.MOVETO, Path.CURVE3, Path.CURVE3]),
                fc="none", transform=ax1.transData)
            pp1.set_label("asdasd")
            pp1.set_joinstyle("miter")

            ax1.add_patch(pp1)
            ax1.set_title('Generated with: CogComp-NLPy')

        ylim((-1, 1))
        xlim(-0.1, 7)
        plt.axis('off')
        plt.show()

def main():
    with open('../../tests/sample_text_annotation2.json', 'r') as myfile:
        data = myfile.read()
    ta = TextAnnotation(json_str=data)
    print(ta)
    print(ta.get_views)
    # TextVizualization.do(ta, "MENTION")
    TextVizualization.do(ta, "SRL_VERB")
    # TextVizualization.do(ta, "POS")

    # import networkx as nx
    # import matplotlib.pyplot as plt
    #
    # # g = nx.DiGraph()
    # # g.add_nodes_from([1, 2, 3, 4, 5])
    # # g.add_edges_from([(1, 2)], label="adasd")
    # # g.add_edge(4, 2)
    # # g.add_edge(3, 5)
    # # g.add_edge(2, 3)
    # # g.add_edge(5, 4)
    #
    #
    # G = nx.MultiGraph()
    # G.add_node(1)
    # G.add_node(2)
    # G.add_edge(1, 2, label='foo', with_labels=True)
    # G.add_edge(1, 2, label='bar', with_labels=True)
    #
    # # nx.draw(g, pos = {0: (1, 0), 1: (2, 0), 2: (3, 0), 3: (4, 0), 4: (5, 0)}, with_labels=True)
    # nx.draw(G,with_labels=True)
    # plt.draw()
    # plt.show()

    # import networkx as nx
    # edges = [['A', 'B'], ['B', 'C'], ['B', 'D']]
    # G = nx.Graph()
    # G.add_edges_from(edges)
    # pos = nx.spring_layout(G)
    # plt.figure()
    # nx.draw(G, pos, edge_color='black', width=1, linewidths=1, \
    #         node_size=500, node_color='pink', alpha=0.9, \
    #         labels={node: node for node in G.nodes()})
    # nx.draw_networkx_edge_labels(G, pos, edge_labels={('A', 'B'): 'AB', \
    #                                                   ('B', 'C'): 'BC', ('B', 'D'): 'BD'}, font_color='red')
    # plt.axis('off')
    # plt.show()

    # G = nx.DiGraph()
    # G.add_nodes_from([0, 1])
    # pos = nx.circular_layout(G)
    # nx.draw_networkx_nodes(G, pos, node_color='r', node_size=100, alpha=1)
    # nx.draw_networkx_edges(G, pos, edgelist=[(0, 1)], width=2, alpha=0.5, edge_color='b')
    # nx.draw_networkx_edges(G, pos, edgelist=[(1, 0)], width=1, alpha=1)
    # plt.axis('off')
    # plt.show()


    # import networkx as nx
    # import matplotlib.pyplot as plt
    # from matplotlib.lines import Line2D
    # G = nx.dodecahedral_graph()
    # pos = nx.spring_layout(G)
    # ax = plt.gca()
    # for u,v in G.edges():
    #     x = [pos[u][0],pos[v][0]]
    #     y = [pos[u][1],pos[v][1]]
    #     l = Line2D(x,y,linewidth=8,solid_capstyle='round')
    #     ax.add_line(l)
    # ax.autoscale()
    # plt.show()

    # import matplotlib.pyplot as plt
    # import numpy as np
    # import mplcursors
    # np.random.seed(42)
    #
    # fig, ax = plt.subplots()
    # ax.scatter(*np.random.random((2, 26)))
    # ax.set_title("Mouse over a point")
    #
    # mplcursors.cursor(hover=True)
    #
    # plt.show()


if __name__ == '__main__':
    main()
