import marimo

__generated_with = "0.24.2"
app = marimo.App(
    width="medium",
    app_title="Control Systems",
    css_file="marimo-custom.css",
)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.image(
        mo.notebook_dir() / "img" / "banner_control.png",
        alt="Control Systems - GNU Radio Conference 2026",
        width="100%",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **License**

    © 2026 The DSP Coach, LLC — <https://dsp-coach.com>

    The code is MIT licensed. The explanatory text and original figures are
    CC BY-NC-ND 4.0. Figures reproduced from manufacturer datasheets remain the
    copyright of their respective owners. Full terms are in `LICENSE` and
    `LICENSE-CONTENT.md` in the repository.

    No warranty is given for this material, and no responsibility is assumed for
    any errors or omissions, or for any damages resulting from its use.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Link to Python Control Library Docs: https://python-control.readthedocs.io/en/
    """)
    return


@app.cell
def _():
    import numpy as np
    import scipy.signal as sig
    import matplotlib.pyplot as plt
    import control as con
    import scipy.fft as fft
    import numpy.random as rand
    import math
    # sound processing
    import wave

    return con, fft, math, np, plt, sig, wave


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Analog Phase Lock Loop Implementation

    For this simulation we will model a PLL using the Microchip PFD1K 8 GHz Phase/Frequency Detector to lock an HMC733LC4B 10 to 20 GHz VCO to a 100 MHz reference for outputs from 10 to 20 GHz in 100 MHz steps.

    This will require a prescaler of 10e9/100e6 = 100 up to 20e9/100e6 = 200.

    We'll design for a loop BW of 1 MHz.
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "analog_pll_block_diagram.png",
                alt="Analog PLL block diagram",
                width=800,
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analog PLL Loop Model
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### VCO

    HMC733LC4B 10-20 GHz VCO

    Establish VCO gain (tuning slope) from ADI datasheet:

    https://www.analog.com/media/en/technical-documentation/data-sheets/hmc733.pdf
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "hmc733_tuning_curve.png",
                alt="HMC733 frequency vs tuning voltage" , width=700,
            ),
            mo.md(
                r"""
    *Source: [Analog Devices HMC733LC4B datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/hmc733.pdf), © Analog Devices, Inc. Reproduced here as the subject of the discussion.*
    """
            ),
            mo.md(
                r"""
    At 10 GHz the control voltage = 0V, at 20 GHz the control voltage = 18V

    Howeer the curve suggests the tuning slope is not quite linear. Conveniently the slope (derivative) is provided to us in the datahsheet:
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "hmc733_tuning_slope.png",
                alt="HMC733 tuning slope vs frequency",  width=700,
            ),
            mo.md(
                r"""
    *Source: [Analog Devices HMC733LC4B datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/hmc733.pdf), © Analog Devices, Inc. Reproduced here as the subject of the discussion*
    """
            ),
            mo.md(
                r"""
    We see from this that we have a frequency dependent gain constant. (Best approach in my opinion is to provide a linearization translation so that we have a constant slope independent of frequency- in this quick example we will determine the gain coefficients for operation at 15 GHz and then from that determined the variability as the frequency is increased and decreased. The different $N$ for each setting also effects the loop parameters).

    From the datasheet plots we see that for operation at a 15 GHz output, the tuning voltage is nearly 7.5V, and at 7.5V the slope is approximately 600 MHz/Volt.

    In radian frequency this is $K_V = 2\pi 600e6 = 3.77e9$ (rad/sec)/V

    For use in a phase lock loop, the phase vs time of the VCO output is the integral of it's frequency vs time. (Since frequency is a change in phase versus a change in time or $d\phi/dt$). The output frequency is directly proportional to the input control voltage, thus in the time domain, the VCO is an integrator as well as unit translator from volts to phase and we have the complete operation of the VCO in the Laplace domain as:

    $$\frac{K_V}{s} = {3.77e9} \text{ rad/V}$$

    The "s" that appears in the formula above is complex frequency, not to be confused with seconds. $s = \sigma + j\omega$ and has units of 1/seconds (hence frequency).
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### PFD

    PFD1K

    Establish Phase Detector Gain $K_{PD}$ from Microchip Datasheet:

    https://ww1.microchip.com/downloads/aemDocuments/documents/RFDS/ProductDocuments/DataSheets/PFD1K.pdf

    Output voltage vs phase with differential output properly terminated to convert currents to voltage:
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "pfd1k_output_voltage_vs_phase.png",
                alt="PFD1K output voltage vs phase", width = 700,
            ),
            mo.md(
                r"""
    *Source: [Microchip PFD1K datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/RFDS/ProductDocuments/DataSheets/PFD1K.pdf), © Microchip Technology Inc. Reproduced here as the subject of the discussion.*
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Loop Filter

    The evaluation board for the PFD1K includes a simple Proportional-Integral (PI) Loop Filter (see page 17 of the datasheet), which integrates the differential voltage out of the PFD and adds a proportional gain to produce the single control voltage the the VCO:
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "pfd1k_pi_loop_filter_schematic.png",
                alt="PFD1K PI loop filter schematic", width = 900,
            ),        
            mo.md(
                r"""
    *Source: [Microchip PFD1K datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/RFDS/ProductDocuments/DataSheets/PFD1K.pdf), © Microchip Technology Inc. Reproduced here as the subject of the discussion.*
    """
            ),
            mo.md(
                r"""
    We will abbreviate $R_2 C_1$ as $\tau_2$ and $R_1 C_1$ at $\tau_1$

    Thus

    $$H(s) = \frac{1+s\tau_2}{s\tau_1}$$

    And we see that the loop filter has a *zero* at:

    $$1+s\tau_2 = 0$$

    $$s=\frac{-1}{\tau_2}$$

    and as an integrator, has a pole at $s=0$, and a gain of $\frac{1}{\tau_1}$.

    Rewriting into it's proportional and integral components, we get:

    $$H(s) = \frac{1}{s\tau_1}+\frac{\tau_2}{\tau_1}$$
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Open Loop Gain

    We will create a Bode plot (by plotting the open loop gain) to see how $\tau_2$ adjusts the gain, and the effect of the zero as adjusted with $\tau_2$

    The Open Loop Gain is the result of cascading the following components, resulting in a product of their gains:

    VCO:  $K_V/s$ <br>
    Phase Detector: $K_{PD}$ <br>
    Loop Filter: $\frac{1+s\tau_2}{s\tau_1}$ <br>
    Frequency Divider: $1/N$ <br>

    The product of the above is the "open loop gain" as:

    $$G_{OL}(s) = \frac{k_V k_{PD}}{Ns}\frac{1+s\tau_2}{s\tau_1} = \frac{k_V k_{PD}}{N\tau_1}\frac{1+s\tau_2}{s^2}$$
    """)
    return


@app.cell
def _(con, np):
    # Loop Equations

    a_kv= 2*np.pi*600e6      # VCO gain in rad/v  (from HMC733 datasheet)
    a_kpd = 0.120            # Phase detector gain v/rad (from PFD1K datasheet)
    a_lbw = 2*np.pi* 1e6     # target loop bw in rad/sec (cuz Dan said)
    a_N = 150                # mid value for N (divider setting to get 15 GHz output)

    # since we'll iterate on loop filter gain constants, make the open loop gain a function
    # Note: numerator and denominator polynomials are entered in positive powers of s in decreasing order
    def gol_analog(tau1, tau2, N):
        return a_kv * a_kpd/(N*tau1)*con.tf([tau2, 1], [1, 0, 0])

    return a_N, a_kpd, a_kv, a_lbw, gol_analog


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Starting Loop Values
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "analog_starting_loop_values.png",
                alt="Analog loop starting values", width=800
            ),
            mo.md(
                r"""
    We can get an initial value for $\tau_1$ by first neglecting the effects of $\tau_2$ by setting $\tau_2=0$ and choosing a zero dB crossing on the Bode gain plot to be the loop BW. 

    The zero dB gain crossing is when: 

    $$|G_{OL}(s)|=1$$

    With $s =  j\omega_{c}$, the loop bandwidth.

    With $\tau_2=0$ and $|G_{OL}(j\omega_c)|=1$ the solution for $\tau_1$ becomes:

    $$\tau_1 = \frac{k_Vk_{PD}}{N\omega_c^2}$$

    We'll then add the zero for stability at the loop bandwidth (for 45° phase margin) or slightly below the loop bandwidth (for higher phase margin).

    This will increase the bandwidth slightly, so then iterate on both from these starting values to decrease the loop gain using $\tau_1$, and increase or decrease $\tau_2$ while observing response on Bode plot for desired gain and phase margin.
    """
            ),
        ]
    )
    return


