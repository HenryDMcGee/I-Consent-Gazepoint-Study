set PYTHON=python
::set WIDTH=1600
::set HEIGHT=900
set WIDTH=1680
set HEIGHT=1050
::set WIDTH=2048
::set HEIGHT=1536
set HERTZ=60
set DIST=22.44
set SCREEN=22
::set XTILES=16
::set YTILES=12
set XTILES=4
set YTILES=2

REM use Butterworth?
set SMOOTH=False

set INDIR=../../exp/jaconde/
set IMGDIR=../../stimulus/jaconde/
set IMGDIR=../../stimulus/jaconde/

set PLTDIR=./plots/
set OUTDIR=./data/
set RAWDIR=./data/raw/

REM process
%PYTHON% filter.py --smooth=%SMOOTH% --indir=%RAWDIR% --imgdir=%IMGDIR% --dist=%DIST% --screen=%SCREEN% --width=%WIDTH% --height=%HEIGHT% --hertz=%HERTZ% --xtiles=%XTILES% --ytiles=%YTILES%
