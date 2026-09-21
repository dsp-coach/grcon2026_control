# Control Systems - GNU Radio Conference 2026

**The DSP Coach, LLC**

**Last Updated: September 20, 2026**

Example material accompanying the "Control Systems" presentation by Dan
Boschen, The DSP Coach, LLC, given at the GNU Radio Conference 2026.

The notebook works through the analysis and design of a phase locked loop,
covering transfer functions, the mapping from the Laplace domain to the
z-domain, loop filter design, Bode plots and stability margins, pole-zero
placement, step response, and the effect of loop bandwidth on reference
tracking and VCO phase noise.

## Getting started

Full installation instructions, written for Windows, macOS and Linux, are in
[INSTALL.md](INSTALL.md). They cover installing Miniforge, creating a conda
environment with the libraries this notebook needs, and confirming that
everything works before the session. The conda environment file
`grcon2026_control.yml` in this folder is one of the two ways those
instructions give for creating that environment.

If you already have a working Python environment with NumPy, SciPy,
Matplotlib, python-control and marimo installed, you can simply run
`marimo edit control_systems.py`.

## Presentation
A pdf copy of the presentation is included as control_presentation_boschen.pdf

## The FM broadcast IQ recording

One section of the notebook demodulates a captured FM broadcast signal. That
recording is **not** included in this repository - see
[data/README.md](data/README.md) for how to obtain it and where to place it.
Every other part of the notebook runs without it.

## Licensing

This repository is deliberately licensed in two parts, so that the code is
genuinely reusable while the written material and slides stay attributable in
the form they were written.

| Material | License |
|---|---|
| Executable Python in `control_systems.py` and any other `.py` files | MIT - see [LICENSE](LICENSE) |
| Notebook explanatory text (`mo.md(...)` blocks), installation instructions, banner image, slides | CC BY-NC-ND 4.0 - see [LICENSE-CONTENT.md](LICENSE-CONTENT.md) |
| Datasheet figures in `img/`, listed in LICENSE-CONTENT.md | Copyright of their respective owners, not licensed here |
| The FM broadcast IQ recording | Not distributed here; no license granted |

In practical terms: take the signal processing code and do whatever you like
with it, including in commercial work. Share the explanatory material and
slides freely for non-commercial purposes with credit, but please do not
publish altered versions of them under my name.

The notebook reproduces plots from manufacturer datasheets, including
Microchip Technology Inc. device datasheets and the Analog Devices HMC733
datasheet; these are the files in `img/` named for those parts, listed
individually in LICENSE-CONTENT.md. Part of what the notebook sets out to
teach is how to pull real loop parameters, such as the phase detector gain and
the VCO tuning slope, out of published manufacturer data, so the actual curves
are shown as the subject of that discussion. Those figures belong to their
respective owners and are not covered by the licenses above; consult the
manufacturers' current datasheets directly if you are designing with these
parts.

## Contact

Questions and corrections are welcome. The DSP Coach, <https://dsp-coach.com>

© 2026 The DSP Coach, LLC