@app.cell
def _(a_N, a_kpd, a_kv, a_lbw):
    print(f"Target loop bw = {a_lbw:0.2f} rad/sec")

    a_tau1_init = (a_kv * a_kpd)/(a_N * a_lbw**2) 
    print(f"Initial value for tau1 = {a_tau1_init:0.2e}")
    return (a_tau1_init,)


@app.cell(hide_code=True)
def _(mo):
    # Slider to explore how tau1 sets the loop bandwidth (tau2 = 0 in the plot below).
    # The scale is in decades relative to the recommended a_tau1_init computed above,
    # so 0 is the recommended value and -1 / +1 are one decade either side.
    # Defined here, but displayed underneath the plot in the next cell.
    a_tau1_slider = mo.ui.slider(
        start=-1.0,
        stop=1.0,
        step=0.05,
        value=0.0,
        label="tau1 scaling, decades from recommended (0 = recommended)",
        show_value=True,
    )
    return (a_tau1_slider,)


@app.cell
def _(
    a_N,
    a_kpd,
    a_kv,
    a_lbw,
    a_tau1_init,
    a_tau1_slider,
    con,
    gol_analog,
    mo,
    np,
    plt,
):
    # To demonstrate show Bode Plot with tau2=0 resulting in the cascade of two integrators
    _a_tau2 = 0
    _a_tau1 = a_tau1_init * 10 ** a_tau1_slider.value
    a_gol = gol_analog(_a_tau1, _a_tau2, a_N)

    # with tau2 = 0 the 0 dB crossing is at sqrt(kv*kpd/(N*tau1))
    _fc = np.sqrt(a_kv * a_kpd / (a_N * _a_tau1)) / (2 * np.pi)
    _ratio = 10 ** a_tau1_slider.value
    _note = "recommended" if abs(a_tau1_slider.value) < 1e-9 else f"{_ratio:0.2f} x recommended"

    # Axes are pinned, so the gain curve slides across a fixed frame as tau1 varies
    # and the 0 dB crossing visibly walks left and right past the target marker,
    # instead of the frame rescaling around the curve each time.
    _wlo, _whi = 100.0, 2 * np.pi * 10e6
    _flo, _fhi = _wlo / (2 * np.pi), _whi / (2 * np.pi)

    plt.figure()
    con.bode(a_gol, dB=True, Hz=True, omega_limits=[_wlo, _whi])

    plt.subplot(2, 1, 1)
    plt.axhline(0, color="0.6", linewidth=0.8)
    plt.axvline(a_lbw / (2 * np.pi), color="r", linestyle="--", linewidth=1.2,
                label="target loop BW")
    plt.legend(loc="lower left", fontsize=8)
    plt.xlim(_flo, _fhi)
    plt.ylim(-70, 220)
    plt.title("Bode Plot")

    plt.subplot(2, 1, 2)
    plt.xlim(_flo, _fhi)
    plt.ylim(-270, -90)

    mo.vstack(
        [
            plt.gcf(),
            a_tau1_slider,
            mo.md(
                f"tau1 = **{_a_tau1:0.3e} s** ({_note}) &nbsp;&nbsp;|&nbsp;&nbsp; "
                f"0 dB crossing = **{_fc / 1e6:0.3f} MHz** (target 1.000 MHz)"
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If the above Bode plot has a 0dB crossing on the magnitude plot when the frequency is 1 MHz: **Success!** We have properly set $\tau_1$ (a gain constant). The closed loop bandwidth will be where the open loop frequency magnitude response crosses 0 dB. Adjusting $\tau_1$ will simply move the gain curve up and down, and thus adjust the loop bandwidth.

    As implemented thus far, with $\tau_2=0$, the loop will not be stable, given the phase of the open loop gain is at 180 degrees when the gain passes through 0. (The critera for stability using the open loop Bode plot is for the phase to be < 180 degrees when the gain passes through 0 dB).

    This is where adding the zero with $\tau_2$ comes in.

    The two poles at $s=0$ (DC) cause the Bode magnitude to drop -40 dB/decade, and the phase be at -180° (-90° for each pole).
    The zero will add an increase to the magnitude +20 dB/decade, and a +90° increase to the phase at an intercept frequency given by:

    $$f_c = \frac{1}{2\pi \tau_2}$$

    If we place the zero right at the loop bw, this will provide 45° of phase margin.

    If we rearrange/simplify the formula for open loop gain to show overall gain, poles and zeros, we can get more insight into how we may adjust these parameters:

    $$G_{OL}(s) =  \frac{k_V k_{PD}}{N\tau_1}\frac{1+s\tau_2}{s^2} = \frac{K}{\tau_1}\frac{1+s\tau_2}{s^2}$$

    $$ =  K\frac{\tau_2}{\tau_1}\frac{1/\tau_2+s}{s^2}$$

    From this we see that we can set the zero as $s=-1/\tau_2$, and move the gain up and down as the ratio $\tau_2/\tau_1$. And therefore we have independent adjustment of our loop bandwidth and phase margin (which controls the damping factor).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Reset button for the two tau sliders below. The counter in value/on_click is
    # what makes the click observable: each press bumps the value, which re-runs the
    # cell that creates the sliders, rebuilding both of them at 0.
    # Displayed under the sliders in the plot cell.
    a_tau_reset = mo.ui.button(
        value=0,
        on_click=lambda n: n + 1,
        label="Reset tau1 and tau2 to recommended",
    )
    return (a_tau_reset,)


@app.cell(hide_code=True)
def _(a_tau_reset, mo):
    # Sliders for the compensated loop: tau1 sets the loop bandwidth, tau2 places the
    # zero that buys back phase margin. Both scales are in decades relative to the
    # iterated values noted below (tau1 = 2.7 x a_tau1_init, tau2 = 2.3 / a_lbw),
    # so 0 is the recommended setting. Both are displayed under the plot in the next cell.
    #
    # Reading the reset button here is what wires the button up: clicking it re-runs
    # this cell, which re-creates both sliders back at 0.
    _ = a_tau_reset.value

    a_tau1_1_slider = mo.ui.slider(
        start=-1.0,
        stop=1.0,
        step=0.05,
        value=0.0,
        label="tau1 scaling, decades from recommended (0 = recommended)",
        show_value=True,
    )
    a_tau2_1_slider = mo.ui.slider(
        start=-1.0,
        stop=1.0,
        step=0.05,
        value=0.0,
        label="tau2 scaling, decades from recommended (0 = recommended)",
        show_value=True,
    )
    return a_tau1_1_slider, a_tau2_1_slider


@app.cell
def _(
    a_N,
    a_lbw,
    a_tau1_1_slider,
    a_tau1_init,
    a_tau2_1_slider,
    a_tau_reset,
    con,
    gol_analog,
    mo,
    np,
    plt,
):
    # inial values were tau2 = 1/lbw and tau1 = 1.4 x tau2 computed above for a 45 degree
    # phase margin then iterate to increase phase margin to increase the damping factor
    # and keep the same loop bw,
    # end result after interating: tau2 = 2.3/lbw, tau1 = 2.7 x tau1 computed above

    # 1/tau1 is the integral gain, and tau2/tau1 is the proportional gain

    # adjusts phase as 1/tau2, this will change the zeo crossing,
    # so adjust tau1 to compensate:
    _a_tau2 = (2.3 / a_lbw) * 10 ** a_tau2_1_slider.value
    a_tau1 = (2.7 * a_tau1_init) * 10 ** a_tau1_1_slider.value
    a_gol_1 = gol_analog(a_tau1, _a_tau2, a_N)

    _gm, _pm, _wcg, _wcp = con.margin(a_gol_1)
    _r1 = 10 ** a_tau1_1_slider.value
    _r2 = 10 ** a_tau2_1_slider.value
    _n1 = "recommended" if abs(a_tau1_1_slider.value) < 1e-9 else f"{_r1:0.2f} x recommended"
    _n2 = "recommended" if abs(a_tau2_1_slider.value) < 1e-9 else f"{_r2:0.2f} x recommended"
    _cross = f"{_wcp / (2 * np.pi) / 1e6:0.3f} MHz" if np.isfinite(_wcp) else "n/a"
    _margin = f"{_pm:0.1f} deg" if np.isfinite(_pm) else "n/a"

    # same fixed frame as the tau2 = 0 plot above, so the two can be read side by side
    _wlo, _whi = 100.0, 2 * np.pi * 10e6
    _flo, _fhi = _wlo / (2 * np.pi), _whi / (2 * np.pi)

    plt.figure()
    con.bode(a_gol_1, dB=True, Hz=True, display_margins=True, omega_limits=[_wlo, _whi])

    plt.subplot(2, 1, 1)
    plt.axhline(0, color="0.6", linewidth=0.8)
    plt.axvline(a_lbw / (2 * np.pi), color="r", linestyle="--", linewidth=1.2,
                label="target loop BW")
    plt.legend(loc="lower left", fontsize=8)
    plt.xlim(_flo, _fhi)
    plt.ylim(-70, 220)
    plt.grid()
    plt.title("Bode Plot")

    plt.subplot(2, 1, 2)
    plt.xlim(_flo, _fhi)
    plt.ylim(-270, -90)
    plt.grid()

    mo.vstack(
        [
            plt.gcf(),
            a_tau1_1_slider,
            a_tau2_1_slider,
            a_tau_reset,
            mo.md(
                f"tau1 = **{a_tau1:0.3e} s** ({_n1}) &nbsp;&nbsp;|&nbsp;&nbsp; "
                f"tau2 = **{_a_tau2:0.3e} s** ({_n2})"
            ),
            mo.md(
                f"0 dB crossing = **{_cross}** (target 1.000 MHz) "
                f"&nbsp;&nbsp;|&nbsp;&nbsp; phase margin = **{_margin}**"
            ),
        ]
    )
    return (a_gol_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Adjusting $\tau_2$ has a dominant effect on the phase, but because it reduced the slope of the gain, it has a secondary effect on the bandwidth.  We notice above if we used tau2 = 1/lbw and tau1 as we previously computed, that the zero crossing is now higher than 1 MHz. We can adjust this by then lowering the gain by increasing $\tau_1$.

    From this we can then tweak $\tau_1$ (gain as the ratio of $\tau_2/\tau_1$, and therefore bandwidth) and $\tau_2$ (phase margin). If we want to reduce the ringing (increase the dampling factor $\zeta$), then we need to increase the phase margin.

    We could determine exact solution for the specific 2nd order PI Loop (such as has been done by Floyd Gardner, "Phase Lock Techniques"), but this exercise in iterative tuning gives insight into what to do for a broader range of applications.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Closed Loop

    Example closed loop gains of interest are:

    * The gain from the reference input to VCO output, to determine tracking of the reference

    * The gain from the vco output to the vco output (to determine attenuation of VCO phase noise)

    $$G_{CL}(s) = \frac{G_F(s)}{1+G_{OL}(s)}$$

    Ref to VCO out

    $$G_{F1}(s) = N G_{OL}(s)$$

    $$G_{CL1}(s) = \frac{G_{F1}(s)}{1 + G_{OL}(s)} = \frac{N G_{OL}(s)}{1 + G_{OL}(s)}$$

    VCO out to VCO out

    $$G_{F2}(s) = 1$$

    $$G_{CL2}(s) = \frac{1}{1+G_{OL}(s)}$$
    """)
    return


@app.cell
def _(a_N, a_gol_1, con):
    # Closed Loop from Ref Input to VCO Output
    a_gcl1 = a_N * a_gol_1 / (1 + a_gol_1)
    print(f'Transfer function before using minreal: {a_gcl1}')
    a_gcl1 = con.minreal(a_N * a_gol_1 / (1 + a_gol_1))
    # good practice to always use the minreal to reduce the transfer function! 
    print(f'Transfer function after using minreal:{a_gcl1}')
    return (a_gcl1,)


@app.cell
def _(a_gol_1, con):
    # Closed Loop from VCO in to VCO out
    a_gcl2 = con.minreal(1 / (1 + a_gol_1))
    print(a_gcl2)
    return (a_gcl2,)


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Damping Factor

    For a second order system the damping factor $\zeta$ is the cosine of the angle to the pole from the negative real axis
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "damping_factor_pole_angle.png",
                alt="Damping factor as cosine of pole angle", width=700,
            ),
            mo.md(
                r"""
    As damping factor approaches 0, rise time will get faster at the expense of more ringing and overshoot.<br>
    As damping factor approaches 1, rise time and overshoot will decrease.<br>
    Once the damping factor is at 1, the poles are on the real axis, and the system is "underdamped".<br>
    A damping factor close to 0.7 is typically desirable as it offers a good compromise for balanceing rise time and overshoot/ringing considerations.
    """
            ),
        ]
    )
    return


@app.cell
def _(a_gcl1, con, np):
    # For a 2nd order system, the damping factor is the cosine of the angle to the pole from the 
    # negative real axis.
    # A Dampling
    print(f"Damping factor is {np.cos(np.pi-np.angle(con.poles(a_gcl1)[0])):0.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pole Zero Map

    Becuase 2nd order systems are so common the pole zero mapping utilities in Python (and Matlab/Octave) will include the option to superimpose lines of constant natural frequency and damping factor. Higher order systems will also approximate a 2nd order system when there are two poles closest to the $j\omega$ axis (dominant poles) with other poles significantly further to the left (~ >10x) into the left half plane.
    """)
    return


@app.cell
def _(a_gcl1, con, mo, plt):
    plt.figure(figsize=(5.5,5.5))
    con.pzmap(a_gcl1, grid=True)
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Closed Loop Time Domain Response (Step)

    Interpreting the step response results:

    The step responses shown are for a normalized step at the input for an actual small signal step (within the loops linear operating range).  The response is for a step from 0 to 1, so in this case 1 radian, and given the frequency multiplication of this loop, we get a 150 radian phase step at the output (which then gets divided in the divider by 150, producing the equal 1 radian step at the other input to the phase detector).
    """)
    return


@app.cell
def _(a_gcl1, a_gcl2, con, mo, plt):
    plt.figure(figsize=(5,5.5))
    plt.subplot(2,1,1)
    plt.plot(*con.step_response(a_gcl1))
    plt.xlabel("Time (seconds)")
    plt.ylabel("Phase (Radians)")
    plt.title("Step Response Ref In (one rad) to VCO Out")
    plt.grid()
    plt.subplot(2,1,2)
    plt.plot(*con.step_response(a_gcl2))
    plt.xlabel("Time (seconds)")
    plt.ylabel("Phase (Radians)")
    plt.title("Step Response VCO Out (one rad) to VCO Out")
    plt.grid()
    plt.tight_layout()
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Closed Loop Frequency Domain Response
    """)
    return


@app.cell
def _(a_gcl1, con, mo, plt):
    plt.figure()
    con.bode(a_gcl1, dB=True, Hz=True, omega_limits=[10000, 50e6])
    plt.subplot(2,1,1)
    plt.title("Frequency Response, Ref In to VCO Out")
    plt.tight_layout()
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that the gain for the lowwer frequency is consistent with $20Log_{10}N = 20Log_{10}(150)= 43.5$ dB consistent with a frequency multiplication from the reference to the output (multiplying frequency multiplies phase).
    """)
    return


@app.cell
def _(a_gcl2, con, mo, plt):
    plt.figure()
    con.bode(a_gcl2, dB=True, Hz=True, omega_limits=[10000, 50e6])
    plt.subplot(2,1,1)
    plt.title("Frequency Response, VCO Out to VCO Out")
    plt.tight_layout()
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    Note the following phase noise plot from the HMC733 datasheet:
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "hmc733_phase_noise.png",
                alt="HMC733 phase noise",
            ),
            mo.md(
                r"""
    *Source: [Analog Devices HMC733LC4B datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/hmc733.pdf), © Analog Devices, Inc. Reproduced here as the subject of the discussion; see LICENSE-CONTENT.md.*
    """
            ),
            mo.md(
                r"""
    In the loop, the VCO is modelled as a pure VCO (with gain $K_V/s$) followed by a summation with the phase noise at the output:
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "vco_phase_noise_loop_model.png",
                alt="VCO phase noise loop model",
            ),
            mo.md(
                r"""
    Thus the frequency response for "VCO Out to VCO Out" refers to the input at the noise input to this summer, and the output at the output of the summer. For low frequency offsets in phase noise fluctuations, the loop will track the phase noise and thus attenuate it according to the frequency response given (and for the low frequency offsets, it will pass the reference oscillator phase noise with gain according to $20\log_{10}(N)$.
    """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Digital PLL Implementation Model

    For a demonstration of a Digital PLL, we'll use the implementation below to capture and track the 19 KHz pilot in an FM broadcast signal.
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "digital_pll_implementation.png",
                alt="Digital PLL implementation",
            ),
        ]
    )
    return


