// const fs = require('fs');
// const path = './save_IP.json';
// let saveIP = '';
// let saveIP = {"current": "", "list": []}
// let change = false
const reg = new RegExp('^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|[1-9])\\.' + '(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\.'+ '(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\.' + '(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$')

// if (fs.existsSync(path)) fetch(path).then((response) => response.json()).then((list) => saveIP = list);
// if (fs.existsSync(path)) fetch(path).then((text) => saveIP = text)


/*window.onbeforeunload = function write_file() {
    if (change) {
        fs.writeFile(path, saveIP, (err) => {
            console.log('Cannot write the ip file');
        })
    }
}*/


function check_ip() {
    const ip = document.getElementById('ip').value
    if (!reg.test(ip)) { alert('Please input correct IP address!'); return; }
    /*if (ip !== saveIP.current) {
        saveIP = ip;
        change = true;
        if (saveIP.list.indexOf(ip) < 0) saveIP.list.push(ip);
        console.log('add ' + ip)
    }*/
}
