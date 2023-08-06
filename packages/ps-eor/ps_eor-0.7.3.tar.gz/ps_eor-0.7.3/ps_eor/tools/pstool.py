#!/usr/bin/env python

from __future__ import print_function
from __future__ import absolute_import

import os
import time
import click

import numpy as np

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

# All ps_eor modules are lazy loaded
from ps_eor import __version__


mpl.rcParams['image.cmap'] = 'Spectral_r'
mpl.rcParams['image.origin'] = 'lower'
mpl.rcParams['image.interpolation'] = 'nearest'
mpl.rcParams['axes.grid'] = True

t_file = click.Path(exists=True, dir_okay=False)
t_dir = click.Path(exists=True, file_okay=False)


@click.group()
@click.version_option(__version__)
def main():
    pass


@main.command('gen_vis_cube')
@click.argument('img_list', type=t_file)
@click.argument('psf_list', type=t_file)
@click.option('--output_name', '-o', help='Output filename', default='datacube.h5', show_default=True)
@click.option('--theta_fov', help='Trim image to FoV (in degrees)', default=4, type=float, show_default=True)
@click.option('--umin', help='Min baseline (in lambda)', default=50, type=float, show_default=True)
@click.option('--umax', help='Max baseline (in lambda)', default=250, type=float, show_default=True)
@click.option('--threshold', '-w', help='Filter all visibilities with weights below T times the max weights',
              default=0.01, type=float, show_default=True)
@click.option('--int_time', '-i', help='Integration time of a single visibility', type=str)
@click.option('--total_time', '-t', help='Total time of observation', type=str)
@click.option('--trim_method', '-m', help="Trim method: 'a': after normalization, 'b': before normalization",
              default='a', type=click.Choice(['a', 'b']), show_default=True)
@click.option('--use_wscnormf', help='Use WSCNORMF to normalize the visibility, and does not use the PSF', is_flag=True)
@click.option('--win_function', help='Apply a window function on the trimmed image')
def gen_vis_cube(img_list, psf_list, output_name, theta_fov, umin, umax, threshold, int_time, total_time,
                 trim_method, use_wscnormf, win_function):
    ''' Create a datacube from image and psf fits files.

        \b
        IMG_LIST: Listing of input fits image files
        PSF_LIST: Listing of input fits psf files
    '''
    import astropy.units as u
    from ps_eor import datacube, psutil

    if int_time is not None:
        int_time = u.Quantity(int_time, u.s).to(u.s).value

    if total_time is not None:
        total_time = u.Quantity(total_time, u.s).to(u.s).value

    imgs = np.loadtxt(img_list, dtype=str)
    psfs = np.loadtxt(psf_list, dtype=str)

    print('Loading %s files ...' % len(imgs))

    imgs = psutil.sort_by_fits_key(imgs, 'CRVAL3')
    psfs = psutil.sort_by_fits_key(psfs, 'CRVAL3')

    win_fct = None
    if win_function:
        name = datacube.WindowFunction.parse_winfct_str(win_function)
        win_fct = datacube.WindowFunction(name)
        print('Using mask: %s' % win_fct)

    data_cube = datacube.CartDataCube.load_from_fits_image_and_psf(imgs, psfs, umin, umax,
                                                                   np.radians(theta_fov),
                                                                   int_time=int_time, total_time=total_time,
                                                                   min_weight_ratio=threshold,
                                                                   trim_method=trim_method,
                                                                   use_wscnormf=use_wscnormf,
                                                                   window_function=win_fct)

    print('Saving to: %s' % output_name)
    data_cube.save(output_name)


@main.command('even_odd_to_sum_diff')
@click.argument('even', type=t_file)
@click.argument('odd', type=t_file)
@click.argument('sum')
@click.argument('diff')
def even_odd_to_sum_diff(even, odd, sum, diff):
    ''' Create SUM / DIFF datacubes from EVEN / ODD datacubes '''
    from ps_eor import datacube

    even = datacube.CartDataCube.load(even)
    odd = datacube.CartDataCube.load(odd)
    (0.5 * (even + odd)).save(sum)
    (0.5 * (even - odd)).save(diff)

    print('All done')


@main.command('diff_cube')
@click.argument('cube1', type=t_file)
@click.argument('cube2', type=t_file)
@click.option('--out_file', '-o', help='output file name', default='diff_cube.h5',
              type=click.Path(file_okay=False), show_default=True)
def diff_cube(cube1, cube2, out_file):
    ''' Compute the difference between CUBE1 and CUBE2 '''
    from ps_eor import datacube

    cube1 = datacube.CartDataCube.load(cube1)
    cube2 = datacube.CartDataCube.load(cube2)

    print('Saving diff cube: %s ...' % out_file)

    cube1, cube2 = datacube.get_common_cube(cube1, cube2)
    (cube1 - cube2).save(out_file)


