# Introduction
Current version provides ULS Checks (NTC-2018) on RC sections based on FEM database.

# Installation
```
pip install pysection
```

# Usage
```
from pysection import *
```
## prepare inputs files (.xlsx) 
files(src): fem_xls, res_xls[]
## prepare directories to store output data
folders: sec_dir, sln_dir, res_dir
## read design sections
```
get_sec(src, sec_dir)
```
## read fem data
```
read_fem(fem_xls, res_xls, save_to) 
```
## create sln objects
```
get_sln(src, sln_dir)
```
## run check
```
run_check(sec_dir, sln_dir, res_dir, data_hdf, data_set)
```
## generate report
### summary tables
```
report_summary(res_dir, filename, ..., detailed)
```
### single results
```
report_single(res_dir, sln_id, filename)
```
## view of results
```
create_view(sln_dir, res_dir, title, ..., view_html)
```
