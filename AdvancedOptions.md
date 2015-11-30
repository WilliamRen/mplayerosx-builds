# Introduction #

This brief document fetures a series of Advanced options. They are intended for users who want a bit more from mplayer than what the GUI has to offer. This is work in progress, come back later.

# Filters #

## Video scaling ##

If you watch a lot of dvd videos, you are probably not satisfied with the resolution and would like to upscale the source. MPlayer can do it! The filter I use looks like this:

```
-vf scale=-3:1050 -sws 9
```

This upscales the video using the lanczos filter, until the height is 1050px. If your monitor has 1920 × 1080 pixel you can use use:

```
-vf scale=-3:1080 -sws 9
```

Hope you too can notice the difference between OSX hardware scaler and mplayer's software upscaler.

## Downmixing DTS 5.1 audio to 2-channels ##

Alot of files come with DTS audio. if you are like me and prefer to watch videos with a good pair of headphones, you need to downmix the audio properly. Basing my calculations on [this forum discussion](http://www.hydrogenaudio.org/forums/index.php?showtopic=55442) I ended up using this filter:

```
-channels 6 -af pan=2:.67:.33:.33:.67:.89:.11:.11:.89:.89:.89:.89:.89
```