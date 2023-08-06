import argparse
import sys
import glob
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import re

from ccdproc import CCDData
from mpl_toolkits.axes_grid1 import make_axes_locatable


class ShowFits(object):

    def __init__(self):
        self.args = self.get_args()
        self.log = self.__get_logger()

        try:
            print(type(self.args.files))
            print(self.args.files)
            if os.path.isfile(self.args.files):
                self.file_list = [self.args.files]
            elif '*' not in self.args.files:
                self.file_list = [arg for arg in self.args.files if '.fits' in arg]
                # self.keywords = [a]
            else:
                self.file_list = glob.glob(self.args.files)

            if self.file_list == []:
                self.log.error('Unable to obtain files.')

        except IndexError:
            pass

    def __call__(self, *args, **kwargs):
        print(self.file_list)
        for file_name in self.file_list:
            ccd = CCDData.read(file_name, unit='adu')

            zlow, zhigh = self.__set_limits(ccd=ccd)

            if self.args.style == 'light':
                plt.style.use('default')
            elif self.args.style == 'dark':
                plt.style.use('dark_background')
            else:
                plt.style.use('dark_background')


            fig, ax = plt.subplots(figsize=(16, 9))
            fig.canvas.set_window_title(file_name)
            ax.set_title(file_name)
            im = ax.imshow(ccd.data, cmap=self.args.cmap, clim=(zlow, zhigh))
            divider = make_axes_locatable(ax)
            cax = divider.append_axes('right', size="3%", pad=0.05)
            fig.colorbar(im, cax=cax)
            plt.tight_layout()
            plt.show()

    def __get_logger(self):

        if self.args.debug:
            log_format = '[%(asctime)s][%(levelname)8s]: %(message)s ' \
                         '[%(module)s.%(funcName)s:%(lineno)d]'
            logging_level = logging.DEBUG
        else:
            log_format = '[%(asctime)s][%(levelname).1s]: %(message)s'
            logging_level = logging.INFO

        date_format = '%H:%M:%S'

        # formatter = logging.Formatter(fmt=log_format,
        #                               datefmt=date_format)

        logging.basicConfig(level=logging_level,
                            format=log_format,
                            datefmt=date_format)

        log = logging.getLogger(__name__)
        return log

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('files', help="File name or pattern to filter files")

        parser.add_argument('--color-map',
                            action='store',
                            default='viridis',
                            type=str,
                            dest='cmap',
                            choices=['gray', 'viridis', 'gray_inverted'],
                            help='Color map to use')

        parser.add_argument('--style',
                            action='store',
                            default='dark',
                            type=str,
                            dest='style',
                            choices=['dark', 'light'],
                            help='Visual style to use')
        parser.add_argument('--debug',
                            action='store_true',
                            dest='debug',
                            help='Debug messages')

        args = parser.parse_args()
        if 'inverted' in args.cmap:
            args.cmap = re.sub('_inverted', '_r', args.cmap)
        return args

    @staticmethod
    def __set_limits(ccd):
        z1 = np.mean(ccd.data) - 0.5 * np.std(ccd.data)
        z2 = np.median(ccd.data) + np.std(ccd.data)

        return z1, z2


def show_fits():
    show__fits = ShowFits()
    show__fits()


if __name__ == '__main__':
    show_fits()
