# Data files

**The DSP Coach, LLC**

**Last Updated: September 20, 2026**

## The FM broadcast IQ recording (not included)

The FM demodulation section of `control_systems.py` reads a captured
baseband IQ recording of the FM broadcast band, saved as a WAV file:

```
data/SDRSharp_20150804_205139Z_0Hz_IQ.wav
```

That file is **not distributed with this repository.** It originates from the
Signal Identification Wiki, which publishes it without any stated copyright or
license terms, so there is no license that can be passed along with it here.
It is also a 24 MB file, which is more than belongs in a git repository.

To run that section of the notebook, download the IQ recording yourself from
the FM Broadcast Radio page of the Signal Identification Wiki:

<https://www.sigidwiki.com/wiki/FM_Broadcast_Radio>

Place the downloaded WAV file in this `data` folder, using the filename shown
above, and the notebook will find it.

Everything else in the notebook - the phase locked loop analysis, the transfer
functions, the Bode plots, the pole-zero maps and the step responses - runs
without this file.

If the wiki link has moved or the download is no longer available, any
baseband IQ capture of an FM broadcast station will work in its place; adjust
the sample rate in the notebook to match your own recording.
