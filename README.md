# wifi-localization

## Commands

Run the following commands in the terminal (requires Anaconda):

```
conda create -n wifi-localization python=3.8 
conda activate wifi-localization
pip3 install wifi
pip3 install pandas
```

Run with:
```
python scan_access_points.py
```

Delete with:
```
conda remove -n wifi-localization --all
```

As this repository is based on the "iwlist" Terminal command, it is required to
run this code from a Debian-based system, for example, Ubuntu (my case).