@app.cell
def _():
    fs = 192e3         # sampling rate

    acc_size = 48      # accumulator size in NCO
    lut_addr=14        # LUT address size in NCO
    lut_out=16         # LUT output size in NCO
    return acc_size, fs, lut_addr, lut_out


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Test Signal : FM Broadcast Pilot Tone

    This is the spectrum from an actual FM signal showing the pilot. The waveform was obviously low-pass filtered since the upper sideband of the L-R signal that is AM modulated to 38 kHz is missing. 
    """ 
            ),
            mo.image(
                mo.notebook_dir() / "img" / "fm_broadcast_pilot_spectrum.png",
                alt="FM broadcast spectrum with 19 kHz pilot",
            ),
        ]
    )
    return


@app.cell
def _(mo, np, wave):
    # Open FM demodulated multiplexed FM Radio Broadcast signal downloaded from
    # https://www.sigidwiki.com/wiki/FM_Broadcast_Radio
    #
    # This recording is not distributed with the repository - see data/README.md
    # for where to download it and where to place it.

    iq_path = mo.notebook_dir() / "data" / "SDRSharp_20150804_205139Z_0Hz_IQ.wav"

    if not iq_path.exists():
        raise FileNotFoundError(
            f"FM broadcast IQ recording not found at {iq_path}.\n"
            "This file is not included in the repository. See data/README.md "
            "for how to download it from the Signal Identification Wiki and "
            "where to place it.\n"
            "Every other section of this notebook runs without it."
        )

    with wave.open(str(iq_path), 'r') as f:
        # extract and plot waveform
        srate = f.getframerate()
        print(f"Sample rate is {srate/1000} KHz")
        signal = f.readframes(-1)
        # from bytes to int16
        signal = np.frombuffer(signal, dtype = "int16")
        params = f.getparams()

    # seperate I and Q channels to be 2 x array
    fmIQ = signal.reshape(-1,2).T

    fm_wfm = fmIQ[1] / np.std(fmIQ[1])   # signal is almost entirely on fmIQ[1] as a real output
    return fm_wfm, srate


@app.cell
def _(fft, np, plt, sig, srate):
    def plot_spectrum(wfm):
        nsamps = len(wfm)
        win = sig.windows.kaiser(nsamps, 12)

        # the following scales by the coherent gain of the window to provide an accurate level in power
        # of tones dB relative to full scale. It will overestimate the spectrum for noise
        # that is spread over multiple bins. To scale noise accurately, we would instead scale
        # by the non-coherent gain of the window (covered more in my DSP for Wireless Comm course)
        freq_out = fft.fft(wfm * win) / np.sum(win) 
        freq_axis = fft.fftfreq(nsamps)
        freq_out = freq_out[freq_axis>=0]
        freq_axis = freq_axis[freq_axis>=0]

        plt.plot(freq_axis * srate, 20*np.log10(np.abs(freq_out)))
        plt.grid()

    return (plot_spectrum,)


@app.cell
def _(fm_wfm, mo, srate):
    mo.audio(fm_wfm, rate=srate)
    return


@app.cell
def _(fm_wfm, lut_out, np, sig, srate):
    # bandpass filter 19 KHz

    r=.99
    ftone = 19e3
    wn = 2 * np.pi * ftone / srate
    pilot = sig.lfilter([1-r], [1., -2*r*np.cos(wn), r**2], fm_wfm)

    scale = 1.8*2**(lut_out) /2**(np.std(pilot))  # for scaling pilot to digital precision of lut outptut 

    pilot =  (pilot * scale).astype('int')
    return ftone, pilot


@app.cell
def _(fm_wfm, lut_out, pilot, plot_spectrum, plt, srate):
    plt.figure(figsize=(8,3))
    plt.subplot(1,2,1)
    plot_spectrum(fm_wfm)
    plt.axis([0, srate/2, -100, 0])
    plt.title("FM Broadcast Signal Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("dBFS")

    plt.subplot(1,2,2)
    plot_spectrum(pilot/2**(lut_out-1))
    plt.axis([0, srate/2, -100, 0])
    plt.title("Bandpass Filtered 19KHz Pilot")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("dBFS")
    plt.tight_layout()
    plt.gcf()
    return


@app.cell
def _(lut_out, np, pilot, plt, srate):
    # compare scale of filtered pilot to "clean" reference signal
    _n = np.arange(len(pilot))
    clean = 2 ** (lut_out - 1) * np.cos(2 * np.pi * 19000.0 / srate * _n)
    plt.figure()
    plt.plot(clean, label='ref')
    plt.plot(pilot, label='filtered pilot')
    plt.title('Confirming Scaling of Pilot')
    plt.legend(loc='lower left')
    return (clean,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Pilot and Reference are not locked above as we see below with a zoom in at two arbitrary locations in the sequence:
    """)
    return


