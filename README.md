# yt-to-xspf
A command line tool that takes a YouTube playlist URL (in the format
`https://youtube.com/playlist?list=<shortcode>`) and outputs a XSPF playlist
file for VLC. It may work with other services supported by yt-dlp and other players
that support the XSPF standard for playlist but it is not tested.

One can also theoretically use the package as a library to provide their own 
playlist_info dictionary (e.g. to do filtering before generating the XSPF) or embed
in another program rather than using the CLI, but these are also not tested.