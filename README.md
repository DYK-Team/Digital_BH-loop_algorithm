Digital BH-loop algorithm for calculating magnetic hysteresis loops. Last update 12.02.2024

The program can be launched in two ways. The executable file "BH.exe" is located in the "dist" folder. Enter the input parameters: copy-paste the directory path, enter the file name without extension (e.g. 50kHz), amend B-scale and H-scale (1 by default), and choose the moving average window (3 by default). If you have a Python IDE, for example PyCharm, Run "BH.py" for GUI. 

A csv file (comma delimited) with data must contain only two columns: (1) signal response proportional to the magnetic induction B and (2) sinusoid proportional to the excitation field H. Four files are provided as examples: 50kHz.csv (time increment 5e-8 s), 100kHz.csv (time increment 2e-8 s), 200kHz.csv (time increment 1e-8 s), and 250kHz.csv (time increment 1e-8 s). In principle, the algorithm is universal and can integrate the differential signal from two pickup coils (longitudinal hysteresis loops, https://github.com/DYK-Team/Digital_BH-meter_NI_DAQ).

A report is provided in the PDF file in the Report folder. However, in the report we are still undecided on how to choose the scales for the fields. The flux-based method gives non-arilist values for magnetic induction. When we reach a final decision, the report will be updated. Also check out the short report on rotating hysteresis loops in the same folder.

Authors:
Ekaterina Nefedova, Dr. Mark Nemirovich, Dr. Nikolay Udanov, and Prof. Larissa Panina,
MISiS, Moscow, Russia, https://en.misis.ru/

Dr. Dmitriy Makhnovskiy,
DYK+ team, United Kingdom, www.dykteam.com
