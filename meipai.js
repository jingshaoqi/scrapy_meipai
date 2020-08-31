function atob(input){
    input = input.replace( /= +$ /, '')
    if (input.length % 4 == 1) throw INVALID_CHARACTER_ERR;
    for (
        // initialize result and counters
        var bc = 0, bs, buffer, idx = 0, output = '';
        // get next character
        buffer = input.charAt(idx++);
        // character found in table? initialize bit storage and add its ascii value;
        ~buffer && (bs = bc % 4 ? bs * 64 + buffer: buffer,
        // and if not first of each 4 characters,
        // convert the first 8 bits to one ascii character
        bc++ % 4) ? output += String.fromCharCode(255 & bs >> (-2 * bc & 6)): 0
    ) {
          // try to find character in table (0-63, not found = > -1)
        var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        buffer = chars.indexOf(buffer);
    }
    return output;
};

var decodeMp4 = {
    getHex: function(str) {
        return {
            str: str['substring'](4),
            hex: str['substring'](0, 4)['split']('').reverse().join('')
        };
    },
    getDec: function(hex) {
        var dec = parseInt(hex, 16).toString();
        return {
            pre: dec['substring'](0, 2)['split'](''),
            tail: dec['substring'](2)['split']('')
        };
    },
    substr: function(str, pos) {
        var str0 = str['substring'](0, pos[0]);
        var str1 = str['substr'](pos[0], pos[1]);
        return str0 + str['substring'](pos[0])['replace'](str1, '');
    },
    getPos: function(str, pos) {
        pos[0] = str.length - pos[0] - pos[1];
        return pos;
    },
    decode: function(str) {
        var result0 = this.getHex(str);
        var dec = this.getDec(result0.hex);
        var result1 = this['substr'](result0.str, dec.pre);
        return atob(this['substr'](result1, this.getPos(result1, dec.tail)));
    }
};
var origin_str = '0c91Ly9tdnMLmfNZpZGVvMTAubWVpdHVkYXRhLmNvbS81ZGJkNTE0OWU0YTc2N2dnMXNmbmltMTIwMl9IMjY0X01QNWRiZDUAKzLm1wNA==';
function decodeVideo(str)
{
    return decodeMp4.decode(str);
}
// console.log(decodeVideo(origin_str));
// console.log(decodeMp4.decode(origin_str));