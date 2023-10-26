document.addEventListener('DOMContentLoaded', function() {
var form = document.createElement('form');
var input = document.createElement('input');

input.name = 'filter';
input.className = 'search';
input.placeholder = 'Type to search...';

form.appendChild(input);

document.querySelector('h1').after(form);

var listItems = [].slice.call(document.querySelectorAll('#list tbody tr'));

input.addEventListener('keyup', function () {
    var inputValue = this.value.trim().toLowerCase();
    var normalizedInput = inputValue.normalize("NFD").replace(/[\u0300-\u036f]/g, ""); // Chuẩn hóa và loại bỏ ký tự dấu
    var regexPattern = "(^|.*[^\\pL])" + XRegExp.escape(normalizedInput).split(/\s+/).join("([^\\pL]|[^\\pL].*[^\\pL])");
    var regex = new XRegExp(regexPattern, "iu");

    listItems.forEach(function(item) {
        var anchor = item.querySelector('td a');
        if (anchor && anchor.hasAttribute('title')) {
            var anchorTitle = anchor.getAttribute('title').toLowerCase();
            var normalizedAnchorTitle = anchorTitle.normalize("NFD").replace(/[\u0300-\u036f]/g, ""); // Chuẩn hóa và loại bỏ ký tự dấu
            var comparisonResult = regex.test(normalizedAnchorTitle);

            if (comparisonResult) {
                item.removeAttribute('hidden');
            } else {
                item.hidden = true;
            }
        }
    });
});


input.addEventListener('keydown', function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
    }
});

});