@app.cell
def _(clean, mo, np, pilot, plt):
    span = 200
    start1 = 552400
    start2 = 3000800 #4303800
    range1 = np.arange(start1, start1 + span)
    range2 = np.arange(start2, start2 + span)
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(range1, clean[range1], label="ref")
    plt.plot(range1, pilot[range1], label="filtered pilot")
    plt.subplot(2,1,2)
    plt.plot(range2, clean[range2], label="ref")
    plt.plot(range2, pilot[range2], label="filtered pilot")
    plt.tight_layout()
    mo.mpl.interactive(plt.gcf())
    return (start1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we multiply and filter the above signals, we can see what the phase is of the reference relative to the 19 KHz pilot prior to locking to it:
    """)
    return


@app.cell
def _(clean, fs, ftone, np, pilot, sig):
    def phase_det(tone, ref, f, fs, ntaps=91, fpass=None, fstop=None):
        '''
        running phase detector of x relative to y
        x: tone (1darray)
        y: reference (1darray)
        f: (approximate) frequency of tone (float)
        fs: sampling rate (float) same units as f
        ntaps: number of taps in filter
        fpass: filter passband corner
        fstop: filter stopband corner
        '''
        if fpass is None:
            fpass = 0.8 * f
        if fstop is None:
            fstop = f

        phase = (np.sign(tone) * np.sign(ref))* np.pi

        # filter to pass difference signal as phase and reject sum signal as 2f: 
        coeff = sig.firls(ntaps, [0, fpass, fstop, fs/2], [1, 1, 0, 0], fs=fs)

        # zero phase filter
        result = sig.filtfilt(coeff, 1, phase)
        return result


    filtered_phase = phase_det(pilot, clean, ftone, fs, ntaps = 501, fpass = 500, fstop = 2000)
    return filtered_phase, phase_det


@app.cell
def _(filtered_phase, fs, mo, np, plt, start1):
    # The reference is not yet locked to the pilot, so the detected phase drifts
    # rather than settling. Zoomed in, since the drift is not visible over the
    # full 31.6 second recording.
    _phase_wide = np.arange(start1, start1 + int(2 * fs))
    _phase_fine = np.arange(start1, start1 + int(0.01 * fs))

    plt.figure(figsize=(9, 4))

    plt.subplot(1, 2, 1)
    plt.plot(_phase_wide / fs, filtered_phase[_phase_wide], linewidth=0.6)
    plt.xlabel('Time (s)')
    plt.ylabel('Phase (rad)')
    plt.title('Pilot Phase Relative to Reference, 2 s')
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(_phase_fine / fs, filtered_phase[_phase_fine])
    plt.xlabel('Time (s)')
    plt.ylabel('Phase (rad)')
    plt.title('Same Phase, 10 ms Zoom')
    plt.grid()

    plt.tight_layout()
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ## Digital Phase Lock Loop Model
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "digital_pll_loop_model.png",
                alt="Digital PLL loop model",
            ),
            mo.md(
                r"""
    Note the units used for error and FCW here are actual counts, so will match the digital values at those nodes.

    Open Loop Gain:

    $$G_{OL}(z)= \frac{k_Vk_{PD}}{z-1}H(z)$$
    """
            ),
        ]
    )
    return


@app.cell
def _(np):
    fs_1 = 192000.0  # sampling rate in Hz. We'll use normalized radian frequency in the model.
    d_lbw = 2 * np.pi * 200 / fs_1  # target loop bw in rad/sample
    return d_lbw, fs_1


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### NCO
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "nco_block_diagram.png",
                alt="NCO block diagram",
            ),
            mo.md(
                r"""
    Input on left is Frequency Control Word (FCW)
    Output on right is the digitized sinusoid as the output of a Look-up Table (LUT) effectively containing one cycle of a sine wave.

    For a small FCW, the accumulator will ramp up slowly. For a large FCW, the accumulator will ramp up more rapidly.

    The Most Significant Bits of the accumulator are used as the address for the LUT. The accumulator wraps around on overflow, and thus produces a digitized sinusoidal output waveform with a frequency directly proportional to FCW, with a full range of DC to half the sampling rate.

    Given a PLL implementation, we will work in units of phase, not frequency. In this context, the NCO, like the VCO, is an integrator, as a "phase accumulator".  The NCO gain for the loop model is $k_V/(z-1)$, where $k_V$ is the slope of the output frequency in radians/sample verus the frequency control word FCW. Note similarity of VCO gain for analog loop as $\frac{K_V}{s}$.

    The frequency vs control word sensitivity is as shown in the plot below, resulting in
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "nco_frequency_vs_fcw.png",
                alt="NCO frequency vs frequency control word",
            ),
            mo.md(
                r"""
     This is a good example of how the mapping from s to z for poles and zeros in vicinity of $z=1$ is simply $s \leftrightarrow z-1$ when working in units of normalized frequency such that the time index is in samples ($T=1$).
    """
            ),
        ]
    )
    return


