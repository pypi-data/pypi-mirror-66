"""
    Copyright (C) 2020 Shandong University

    This program is licensed under the GNU General Public License 3.0 
    (https://www.gnu.org/licenses/gpl-3.0.html). 
    Any derivative work obtained under this license must be licensed 
    under the GNU General Public License as published by the Free 
    Software Foundation, either Version 3 of the License, or (at your option) 
    any later version, if this derivative work is distributed to a third party.

    The copyright for the program is owned by Shandong University. 
    For commercial projects that require the ability to distribute 
    the code of this program as part of a program that cannot be 
    distributed under the GNU General Public License, please contact 
            
            sailist@outlook.com
             
    to purchase a commercial license.
"""
import os
import pickle
import pprint as pp

from tensorboard.backend.event_processing import event_accumulator

from thexp.utils.generel_util import curent_date


#
# ScalarEvent = namedtuple('ScalarEvent', ['wall_time', 'step', 'value'])
# CompressedHistogramEvent = namedtuple('CompressedHistogramEvent',
#                                       ['wall_time', 'step',
#                                        'compressed_histogram_values'])
# HistogramEvent = namedtuple('HistogramEvent',
#                             ['wall_time', 'step', 'histogram_value'])
# HistogramValue = namedtuple('HistogramValue', ['min', 'max', 'num', 'sum',
#                                                'sum_squares', 'bucket_limit',
#                                                'bucket'])
# ImageEvent = namedtuple('ImageEvent', ['wall_time', 'step',
#                                        'encoded_image_string', 'width',
#                                        'height'])
# AudioEvent = namedtuple('AudioEvent', ['wall_time', 'step',
#                                        'encoded_audio_string', 'content_type',
#                                        'sample_rate', 'length_frames'])
# TensorEvent = namedtuple('TensorEvent', ['wall_time', 'step', 'tensor_proto'])


class BoardPlotter:
    """Extract image/scalars/... from tensorboard files and save it to images"""

    def __init__(self, plot_dir):
        self.plot_dir = plot_dir

    def dynamic_board(self, file, mode=None):
        if mode is None or mode == "created":
            self.ea = event_accumulator.EventAccumulator(file,
                                                         size_guidance={  # see below regarding this argument
                                                             event_accumulator.COMPRESSED_HISTOGRAMS: 500,
                                                             event_accumulator.IMAGES: 4,
                                                             event_accumulator.AUDIO: 4,
                                                             event_accumulator.SCALARS: 0,
                                                             event_accumulator.HISTOGRAMS: 1,
                                                         })
            print("\nLoad board in {}".format(file))

    def get_scalars(self, tag):
        return self.ea.Scalars(tag)  # 'wall_time', 'step', 'value'

    def get_histograms(self, tag):
        return self.ea.Histograms(tag)

    def get_audio(self, tag):
        return self.ea.Audio(tag)

    def get_images(self, tag):
        return self.ea.Images(tag)

    def get_compressed_histograms(self, tag):
        return self.ea.CompressedHistograms(tag)

    def get_tensor(self, tag):
        return self.ea.Tensors(tag)

    def summary(self):
        self.ea.Reload()
        pp.pprint(self.ea.Tags())


def draw_dict():
    res = dict()

    res["x"] = []
    res['y'] = []
    return res


class Reporter():
    def __init__(self, pltf_dir, exts=None):

        self.base_dir = pltf_dir
        from collections import defaultdict
        self.cur_key = curent_date()
        self.plot_dicts = {self.cur_key: defaultdict(draw_dict)}
        self.plot_dict = self.plot_dicts[self.cur_key]
        self.cur_dir = self.savedir()

    def savedir(self):
        i = 1
        fn = os.path.join(self.base_dir, "{:04}".format(i))
        while os.path.exists(fn):
            i += 1
            fn = os.path.join(self.base_dir, "{:04}".format(i))
        os.makedirs(fn, exist_ok=True)

        return fn

    def as_numpy(self, var):
        import torch, numpy as np
        if isinstance(var, (int, float)):
            return var

        if isinstance(var, torch.Tensor):
            return var.detach().cpu().item()

        if isinstance(var, np.ndarray):
            return var.item()

        assert False

    def add_scalar(self, var, step, tag):
        self.plot_dict[tag]['x'].append(step)
        self.plot_dict[tag]['y'].append(self.as_numpy(var))

    def savefig(self):
        from matplotlib import pyplot as plt
        from thexp.utils.generel_util import filter_filename
        dir = self.cur_dir
        for k, v in self.plot_dict.items():
            plt.figure()
            base_name = filter_filename("{}.jpg".format(k))
            fn = os.path.join(dir, base_name)
            plt.plot(v['x'], v['y'])
            plt.title(k)
            plt.savefig(fn)
            v['fn'] = base_name
        return dir

    @property
    def picklefile(self):
        return "plot_data.pkl"

    @property
    def reportfile(self):
        return "report.md"

    def savearr(self):

        dir = self.cur_dir
        fn = os.path.join(dir, self.picklefile)
        with open(fn, "wb") as w:
            pickle.dump(self.plot_dicts, w)

    def loadarr(self, dir=None):
        if dir is None:
            dir = self.cur_dir

        fn = os.path.join(dir, self.picklefile)
        with open(fn, "rb") as w:
            self.plot_dicts = pickle.load(w)
            for k in self.plot_dicts:
                self.plot_dict = self.plot_dicts[k]

    def report(self, every=20):
        from thexp.utils.markdown_writer import Markdown
        md = Markdown()
        md.add_title(curent_date("%y-%m-%d-%H:%M:%S"))
        for k, v in self.plot_dict.items():
            md.add_title(k, level=2)
            if "fn" in v:
                md.add_picture("./{}".format(v["fn"]), k, False)


            lines = []
            head = ["step"]
            vars = ["values"]

            for x, y in zip(v["x"][::every], v["y"][::every]):
                head.append("**{}**".format(x))
                vars.append("{:.4f}".format(y))
                if len(head) > 10:
                    lines.append(head)
                    lines.append(vars)
                    head = ["**step**"]
                    vars = ["values"]

            if len(head) != 1:
                lines.append(head)
                lines.append(vars)

            md.add_table(lines)

        dir = self.cur_dir
        fn = os.path.join(dir, self.reportfile)
        md.to_file(fn)
        return fn
