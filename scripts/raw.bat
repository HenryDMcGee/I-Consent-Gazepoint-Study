set PYTHON=python

set INDIR=../result/
set IMGDIR=../src/static/

set PLTDIR=./plots/
set OUTDIR=./data/
set RAWDIR=./data/raw/

REM raw
%PYTHON% csv2raw.py --indir=%INDIR% --outdir=%RAWDIR%
