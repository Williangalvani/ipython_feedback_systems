from myanimation import anim_to_html, display_animation
from sympy import Poly, roots
import matplotlib.patches as mpatches
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from tempfile import NamedTemporaryFile
from matplotlib import animation



def toPoly(a):
    try:
       return np.array(Poly(a).coeffs(),dtype=np.float64)
    except:
        return float(a)
        
    
def analysis(system,symbol,trange,s):
    ############################# startint value #####################################3
    G = system.subs(symbol,1)

    freqrange =[1e-1,1e2]

    a1, b1 = G.as_numer_denom()
    #print a1, b1
    a1 = toPoly(a1)
    b1 = toPoly(b1)
    s1 = signal.lti(a1, b1)
    w, mag, phase = s1.bode(w=freqrange)

    ###################    PLOT   ############################3
    fig = plt.figure()

    ax_gain  = fig.add_subplot(3, 1, 1)
    ax_phase = fig.add_subplot(3, 1, 2)
    ax_step  = fig.add_subplot(3, 2, 5)
    ax_pz    = fig.add_subplot(3, 2, 6)

    ###################     GAIN     ######################################

    ax_gain.set_xlabel('w')
    ax_gain.set_ylabel('gain')

    line_gain = Line2D([], [], color='black',label="...")

    ax_gain.add_line(line_gain)
    ax_gain.semilogx(w,mag)
    ax_gain.set_ylim([-30,10])
    ax_gain.set_xlim(freqrange)

    #####################    PHASE    ##########################
    ax_phase.set_xlabel('omega')
    ax_phase.set_ylabel('theta')

    line_phase = Line2D([], [], color='black')

    ax_phase.add_line(line_phase)

    ax_phase.semilogx(w, phase)  # Bode phase plot
    ax_phase.set_ylim([-180,180])
    ax_phase.set_xlim(freqrange)

    legend = ax_gain.legend(loc='upper center', shadow=True)

    #####################   step  ##################################
    ax_step.set_xlabel('t')
    ax_step.set_ylabel('Y')

    line_step = Line2D([], [], color='black')

    ax_step.add_line(line_step)

    t, response = signal.step(s1)

    ax_step.plot(t, response)  # Bode phase plot
    #ax_phase.set_ylim([-180,180])
    #ax_phase.set_xlim(freqrange)
    #########################   zeros, poles #######################################



    a1, b1 = G.as_numer_denom()
    z, p = roots(a1,s), roots(b1,s)
    #print z.keys(), p.keys()
    z, p = np.array(z.keys(),dtype=np.complex64), np.array(p.keys(), dtype=np.complex64)


    # Add unit circle and zero axes    
    unit_circle = mpatches.Circle((0,0), radius=1, fill=False,
                                 color='black', ls='solid', alpha=0.1)
    ax_pz.add_patch(unit_circle)
    ax_pz.axvline(0, color='0.7')
    ax_pz.axhline(0, color='0.7')

    # Plot the poles and set marker properties
    poles = ax_pz.plot(p.real, p.imag, 'x', markersize=9, alpha=0.5)

    # Plot the zeros and set marker properties
    zeros = ax_pz.plot(z.real, z.imag,  'o', markersize=9, 
             color='red', alpha=0.5,
             #markeredgecolor=poles[0].get_color(), # same color as poles
             )

    # Scale axes to fit
    r = 1.5 * np.amax(np.concatenate((abs(z), abs(p), [1])))
    ax_pz.axis('scaled')
    ax_pz.axis([-r, r, -r, r])
    #    ticks = [-1, -.5, .5, 1]
    #    plt.xticks(ticks)


    ############################################################################


    # initialization function: plot the background of each frame

    # animation function.  This is called sequentially
    step = (trange[1]-trange[0])/10.0
    #print step
    
    def animate(i): 
        k = trange[0]+i*step
        a1, b1 = system.as_numer_denom()
        G = a1.subs(T,k)/b1.subs(T,k)
        a1 = toPoly(a1)
        b1 = toPoly(b1)
        s1 = signal.lti(a1,b1)
        w, mag, phase = s1.bode(w=freqrange)
        
        line_gain.set_data(w, mag)
        line_phase.set_data(w, phase)
        line_gain.set_label("T={0}".format(k))
        line_step.set_data(signal.step(s1))
        legend = ax_gain.legend(loc='upper center', shadow=True)
        
        for axis in [ax_gain,ax_phase,ax_pz,ax_step]:
            axis.relim()                      # reset intern limits of the current axes 
            axis.autoscale_view()   # reset axes limits 

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, frames=10, interval=50, blit=True)

    # call our new function to display the animatio1
    display_animation(anim)
    #print "done!
                      
                      

