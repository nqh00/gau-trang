![forthebadge](https://forthebadge.com/images/badges/works-on-my-machine.svg)
# Overview
Solution to create a movie streaming website using _Jellyfin_. _Jellyfin_ is a free, open-source media server software that allows you to host your own movies, TV shows, and music collections. In this setup, _Jellyfin_ is seamlessly integrated with _Nginx_ acting as a reverse proxy for enhanced security and efficient handling of incoming requests while media files are sourced from multiple cloud drives using _Rclone_, allowing seamless playback directly from multiple clouds.
# How it works
| [Jellyfin](https://jellyfin.org) | [Nginx](https://www.nginx.com) | [Rclone](https://rclone.org) |
| -------- | ----- | ------ |
| Utilize as the core media server, managing your movie and TV show libraries. _Jellyfin Web_ offers a user-friendly interface and robust media management capabilities. | Serves as a reverse proxy, directing external requests to _Jellyfin_. It manages _SSL/TLS encryption_, load balancing, and caching, enhancing the performance and security of your media server. | Mount multiple cloud drives as a _VFS (Virtual File System)_. This integration enables _Jellyfin_ to seamlessly access and stream media files directly from the cloud, reducing the need for local storage.
# Limitations
| [Transcoding Dependency](https://jellyfin.org/docs/general/clients/codec-support) |
| -------------------------- |
| _Jellyfin_ sends media files directly to the client without prior encoding. If the media codec is unsupported or incompatible with the client (such as playing a _.mkv_ file), it relies on the client's ability to transcode the video in real-time. If the client lacks transcoding capabilities, users will not stream that media. |
# Data Flow Diagram
![diagram](https://user-images.githubusercontent.com/76725656/280393570-eb8833c6-5bcf-48b2-b277-09dbae0578c9.png)
# Screenshots
| LOGIN |
| ----- |
| ![LOGIN](https://user-images.githubusercontent.com/76725656/280264563-2eae9e10-619e-4541-affd-0451de84c18e.png) |

| HOME SCREEN |
| ----------- |
| ![HOME SCREEN](https://user-images.githubusercontent.com/76725656/280264968-5068fb12-0678-402d-8f97-bad6a3ef9d5c.png) |

| MEDIA SCREEN |
| ------------ |
| ![MEDIA SCREEN](https://user-images.githubusercontent.com/76725656/280265366-87ce9a92-e3ec-425a-a469-96c6c52b109d.png) |

| TITLE SCREEN |
| ------------ |
| ![TITLE SCREEN](https://user-images.githubusercontent.com/76725656/280266680-1d18dac5-110e-4899-a5b2-dab630fc77eb.png) |

| EPISODE SCREEN |
| -------------- |
| ![EPISODE SCREEN](https://user-images.githubusercontent.com/76725656/280269056-85fca8b3-900c-4169-a6fd-d37be5be85f6.png) |

| MEDIA PLAYER |
| ------------ |
| ![MEDIA PLAYER](https://user-images.githubusercontent.com/76725656/280269194-8457b58a-2a5a-4fb4-a5e0-8fc5d2f6fe34.png) |
