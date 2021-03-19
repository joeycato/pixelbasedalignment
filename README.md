# pixelbasedalignment

## Description

Attempt to correct the wavy image by sweeping through the pixel columns left to right and choosing the most optimal vertical offset ( as determined by the color difference with the left neighbor column )

Special Thanks to /u/smushkan for proposing the idea!

## Python Dependencies

```
pip install Pillow
pip install colormath
pip install progressbar2
```

## Related Links

https://colab.research.google.com/drive/1E8vChvNKPBGS77_HVWqiR_ccCMCLXOH2#scrollTo=w9ncG7esirIN

Related JsFiddle (Interactive Mode)

https://jsfiddle.net/joeycato/zegwo06k/108/

Reference for scoring method: https://www.microsoft.com/en-us/research/wp-content/uploads/2004/10/tr-2004-92.pdf

Uploaded input_paris.png:
https://i.imgur.com/7TIpiRc.png

Uploaded input_paris_bad.png:
https://i.imgur.com/l4Jp30I.png

Uploaded comparison_paris.png:
https://i.imgur.com/qPdC7zG.png

Uploaded input_starrynight_bad.png:
https://i.imgur.com/UEPL0RM.png

Uploaded comparison_starry_night.png:
https://i.imgur.com/ThsDB5I.png
