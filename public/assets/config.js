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

    function isFolderLink(link) {
        var href = link.getAttribute('href');
        var regex = /\/\?[C]\=[NSM]\&[O]\=[DA]$/;
        return href.endsWith('/') || regex.test(href);
    }

    function updateLink(link, isFolder) {
        var href = link.getAttribute('href');
        var title = link.getAttribute('title');

        if (href && title) {
            if (isFolder) {
                    link.innerHTML = '<img src="data:image/svg+xml;base64,CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIgogICAgIGNsYXNzPSJzdmctc25vd2ViIHN2Zy10aGVtZS1kYXJrIgogICAgIHg9IjAiCiAgICAgeT0iMCIKICAgICB3aWR0aD0iMTAwJSIKICAgICBoZWlnaHQ9IjMwIgogICAgIHZpZXdCb3g9IjAgMCAxMDAgMTAwIgogICAgIHByZXNlcnZlQXNwZWN0UmF0aW89InhNaWRZTWlkIG1lZXQiCj4KPGRlZnM+CiAgICA8c3R5bGU+CiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgCgogICAgICAgIC5zdmctZmlsbC1wcmltYXJ5IHsKICAgICAgICAgICAgZmlsbDogI2ZmYTEwMDsKICAgICAgICB9CgogICAgICAgIC5zdmctZmlsbC1zZWNvbmRhcnkgewogICAgICAgICAgICBmaWxsOiAjNjVDREFFOwogICAgICAgIH0KCiAgICAgICAgLnN2Zy1maWxsLXRlcnRpYXJ5IHsKICAgICAgICAgICAgZmlsbDogIzM3QTk4NzsKICAgICAgICB9CgogICAgICAgIC5zdmctc3Ryb2tlLXByaW1hcnkgewogICAgICAgICAgICBzdHJva2U6ICNmZmExMDA7CiAgICAgICAgfQoKICAgICAgICAuc3ZnLXN0cm9rZS1zZWNvbmRhcnkgewogICAgICAgICAgICBzdHJva2U6ICM2NUNEQUU7CiAgICAgICAgfQoKICAgICAgICAuc3ZnLXN0cm9rZS10ZXJ0aWFyeSB7CiAgICAgICAgICAgIHN0cm9rZTogIzM3QTk4NzsKICAgICAgICB9CiAgICA8L3N0eWxlPgo8L2RlZnM+CiAgICA8cGF0aCBkPSJNMTcuOSwzMi4yVjY3LjhBNy4xLDcuMSwwLDAsMCwyNSw3NUg3NWE3LjEsNy4xLDAsMCwwLDcuMS03LjJWMzkuM0E3LjEsNy4xLDAsMCwwLDc1LDMyLjJINTMuNkw0Ni40LDI1SDI1QTcuMSw3LjEsMCwwLDAsMTcuOSwzMi4yWiIKICAgICAgZmlsbD0ibm9uZSIgY2xhc3M9InN2Zy1zdHJva2UtcHJpbWFyeSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBzdHJva2Utd2lkdGg9IjgiLz4KCjwvc3ZnPg==" style="margin:0 5px -10px 0">' + link.getAttribute('title');
            } else {
                var hrefSplit = link.getAttribute('href').split('.');
                var fileExt = hrefSplit[hrefSplit.length - 1].toLowerCase();
                var displayedTitle = link.getAttribute('title').split('.').slice(0, -1).join('.');
                displayedTitle = displayedTitle.length > 20 ? displayedTitle.substring(0, 20) + '—' : displayedTitle + '.' ;
                link.innerHTML = '<img src="data:image/svg+xml;base64,CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIgogICAgIGNsYXNzPSJzdmctc25vd2ViIHN2Zy10aGVtZS1kYXJrIgogICAgIHg9IjAiCiAgICAgeT0iMCIKICAgICB3aWR0aD0iMTAwJSIKICAgICBoZWlnaHQ9IjI1IgogICAgIHZpZXdCb3g9IjAgMCAxMDAgMTAwIgogICAgIHByZXNlcnZlQXNwZWN0UmF0aW89InhNaWRZTWlkIG1lZXQiCj4KPGRlZnM+CiAgICA8c3R5bGU+CiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgCgogICAgICAgIC5zdmctZmlsbC1wcmltYXJ5IHsKICAgICAgICAgICAgZmlsbDogI2ZmYTEwMDsKICAgICAgICB9CgogICAgICAgIC5zdmctZmlsbC1zZWNvbmRhcnkgewogICAgICAgICAgICBmaWxsOiAjNjVDREFFOwogICAgICAgIH0KCiAgICAgICAgLnN2Zy1maWxsLXRlcnRpYXJ5IHsKICAgICAgICAgICAgZmlsbDogIzM3QTk4NzsKICAgICAgICB9CgogICAgICAgIC5zdmctc3Ryb2tlLXByaW1hcnkgewogICAgICAgICAgICBzdHJva2U6ICNmZmExMDA7CiAgICAgICAgfQoKICAgICAgICAuc3ZnLXN0cm9rZS1zZWNvbmRhcnkgewogICAgICAgICAgICBzdHJva2U6ICM2NUNEQUU7CiAgICAgICAgfQoKICAgICAgICAuc3ZnLXN0cm9rZS10ZXJ0aWFyeSB7CiAgICAgICAgICAgIHN0cm9rZTogIzM3QTk4NzsKICAgICAgICB9CiAgICA8L3N0eWxlPgo8L2RlZnM+CiAgICA8cGF0aCBkPSJNMzAuMSw4NS43SDY5LjlhNy45LDcuOSwwLDAsMCw3LjktNy45VjM5LjdhMy45LDMuOSwwLDAsMC0xLjItMi44TDU1LjEsMTUuNGEzLjksMy45LDAsMCwwLTIuOC0xLjFIMzAuMWE3LjksNy45LDAsMCwwLTcuOSw3LjlWNzcuOEE3LjksNy45LDAsMCwwLDMwLjEsODUuN1oiCiAgICAgIGZpbGw9Im5vbmUiIGNsYXNzPSJzdmctc3Ryb2tlLXByaW1hcnkiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgc3Ryb2tlLXdpZHRoPSI4Ii8+Cgo8L3N2Zz4=" style="margin:0 5px -10px 0"></img><a href="' + link.getAttribute('href') + '">' + displayedTitle + fileExt + '</a>';
            }
        } else if (link.textContent.indexOf("Parent directory") >= 0) {
            link.innerHTML = '<img src="data:image/svg+xml;base64,CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIgogICAgIGNsYXNzPSJzdmctc25vd2ViIHN2Zy10aGVtZS1kYXJrIgogICAgIHg9IjAiCiAgICAgeT0iMCIKICAgICB3aWR0aD0iMTAwJSIKICAgICBoZWlnaHQ9IjI1IgogICAgIHZpZXdCb3g9IjAgMCAxMDAgMTAwIgogICAgIHByZXNlcnZlQXNwZWN0UmF0aW89InhNaWRZTWlkIG1lZXQiCj4KPGRlZnM+CiAgICA8c3R5bGU+CiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgCgogICAgICAgIC5zdmctZmlsbC1wcmltYXJ5IHsKICAgICAgICAgICAgZmlsbDogI2ZmYTEwMDsKICAgICAgICB9CgogICAgICAgIC5zdmctZmlsbC1zZWNvbmRhcnkgewogICAgICAgICAgICBmaWxsOiAjNjVDREFFOwogICAgICAgIH0KCiAgICAgICAgLnN2Zy1maWxsLXRlcnRpYXJ5IHsKICAgICAgICAgICAgZmlsbDogIzM3QTk4NzsKICAgICAgICB9CgogICAgICAgIC5zdmctc3Ryb2tlLXByaW1hcnkgewogICAgICAgICAgICBzdHJva2U6ICNmZmExMDA7CiAgICAgICAgfQoKICAgICAgICAuc3ZnLXN0cm9rZS1zZWNvbmRhcnkgewogICAgICAgICAgICBzdHJva2U6ICM2NUNEQUU7CiAgICAgICAgfQoKICAgICAgICAuc3ZnLXN0cm9rZS10ZXJ0aWFyeSB7CiAgICAgICAgICAgIHN0cm9rZTogIzM3QTk4NzsKICAgICAgICB9CiAgICA8L3N0eWxlPgo8L2RlZnM+CiAgICA8cGF0aCBkPSJNNDMuMyw3My41LDE5LjgsNTBtMCwwTDQzLjMsMjYuNU0xOS44LDUwSDgwLjIiIGZpbGw9Im5vbmUiIGNsYXNzPSJzdmctc3Ryb2tlLXByaW1hcnkiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIKICAgICAgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgc3Ryb2tlLXdpZHRoPSI4Ii8+Cgo8L3N2Zz4=" style="margin:0 5px -10px 5px">Back';
        }
    }

    var tableLinks = document.querySelectorAll('td a');
    tableLinks.forEach(function(link) {
        var isFolder = isFolderLink(link);
        updateLink(link, isFolder);
    });

});