@app.cell
def _(np):
    # NCO 
    accum_size = 48
    fcw_size = 47


    d_kv= np.pi/2**fcw_size        # NCO gain in rad/count
    return (d_kv,)


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### Phase Detector
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "digital_phase_detector.png",
                alt="Digital phase detector",
            ),
        ]
    )
    return


@app.cell
def _():
    precision = 16               # precision of both phase detector inputs
    d_kpd = 2**(precision-1)     # Phase detector gain counts/rad
    return (d_kpd,)


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    ### PI Loop Filter
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "pi_loop_filter_block_diagram.png",
                alt="PI loop filter block diagram",
            ),
            mo.md(
                r"""
    $$H(z) = P+I\frac{1}{z-1} = \frac{\tau_2}{\tau_1} + \frac{1}{\tau_1}\frac{1}{z-1}$$

    $$=\frac{\tau_2(z-1) + 1}{\tau_1(z-1)} = \frac{\tau_2z +1 - \tau_2}{\tau_1(z-1)} $$

    ### Open Loop Gain

    $$G_{OL}(z)= \frac{k_Vk_{PD}}{z-1}H(z)$$

    $$=  \bigg(\frac{k_Vk_{PD}}{z-1}\bigg)\bigg(\frac{\tau_2z +1 - \tau_2}{\tau_1(z-1)}\bigg)$$

    $$ = \bigg(\frac{k_Vk_{PD}}{\tau_1}\bigg)\bigg(\frac{\tau_2z +1 - \tau_2}{(z-1)^2}\bigg)$$
    """
            ),
        ]
    )
    return


