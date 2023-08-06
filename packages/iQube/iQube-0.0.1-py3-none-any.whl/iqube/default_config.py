data_fields = (
    'source_file',        # source file for SiNo evaluation
    'left_edge',          # lower index of frame location for peak selection
    'right_edge',         # upper index for frame location for peak selection
    'signal2noise',       # signal-to-noise ratio
    'slope2noise',        # slope-to-noise ratio which needs to be rescaled
    'p_kHz',              # cutoff frequency for second order butter worth filter in kHz
    'p_probe',            # probe beam power in µW
    'p_pump',             # pump beam power in µW
    'p_pd',               # power on photo diode in µW
    'comment'             # comment based on experiment and observations
)

description_fields = (
    'Source-File Name',                     # source file for SiNo evaluation
    'Lower Bound Index',                    # lower index of frame location for peak selection
    'Upper Bound Index',                    # upper index for frame location for peak selection
    'Signal-To-Noise Ratio',                # signal-to-noise ratio
    'Slope-To-Noise Ratio [a.u.]',          # slope-to-noise ratio which needs to be rescaled
    'Filter Cutoff Frequency [kHz]',        # cutoff frequency for second order butter worth filter in kHz
    'Optical Power of Probe Beam [µW]',     # probe beam power in µW
    'Optical Power of Pump Beam [µW]',      # pump beam power in µW
    'Optical Power on Photo Diode [µW]',    # power on photo diode in µW
    'Comment'                               # comment based on experiment and observations
)