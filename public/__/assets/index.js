document.addEventListener('DOMContentLoaded', function() {
    const ____ = '';
    const keyword = document.getElementById( g0 );
    keyword.addEventListener( g1 , function(event) {
        if (keyword.value.length > 2 && event.keyCode === 13 && keyword.value.match(/^[a-zA-Z0-9\ ]+$/)) {
            const message = document.getElementById( g2 );
            message.innerHTML =  g3 ;
            const appCheck = firebase.appCheck();
            appCheck.activate( g4 , false);
            appCheck.getToken().then(function() {
                const dbRef = firebase.database().ref();
                const dataRef = dbRef.child( g5 );
                const query = keyword.value.replace(/\s(?=\s)/g, '').trim().toLowerCase();
                dataRef.orderByChild( g6 ).startAt(query).endAt(`${query}\uf8ff`).on('value', snapshot => extract(snapshot.val()), function() {
                    message.innerHTML =  g7 ;
                });
            }).catch(function() {
                message.innerHTML =  g8 ;
            });
        }
    });

    const randomId = () => Math.random().toString(36).substr(2, 9);

    const extract = function(snapshot) {
        if (snapshot === null) {
            message.innerHTML = g9 ;
        } else {
            let content = "";
            const infos = [];
            for (const [key, value] of Object.entries(snapshot)) {
                const id = randomId();
                infos.push(value.e.map(info => [[id, value.t, value.p], randomId(), info.i, info.u]));
            }
            for (const info of infos) {
                let i = 1;
                const img = (info[0][0][2] === '') ?  ga  :  gb  + info[0][0][2] +  gc ;
                content +=  gd  + info[0][0][0] +  ge  + img +  gf  + info[0][0][1] +  gg ;
                for (const [__, id, title] of info) {
                    if (title === '') {
                        content +=  gh  + id +  gi  +  gj  + i +  gk ;
                        i++;
                    } else {
                        content +=  gh  + id +  gi  + title +  gk ;
                    }
                }
                content +=  gl ;
            }
            message.remove();
            document.getElementById( gm ).innerHTML = content;
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
        meta.getElementsByClassName( gn )[0].addEventListener( gp , () => meta.getElementsByClassName( gq )[0].classList.toggle( gr ));
        meta.getElementsByClassName( go )[0].addEventListener( gp , () => meta.getElementsByClassName( gq )[0].classList.toggle( gr ));
    };

    const createWindowEventListener = function(id, encrypted) {
        document.getElementById(id).addEventListener( gp , function() {
            const blob = new Blob([ gs  + CryptoJS.AES.decrypt(encrypted,  g4 ).toString(CryptoJS.enc.Utf8) +  gt ], {type: gu });
            const objectBlob = window.URL.createObjectURL(blob);
            window.open(objectBlob,  gv ).onload = e => window.URL.revokeObjectURL(objectBlob);
        }, false);
    };
});