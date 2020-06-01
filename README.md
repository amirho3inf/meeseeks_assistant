
# Meeseeks Assistant
This project is under development and you can see its tutorials on [this YouTube Playlist](https://www.youtube.com/playlist?list=PLdrAyeVa-HC8iwbi274ze77WpO6hMDYlG) [Persian]

# Guide
1. Put your Vosk and SnowBoy models in directory *assets/models*
2. Make snowboy for python3 and put here
First, you have to install [snowboy dependencies](https://github.com/Kitt-AI/snowboy/blob/master/README.md#dependencies)
Then, clone the snowboy git:
```git clone https://github.com/Kitt-AI/snowboy.git```
After that, go to [snowboy/swig/Python3](https://github.com/Kitt-AI/snowboy/tree/master/swig/Python3) and run:
```make```
Note: if you on ArchLinux, run the following command before `make`, Also no need to install `libatlas`
```sed -i -e "s|-lf77blas -lcblas -llapack -latlas|-lcblas|g" -e 's/ -shared/ -Wl,-O1,--as-needed\0/g' Makefile```
When make done, go to [snowboy/examples/Python3](https://github.com/Kitt-AI/snowboy/tree/master/examples/Python3) and run the following command to delete linked files:
```rm -rf _snowboydetect.so snowboydetect.py requirements.txt resources```
And then run this to replace original files:
```cp -r ../../swig/Python3/_snowboydetect.so ../../swig/Python3/snowboydetect.py ../Python/requirements.txt ../../resources/ .```
Now copy all files in [snowboy/examples/Python3](https://github.com/Kitt-AI/snowboy/tree/master/examples/Python3) and paste in *assets/snowboy* directory
And delete the snowboy git files cloned at the first step.
