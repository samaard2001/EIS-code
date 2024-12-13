import matplotlib.pyplot as plt 
from matplotlib.gridspec import GridSpec
import datetime
import numpy as np



def plot_impedance(data, names, labels: list[str] = None, title=None, bode=True, nyquist=True, degrees=False):
    # Type hinting throwing error: data: list[tuple[np.array[np.float64], np.array[np.complex128]]]
    """
    Reference 
    ---
    [1] Amund Raniseth. NTNU, Norway. 2024
    ---
    
    Plots impedance data from input data on the form:
        list(
            tuple(
                np.array[np.float64], np.array[np.complex128]
            )
        )
    Where the float64 values are the frequencies, and complex128 the corresponding impedance.
    """

 
    fig = plt.figure(layout="constrained", figsize=(12, 6))
    gs = GridSpec(2, 2, figure=fig)
 
    # Bode
    ax_magni = fig.add_subplot(gs[0, 0])
    ax_magni.set_ylabel(r"Magnitude [$\Omega$]")
    ax_magni.set_xscale('log')
 
    ax_phase = fig.add_subplot(gs[1, 0])
    if degrees:
        ax_phase.set_ylabel(r"Phase [$^\circ C$]")
    else:
        ax_phase.set_ylabel("Phase [rad]")
    ax_phase.set_xscale('log')
    ax_phase.set_xlabel("Frequency [Hz]")
 
    # Nyquist
    ax_nyqui = fig.add_subplot(gs[:, 1])
    ax_nyqui.set_xlabel(r"Z' [$\Omega$]")
    ax_nyqui.set_ylabel(r"-Z'' [-$\Omega$]")
 
    # Insert data
    if labels:
        assert len(labels) == len(data), "Length of labels list must match length of data list"
    else:
        labels = [names[i] for i in range(len(data))]
        #labels = [f"Pattern {i}" for i in range(len(data))]
    
    for pattern, label in zip(data, labels):
        ax_magni.scatter(pattern[0], abs(pattern[1]), label=label)
        ax_phase.scatter(pattern[0],
                         np.angle(pattern[1], deg=True) if degrees else np.angle(pattern[1]),
                         label=label)
        ax_nyqui.scatter(pattern[1].real, -pattern[1].imag, label=label)
    ax_nyqui.legend()
    if title:
        fig.suptitle(title)
    plt.show()