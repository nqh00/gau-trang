![forthebadge](https://forthebadge.com/images/badges/works-on-my-machine.svg)
# Overview
This is a solution to create a media streaming website using _Jellyfin_ — a free, open-source media server software that allows you to host your own movies, TV shows, and music collections.

In this setup, _Jellyfin_ is integrated with _Nginx_ acting as a reverse proxy for enhanced security and efficient handling of incoming requests while media files are sourced from multiple cloud drives by using _Rclone_, allowing playback directly from multiple clouds.
# How it works
| [Jellyfin](https://jellyfin.org) | [Nginx](https://www.nginx.com) | [Rclone](https://rclone.org) |
| -------- | ----- | ------ |
| Utilize as the core media server, managing your movie and TV show libraries.  | Serves as a reverse proxy, directing external requests to _Jellyfin_. | Mount multiple cloud drives as a _Virtual File System_. |
| _Jellyfin Web_ offers a user-friendly interface and robust media management capabilities. | _Nginx_ manages _SSL/TLS encryption_, load balancing, and caching, enhancing the performance and security of your media server. | _Rclone_ enables _Jellyfin_ to seamlessly access and stream media files directly from the cloud, reducing the need for local storage. | 
# Limitations
|   | [Hardware Transcoding](https://jellyfin.org/docs/general/clients/codec-support) |
| - | ------------------------------------------------------------------------------- |
| Reason | _Jellyfin_ has the hardware transcoding feature but in this setup I have to disable it. My server can only afford _Jellyfin_ to send media files directly to the client without prior encoding. The clients have to transcode the video by themselves. |
| Result | If the client is trying to play a media file such as a _.mkv_ file and their device lacks transcoding capabilities, the media codec will be unsupported or incompatible with the client, thus users will not be able to stream that media. |
# Data Flow Diagram
![diagram](https://user-images.githubusercontent.com/76725656/280446653-eb8edefd-3e84-4cf5-b611-94169ff6e430.png)
# Screenshots
## DESKTOP LAYOUT
![DESKTOP](https://user-images.githubusercontent.com/76725656/280929392-46b52bff-5cb7-4b71-b500-add0c87e7297.gif)
## MOBILE LAYOUT
![MOBILE](https://user-images.githubusercontent.com/76725656/280926230-29b92339-784d-4093-ba5a-9b5642381401.gif)
