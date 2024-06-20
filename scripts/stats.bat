set R="C:\Program Files\R\R-3.5.0\bin\R.exe"

::set XTILES=16
::set YTILES=12
set XTILES=4
set YTILES=2

REM stats
%R% --vanilla --args %XTILES% %YTILES% < tm.R > tm.out
%R% --vanilla < fxtn-aois.R > fxtn-aois.out
%R% --vanilla < anns.R > anns.out