@main.command('run_flagger')
@click.argument('file_i', type=t_file)
@click.argument('file_v', type=t_file)
@click.argument('flag_config', type=t_file)
@click.option('--output_dir', '-o', type=t_dir, help='Output directory', default='.')
def run_flagger(file_i, file_v, flag_config, output_dir):
    ''' Run flagger on datacubes and save flag.

        \b
        FILE_I: Input Stoke I datacube
        FILE_V: Input Stoke V datacube
        FLAG_CONFIG: Flagger configuration file
    '''
    from ps_eor import datacube, flagger, psutil

    print('Loading cube ...')
    i_cube = datacube.CartDataCube.load(file_i)
    v_cube = datacube.CartDataCube.load(file_v)

    print('Running flagger ...')
    flagger_runner = flagger.FlaggerRunner.load(flag_config)
    flagger_runner.run(i_cube, v_cube)

    out_flag_name = psutil.append_postfix(os.path.basename(file_i), 'flag')
    out_flag_plot_name = psutil.append_postfix(os.path.basename(file_i), 'flag').replace('.h5', '.pdf')

    print('Saving flags to: %s ...' % out_flag_name)
    fig = flagger_runner.plot()
    fig.savefig(os.path.join(output_dir, out_flag_plot_name))
    flagger_runner.flag.save(os.path.join(output_dir, out_flag_name))

    print('All done!')


@main.command('make_ps')
@click.argument('file_i', type=t_file)
@click.argument('file_v', type=t_file)
@click.argument('file_dt', required=False, type=t_file)
@click.option('--flag_config', '-f', help='Flagging configuration parset', type=t_file)
@click.option('--eor_bins_list', '-e', help='Listing of EoR redshift bins', type=t_file)
@click.option('--ps_conf', '-c', help='Power Spectra configuration parset', type=t_file)
@click.option('--output_dir', '-o', help='Output directory', default='.', type=click.Path(file_okay=False))
@click.option('--plots_output_dir', '-po', help='Output directory for plots', default='.',
              type=click.Path(file_okay=False))
