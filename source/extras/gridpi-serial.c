/*
 * This file, gridpi-serial.c, is example code and part of the SURFsara HPC Cloud workshop 2016.
 * Copyright (c) 2015-2016 SURFsara, all rights reserved
 * This file is Open Source under the BSD 2-Clause License: http://opensource.org/licenses/BSD-2-Clause
 */

/*
 * This example implements a serial calculation of an estimate of pi.
 * Its sole purpose is to provide some workload to be parallelized with OpenMP.
 *
 * Compile with C99, e.g.:
 *    gcc -std=c99 -Wall -Werror -pedantic gridpi-serial.c -o gridpi-serial
 */

/*
 * Algorithm to calculate an estimate of pi:
 *
 * Imagine a circle, radius R with its center at [0,0].
 * The circle's surface area is described by: x*x + y*y < R*R
 * Imagine a square, 2R by 2R with its center at [0,0].
 * The square's surface area is described by: (-R < x < R) and (-R < y < R)
 *
 * Consider the upper right quadrant of the square: 0 < x < R, 0 < y < R
 * The surface of that part of the circle is: (pi * R*R)/4
 * The surface of that part of the square is: R*R
 * Divide the circle's surface by the square's surface and we get: pi/4
 * Therefore pi = 4 * circle / square
 *
 * Use a grid to sample the square's upper right quadrant and
 * see how many of the total samples lies inside the circle.
 * Then pi = 4 * inside / total.
 */

/*** tweak this if you like:
 *** the number of points on one axis of the grid
 ***/
static long POINTS_ON_AXIS = 100000L;

/* general includes: */
#include <stdio.h>
#include <stdlib.h>

/* for acos(): */
#include <math.h>

/* for reporting the time: */
#include <sys/times.h>
#include <unistd.h>

/* function declarations */
double gridpi(long points_on_axis);

double gridpi(long points_on_axis)
{
    unsigned long inside = 0; /* count hits inside circle */

    for (long ix = 0; ix < points_on_axis; ix++) {
        for (long iy = 0; iy < points_on_axis; iy++) {
            /* create a point inside the square's upper right quadrant, avoid 0.0 and 1.0 */
            double x = ((double) ix + 0.5) / (double) points_on_axis;
            double y = ((double) iy + 0.5) / (double) points_on_axis;
            /* test if point is inside circle */
            if (x*x + y*y < 1) {
                inside++; /* yep, count it */
            }
        }
    }

    /* calculate an estimation of PI from the Monte Carlo hits */
    double estimate = 4 * (double) inside / (double) (points_on_axis * points_on_axis);

    return estimate;
}

int main(void)
{
    /* get gridpi starting times() */
    struct tms start_times;
    clock_t start_real = times(&start_times);

    /* call gridpi */
    double estimate = gridpi(POINTS_ON_AXIS);

    /* get gridpi end times() */
    struct tms end_times;
    clock_t end_real = times(&end_times);

    /* report gridpi result */
    const double pi = acos(-1.0); /* remember from kindergarten? */
    printf("gridpi(%lu) = %23.20f -- diff: %23.20f\n", POINTS_ON_AXIS, estimate, estimate - pi);

    /* report used time */
    clock_t elapsed_r = end_real - start_real;
    clock_t elapsed_u = end_times.tms_utime - start_times.tms_utime;
    clock_t elapsed_s = end_times.tms_stime - start_times.tms_stime;
    float tps = (float) sysconf(_SC_CLK_TCK); /* system clock ticks per second */
    printf("Elapsed (seconds): real %.3f, user %.3f, sys %.3f\n", (float) elapsed_r/tps, (float) elapsed_u/tps, (float) elapsed_s/tps);

    return 0;
}
