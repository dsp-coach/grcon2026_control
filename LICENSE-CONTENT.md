# Content License

**The DSP Coach, LLC**

**Last Updated: September 20, 2026**

© 2026 The DSP Coach, LLC (https://dsp-coach.com)

The written and visual material in this repository - the explanatory text in
the notebook's markdown blocks (the mo.md(...) content in
`control_systems.py`), the installation instructions, the banner image, and
the accompanying "Control Systems" presentation - is licensed
under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0
International License (CC BY-NC-ND 4.0), except for the third-party material
identified below, which remains under its own terms.

To view a copy of this license, visit
<https://creativecommons.org/licenses/by-nc-nd/4.0/>

In short, you are free to share this material, in any medium or format, for
non-commercial purposes, provided you give appropriate credit to The DSP
Coach. You may not distribute a modified version of it. You may of course
modify it for your own private use.

## What this license does not cover

**The source code.** The executable Python in `control_systems.py`, and any
other `.py` files, is licensed separately under the MIT License, which permits
modification and redistribution including for commercial purposes. See
`LICENSE`. Because this is a marimo notebook, code and prose share one file:
the Python statements are MIT, while the text inside `mo.md(...)` blocks is
written material under the license above. The intent is unchanged - the signal
processing code here is yours to take and build on, while the explanatory
material and slides remain attributable to The DSP Coach in the form they were
written.

**Third-party figures from manufacturer datasheets.** Several figures shown in
the notebook are reproduced from manufacturer datasheets and are the copyright
of their respective owners:

- `hmc733_phase_noise.png` - "Typical SSB Phase Noise vs. Temperature,
  Vtune = +10V", from the Analog Devices HMC733LC4B datasheet
- `hmc733_tuning_curve.png` - "Frequency vs. Tuning Voltage, T = +25 °C",
  same datasheet
- `hmc733_tuning_slope.png` - "Sensitivity vs. Tuning Voltage, Vcc = +5V,
  T = +25 °C", same datasheet
- `pfd1k_output_voltage_vs_phase.png` - "Figure 1-7. Diff. Output Voltage vs.
  Frequency (0 dBm Pin)", from the Microchip Technology Inc. PFD1K datasheet

`vco_phase_noise_loop_model.png` is The DSP Coach's own block diagram, but it
reproduces the HMC733 phase noise plot within it, and that plot is subject to
the same terms.

They appear here as the direct subject of the accompanying commentary: the
notebook teaches how to extract loop parameters such as the phase detector
gain and the VCO tuning slope from manufacturer data, and showing the actual
published curves is what makes that method teachable. That they are stored as
separate files is a consequence of how marimo displays images, and is not an
invitation to reuse them on their own. They are **not** covered by the license
above, and no right in them is granted by this repository.
Readers wanting to work with those figures, or to design with these parts,
should obtain the current datasheets from the manufacturers directly and
observe the terms those manufacturers set:

- Analog Devices HMC733LC4B:
  <https://www.analog.com/media/en/technical-documentation/data-sheets/hmc733.pdf>
- Microchip PFD1K:
  <https://ww1.microchip.com/downloads/aemDocuments/documents/RFDS/ProductDocuments/DataSheets/PFD1K.pdf>

**Third-party images under open licenses.** Two images are the work of others,
published under their own open licenses. They are **not** covered by the
CC BY-NC-ND license above. Each remains under the license shown, and the
credit that license requires is carried with the image:

- `fm_broadcast_pilot_spectrum.png` - a screenshot of SDRConsole
  (sdr-radio.com) showing the pilot signal of an FM broadcast channel,
  obtained from Wikimedia Commons and licensed
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
  Source: <https://commons.wikimedia.org/w/index.php?curid=129702149>
- `banner_control.png` - the banner incorporates the cartoon panel from
  xkcd #912, by Randall Munroe, <https://xkcd.com/912/>, licensed
  [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/). The rest
  of the banner - the title, the conference line and the layout - is
  The DSP Coach's own work.

The CC BY-SA 4.0 image is reproduced unaltered and is assembled with
separate, independently authored material rather than adapted into it. It is
therefore included as a collection, and the share-alike condition does not
extend the BY-SA license to the surrounding material.

**The FM broadcast IQ recording.** The recording used by the FM demodulation
example is not distributed in this repository, because it originates from a
third party that publishes it without any stated license. See `data/README.md`
for how to obtain it. No right in that recording is granted here.

**The software being installed.** Miniforge, Python, NumPy, SciPy, Matplotlib,
python-control, marimo and IPython are independent open-source projects, each
distributed by its own authors under its own license. Nothing in this
repository grants, restricts or alters any right in them. Product and
company names used throughout are the trademarks of their respective owners
and appear only to identify the software concerned.

## Suggested attribution

Attribution is a condition of the license above. When you share this material,
please credit it like this:

> "Control Systems," Dan Boschen, The DSP Coach, LLC, presented at the
> GNU Radio Conference 2026.
> <https://github.com/dsp-coach/grcon2026_control>.
> Licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).

For a single slide or figure, a one-line credit on the slide is enough:

> © 2026 The DSP Coach, LLC - CC BY-NC-ND 4.0 - dsp-coach.com

If you are reusing one specific part, name it as well - for example, "loop
filter design section." Please keep the link to the license intact, do not
present the material as modified or as your own, and do not suggest that
The DSP Coach endorses you or your work.

This suggested credit covers The DSP Coach's own material only. The
third-party images identified above carry their own credit requirements,
which travel with those images.
