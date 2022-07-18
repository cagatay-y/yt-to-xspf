#! /usr/bin/env python3

"""Convert a playlist to a XSPF file via yt-dlp"""

__version__ = "0.1"

import yt_dlp
import argparse
import sys
import xml.etree.ElementTree as ET

if __name__=='__main__':
    main()
    
def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Convert a playlist to a XSPF file via yt-dlp')
    parser.add_argument("playlist_url", help="URL of the playlist")
    parser.add_argument("-o", "--output", type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
   
    # Prevent yt-dlp from printing when outputting to stdout to keep output directable
    playlist_info = extract_playlist_info(args.playlist_url, quiet_yt_dlp=(args.output == sys.stdout))
    xspf = generate_xspf(playlist_info)
    ET.indent(xspf)
    xspf.write(args.output, encoding='unicode')
    
def extract_playlist_info(playlist_url: str, quiet_yt_dlp: bool = False) -> dict:
    ydl_opts = {"extract_flat": True}
    if quiet_yt_dlp:
        ydl_opts["quiet"] = True 
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(playlist_url, download=False)
        
def generate_xspf(playlist_info: dict) -> ET.ElementTree:
    xspf_root = ET.Element("playlist", attrib={"xmlns": "http://xspf.org/ns/0/", "version": "1"})
    ET.SubElement(xspf_root, "title").text = playlist_info["title"]
    if playlist_info["channel"]:
        ET.SubElement(xspf_root, "creator").text = playlist_info["channel"]
    ET.SubElement(xspf_root, "annotation").text = playlist_info["description"]
    ET.SubElement(xspf_root, "info").text = playlist_info["webpage_url"]
    ET.SubElement(xspf_root, "location").text = playlist_info["webpage_url"]

    track_list = ET.SubElement(xspf_root, "trackList")
    for track_info in playlist_info["entries"]:
        track = ET.SubElement(track_list, "track")
        ET.SubElement(track, "location").text = track_info["url"]
        ET.SubElement(track, "title").text = track_info["title"]
        ET.SubElement(track, "creator").text = track_info["uploader"]
        ET.SubElement(track, "duration").text = str(int(track_info["duration"]*1000))
    
    xspf = ET.ElementTree(element=xspf_root)
    return xspf