def make_ps(file_i, file_v, file_dt, flag_config, eor_bins_list, ps_conf, output_dir, plots_output_dir):
    ''' Produce power-spectra of datacubes

        \b
        FILE_I: Input Stoke I datacube
        FILE_V: Input Stoke V datacube
        FILE_DT: Optional input time-diffence datacube
        '''
    from ps_eor import datacube, pspec, flagger, psutil

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(plots_output_dir):
        os.makedirs(plots_output_dir)

    print('Loading data ...')
    i_cube = datacube.DataCube.load(file_i)
    v_cube = datacube.DataCube.load(file_v)

    ps_builder = pspec.PowerSpectraBuilder(ps_conf, eor_bins_list)
    ps_conf = ps_builder.ps_config

    i_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)
    v_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)

    dt_i_cube = None
    if file_dt is not None:
        dt_i_cube = datacube.DataCube.load(file_dt)
        dt_i_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)

    if flag_config is not None:
        print('Running flagger ...')
        flagger_runner = flagger.FlaggerRunner.load(flag_config)
        i_cube, v_cube = flagger_runner.run(i_cube, v_cube)
        if dt_i_cube is not None:
            dt_i_cube = flagger_runner.apply_last(dt_i_cube)

        fig = flagger_runner.plot()
        fig.savefig(os.path.join(plots_output_dir, 'flagger.pdf'))

    ps_conf.el = 2 * np.pi * np.arange(i_cube.ru.min(), i_cube.ru.max(), ps_conf.du)

    for eor_name in ps_builder.eor_bin_list.get_all_names():
        if not ps_builder.eor_bin_list.get(eor_name, freqs=i_cube.freqs):
            continue

        ps_gen = ps_builder.get(i_cube, eor_name)
        eor = ps_gen.eor

        if eor.bw_total < 2e6:
            continue

        plot_out_dir = os.path.join(plots_output_dir, 'eor%s_u%s-%s' %
                                    (eor_name, int(ps_conf.umin), int(ps_conf.umax)))
        out_dir = os.path.join(output_dir, 'eor%s_u%s-%s' % (eor_name, int(ps_conf.umin), int(ps_conf.umax)))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        if not os.path.exists(plot_out_dir):
            os.makedirs(plot_out_dir)

        kbins = np.logspace(np.log10(ps_gen.kmin), np.log10(ps_conf.kbins_kmax), ps_conf.kbins_n)

        if ps_conf.empirical_weighting:
            v_cube.weights.scale_with_noise_cube(eor.get_slice(
                v_cube), sefd_poly_fit_deg=ps_conf.empirical_weighting_polyfit_deg)
            i_cube.weights.scale_with_noise_cube(eor.get_slice(
                v_cube), sefd_poly_fit_deg=ps_conf.empirical_weighting_polyfit_deg)

        print('\nGenerating power spectra for EoR bin:', eor.name)
        print('Frequency range: %.2f - %.2f MHz (%i SB)\n' % (eor.fmhz[0], eor.fmhz[-1], len(eor.fmhz)))
        print('Mean redshift: %.2f (%.2f MHz)\n' % (eor.z, eor.mfreq * 1e-6))

        for cube, stokes in zip([i_cube, v_cube, dt_i_cube], ['I', 'V', 'dt_V']):
            if cube is None:
                continue

            fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4))
            ps = ps_gen.get_ps(cube)
            ps2d = ps_gen.get_ps2d(cube)
            ps3d = ps_gen.get_ps3d(kbins, cube)

            ps.plot(ax=ax1)
            ps2d.plot(ax=ax2, wedge_lines=[90, 45], z=eor.z)

            ps.save_to_txt(os.path.join(out_dir, 'ps_%s.txt' % stokes))
            ps2d.save_to_txt(os.path.join(out_dir, 'ps2d_%s.txt' % stokes))
            ps3d.save_to_txt(os.path.join(out_dir, 'ps3d_%s.txt' % stokes))

            fig.tight_layout()
            fig.savefig(os.path.join(plot_out_dir, 'ps_%s.pdf' % stokes))

        fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(12, 5))
        ps_gen.get_cl(i_cube).plot_kper(ax=ax1, c=psutil.blue, l_lambda=True, normalize=True, label='I')
        ps_gen.get_cl(i_cube.make_diff_cube_interp()).plot_kper(
            ax=ax1, c=psutil.orange, l_lambda=True, normalize=True, label='dI')
        ps_gen.get_cl(v_cube.make_diff_cube_interp()).plot_kper(
            ax=ax1, c=psutil.green, l_lambda=True, normalize=True, label='dV')
        # ax1.axvline(250, ls='--', c=psutil.dblack)
        ax1.set_xscale('log')

        ps_gen.get_variance(i_cube).plot(ax=ax2, c=psutil.blue, label='I')
        ps_gen.get_variance(i_cube.make_diff_cube_interp()).plot(ax=ax2, c=psutil.orange, label='dI')
        ps_gen.get_variance(v_cube.make_diff_cube_interp()).plot(ax=ax2, c=psutil.green, label='dV')

        if dt_i_cube is not None:
            ps_gen.get_cl(dt_i_cube).plot_kper(ax=ax1, ls='--', c=psutil.black,
                                               l_lambda=True, normalize=True, label='th_noise')
            ps_gen.get_variance(dt_i_cube).plot(ax=ax2, ls='--', c=psutil.black, label='th_noise')

        lgd = fig.legend(*ax1.get_legend_handles_labels(), bbox_to_anchor=(0.5, 1), loc="lower center", ncol=4)
        fig.tight_layout(pad=0.4)
        fig.savefig(os.path.join(plot_out_dir, 'variance_cl.pdf'), bbox_extra_artists=(lgd,), bbox_inches='tight')


@main.command('vis_to_sph')
@click.argument('vis_cube', type=t_file)
@click.argument('sph_cube', type=click.Path(dir_okay=False))
@click.option('--umin', help='Min baseline (in lambda)', default=0, type=float)
@click.option('--umax', help='Max baseline (in lambda)', default=1000, type=float)
@click.option('--nside', '-n', help='Nside (if not set, default to 1/3 of lmax', type=int)
@click.option('--flagfile', '-f', help='Flag to be applied to visibility cube before transformation', type=t_file)
def vis_to_sph(vis_cube, sph_cube, umin, umax, nside, flagfile):
    ''' Load visibilities datacubes VIS_CUBE, transform to sph datacube and save to SPH_CUBE '''
    from ps_eor import datacube, sphcube, flagger

    cube = datacube.CartDataCube.load(vis_cube)

    if flagfile is not None:
        print('Applying flag ...')
        flag = flagger.Flag.load(flagfile)
        cube = flag.apply(cube)

    cube.filter_uvrange(umin, umax)

    lmax = int(np.floor(2 * np.pi * cube.ru.max()))

    if nside is None:
        nside = int(2 ** (np.ceil(np.log2(lmax / 3.))))

    out_cube = sphcube.SphDataCube.from_cartcube(cube, nside, lmax)
    out_cube.save(sph_cube)