@app.cell
def _(con, d_kpd, d_kv, fs_1):
    # since we'll iterate on gain constants, make the open loop gain a function
    def gol_digital(tau1, tau2):
    # setting dt is what makes this a transfer function in z instead of s (digital instead of analog)
    # setting dt will not affect the decision to use normalized frequency or not (gains don't change)
    # but will effect the units on the horizontal axis for Bode plots
        return d_kv * d_kpd / tau1 * con.tf([tau2, 1 - tau2], [1, -2, 1], dt=1 / fs_1)

    return (gol_digital,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Starting Loop Values

    Like we did for the analog 2nd order PLL, we'll first set $\tau_2=0$ and adjust $\tau_1$ (primary gain control) such that the zero dB gain crossing is right at the loop bandwidth.

    With $\tau_2=0$, the open loop gain simplifies to:

    $$ G_{OL}(z)|_{\tau_2=0}= \bigg(\frac{k_Vk_{PD}}{\tau_1(z-1)^2}\bigg)$$

    Similar to estimating $\tau_1$ in the analog loop, but with added complexity of the unit circle on the z-plane being the frequency axis. Therefore we set $z=e^{j\omega_c}$  (like we set $s=\omega_c$ for the analog loop), and determine $\tau_1$ such that $|G_{OL}(z)|=1$

    This becomes:

    $$\tau_1 = \bigg| \frac{k_Vk_{PD}}{(e^{j\omega_c}-1)^2}  \bigg| $$

    Assuming a positive $k_V$ and $k_{PD}$ (when negative that is considered the negative feedback for the loop and only positive gain values are used), then

    $$\tau_1 =\frac{k_Vk_{PD}}{|(e^{j\omega_c}-1)|^2}  $$

    Note for $\omega_c<< 1$,   $|(e^{j\omega_c}-1)|^2  \approx \omega_c^2$ (looking at that graphically on the complex plane provides great intuition for this) and for these cases we end up with a similar equation to the analog loop:

    $$\tau_1 \approx \frac{k_Vk_{PD}}{\omega_c^2}, \text{   for } \omega_c<< 1  $$

    This is intuitively pleasing as we would expect the loop models to match the analog models if we significantly oversample the loop. Since we are dealing with normalized frequencies in the digital case (divide by the sampling rate), as the sampling rate increases, $\omega_n$ will get increasingly smaller for the same loop bandwidth in Hz.

    Since we are iterating after setting the initial values, this will be a sufficient estimate even for higher frequency cases.

    We'll then add the zero at (45° phase margin) or slightly below (higher phase margin) the loop bandwidth for stability.

    This will increase the bandwidth slightly, so then iterate on both from these starting values to decrease the loop gain using $\tau_1$, and increase or decrease $\tau_2$ while observing response on Bode plot for desired gain and phase margin.
    """)
    return


@app.cell
def _(d_kpd, d_kv, d_lbw, np):
    print(f"Target loop bw = {d_lbw:0.5f} rad/sample")
    print(f" = {d_lbw/(2*np.pi):0.4f} cycles/sample")

    d_tau1_init = (d_kv * d_kpd)/d_lbw**2
    print(f"Initial value for tau1 = {d_tau1_init:0.2e}")
    return (d_tau1_init,)


@app.cell
def _(con, d_tau1_init, fs_1, gol_digital, mo, plt):
    _d_tau2_zero = 0
    d_gol = gol_digital(d_tau1_init, _d_tau2_zero)
    print(d_gol)
    plt.figure()
    __ = con.bode(d_gol, Hz=True, dB=True)
    plt.subplot(2, 1, 1)
    plt.title('Bode Plot')
    plt.axis([1, fs_1 / 2, -100, 100])
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note the additional lagging phase due to the parastic $z^{-1}$ delays in the implementation. This will limit the minimum sampling rate to loop bandwidth ratio.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Reset button for the two digital tau sliders below. The counter in value/on_click
    # is what makes the click observable: each press bumps the value, which re-runs the
    # cell that creates the sliders, rebuilding both of them at 0.
    d_tau_reset = mo.ui.button(
        value=0,
        on_click=lambda n: n + 1,
        label="Reset d_tau1 and d_tau2 to recommended",
    )
    return (d_tau_reset,)


@app.cell
def _(d_lbw, d_tau1_init):
    # The design point for the digital loop, from the iteration described below.
    # Kept in its own cell on purpose: marimo tracks dependencies per cell, so if these
    # lived alongside the slider-driven values the Time Sequenced Component Model would
    # re-run its 8 second bit-accurate simulation on every slider move.
    d_tau2_design = 2 / d_lbw
    d_tau1_design = 2.2 * d_tau1_init  # adjusts gain as 1/tau1
    return d_tau1_design, d_tau2_design


@app.cell(hide_code=True)
def _(d_tau_reset, mo):
    # Sliders for the digital compensated loop, in decades relative to the iterated
    # design values (d_tau1 = 2.2 x d_tau1_init, d_tau2 = 2 / d_lbw), so 0 is the
    # recommended setting. Displayed under the plot in the next cell.
    #
    # Reading the reset button here is what wires it up: clicking re-runs this cell,
    # which re-creates both sliders back at 0.
    _ = d_tau_reset.value

    d_tau1_1_slider = mo.ui.slider(
        start=-1.0,
        stop=1.0,
        step=0.05,
        value=0.0,
        label="d_tau1 scaling, decades from recommended (0 = recommended)",
        show_value=True,
    )
    d_tau2_1_slider = mo.ui.slider(
        start=-1.0,
        stop=1.0,
        step=0.05,
        value=0.0,
        label="d_tau2 scaling, decades from recommended (0 = recommended)",
        show_value=True,
    )
    return d_tau1_1_slider, d_tau2_1_slider


@app.cell
def _(
    con,
    d_lbw,
    d_tau1_1_slider,
    d_tau1_design,
    d_tau2_1_slider,
    d_tau2_design,
    d_tau_reset,
    fs_1,
    gol_digital,
    mo,
    np,
    plt,
):
    # inial values were tau2 = 1/lbw and tau1 = 1.4 x tau1 computed above for a 45 degree phase margin
    # then to increase phase margin to increase the damping factor and keep the same loop bw,
    # end result after interating: tau2 = 4fs/lbw, tau1 = 4 x tau1 computed above

    # adjusts phase as 1/tau2, this will change the zeo crossing, so adjust tau1 to compensate:

    # what the sliders explore: the loop model analysis follows these
    d_tau2 = d_tau2_design * 10 ** d_tau2_1_slider.value
    d_tau1 = d_tau1_design * 10 ** d_tau1_1_slider.value
    print(f'd_tau2={d_tau2!r}')
    print(f'd_tau1={d_tau1!r}')
    d_gol_1 = gol_digital(d_tau1, d_tau2)

    # method='frd' matches the bode call below and avoids the poly-method fallback warning
    _gm, _pm, _sm, _wpc, _wgc, _wms = con.stability_margins(d_gol_1, method='frd')
    _r1 = 10 ** d_tau1_1_slider.value
    _r2 = 10 ** d_tau2_1_slider.value
    _n1 = "recommended" if abs(d_tau1_1_slider.value) < 1e-9 else f"{_r1:0.2f} x recommended"
    _n2 = "recommended" if abs(d_tau2_1_slider.value) < 1e-9 else f"{_r2:0.2f} x recommended"
    _cross = f"{_wgc / (2 * np.pi):0.1f} Hz" if np.isfinite(_wgc) else "n/a"
    _margin = f"{_pm:0.1f} deg" if np.isfinite(_pm) else "n/a"
    _ftarget = d_lbw * fs_1 / (2 * np.pi)

    # axes pinned so the curve slides across a fixed frame as the taus vary
    _wlo, _whi = 1.0, np.pi * fs_1
    _flo, _fhi = _wlo / (2 * np.pi), _whi / (2 * np.pi)

    plt.figure()
    con.bode(d_gol_1, dB=True, Hz=True, display_margins=True, margins_method='frd',
             omega_limits=[_wlo, _whi])

    plt.subplot(2, 1, 1)
    plt.axhline(0, color="0.6", linewidth=0.8)
    plt.axvline(_ftarget, color="r", linestyle="--", linewidth=1.2, label="target loop BW")
    plt.legend(loc="lower left", fontsize=8)
    plt.xlim(_flo, _fhi)
    plt.ylim(-100, 145)
    plt.grid()
    plt.title('Bode Plot')

    plt.subplot(2, 1, 2)
    plt.xlim(_flo, _fhi)
    plt.ylim(-190, -80)
    plt.grid()

    mo.vstack(
        [
            plt.gcf(),
            d_tau1_1_slider,
            d_tau2_1_slider,
            d_tau_reset,
            mo.md(
                f"d_tau1 = **{d_tau1:0.4e}** ({_n1}) &nbsp;&nbsp;|&nbsp;&nbsp; "
                f"d_tau2 = **{d_tau2:0.4e}** ({_n2})"
            ),
            mo.md(
                f"0 dB crossing = **{_cross}** (target {_ftarget:0.1f} Hz) "
                f"&nbsp;&nbsp;|&nbsp;&nbsp; phase margin = **{_margin}**"
            ),
        ]
    )
    return (d_gol_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The vertical line in plots above on right is to show Nyquist, and is not part of the response.

    Ignore the reported gain margin since the phase didn't cross 180 degrees it was unable to detect the margin (add an extra delay sample delay to the transfer function by changing denominator to [dpll.tau1, -dpll.tau1, 0] to see proper gain and phase margin computation for that case. What is significant in the above plot is the phase margin and showing us the zero crossing close to 400 Hz.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Closed Loop
    """)
    return


