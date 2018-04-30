import copy
from math import sqrt

from matplotlib.pyplot import ylim
from matplotlib.pyplot import xlim

import matplotlib.path as mpath
import matplotlib.patches as mpatches

Path = mpath.Path

from ccg_nlpy import TextAnnotation

import networkx as nx
import matplotlib.pyplot as plt


class TextVizualization():
    @classmethod
    def get_len(cls, t):
        return max(len(t['tokens']), t['label_len'], len(t['label']))

    @classmethod
    def do(cls, ta, view_name, break_sentences=True):
        constituents1 = ta.get_view(view_name).cons_list
        relations1 = ta.get_view(view_name).relation_array

        start_idx = 0
        figscale = 10
        height = 0.08
        scale = 0.039

        fig1 = plt.figure(figsize=(figscale * 2, figscale * 1.5), facecolor='white', edgecolor='black')
        ax1 = fig1.add_subplot(111, aspect='equal')

        sentence_end_position = [len(ta.tokens) + 1]
        if(break_sentences):
            sentence_end_position = ta.sentence_end_position

        tokens = []
        for i, t in enumerate(ta.get_view(view_name).tokens):
            token = {}
            token['start'] = i
            token['end'] = i + 1
            token['label'] = ""
            token['tokens'] = t
            token['label_len'] = 0
            tokens.append(token)

        for i, node in enumerate(constituents1):
            start_token = node["start"]
            end_token = node["end"]
            for token_idx in range(start_token, end_token):
                tokens[token_idx]["label_len"] = len(node["label"]) / (end_token - start_token)

        for sent_idx, end_idx in enumerate(sentence_end_position):
            y = -0.5 * sent_idx
            if (sent_idx > 0):
                start_idx = sentence_end_position[sent_idx - 1]

            offset = [0]
            for t_idx, t in enumerate(tokens):
                if (t_idx >= start_idx and t_idx < end_idx):
                    offset.append(offset[-1] + cls.get_len(t) + 1)
                    t["sentId"] = sent_idx

            for t_idx, node in enumerate(tokens):
                if (t_idx >= start_idx and t_idx < end_idx):
                    x = scale * offset[t_idx - start_idx]
                    width = scale * cls.get_len(node)
                    center_x = x + width / 2
                    center_y = y
                    node["x"] = center_x
                    plt.text(center_x, center_y - height, node['tokens'], ha="center", fontsize=figscale)

            for i, node in enumerate(constituents1):
                start = node["start"]
                end = node["end"]
                if (start >= start_idx and start < end_idx):
                    node["sentId"] = sent_idx
                    center_x = (tokens[start]["x"] + tokens[end - 1]["x"]) / 2
                    center_y = y
                    node["x"] = center_x
                    extra_whitespace = ""
                    if (len(node['tokens']) > len(node['label'])):
                        extra_whitespace = ' ' * int((len(node['tokens']) - len(node['label'])) / 2.0)
                    label = extra_whitespace + node['label'] + extra_whitespace
                    plt.text(center_x, center_y, label, ha="center", fontsize=figscale,
                             bbox=dict(alpha=0.1, facecolor='red', edgecolor='none', boxstyle='round')
                             )

            if(relations1 is not None):
                for r in relations1:
                    start_idx = r["srcConstituent"]
                    end_idx = r["targetConstituent"]
                    if ("sentId" in constituents1[start_idx] and constituents1[start_idx]["sentId"] == sent_idx):
                        if (sent_idx == 3):
                            print("Relation sentence 3 ")
                        start_x = constituents1[start_idx]["x"]
                        end_x = constituents1[end_idx]["x"]
                        middle_x = (start_x + end_x) / 2
                        middle_y = 0.8 * sqrt(abs(end_x - start_x))
                        pp1 = mpatches.PathPatch(
                            Path([(start_x, y + height), (middle_x, y + middle_y), (end_x, y + height)],
                                 [Path.MOVETO, Path.CURVE3, Path.CURVE3]),
                            fc="none", transform=ax1.transData)
                        ax1.add_patch(pp1)
                        # dy = -0.01
                        # offset = 0.05
                        # if(end_x > start_x):
                        #     dy = -dy
                        #     offset = -0.05
                        # pp2 = mpatches.FancyArrow(middle_x + offset, middle_y / 2, dy, 0.0, width=0.02, edgecolor="white", facecolor="black")
                        # ax1.add_patch(pp2)

        # for c in constituents1:
        #     print(c)
        #
        # for r in relations1:
        #     print(r)
        #
        # for t in tokens:
        #     print(t)

        ylim((-1, 1))
        xlim(-0.1, 7)
        plt.axis('off')
        plt.title('Generated with: CogComp-NLPy')
        plt.show()


def main():
    with open('../../tests/sample_text_annotation2.json', 'r') as myfile:
        data = myfile.read()
    ta = TextAnnotation(json_str=data)
    print(ta)
    print(ta.get_views)
    # TextVizualization.do(ta, "MENTION")
    TextVizualization.do(ta, "SRL_VERB", True)
    # TextVizualization.do(ta, "POS")

if __name__ == '__main__':
    main()
