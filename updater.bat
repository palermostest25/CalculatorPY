@echo off
move Calculator.py Calculator.py.bak
powershell -noprofile start-bitstransfer -Priority foreground -Source https://github.com/palermostest25/CalculatorPY/releases/download/latest/Calculator.py -Destination Calculator.py
echo Done!
pause
python Calculator.py