@app.cell
def _(con, d_gol_1):
    # Closed Loop from Ref Input to VCO Output
    d_gcl1 = con.minreal(d_gol_1 / (1 + d_gol_1))
    print(d_gcl1)
    return (d_gcl1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pole Zero Map
    """)
    return


@app.cell
def _(con, d_gcl1, mo, plt):
    plt.figure(figsize=(5.5,5.5))
    con.pzmap(d_gcl1, grid=True)
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Closed Loop Time Domain Response (Step)

    See notes above in the Closed Loop Time Domain Response for the analog loop about interpreting these plots. The plots show the response in the units of the output port to a normalized step in the units for that input port. (so in this case a response in phase to a step in phase).
    """)
    return


@app.cell
def _(con, d_gcl1, mo, plt):
    plt.figure(figsize=(7,4))
    plt.plot(*con.step_response(d_gcl1))
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Step Response Signal In to NCO Out")
    plt.grid()
    plt.axis([0, .025, 0, 1.5])
    plt.tight_layout()
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Closed Loop Frequency Domain Response

    The vertical line in plot on right is to show Nyquist, and is not part of the response.
    """)
    return


@app.cell
def _(con, d_gcl1, fs_1, mo, np, plt):
    plt.figure(figsize=(7, 5))
    con.bode(d_gcl1, dB=True, Hz=True, omega_limits=[2 * np.pi * 10, 2 * np.pi * fs_1 / 2])
    plt.subplot(2, 1, 1)
    plt.title('Frequency Response, Ref In to VCO Out')
    plt.tight_layout()
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Time Sequenced Component Model

    This is not the Loop Model but a model of the actual implementation.

    Below is a bit and cycle accurate Component Object model. A Component Object takes inputs and provides outputs on each sample of a "master clock" for discrete time time stepped simulations. Modelling with Component Objects is detailed in my course "Python Applications for Digital Design and Signal Processing". This is a simulation of the actual implementation which would capture non-linear effects, which we compare against the much simpler Loop Model developed above. It uses the loop constants derived there.
    """)
    return


@app.cell
def _(math):
    # NCO Component:

    def Nco(sum1=0, acc_size=28, lut_addr=14, lut_out=16):
        '''
        NCO as a Component Object
        Parameters are object initialation:
        sum1: initial state (count) for accumulator
        acc_size: accumulator precision in bits (wrap on overflow)
        lut_addr: look-up table address precision in bits
        lut_out: look-up table data precision in bits

        (fcw input size is one less than acc_size)
        Dan Boschen 9/25/2023

        To use:
        instantiate:  my_nco= NCO(....)
        prime:        my_nco.send(None)
        pass in fcw and pcw samples and get sample out for each clock cycle: 
                      output = my_nco.send((fcw, pcw))

        '''
        data = None
        while True:
            fcw, pcw = yield data

            sum2 = (sum1 + pcw) % 2**acc_size         # max bit width acc_size
            sum2 = sum2 // 2**(acc_size - lut_addr)   # phase truncation
            sum1 = (sum1 + fcw) % 2**acc_size    # modulo acccumulator

            sine = math.sin((2 * math.pi * sum2) / 2**lut_addr)
            # maps -1/+1 sine to the signed digital range -2**(lut_out-1) to 2**(lut_out-1)-1:
            data = round(((sine+1)/2  * (2**(lut_out)-1)- (2**(lut_out)-1)/2)-.5)

    return (Nco,)


@app.function
# Loop Filter Component
def PropIntFilter(accum, integral, proportional):
    sum_out = accum
    while True:
        # allows for updating integral and proportional gain on each input sample
        error_sig = (yield sum_out)
        accum = accum + error_sig
        sum_out = integral * accum + proportional * error_sig


@app.cell
def _(signal_out):
    # Top Level DPLL Component Model

    def Dpll(nco, loopfilter, integral, bitw):
        '''
        nco: instantiated and primed NCO Component: requires fcw, pcw inputs and provides data output
        fcw: initial state for nco input
        loopfilter: instantiated and primed Loop Filter Component: requires err input and provides control output
        bitw: bit width of input and output (currently limited to be the same)
        '''
        while True:
            signal_in = yield signal_out

            # phase detector
            phase_err = int((signal_in * signal_out)/2**(bitw-1))     # scales back to same precision as input

            # loop filter
            fcw = loopfilter.send(phase_err)

            # NCO
            signal_out = nco.send((fcw, 0))   # no phase change input (pcw) used

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Functional Tests
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    #### Functional Test of Loop Filter and NCO
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "functest_loop_filter_nco.png",
                alt="Functional test: loop filter and NCO",
            ),
        ]
    )
    return


@app.cell
def _(Nco, acc_size, lut_addr, lut_out, mo, plt):
    # Functional Test of Loop Filter and NCO
    # Simple Open Loop Test with P=0 (integrate only) resulting in ramping FCW
    nsamps = 2 ** 14
    _nco = Nco(sum1=0, acc_size=acc_size, lut_addr=lut_addr, lut_out=lut_out)
    _nco.send(None)  # number of samples ot simulate
    _loop_filter = PropIntFilter(accum=0, integral=2 ** (acc_size - lut_out - 5), proportional=0)
    # instantiate and prime components
    _loop_filter.send(None)
    result = []
    fcw_result = []
    error = 1
    for _n in range(nsamps):
        _fcw = _loop_filter.send(error)
    # run sim
        fcw_result.append(_fcw)
        result.append(_nco.send((_fcw, 0)))
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(fcw_result)
    plt.title('Frequency Control Word')
    plt.subplot(2, 1, 2)
    plt.plot(result)
    plt.title('NCO Output')
    # plot results
    plt.xlabel('Time (samples)')
    plt.tight_layout()
    mo.mpl.interactive(plt.gcf())
    return error, fcw_result


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.md(
                r"""
    #### Functional Test of NCO and Phase Detector
    """
            ),
            mo.image(
                mo.notebook_dir() / "img" / "functest_nco_phase_detector.png",
                alt="Functional test: NCO and phase detector",
            ),
        ]
    )
    return