def do_gpr(i_cube, v_cube, gpr_config_i, gpr_config_v, rnd_seed=1):
    from ps_eor import fgfit

    t = time.time()
    np.random.seed(rnd_seed)

    gpr_config_v = fgfit.fitutil.GprConfig.load(gpr_config_v)
    gpr_config_i = fgfit.fitutil.GprConfig.load(gpr_config_i)

    print('Running GPR for Stokes V ...\n')

    gpr_fit = fgfit.GprForegroundFit(gpr_config_v)
    gpr_res_v = gpr_fit.run(v_cube, v_cube, rnd_seed=rnd_seed)

    print("\nDone in %.2f s\n" % (time.time() - t))

    t = time.time()
    print('Running GPR for Stokes I ...\n')

    gpr_fit = fgfit.ScaleNoiseGprForegroundFit(gpr_config_i)
    gpr_res_i = gpr_fit.run(i_cube, gpr_res_v.sub, rnd_seed=rnd_seed)

    print("\nDone in %.2f s\n" % (time.time() - t))

    return gpr_res_i, gpr_res_v


def plot_img_and_freq_slice(eor, data_cube, ax1, ax2, name):
    img_cube = eor.get_slice(data_cube).regrid().image()

    img_cube.plot(ax=ax1, auto_scale_quantiles=(0.1, 0.999))
    img_cube.plot_slice(ax=ax2)

    ax1.text(0.03, 0.94, name, transform=ax1.transAxes, ha='left', fontsize=10)
    ax2.text(0.03, 0.94, name, transform=ax2.transAxes, ha='left', fontsize=10)


def save_img_and_ps(ps_gen, eor, kbins, cmpts, names, filename_img, filename_ps, cycler=None):
    fig, axs = plt.subplots(ncols=2, nrows=len(cmpts), figsize=(11, 3.5 * len(cmpts)))
    fig2, axs2 = plt.subplots(ncols=2, nrows=2, figsize=(10, 7))
    axs2 = axs2.flatten()

    if cycler is None:
        cycler = mpl.rcParams['axes.prop_cycle'] * mpl.cycler('linestyle', ['-'])

    for i, (cmpt, name, prop) in enumerate(zip(cmpts, names, cycler)):
        plot_img_and_freq_slice(eor, cmpt, axs[i, 0], axs[i, 1], name)

        ps_gen.get_ps3d(kbins, cmpt).plot(ax=axs2[0], label=name, c=prop['color'], ls=prop['linestyle'])
        ps_gen.get_ps2d(cmpt).plot_kpar(ax=axs2[1], label=name, c=prop['color'], ls=prop['linestyle'])
        ps_gen.get_ps2d(cmpt).plot_kper(ax=axs2[2], label=name, c=prop['color'], ls=prop['linestyle'])
        ps_gen.get_variance(cmpt).plot(ax=axs2[3], label=name, c=prop['color'], ls=prop['linestyle'])

    lgd = fig2.legend(*axs2[0].get_legend_handles_labels(),
                      bbox_to_anchor=(0.5, 1.02), loc="upper center", ncol=len(cmpts))

    fig.tight_layout()
    fig2.tight_layout()
    fig.savefig(filename_img)
    fig2.savefig(filename_ps, bbox_extra_artists=(lgd,), bbox_inches='tight')


def save_ps2d(ps_gen, ps, ps2d, title, filename, **kargs):
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4))
    ps.plot(ax=ax1, **kargs)
    ps2d.plot(ax=ax2, wedge_lines=[45, 90], z=ps_gen.eor.z, **kargs)
    fig._plotutils_colorbars[ax2].ax.set_xlabel(r'$\mathrm{K^2\,h^{-3}\,cMpc^3}$')

    ax1.text(0.03, 0.92, title, transform=ax1.transAxes, ha='left', fontsize=11)
    ax2.text(0.03, 0.92, title, transform=ax2.transAxes, ha='left', fontsize=11)
    fig.tight_layout()
    fig.savefig(filename)


def get_ratios(ps_gen, ps2d_ratio):
    ratio = np.median(ps2d_ratio.data)
    ratio_high = np.median((ps2d_ratio.data)[ps_gen.k_par > 0.8])
    ratio_low = np.median((ps2d_ratio.data)[ps_gen.k_par < 0.6])

    return ratio, ratio_high, ratio_low


