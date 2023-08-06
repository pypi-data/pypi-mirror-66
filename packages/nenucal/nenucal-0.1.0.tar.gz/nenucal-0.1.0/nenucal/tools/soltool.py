#!/usr/bin/env python

import os

import click

import numpy as np
import astropy.stats as astats

from losoto.h5parm import h5parm
from losoto.operations import plot as loplot

t_file = click.Path(exists=True, dir_okay=False)


@click.group()
def main():
    pass


@main.command('plot')
@click.argument('sols', nargs=-1, type=t_file)
@click.option('--plot_dir', help='Plot directory', type=str, default='sol_plots')
@click.option('--clip', help='Clip ', is_flag=True)
def plot(sols, plot_dir, clip):
    ''' Plot solutions of the h5 files SOLS '''
    for sol_file in sols:
        sol = h5parm(sol_file, readonly=not clip)
        try:
            soltab_amp = sol.getSolset('sol000').getSoltab('amplitude000')
            soltab_phase = sol.getSolset('sol000').getSoltab('phase000')

            mask = ~(soltab_amp.getValues(weight=True)[0].astype(bool))
            amp = np.ma.array(soltab_amp.getValues(weight=False)[0], mask=mask)

            if clip:
                print('Clipping %s ...' % sol_file)

                amp_clip = astats.sigma_clip(np.ma.mean(amp, axis=(1, 2, 3)), sigma=3, sigma_lower=3, maxiters=10)
                time_mask = amp_clip.mask.sum(axis=1).astype(bool)

                amp.mask = amp.mask + time_mask[:, None, None, None, None]

                amp_clip = astats.sigma_clip(np.ma.mean(amp, axis=(0, 1, 3)), sigma=5, sigma_lower=5, axis=0)
                ant_mask = amp_clip.mask.sum(axis=1) >= 2

                amp.mask = amp.mask + ant_mask[None, None, :, None, None]

                for soltab in [soltab_amp, soltab_phase]:
                    soltab.setValues((~amp.mask).astype(float), weight=True)

            print('Plotting %s ...' % sol_file)
            plot_dir = os.path.join(os.path.dirname(sol_file), plot_dir)

            if amp.shape[0] > 1:
                loplot.run(soltab_amp, ['time', 'freq'], axisInTable='ant', prefix='%s/amp_' % plot_dir)
                loplot.run(soltab_phase, ['time', 'freq'], axisInTable='ant', prefix='%s/phase_' % plot_dir)
            else:
                loplot.run(soltab_amp, ['freq'], axisInTable='ant', prefix='%s/amp_' % plot_dir)
                loplot.run(soltab_phase, ['freq'], axisInTable='ant', prefix='%s/phase_' % plot_dir)
        finally:
            sol.close()


if __name__ == '__main__':
    main()
