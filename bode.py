from scipy import signal
import matplotlib.pyplot as plt
s1 = signal.lti([1], [1, 1])
w, mag, phase = s1.bode()
plt.figure()
plt.subplot(2,1,1)
plt.semilogx(w, mag)    # Bode magnitude plot

plt.subplot(2,1,2)
plt.semilogx(w, phase)  # Bode phase plot
plt.show()
