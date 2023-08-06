Python package for foreground removal and power spectra generation:
==================================================================

Requirements
------------

You will need the following packages:

- click
- numpy
- scipy
- astropy
- matplotlib
- pytable (for saving loading in h5 format)
- pyfftw (optional, can save time)
- sklearn (for PCA)
- GPy (for GPR)
- healpy,reproject (optional)


Usage: 
------

This package provide a simple interface for Foreground removal and PS estimation tasks.

Below we briefly document the main tasks that can be perform with this package:


1. Loading your data: 
---------------------

    data_cube_i = datacube.CartDataCube.load_from_fits_image(files, umin, umax, theta_fov)

This will do the following steps:
- Read Fits image file
- Trim image to theta_fov
- Convert image from Jy/PSF to K, using imager_scale_factor or WSCNORMF
 attribute to get PSF "solid angle" (otherwise use Gaussian approx of the PSF)
- FFT image per frequencies to get visibilities
- Keep only non-zero visibilities between umin and umax.
and return a CartDataCube object storing the visibilities in an ungridded way.

It is possible (recommended) to save/load to an h5 format with the save()/load() method.

One can also regrid the data and make an image with the regrid() and image() method.


2. Run FG removal algorithm:
----------------------------

The main FG removal code is GPR, but PCA, GMCA (the python version) and Poly fitting are also implemented.

To run GPR, one do the following:

    data_cube_i = datacube.CartDataCube.load_from_fits_image(files_i, umin, umax, theta_fov)
    data_cube_v = datacube.CartDataCube.load_from_fits_image(files_v, umin, umax, theta_fov)

    eor_bin_list = pspec.EorBinList(data_cube_i.freqs)
    # Create an EoR bin 122-134 MHz with a 120-136MHz range for the FG fitting
    eor_bin_list.add_freq(1, 122, 134, 120, 136)
    eor = eor_bin_list.get(1)

    gpr_config = fitutil.GprConfig.load(gpr_config_filename)
    gpr_fit = fgfit.GprForegroundFit(gpr_config)
    gpr_res = gpr_fit.run(eor.get_slice_fg(data_cube_i), eor.get_slice_fg(data_cube_v))

This return a GprForegroundResult object which have the following attributes:
- fit: The FG model in a form of a CartDataCube object
- sub: The residual 
- pre_fit: The pre-fit FG model
- post_fit: The post-fit FG model

And the following method:
- get_fg_model(): return the GPR fg model
- get_eor_model(): return the GPR eor model

On can then save/load those CartDataCube as needed for later processing.

The CartDataCube cubes of the GPR model and residual contains the error covariance 
from the GPR model that need to be taken into account when generating the 
power spectra (see fitutil.get_ps_err_from_cov_err for an exemple of how this can be done.).

Look at gpr_config.parset and gpr_config_v.parset for examples of GPR configuration.


3. Generate Power Spectra:
--------------------------

The PS code into account automatically the error covariance of the GPR model.

It is possible to generate spatial only PS, Cylindrically averaged PS (2D) or spherically averaged PS (3D).

    # Create a PS configuration
    el = 2 * np.pi * (np.arange(data_cube.ru.min(), data_cube.ru.max(), du))
    ps_conf = pspec.PowerSpectraConfig(el)

    pb = datacube.LofarHBAPrimaryBeam()
    
    # Create a PS generation object
    ps_gen = pspec.PowerSpectraCart(eor, ps_conf, pb)

    # Create a Spatial PS, plot it and save it to a file
    ps = ps_gen.get_ps(data_cube)
    ps.plot(title='Spatial power spectra')
    plt.savefig('ps.pdf')
    ps.save_to_txt('ps.txt')

    # Create a Cylindrically averaged PS
    ps2d = ps_gen.get_ps2d(data_cube)
    ps2d.plot(title='Cylindrically averaged power spectra')
    plt.savefig('ps2d.pdf')
    ps2d.save_to_txt('ps2d.txt')

    # Create a Spherically averaged PS
    kbins = np.logspace(np.log10(ps_gen.kmin), np.log10(0.5), 10)
    ps3d = ps_gen.get_ps3d(kbins, data_cube)
    ps3d.plot(title='Spherically averaged power spectra')
    plt.savefig('ps3d.pdf')
    ps3d.save_to_txt('ps3d.txt')