@main.command('run_gpr')
@click.argument('file_i', type=t_file)
@click.argument('file_v', type=t_file)
@click.argument('gpr_config_i', type=t_file)
@click.argument('gpr_config_v', type=t_file)
@click.option('--flag_config', '-f', type=t_file, help='GPR configuration parset for Stokes I')
@click.option('--eor_bins_list', '-e', type=t_file, help='Listing of EoR redshift bins')
@click.option('--ps_conf', '-c', type=t_file, help='Power spectra configuration file')
@click.option('--output_dir', '-o', help='Output directory', default='.')
@click.option('--plots_output_dir', '-po', help='Output directory for the figures')
@click.option('--rnd_seed', help='Set a random seed', default=3, type=int)
def run_gpr(file_i, file_v, gpr_config_i, gpr_config_v, flag_config, eor_bins_list, ps_conf,
            output_dir, plots_output_dir, rnd_seed):
    ''' Run GPR & generate power spectra

    \b
    FILE_I: Input Stoke I datacube
    FILE_V: Input Stoke V datacube
    GPR_CONFIG_I: GPR configuration parset for Stokes I
    GPR_CONFIG_V: GPR configuration parset for Stokes V
    '''
    from ps_eor import datacube, pspec, flagger, psutil

    if plots_output_dir is None:
        plots_output_dir = output_dir

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(plots_output_dir):
        os.makedirs(plots_output_dir)

    print('Loading data ...')
    i_cube = datacube.DataCube.load(file_i)
    v_cube = datacube.DataCube.load(file_v)

    ps_builder = pspec.PowerSpectraBuilder(ps_conf, eor_bins_list)
    ps_conf = ps_builder.ps_config

    i_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)
    v_cube.filter_uvrange(ps_conf.umin, ps_conf.umax)

    if flag_config:
        print('Running flagger ...')
        flagger_runner = flagger.FlaggerRunner.load(flag_config)
        i_cube, v_cube = flagger_runner.run(i_cube, v_cube)

    ps_conf.el = 2 * np.pi * np.arange(i_cube.ru.min(), i_cube.ru.max(), ps_conf.du)

    for eor_name in ps_builder.eor_bin_list.get_all_names():
        if not ps_builder.eor_bin_list.get(eor_name, freqs=i_cube.freqs):
            continue

        ps_gen = ps_builder.get(i_cube, eor_name)
        eor = ps_gen.eor

        if eor.bw_total < 2e6:
            continue

        out_dir = os.path.join(output_dir, 'eor%s_u%s-%s' % (eor_name, int(ps_conf.umin), int(ps_conf.umax)))
        plot_out_dir = os.path.join(plots_output_dir, 'eor%s_u%s-%s' %
                                    (eor_name, int(ps_conf.umin), int(ps_conf.umax)))

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        if not os.path.exists(plot_out_dir):
            os.makedirs(plot_out_dir)

        ps_gen_fg = ps_builder.get(i_cube, eor_name, window_fct='hann', rmean_freqs=True)

        if ps_conf.empirical_weighting:
            sefd = v_cube.make_diff_cube().estimate_sefd()
            poly_deg = ps_conf.empirical_weighting_polyfit_deg
            v_cube.weights.scale_with_noise_cube(eor.get_slice(
                v_cube.make_diff_cube()), sefd_poly_fit_deg=poly_deg, expected_sefd=sefd)
            i_cube.weights.scale_with_noise_cube(eor.get_slice(
                v_cube.make_diff_cube()), sefd_poly_fit_deg=poly_deg, expected_sefd=sefd)

        kbins = np.logspace(np.log10(ps_gen.kmin), np.log10(ps_conf.kbins_kmax), ps_conf.kbins_n)

        print('\nRunning GPR for EoR bin:', eor.name)
        print('Frequency range: %.2f - %.2f MHz (%i SB)\n' % (eor.fmhz[0], eor.fmhz[-1], len(eor.fmhz)))
        print('Mean redshift: %.2f (%.2f MHz)\n' % (eor.z, eor.mfreq * 1e-6))

        print('Saving GPR result...\n')

        gpr_res, gpr_res_v = do_gpr(eor.get_slice_fg(i_cube), eor.get_slice_fg(v_cube),
                                    gpr_config_i, gpr_config_v, rnd_seed=rnd_seed)

        gpr_res_v.save(out_dir, 'gpr_res_V')
        gpr_res.save(out_dir, 'gpr_res_I')

        # Saving residuals I and V PS
        ps2d_i_res = ps_gen.get_ps2d(gpr_res.sub)
        ps2d_v_res = ps_gen.get_ps2d(gpr_res_v.sub)
        ps_i_res = ps_gen.get_ps(gpr_res.sub)
        ps_v_res = ps_gen.get_ps(gpr_res_v.sub)
        ps3d_i_res = ps_gen.get_ps3d(kbins, gpr_res.sub)
        ps3d_v_res = ps_gen.get_ps3d(kbins, gpr_res_v.sub)
        ps3d_noise_i = ps_gen.get_ps3d(kbins, gpr_res.noise)
        ps3d_rec = ps_gen.get_ps3d_with_noise(kbins, gpr_res.sub, gpr_res.noise)

        ratio, ratio_high, ratio_low = get_ratios(ps_gen, ps2d_i_res / ps2d_v_res)
        ratio_txt = 'Ratio I / V (med: %.2f / %.2f / %.2f)' % (ratio, ratio_high, ratio_low)
        print(ratio_txt)

        ps2d_i_res.save_to_txt(os.path.join(out_dir, 'ps2d_I_residual.txt'))
        ps2d_v_res.save_to_txt(os.path.join(out_dir, 'ps2d_V_residual.txt'))

        ps3d_i_res.save_to_txt(os.path.join(out_dir, 'ps3d_I_residual.txt'))
        ps3d_v_res.save_to_txt(os.path.join(out_dir, 'ps3d_V_residual.txt'))
        ps3d_rec.save_to_txt(os.path.join(out_dir, 'ps3d_I_minus_V.txt'))
        ps3d_noise_i.save_to_txt(os.path.join(out_dir, 'ps3d_I_noise.txt'))

        up = ps3d_rec.get_upper()
        k_up = ps3d_rec.k_mean[np.nanargmin(up)]
        upper_limit = '2 sigma upper limit: (%.1f)^2 mK^2 at k = %.3f' % (np.nanmin(up), k_up)
        print(upper_limit)

        print('Plotting results ...\n')

        # Plotting GPR results
        save_ps2d(ps_gen, ps_i_res, ps2d_i_res, 'Stokes I residual',
                  os.path.join(plot_out_dir, 'ps2d_I_residual.pdf'))
        save_ps2d(ps_gen, ps_v_res, ps2d_v_res, 'Stokes V residual',
                  os.path.join(plot_out_dir, 'ps2d_V_residual.pdf'))

        save_ps2d(ps_gen, ps_i_res / ps_v_res, ps2d_i_res / ps2d_v_res, 'I residual / V residual',
                  os.path.join(plot_out_dir, 'ps2d_I_over_V_residual.pdf'), vmin=1, vmax=10)

        save_ps2d(ps_gen, ps_i_res / ps_v_res, ps2d_i_res / ps_gen.get_ps2d(gpr_res.noise), 'I residual / noise',
                  os.path.join(plot_out_dir, 'ps2d_I_over_noise.pdf'), vmin=0.5, vmax=10)

        cmpts = [i_cube, v_cube, gpr_res.fit, gpr_res.sub, gpr_res_v.sub]
        names = ['I', 'V', 'I fg', 'I residual', 'V residual']
        cycler = mpl.cycler('color', [psutil.lblue, psutil.lgreen, psutil.red, psutil.dblue, psutil.dgreen]) \
            + mpl.cycler('linestyle', ['-', '-', ':', '-', '-'])
        save_img_and_ps(ps_gen_fg, eor, kbins, cmpts, names,
                        os.path.join(plot_out_dir, 'img_I_V_residuals.pdf'),
                        os.path.join(plot_out_dir, 'ps_I_V_residuals.pdf'), cycler)

        cmpts = [gpr_res.pre_fit, gpr_res.get_fg_model(), gpr_res.get_eor_model(), gpr_res.sub, gpr_res.noise]
        names = ['fg int', 'fg mix', 'eor', 'I residual', 'noise I']

        if gpr_res.post_fit.data.mean() != 0:
            cmpts.append(gpr_res.post_fit)
            names.append('fg pca')

        save_img_and_ps(ps_gen_fg, eor, kbins, cmpts, names,
                        os.path.join(plot_out_dir, 'img_gpr_cmpts.pdf'),
                        os.path.join(plot_out_dir, 'ps_gpr_cmpts.pdf'))

        # PS3D plot
        fig, ax = plt.subplots()
        ps3d_i_res.plot(label='I residual', ax=ax, nsigma=2, c=psutil.dblue)
        ps3d_noise_i.plot(label='noise I', ax=ax, nsigma=2, c=psutil.green)
        ps3d_rec.plot(label='I residual - noise', ax=ax, nsigma=2, c=psutil.orange)

        ax.legend()
        fig.savefig(os.path.join(plot_out_dir, 'ps3d.pdf'), bbox_inches='tight')