@app.cell
def _(
    Nco,
    acc_size,
    error,
    fcw_result,
    fs,
    lut_addr,
    lut_out,
    mo,
    np,
    plt,
    sig,
):
    # Phase Detector

    nsamps_1 = 1000

    # create two NCO's offset in frequency
    # set initial fcw for 19KHz
    fcw1 = int(19000.0 * 2 ** acc_size / fs)  # frequency for nco1
    fcw2 = int(20000.0 * 2 ** acc_size / fs)  # frequency for nco2
    print(f'fcw1={fcw1!r}')
    print(f'fcw2={fcw2!r}')

    # instantiate and prime components
    nco1 = Nco(sum1=0, acc_size=acc_size, lut_addr=lut_addr, lut_out=lut_out)
    nco1.send(None)
    nco2 = Nco(sum1=0, acc_size=acc_size, lut_addr=lut_addr, lut_out=lut_out)
    nco2.send(None)
    _loop_filter = PropIntFilter(accum=0, integral=2 ** (acc_size - lut_out - 5), proportional=0)
    _loop_filter.send(None)

    # run sim:
    result_nco1 = []
    result_nco2 = []
    result_pd = []
    for _n in range(nsamps_1):
        _fcw = _loop_filter.send(error)
        fcw_result.append(_fcw)
        nco1_out = nco1.send((fcw1, 0))
        nco2_out = nco2.send((fcw2, 0))
        _phase_err = int(nco1_out * nco2_out / 2 ** (lut_out - 2))
        result_nco1.append(nco1_out)
        result_nco2.append(nco2_out)
        result_pd.append(_phase_err)
        _fcw = _loop_filter.send(_phase_err)

    # plot results
    plt.figure(figsize=(8, 5))
    plt.subplot(2, 1, 1)
    plt.plot(result_nco1)
    plt.plot(result_nco2)
    plt.title('Test NCO Outputs')
    plt.subplot(2, 1, 2)
    plt.plot(result_pd)
    plt.plot(sig.filtfilt(np.ones(10), 10, result_pd))
    plt.title('PD Output')
    plt.xlabel('Time (samples)')
    plt.tight_layout()
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Closed Loop Simulation
    """)
    return


@app.cell
def _(
    Nco,
    acc_size,
    d_tau1_design,
    d_tau2_design,
    fs,
    lut_addr,
    lut_out,
    pilot,
):
    nsamps_2 = int(8 * fs)  # number of samples ot simulate; -1 = all samples
    print(f'nsamps={nsamps_2!r}')
    print(f'fs={fs!r}')
    print(f'acc_size={acc_size!r}')
    print(f'lut_addr={lut_addr!r}')
    print(f'lut_out={lut_out!r}')

    # instantiate and prime components
    _nco = Nco(sum1=0, acc_size=acc_size, lut_addr=lut_addr, lut_out=lut_out)
    _nco.send(None)
    # loop constants as designed in the Loop Model above
    tau1 = d_tau1_design
    tau2 = d_tau2_design
    print(f'tau1={tau1:0.5f}')
    print(f'tau2={tau2:0.5f}')

    # other values determined:
    #  LBW          tau1           tau2
    #  20 Hz        0.0037566      3055.774907364391
    #  100 Hz       0.00015        611.154981472878
    #  200 Hz       3.756604e-5    305.57749

    integral = int(1 / tau1)
    print(f'integral={integral:}')
    proportional = int(tau2 / tau1)
    print(f'proportional={proportional:}')
    fcw_start = int(19000.0 * 2 ** acc_size / fs)
    print(f'fcw_start={fcw_start!r}')
    accum_state = fcw_start * tau1  # sets initial state at 19KHz
    _loop_filter = PropIntFilter(accum=accum_state, integral=integral, proportional=proportional)
    _loop_filter.send(None)

    # run sim
    result_1 = []
    test_point = []
    nco_out = 0
    error_1 = 1
    for sample in pilot[:nsamps_2]:  # use pilot, clean,
        _phase_err = sample * nco_out / 2 ** (lut_out - 1)
        # _phase_err = np.sign(sample) * nco_out / 2
        _fcw = _loop_filter.send(_phase_err)
        nco_out = _nco.send((_fcw, 0))
        test_point.append(_fcw)
        result_1.append(nco_out)
    return nsamps_2, result_1, test_point


@app.cell
def _(fs, np, plt, test_point):
    plt.figure()
    #plt.plot(result)
    time = np.arange(len(test_point))/fs
    plt.plot(time, np.array(test_point))
    plt.xlabel("Time (seconds)")
    plt.title("FCW")
    return (time,)


@app.cell
def _(fs, lut_out, np, plot_spectrum, plt, result_1, srate):
    plt.figure()
    plot_start = int(0.5 * fs)
    #plt.subplot(1,2,1)
    plot_spectrum(np.array(result_1[plot_start:]) / 2 ** (lut_out - 1))
    plt.axis([0, srate / 2, -100, 0])
    plt.title('PLL Locked Output')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('dBFS')
    return


@app.cell
def _(nsamps_2, pilot, plt, result_1, time):
    plt.figure()
    plt.plot(time, result_1)
    plt.plot(time, pilot[:nsamps_2])
    plt.title('Locked NCO Output and Input')
    plt.xlabel('Time (seconds)')
    return


@app.cell
def _(clean, fs, ftone, np, nsamps_2, phase_det, pilot, plt, result_1):
    filtered_phase_OL = phase_det(pilot[:nsamps_2], clean[:nsamps_2], ftone, fs, ntaps=501, fpass=500, fstop=1000)
    time_axis = np.arange(nsamps_2) / fs
    filtered_phase_CL = phase_det(pilot[:nsamps_2], result_1, ftone, fs, ntaps=501, fpass=500, fstop=1000)
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.plot(time_axis, filtered_phase_OL)
    plt.xlabel('Time (s)')
    plt.ylabel('Phase (rad)')
    plt.title('Filtered Pilot Phase vs Time Before PLL')
    #plt.axis(
    plt.subplot(1, 2, 2)
    plt.plot(time_axis, filtered_phase_CL)
    plt.xlabel('Time (s)')
    plt.ylabel('Phase (rad)')
    plt.title('Extracted Pilot Phase vs Time After PLL')
    plt.tight_layout()
    plt.gcf()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mapping s to z

    A deeper understanding of poles and zeros and there significance in placement on the s and z planes is very helpful in control system design.

    The simple "matched-z" mapping was used to demonstrate mapping from the Laplace Transform to the z-Trasform using:

    $$z=e^{sT}$$

    The graphics below show how a grid in the s plane would transform to the z plane.

    The matched z transform is instructional but has limited use as it doesn't in all cases maintain either the time or frequency domain response for the system. However when used to map systems with poles only, it will provide an impulse invariant result identical to the Method of Impulse Invariance (so retains the time domain response in the mapping for those cases).
    """)
    return


@app.cell
def _(mo, np, plt):
    # graphically showing the mapping from s to z for z=e^s
    # by drawing a 

    xbox = (-5, 0)
    ybox = (-2.5, 2.5)
    grids=20
    vert = np.linspace(ybox[0], ybox[1],100)
    omega = np.linspace(ybox[0], ybox[1], grids)

    horiz = np.linspace(xbox[0], xbox[1],100)
    sigma = np.linspace(xbox[0], xbox[1], grids)



    yaxis = np.zeros(100)+1j*np.linspace(-3,3,100)
    xaxis = np.linspace(-5,.5,100) + 1j*np.zeros(100)


    plt.figure(figsize=(8,4))

    # s plane
    plt.subplot(1,2,1)


    # plot vertical and horizontal axis
    plt.plot(np.real(xaxis), np.imag(xaxis), 'k', linewidth=3)
    plt.plot(np.real(yaxis), np.imag(yaxis), 'k', linewidth=3)

    for s in sigma:
        plt.plot(np.real((s+1j*vert)), np.imag((s+1j*vert)), 'r')

    for o in omega:    
        plt.plot(np.real((horiz+1j*o)), np.imag((horiz+1j*o)), 'g')


    # plot dot at orgin
    plt.plot(0, 0, 'ro')

    plt.axis('equal')
    plt.title('s Plane')
    plt.grid()
    # zplane
    plt.subplot(1,2,2)


    #plot vertical and horizontal axis
    plt.plot(np.real(np.exp(xaxis)), np.imag(np.exp(xaxis)), 'k', linewidth=3)
    plt.plot(np.real(np.exp(yaxis)), np.imag(np.exp(yaxis)), 'k', linewidth=3)


    # plot the unit circle
    circle = np.linspace(0, 2*np.pi, 100)
    plt.plot((np.cos(circle)), (np.sin(circle)), 'k--', linewidth=0.5)


    for s in sigma:
        plt.plot(np.real(np.exp(s+1j*vert)), np.imag(np.exp(s+1j*vert)), 'r')

    for o in omega:    
        plt.plot(np.real(np.exp(horiz+1j*o)), np.imag(np.exp(horiz+1j*o)), 'g')


    # plot dot at orgin
    plt.plot(1, 0, 'ro')

    plt.grid()
    plt.axis('equal')
    plt.title('z Plane')
    mo.mpl.interactive(plt.gcf())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If the grid in the s plane extended to $-\pi$ and $+\pi$ vertically, then the circle would be completely filled. If the grid extends beyond $\pm\pi$ vertically, the mapping will repeat in side the unit circle (aliasing).  Zoom in on the z-plane origin to see how the vertical grid lines to the far left map with increasingly (logarithmically) closer spacing.
    """)
    return


if __name__ == "__main__":
    app.run()
