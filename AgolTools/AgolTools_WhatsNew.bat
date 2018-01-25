@ECHO OFF

cd %~dp0

python -c "import AgolTools; AgolTools.WhatsNew()"

PAUSE