set PYTHON=python
set WIDTH=1680
set HEIGHT=1050
::set WIDTH=2048
::set HEIGHT=1536
::set HERTZ=150
set HERTZ=60
set DIST=22.44
set SCREEN=22
::set XTILES=16
::set YTILES=12
REM set XTILES=4
REM set YTILES=2

REM use Butterworth?
set SMOOTH=False

set INDIR=../result/
set IMGDIR=../src/static/

set PLTDIR=./plots/
set OUTDIR=./data/
set RAWDIR=./data/raw/

REM process
REM graph.py knows xtiles and ytiles for each image and its corresponding AOIs
%PYTHON% graph.py --smooth=%SMOOTH% --indir=%RAWDIR% --imgdir=%IMGDIR% --dist=%DIST% --screen=%SCREEN% --width=%WIDTH% --height=%HEIGHT% --hertz=%HERTZ% --outdir=%OUTDIR% --pltdir=%PLTDIR%
