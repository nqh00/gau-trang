document.addEventListener('DOMContentLoaded', function() {
    const keyword = document.getElementById('kw');
    keyword.addEventListener('keyup', function(event) {
        if (keyword.value.length > 2 && event.keyCode === 13 && keyword.value.match(/^[a-zA-Z0-9\ ]+$/)) {
            const message = document.getElementById('message');
            message.innerHTML = '<div class="loading"><span></span><span></span><span></span><span></span></div>';
            const appCheck = firebase.appCheck();
            appCheck.activate('6LeEFHwcAAAAAJ4i-kvaHhGiIMu7C9OKXke6aVQr', false);
            appCheck.getToken().then(function() {
                const dbRef = firebase.database().ref();
                const dataRef = dbRef.child('___');
                const query = keyword.value.replace(/\s(?=\s)/g, '').trim().toLowerCase();
                dataRef.orderByChild('t').startAt(query).endAt(`${query}\uf8ff`).on('value', snapshot => extract(snapshot.val()), function() {
                    message.innerHTML = '<p class="paragraph">Permission denied.</p>';
                });
            }).catch(function() {
                message.innerHTML = '<p class="paragraph">Unable to verify the token, please try again later.</p>';
            });
        }
    });

    const randomId = () => Math.random().toString(36).substr(2, 9);

    const extract = function(snapshot) {
        if (snapshot === null) {
            message.innerHTML = '<p class="paragraph">No results found.</p>';
        } else {
            let content = "";
            const infos = [];
            for (const [key, value] of Object.entries(snapshot)) {
                const id = randomId();
                infos.push(value.e.map(info => [[id, value.t, value.p], randomId(), info.i, info.u]));
            }
            for (const info of infos) {
                let i = 1;
                const img = (info[0][0][2] === '') ? 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs%3D' : `img/posters/${info[0][0][2]}.jpg`;
                content += `<div class="movie" id="${info[0][0][0]}"><img class="poster" width="200px" height="300px" src="${img}" loading="lazy"/><p class="title">${info[0][0][1]}</p><div class="episode"><ol class="list">`;
                for (const [__, id, title] of info) {
                    if (title === '') {
                        content += `<li class="list-item"><a href="javascript:;" class="bonsoir" id="${id}">Link #${i}</a></li>`;
                        i++;
                    } else {
                        content += `<li class="list-item"><a href="javascript:;" class="bonsoir" id="${id}">${title}</a></li>`;
                    }
                }
                content += '</ol></div></div>';
            }
            message.remove();
            document.getElementById('mc').innerHTML = content;
            for (const info of infos) {
                createShowEventListener(info[0][0][0]);
                for (const [__, id, ___, slug] of info) {
                    createWindowEventListener(id, slug);
                }
            }
        }
    };

    const createShowEventListener = function(id) {
        const meta = document.getElementById(id);
        meta.getElementsByClassName("poster")[0].addEventListener('click', () => meta.getElementsByClassName("episode")[0].classList.toggle("show"));
        meta.getElementsByClassName("title")[0].addEventListener('click', () => meta.getElementsByClassName("episode")[0].classList.toggle("show"));
    };

    const createWindowEventListener = function(id, slug) {
        document.getElementById(id).addEventListener('click', function() {
            const doc = window.open('', '_blank').document;
            doc.implementation.createHTMLDocument();
            doc.title = 'Bonsoir';
            doc.head.insertAdjacentHTML('beforeend', '<style>html{background:#000}.plr{position:fixed;top:0;right:0;bottom:0;left:0}</style>');
            doc.body.innerHTML = `<div class="plr"><video controls width="100%" height="100%"><source src="https://storage.googleapis.com/${slug}.mp4" type="video/mp4">`;
            doc.close();
        }, false);
    } 
});