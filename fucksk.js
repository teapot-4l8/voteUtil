const crypto = require('crypto');

encryptParamNew = function(e, n) {
    var t = [];
    for (var o in e)
        t.push(o);
    t.sort();
    var a = "";
    for (var u in t)
        a += t[u] + "=" + e[t[u]] + "&";
    return n && (a += "key=" + n),
    crypto.createHash('md5').update(a).digest('hex');
}

var t = {
    aFrom: 5,
    anniTime: 1722958618444,
    isQQ: false,
    pId: "15552",
    randomStr: 393939136,
    userId: 3414092
}

var a = {
    uk: "d2602e5c3a2fa050cdd52cc40cbcb014"
}

var c = encryptParamNew(t, a.uk);
console.log(c);