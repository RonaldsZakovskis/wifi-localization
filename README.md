# wifi-localization

## Commands

### Requirements and Setup

As this repository is based on the "iwlist" Terminal command, it is required to
run this code from a Debian-based system, for example, Ubuntu (my case).

Run the following commands in the terminal (requires Anaconda):

```
conda create -n wifi-localization python=3.8 
conda activate wifi-localization
pip3 install wifi
pip3 install pandas
pip3 install scikit-learn
pip3 install matplotlib
```

<!---
Note: This comment can be seen in the generated HTML.
"wifi" package is used for scanning the nearby access points, for example, to
get their RSSI value.
"pandas" package is used by the code in the fingerprinting_based directory, to
create dataframes.
"scikit-learn" package is used by the code in the fingerprinting_based
directory to use SVM.
"matplotlib" package is used in the visualize file.
-->

### Usage

Run with:
```
python scan_access_points.py
```

### Cleanup

Delete the environment with:
```
conda remove -n wifi-localization --all
```