@main.command('combine')
@click.argument('file_list', type=t_file)
@click.option('--umin', help='Minimum baseline in lambda', type=float, default=10, show_default=True)
@click.option('--umax', help='Maximum baseline in lambda', type=float, default=1000, show_default=True)
@click.option('--weights_mode', '-w', help='Weights mode', type=str, default='full', show_default=True)
@click.option('--inhomogeneous', '-ih', help='Combine non homogeneous', is_flag=True)
@click.option('--pre_flag', help='Pre-combine flagging parset', type=t_file)
@click.option('--post_flag', help='Post-combine flagging parset', type=t_file)
@click.option('--scale_with_noise', '-s', help='Scale weights with noise estimated from Stokes V', is_flag=True)
@click.option('--output_template', '-o', help='Output template name. %STOKES% and %NUM% will be replaced',
              default='c_cube_%STOKES%_%NUM%.h5', show_default=True, type=click.Path(resolve_path=True))
@click.option('--output_multi_template', '-om',
              help='Output template name for multi cube. %STOKES% and %NUM% will be replaced.',
              default=None, type=click.Path(resolve_path=True))
@click.option('--save_intermediate', '-si', help='Save intermediate combined nights', is_flag=True)
def combine(file_list, umin, umax, weights_mode, inhomogeneous, pre_flag, post_flag, scale_with_noise,
            output_template, output_multi_template, save_intermediate):
    ''' Combine all datacubes listed in FILE_LIST

        \b
        FILE_LIST is a text file with 4 columns, whitespace separated:

        \b
        OBS_ID CUBE1_I CUBE1_V CUBE1_DT
        OBS_ID CUBE2_I CUBE2_V CUBE2_DT
        ... '''
    from ps_eor import datacube, flagger

    file_list = np.loadtxt(file_list, dtype=str)

    i_cubes = []
    v_cubes = []
    dt_cubes = []
    sefds = []
    night_ids = []

    for night_id, file_i, file_v, file_dt in file_list:
        i_cube = datacube.CartDataCube.load(file_i)
        v_cube = datacube.CartDataCube.load(file_v)
        dt_cube = datacube.CartDataCube.load(file_dt)

        i_cube.filter_uvrange(umin, umax)
        v_cube.filter_uvrange(umin, umax)
        dt_cube.filter_uvrange(umin, umax)

        if pre_flag:
            flagger_runner = flagger.FlaggerRunner.load(pre_flag)
            i_cube, v_cube = flagger_runner.run(i_cube, v_cube)
            dt_cube = flagger_runner.apply_last(dt_cube)

        noise_cube = v_cube.make_diff_cube()
        sefds.append(noise_cube.estimate_sefd())

        i_cubes.append(i_cube)
        v_cubes.append(v_cube)
        dt_cubes.append(dt_cube)
        night_ids.append(night_id)

    expected_sefd = np.mean(sefds)

    print('Mean sefd=%.1f' % expected_sefd)

    combiner_i = datacube.DataCubeCombiner(umin, umax, weighting_mode=weights_mode,
                                           inhomogeneous=inhomogeneous)
    combiner_v = datacube.DataCubeCombiner(umin, umax, weighting_mode=weights_mode,
                                           inhomogeneous=inhomogeneous)
    combiner_dt = datacube.DataCubeCombiner(umin, umax, weighting_mode=weights_mode,
                                            inhomogeneous=inhomogeneous)

    if output_multi_template is not None:
        multi_i = datacube.MultiNightsCube(inhomogeneous=inhomogeneous)
        multi_v = datacube.MultiNightsCube(inhomogeneous=inhomogeneous)
        multi_dt = datacube.MultiNightsCube(inhomogeneous=inhomogeneous)

    for i, (night_id, i_cube, v_cube, dt_cube, sefd) in enumerate(zip(night_ids, i_cubes, v_cubes, dt_cubes, sefds)):
        i_str = '%03d' % (i + 1)
        print('%s, sefd=%.1f' % (night_id, sefd))
        noise_cube = v_cube.make_diff_cube()

        if scale_with_noise:
            i_cube.weights.scale_with_noise_cube(noise_cube, sefd_poly_fit_deg=3, expected_sefd=expected_sefd)
            v_cube.weights.scale_with_noise_cube(noise_cube, sefd_poly_fit_deg=3, expected_sefd=expected_sefd)
            dt_cube.weights.scale_with_noise_cube(noise_cube, sefd_poly_fit_deg=3, expected_sefd=expected_sefd)

        combiner_i.add(i_cube, night_id)
        combiner_v.add(v_cube, night_id)
        combiner_dt.add(dt_cube, night_id)

        if output_multi_template is not None:
            multi_i.add(i_cube, night_id)
            multi_v.add(v_cube, night_id)
            multi_dt.add(dt_cube, night_id)

        if save_intermediate or i == len(night_ids) - 1:
            c_i_cube = combiner_i.get()
            c_v_cube = combiner_v.get()
            c_dt_cube = combiner_dt.get()

            if post_flag:
                flagger_runner = flagger.FlaggerRunner.load(post_flag)
                c_i_cube, c_v_cube = flagger_runner.run(c_i_cube, c_v_cube)
                c_dt_cube = flagger_runner.apply_last(c_dt_cube)

            out_i = output_template.replace('%STOKES%', 'I').replace('%NUM%', i_str)
            out_v = output_template.replace('%STOKES%', 'V').replace('%NUM%', i_str)
            out_dt = output_template.replace('%STOKES%', 'dt_V').replace('%NUM%', i_str)

            for out in [out_i, out_v, out_dt]:
                if not os.path.exists(os.path.dirname(out)):
                    os.makedirs(os.path.dirname(out))

            c_i_cube.save(out_i)
            c_v_cube.save(out_v)
            c_dt_cube.save(out_dt)

    if output_multi_template is not None:
        multi_i.done()
        multi_v.done()
        multi_dt.done()

        m_i_cube = multi_i.concat()
        m_v_cube = multi_v.concat()
        m_dt_cube = multi_dt.concat()

        out_i = output_multi_template.replace('%STOKES%', 'I').replace('%NUM%', i_str)
        out_v = output_multi_template.replace('%STOKES%', 'V').replace('%NUM%', i_str)
        out_dt = output_multi_template.replace('%STOKES%', 'dt_V').replace('%NUM%', i_str)

        for out in [out_i, out_v, out_dt]:
            if not os.path.exists(os.path.dirname(out)):
                os.makedirs(os.path.dirname(out))

        m_i_cube.save(out_i)
        m_v_cube.save(out_v)
        m_dt_cube.save(out_dt)

    print('All done !')


