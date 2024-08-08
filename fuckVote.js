const crypto = require('crypto');

var e = "www.annikj.cn/vote/SECRET_KEY";
encryptParam = function(n) {
    var t = [];
    for (var o in n)
        t.push(o);
    t.sort();
    var a = "";
    for (var o in t)
        a += t[o] + "=" + n[t[o]] + "&";
    return a += "key=" + e,
    crypto.createHash('md5').update(a).digest('hex');;
}

var t = {
    aFrom: 5,
    anniTime: 1722958618444,
    isQQ: false,
    pId: "15552",
    randomStr: 393939136,
    userId: 3414092
}
var i = encryptParam(t);

console.log(i);

// a8b29b3328706f11ee0b92ea98116163