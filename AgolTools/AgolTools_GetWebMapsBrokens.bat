@ECHO OFF

cd %~dp0

python -c "import AgolTools; AgolTools.GetWebMaps('AgolTools_GetWebMapsBroken', True)"

PAUSE