# youtube-dl-helper  

This script is intended to help format youtube autogenerated music downloaded with youtube-dl.  

Example of autogenerated music video:  
https://www.youtube.com/watch?v=jPe0bX_GtBo  

Specifically, this tool  
1. Automatically adds artist, album, and title tags to the mp3  
2. Embeds the first frame of the video as the album cover.  
While youtube-dl does have an --embed-thumbnail option,it uses a low-quality version of the thumbnail which contains uncropped padding.

Example of original:  
![img](assets/example_original_embed_thumbnail.jpg)
  
High Quality:  
![img](assets/example_hq_embed_thumbnail.png)

Usage:  
TODO
  
Requirements:  
youtube-dl  
ffmpeg v4.x  
eyed3  
<!-- cv2   -->
