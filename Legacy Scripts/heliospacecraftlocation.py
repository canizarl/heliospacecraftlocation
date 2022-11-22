import heliopy.data.spice as spicedata
import heliopy.spice as spice
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta
import astropy.units as u
from astropy.constants import c, m_e, R_sun, e, eps0, au
import numpy as np
import sys





if __name__ == '__main__':

    # #########################
    # SETINGS
    # #########################
    if len(sys.argv)>1:
        day = int(sys.argv[1])
        month = int(sys.argv[2])
        year = int(sys.argv[3])
    else:
        day = 27
        month = 9
        year = 2012




    # toggle 1 (show)  or 0 (hide) the following objects.
    # Planets
    earth = 1
    venus = 1
    mercury = 0 # Not supported yet
    sun = 1     # HEE coordinates, by default at x = 0 y=0


    # Spacecraft, make sure they were in space at the selected date
    parker_solar_probe = 0
    solar_orbiter = 0
    stereo_A = 1
    stereo_B = 1   # note: Spacecraft Not operational
    winds = 1

    # plot orbits? 1=yes 0=no
    plot_orbit = 1
    spacecraft_orbit_length = 100   #days


    # Constants
    r_sun = R_sun.value  # km
    AU = au.value  # km




    # #######################
    # time settings
    # #######################
    starttime = dt(year, month, day)
    endtime = starttime + timedelta(days=spacecraft_orbit_length)
    times = []
    while starttime < endtime:
        times.append(starttime)
        starttime += timedelta(hours=6)




    if parker_solar_probe == 1:
        # PSP location
        kernels = spicedata.get_kernel('psp')
        kernels += spicedata.get_kernel('psp_pred')
        spice.furnish(kernels)
        psp = spice.Trajectory('SPP')

        psp.generate_positions(times, 'Sun', 'HEE')
        psp.change_units(u.solRad)
        ##

    if solar_orbiter == 1:
        kernels = spicedata.get_kernel('solo')
        spice.furnish(kernels)
        solo = spice.Trajectory('Solar Orbiter')


        solo.generate_positions(times, 'Sun', 'HEE')
        solo.change_units(u.solRad)

        ##



    if stereo_A ==1:
        # STEREO A POSITION
        kernels = spicedata.get_kernel('stereo_a')
        kernels += spicedata.get_kernel('stereo_a_pred')
        spice.furnish(kernels)
        stereo_a = spice.Trajectory('Stereo Ahead')
        stereo_a.generate_positions(times, 'Sun', 'HEE')
        stereo_a.change_units(u.solRad)
        ##

    if stereo_B ==1:
        # STEREO B POSITION
        kernels = spicedata.get_kernel('stereo_b')
        kernels += spicedata.get_kernel('stereo_b_pred')
        spice.furnish(kernels)
        stereo_b = spice.Trajectory('Stereo Behind')
        stereo_b.generate_positions(times, 'Sun', 'HEE')
        stereo_b.change_units(u.solRad)
        ##

    if earth == 1:
        # Earth location
        kernels = spicedata.get_kernel('planet_trajectories')
        spice.furnish(kernels)
        earth_planet = spice.Trajectory('Earth')
        earth_planet.generate_positions(times, 'Sun', 'HEE')
        earth_planet.change_units(u.solRad)


    if winds == 1:
        # Winds location is in Sun - Earth L1
        winds_HEE_x = earth_planet.x[0]*0.99
        winds_HEE_y = earth_planet.y[0]

    if venus == 1:
        # VENUS POSITION
        kernels = spicedata.get_kernel('planet_trajectories')
        spice.furnish(kernels)
        venus_planet = spice.Trajectory('Venus')
        venus_planet.generate_positions(times, 'Sun', 'HEE')
        venus_planet.change_units(u.solRad)



    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    lim_plot = AU/r_sun + 15
    ax.set(xlim=(-lim_plot, lim_plot), ylim=(-lim_plot, lim_plot))


    if sun == 1:
        # circle for the sun
        sun = plt.Circle((0, 0), 3, color='gold', fill=True)
        ax.add_artist(sun)

    if parker_solar_probe == 1:
        psplocation = plt.plot(psp.x[0], psp.y[0], 'ro')
        plt.text(np.array(psp.x[0]) + 1, np.array(psp.y[0]) + 1, 'PSP')
        if plot_orbit == 1:
            plt.plot(psp.x, psp.y, 'r-')

    if solar_orbiter == 1:
        sololocation = plt.plot(solo.x[0], solo.y[0], 'ro')
        plt.text(np.array(solo.x[0]) + 1, np.array(solo.y[0]) + 1, 'Solar Orbiter')
        if plot_orbit == 1:
            plt.plot(solo.x, solo.y, 'r-')


    if stereo_A == 1:
        stereo_a_location = plt.plot(stereo_a.x[0], stereo_a.y[0], 'ko')
        plt.text(np.array(stereo_a.x[0]) + 1, np.array(stereo_a.y[0]) + 1, 'Stereo A')
        if plot_orbit ==1:
            plt.plot(stereo_a.x, stereo_a.y, 'k-')
    if stereo_B == 1:
        stereo_b_location = plt.plot(stereo_b.x[0], stereo_b.y[0], 'ko')
        plt.text(np.array(stereo_b.x[0]) + 1, np.array(stereo_b.y[0]) + 1, 'Stereo B')
        if plot_orbit ==1:
            plt.plot(stereo_b.x, stereo_b.y, 'k-')

    if winds == 1:
        windslocation = plt.plot(winds_HEE_x,winds_HEE_y, 'co')
        plt.text(winds_HEE_x.value - 50, winds_HEE_y.value + 1, 'Wind')

    if earth == 1:
        earthlocation = plt.plot(earth_planet.x[0], earth_planet.y[0], 'bo')
        plt.text(np.array(earth_planet.x[0]) + 1, np.array(earth_planet.y[0]) + 1, 'Earth')
        r_e = np.sqrt(earth_planet.x ** 2 + earth_planet.y ** 2)
        circle_e = plt.Circle((0, 0), r_e[0].value, color='k', fill=False, linestyle='--', linewidth=1)
        ax.add_artist(circle_e)
    if venus == 1:
        venus_location = plt.plot(venus_planet.x[0], venus_planet.y[0], 'yo')
        plt.text(np.array(venus_planet.x[0]) + 1, np.array(venus_planet.y[0]) + 1, 'Venus')
        if plot_orbit ==1:
            plt.plot(venus_planet.x, venus_planet.y, 'k-')
            r_v = np.sqrt(venus_planet.x**2 + venus_planet.y**2)
            circle_v = plt.Circle((0, 0), r_v[0].value, color='k', fill=False, linestyle='--', linewidth=1)
            ax.add_artist(circle_v)

    lim_plot = AU/r_sun + 15
    ax.set(xlim=(-lim_plot, lim_plot), ylim=(-lim_plot, lim_plot))


    month_strings = {
        1:'Jan',
        2:'Feb',
        3:'Mar',
        4:'Apr',
        5:'May',
        6:'Jun',
        7:'Jul',
        8:'Aug',
        9:'Sep',
        10:'Oct',
        11:'Nov',
        12:'Dec'}

    plt.rcParams.update({'font.size': 20})
    ax.set_title(f'Spacecraft Coordinates - {day} / {month_strings[month]} / {year}',fontsize=22)
    ax.set_xlabel('HEE - X / $R_{\odot}$', fontsize=22)
    ax.set_ylabel('HEE - Y / $R_{\odot}$', fontsize=22)
    ax.grid()



    print(f"REPORT:")
    print(f"Date: {year}/{month}/{day}")
    print(f"Spacecraft Location in HEE [R_sun]: ")
    print(f"")
    if parker_solar_probe == 1:
        print(f"PSP: ({psp.x[0]},{psp.y[0]})")
    if solar_orbiter == 1:
        print(f"SO: ({psp.x[0]},{psp.y[0]})")
    if stereo_A == 1:
        print(f"StereoA: ({stereo_a.x[0]},{stereo_a.y[0]})")
    if stereo_B == 1:
        print(f"StereoB: ({stereo_b.x[0]},{stereo_b.y[0]})")
    if winds == 1:
        print(f"Wind: ({winds_HEE_x},{winds_HEE_y})")



    plt.show(block=False)