@main.command('combine_sph')
@click.argument('file_list', type=t_file)
@click.option('--pre_flag', help='Pre-combine flagging parset', type=t_file)
@click.option('--post_flag', help='Post-combine flagging parset', type=t_file)
@click.option('--output_template', '-o', help='Output template name. %STOKES% and %NUM% will be replaced',
              default='c_cube_%STOKES%_%NUM%.h5', show_default=True, type=click.Path(resolve_path=True))
@click.option('--save_intermediate', '-si', help='Save intermediate combined nights', is_flag=True)
def combine_sph(file_list, pre_flag, post_flag, output_template, save_intermediate):
    ''' Combine all sph datacubes listed in FILE_LIST

        \b
        FILE_LIST is a text file with 4 columns, whitespace separated:

        \b
        OBS_ID CUBE1_I CUBE1_V CUBE1_DT
        OBS_ID CUBE2_I CUBE2_V CUBE2_DT
        ... '''
    from ps_eor import sphcube, flagger, psutil

    file_list = np.loadtxt(file_list, dtype=str)

    i_cubes = []
    v_cubes = []
    dt_cubes = []
    rms_noises = []
    night_ids = []

    for night_id, file_i, file_v, file_dt in file_list:
        i_cube = sphcube.SphDataCube.load(file_i)
        v_cube = sphcube.SphDataCube.load(file_v)
        dt_cube = sphcube.SphDataCube.load(file_dt)

        flagger_runner = flagger.FlaggerRunner.load(pre_flag)
        i_cube, v_cube = flagger_runner.run(i_cube, v_cube)
        dt_cube = flagger_runner.apply_last(dt_cube)

        noise_cube = v_cube.make_diff_cube()
        rms_noises.append(psutil.mad(noise_cube.data))

        i_cubes.append(i_cube)
        v_cubes.append(v_cube)
        dt_cubes.append(dt_cube)
        night_ids.append(night_id)

    combiner_i = sphcube.SphDataCubeCombiner()
    combiner_v = sphcube.SphDataCubeCombiner()
    combiner_dt = sphcube.SphDataCubeCombiner()

    for i, (night_id, i_cube, v_cube, dt_cube, rms_noise) in enumerate(zip(night_ids, i_cubes, v_cubes,
                                                                           dt_cubes, rms_noises)):
        weight = 1 / rms_noise ** 2
        i_str = '%03d' % (i + 1)
        print('%s, rms noise = %s K' % (night_id, rms_noise))

        combiner_i.add(i_cube, weight)
        combiner_v.add(v_cube, weight)
        combiner_dt.add(dt_cube, weight)

        if save_intermediate or i == len(night_ids) - 1:
            c_i_cube = combiner_i.get()
            c_v_cube = combiner_v.get()
            c_dt_cube = combiner_dt.get()

            if post_flag:
                flagger_runner = flagger.FlaggerRunner.load(post_flag)
                c_i_cube, c_v_cube = flagger_runner.run(c_i_cube, c_v_cube)
                c_dt_cube = flagger_runner.apply_last(c_dt_cube)

            out_i = output_template.replace('%STOKES%', 'I').replace('%NUM%', i_str)
            out_v = output_template.replace('%STOKES%', 'V').replace('%NUM%', i_str)
            out_dt = output_template.replace('%STOKES%', 'dt_V').replace('%NUM%', i_str)

            for out in [out_i, out_v, out_dt]:
                if not os.path.exists(os.path.dirname(out)):
                    os.makedirs(os.path.dirname(out))

            print(out_i)

            c_i_cube.save(out_i)
            c_v_cube.save(out_v)
            c_dt_cube.save(out_dt)


if __name__ == '__main__':
    main()
