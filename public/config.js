document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.loader-wrapper').style.display = 'none';
    var websiteName = '';
    var websiteURL = '';

    var h1Element = document.querySelector('h1');
    var text = h1Element.textContent;
    var array = text.split('/');
    var last = array[array.length - 2];
    var currentDir = last.charAt(0).toUpperCase() + last.slice(1);

    // Updating page title.
    document.title = currentDir;

    // Add folder title and href.
    h1Element.innerHTML = '<a href="/home">' + currentDir + '</a>';

    // Establish supported formats.
    var formats = ["aac", "flv", "m3u", "mp4", "srt", "webp", "avi", "folder", "m4a", "mpeg", "iso", "ts", "wma", "gif", "mkv", "mts", "txt", "wmv", "exe", "jpg", "mov", "ogg", "wav", "zip", "flac", "m2ts", "mp3", "png", "webm"]

    // Scan all files in the directory, check the extensions and show the right MIME-type image.
    var tableLinks = document.querySelectorAll('td a');
    tableLinks.forEach(function(link) {
        var hrefSplit = link.getAttribute('href').split('.');
        var fileExt = hrefSplit[hrefSplit.length - 1].toLowerCase();
        var found = false;

        formats.forEach(function(format) {
            if (fileExt === format.toLowerCase()) {
                var titleSplit = link.getAttribute('title').split('.').slice(0, -1).join('.');
                var displayedTitle = titleSplit.length > 34 ? titleSplit.substring(0, 34) + '—' : titleSplit;
                link.innerHTML = '<img class="icons" src="/icons/' + format + '.png" style="margin:0px 4px -4px 0px"></img><a href="' + link.getAttribute('href') + '">' + displayedTitle + '</a>';
                found = true;
                return;
            }
        });

        // Add an icon for the go-back link.
        if (link.textContent.indexOf("Parent directory") >= 0) {
            link.innerHTML = '<img class="icons" src="data:image/svg+xml;base64,PG5zMDpzdmcgeG1sbnM6bnMwPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiB2aWV3Qm94PSIwIDAgMjQgMjQiPjxuczA6cGF0aCBkPSJNMCAxMmw5LTh2NmgxNXY0aC0xNXY2eiIgZmlsbD0iI2NjYyIgLz48L25zMDpzdmc+" style="margin:0px 4px -4px 0px">Back';
            return;
        }

        // Check for folders as they don't have extensions.
        if (link.getAttribute('href').charAt(link.getAttribute('href').length - 1) === '/') {
            var oldText = link.textContent;
            link.innerHTML = '<img class="icons" src="/icons/folder.png" style="margin:0px 4px -4px 0px">' + oldText.substring(0, oldText.length - 1);
            return;
        }

        // Folder is error after sorting file name or file size or file type is not support, let's load folder icon.
        if (!found) {
            var oldText = link.textContent;
            link.innerHTML = '<img class="icons" src="/icons/folder.png" style="margin:0px 4px -4px 0px">' + oldText.substring(0, oldText.length - 1);
        }
    });
});
