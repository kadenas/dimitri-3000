(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9950],{49387:function(e,t,r){let n=r(66119),a={};for(let e of Object.keys(n))a[n[e]]=e;let i={rgb:{channels:3,labels:"rgb"},hsl:{channels:3,labels:"hsl"},hsv:{channels:3,labels:"hsv"},hwb:{channels:3,labels:"hwb"},cmyk:{channels:4,labels:"cmyk"},xyz:{channels:3,labels:"xyz"},lab:{channels:3,labels:"lab"},lch:{channels:3,labels:"lch"},hex:{channels:1,labels:["hex"]},keyword:{channels:1,labels:["keyword"]},ansi16:{channels:1,labels:["ansi16"]},ansi256:{channels:1,labels:["ansi256"]},hcg:{channels:3,labels:["h","c","g"]},apple:{channels:3,labels:["r16","g16","b16"]},gray:{channels:1,labels:["gray"]}};for(let t of(e.exports=i,Object.keys(i))){if(!("channels"in i[t]))throw Error("missing channels property: "+t);if(!("labels"in i[t]))throw Error("missing channel labels property: "+t);if(i[t].labels.length!==i[t].channels)throw Error("channel and label counts mismatch: "+t);let{channels:e,labels:r}=i[t];delete i[t].channels,delete i[t].labels,Object.defineProperty(i[t],"channels",{value:e}),Object.defineProperty(i[t],"labels",{value:r})}i.rgb.hsl=function(e){let t;let r=e[0]/255,n=e[1]/255,a=e[2]/255,i=Math.min(r,n,a),o=Math.max(r,n,a),l=o-i;o===i?t=0:r===o?t=(n-a)/l:n===o?t=2+(a-r)/l:a===o&&(t=4+(r-n)/l),(t=Math.min(60*t,360))<0&&(t+=360);let s=(i+o)/2;return[t,100*(o===i?0:s<=.5?l/(o+i):l/(2-o-i)),100*s]},i.rgb.hsv=function(e){let t,r,n,a,i;let o=e[0]/255,l=e[1]/255,s=e[2]/255,u=Math.max(o,l,s),c=u-Math.min(o,l,s),h=function(e){return(u-e)/6/c+.5};return 0===c?(a=0,i=0):(i=c/u,t=h(o),r=h(l),n=h(s),o===u?a=n-r:l===u?a=1/3+t-n:s===u&&(a=2/3+r-t),a<0?a+=1:a>1&&(a-=1)),[360*a,100*i,100*u]},i.rgb.hwb=function(e){let t=e[0],r=e[1],n=e[2];return[i.rgb.hsl(e)[0],1/255*Math.min(t,Math.min(r,n))*100,100*(n=1-1/255*Math.max(t,Math.max(r,n)))]},i.rgb.cmyk=function(e){let t=e[0]/255,r=e[1]/255,n=e[2]/255,a=Math.min(1-t,1-r,1-n);return[100*((1-t-a)/(1-a)||0),100*((1-r-a)/(1-a)||0),100*((1-n-a)/(1-a)||0),100*a]},i.rgb.keyword=function(e){let t;let r=a[e];if(r)return r;let i=1/0;for(let r of Object.keys(n)){let a=n[r],o=(e[0]-a[0])**2+(e[1]-a[1])**2+(e[2]-a[2])**2;o<i&&(i=o,t=r)}return t},i.keyword.rgb=function(e){return n[e]},i.rgb.xyz=function(e){let t=e[0]/255,r=e[1]/255,n=e[2]/255;return[100*(.4124*(t=t>.04045?((t+.055)/1.055)**2.4:t/12.92)+.3576*(r=r>.04045?((r+.055)/1.055)**2.4:r/12.92)+.1805*(n=n>.04045?((n+.055)/1.055)**2.4:n/12.92)),100*(.2126*t+.7152*r+.0722*n),100*(.0193*t+.1192*r+.9505*n)]},i.rgb.lab=function(e){let t=i.rgb.xyz(e),r=t[0],n=t[1],a=t[2];return r/=95.047,n/=100,a/=108.883,[116*(n=n>.008856?n**(1/3):7.787*n+16/116)-16,500*((r=r>.008856?r**(1/3):7.787*r+16/116)-n),200*(n-(a=a>.008856?a**(1/3):7.787*a+16/116))]},i.hsl.rgb=function(e){let t,r,n;let a=e[0]/360,i=e[1]/100,o=e[2]/100;if(0===i)return[n=255*o,n,n];t=o<.5?o*(1+i):o+i-o*i;let l=2*o-t,s=[0,0,0];for(let e=0;e<3;e++)(r=a+-(1/3*(e-1)))<0&&r++,r>1&&r--,n=6*r<1?l+(t-l)*6*r:2*r<1?t:3*r<2?l+(t-l)*(2/3-r)*6:l,s[e]=255*n;return s},i.hsl.hsv=function(e){let t=e[0],r=e[1]/100,n=e[2]/100,a=r,i=Math.max(n,.01);n*=2,r*=n<=1?n:2-n,a*=i<=1?i:2-i;let o=(n+r)/2;return[t,100*(0===n?2*a/(i+a):2*r/(n+r)),100*o]},i.hsv.rgb=function(e){let t=e[0]/60,r=e[1]/100,n=e[2]/100,a=t-Math.floor(t),i=255*n*(1-r),o=255*n*(1-r*a),l=255*n*(1-r*(1-a));switch(n*=255,Math.floor(t)%6){case 0:return[n,l,i];case 1:return[o,n,i];case 2:return[i,n,l];case 3:return[i,o,n];case 4:return[l,i,n];case 5:return[n,i,o]}},i.hsv.hsl=function(e){let t,r;let n=e[0],a=e[1]/100,i=e[2]/100,o=Math.max(i,.01);r=(2-a)*i;let l=(2-a)*o;return[n,100*(a*o/(l<=1?l:2-l)||0),100*(r/=2)]},i.hwb.rgb=function(e){let t,r,n,a;let i=e[0]/360,o=e[1]/100,l=e[2]/100,s=o+l;s>1&&(o/=s,l/=s);let u=Math.floor(6*i),c=1-l;t=6*i-u,(1&u)!=0&&(t=1-t);let h=o+t*(c-o);switch(u){default:case 6:case 0:r=c,n=h,a=o;break;case 1:r=h,n=c,a=o;break;case 2:r=o,n=c,a=h;break;case 3:r=o,n=h,a=c;break;case 4:r=h,n=o,a=c;break;case 5:r=c,n=o,a=h}return[255*r,255*n,255*a]},i.cmyk.rgb=function(e){let t=e[0]/100,r=e[1]/100,n=e[2]/100,a=e[3]/100;return[255*(1-Math.min(1,t*(1-a)+a)),255*(1-Math.min(1,r*(1-a)+a)),255*(1-Math.min(1,n*(1-a)+a))]},i.xyz.rgb=function(e){let t,r,n;let a=e[0]/100,i=e[1]/100,o=e[2]/100;return t=(t=3.2406*a+-1.5372*i+-.4986*o)>.0031308?1.055*t**(1/2.4)-.055:12.92*t,r=(r=-.9689*a+1.8758*i+.0415*o)>.0031308?1.055*r**(1/2.4)-.055:12.92*r,n=(n=.0557*a+-.204*i+1.057*o)>.0031308?1.055*n**(1/2.4)-.055:12.92*n,[255*(t=Math.min(Math.max(0,t),1)),255*(r=Math.min(Math.max(0,r),1)),255*(n=Math.min(Math.max(0,n),1))]},i.xyz.lab=function(e){let t=e[0],r=e[1],n=e[2];return t/=95.047,r/=100,n/=108.883,[116*(r=r>.008856?r**(1/3):7.787*r+16/116)-16,500*((t=t>.008856?t**(1/3):7.787*t+16/116)-r),200*(r-(n=n>.008856?n**(1/3):7.787*n+16/116))]},i.lab.xyz=function(e){let t,r,n;let a=e[0],i=e[1],o=e[2];t=i/500+(r=(a+16)/116),n=r-o/200;let l=r**3,s=t**3,u=n**3;return r=(l>.008856?l:(r-16/116)/7.787)*100,[t=(s>.008856?s:(t-16/116)/7.787)*95.047,r,n=(u>.008856?u:(n-16/116)/7.787)*108.883]},i.lab.lch=function(e){let t;let r=e[0],n=e[1],a=e[2];return(t=360*Math.atan2(a,n)/2/Math.PI)<0&&(t+=360),[r,Math.sqrt(n*n+a*a),t]},i.lch.lab=function(e){let t=e[0],r=e[1],n=e[2]/360*2*Math.PI;return[t,r*Math.cos(n),r*Math.sin(n)]},i.rgb.ansi16=function(e,t=null){let[r,n,a]=e,o=null===t?i.rgb.hsv(e)[2]:t;if(0===(o=Math.round(o/50)))return 30;let l=30+(Math.round(a/255)<<2|Math.round(n/255)<<1|Math.round(r/255));return 2===o&&(l+=60),l},i.hsv.ansi16=function(e){return i.rgb.ansi16(i.hsv.rgb(e),e[2])},i.rgb.ansi256=function(e){let t=e[0],r=e[1],n=e[2];return t===r&&r===n?t<8?16:t>248?231:Math.round((t-8)/247*24)+232:16+36*Math.round(t/255*5)+6*Math.round(r/255*5)+Math.round(n/255*5)},i.ansi16.rgb=function(e){let t=e%10;if(0===t||7===t)return e>50&&(t+=3.5),[t=t/10.5*255,t,t];let r=(~~(e>50)+1)*.5;return[(1&t)*r*255,(t>>1&1)*r*255,(t>>2&1)*r*255]},i.ansi256.rgb=function(e){let t;if(e>=232){let t=(e-232)*10+8;return[t,t,t]}return[Math.floor((e-=16)/36)/5*255,Math.floor((t=e%36)/6)/5*255,t%6/5*255]},i.rgb.hex=function(e){let t=(((255&Math.round(e[0]))<<16)+((255&Math.round(e[1]))<<8)+(255&Math.round(e[2]))).toString(16).toUpperCase();return"000000".substring(t.length)+t},i.hex.rgb=function(e){let t=e.toString(16).match(/[a-f0-9]{6}|[a-f0-9]{3}/i);if(!t)return[0,0,0];let r=t[0];3===t[0].length&&(r=r.split("").map(e=>e+e).join(""));let n=parseInt(r,16);return[n>>16&255,n>>8&255,255&n]},i.rgb.hcg=function(e){let t;let r=e[0]/255,n=e[1]/255,a=e[2]/255,i=Math.max(Math.max(r,n),a),o=Math.min(Math.min(r,n),a),l=i-o;return t=l<1?o/(1-l):0,[(l<=0?0:i===r?(n-a)/l%6:i===n?2+(a-r)/l:4+(r-n)/l)/6%1*360,100*l,100*t]},i.hsl.hcg=function(e){let t=e[1]/100,r=e[2]/100,n=r<.5?2*t*r:2*t*(1-r),a=0;return n<1&&(a=(r-.5*n)/(1-n)),[e[0],100*n,100*a]},i.hsv.hcg=function(e){let t=e[1]/100,r=e[2]/100,n=t*r,a=0;return n<1&&(a=(r-n)/(1-n)),[e[0],100*n,100*a]},i.hcg.rgb=function(e){let t=e[0]/360,r=e[1]/100,n=e[2]/100;if(0===r)return[255*n,255*n,255*n];let a=[0,0,0],i=t%1*6,o=i%1,l=1-o,s=0;switch(Math.floor(i)){case 0:a[0]=1,a[1]=o,a[2]=0;break;case 1:a[0]=l,a[1]=1,a[2]=0;break;case 2:a[0]=0,a[1]=1,a[2]=o;break;case 3:a[0]=0,a[1]=l,a[2]=1;break;case 4:a[0]=o,a[1]=0,a[2]=1;break;default:a[0]=1,a[1]=0,a[2]=l}return s=(1-r)*n,[(r*a[0]+s)*255,(r*a[1]+s)*255,(r*a[2]+s)*255]},i.hcg.hsv=function(e){let t=e[1]/100,r=t+e[2]/100*(1-t),n=0;return r>0&&(n=t/r),[e[0],100*n,100*r]},i.hcg.hsl=function(e){let t=e[1]/100,r=e[2]/100*(1-t)+.5*t,n=0;return r>0&&r<.5?n=t/(2*r):r>=.5&&r<1&&(n=t/(2*(1-r))),[e[0],100*n,100*r]},i.hcg.hwb=function(e){let t=e[1]/100,r=t+e[2]/100*(1-t);return[e[0],(r-t)*100,(1-r)*100]},i.hwb.hcg=function(e){let t=e[1]/100,r=1-e[2]/100,n=r-t,a=0;return n<1&&(a=(r-n)/(1-n)),[e[0],100*n,100*a]},i.apple.rgb=function(e){return[e[0]/65535*255,e[1]/65535*255,e[2]/65535*255]},i.rgb.apple=function(e){return[e[0]/255*65535,e[1]/255*65535,e[2]/255*65535]},i.gray.rgb=function(e){return[e[0]/100*255,e[0]/100*255,e[0]/100*255]},i.gray.hsl=function(e){return[0,0,e[0]]},i.gray.hsv=i.gray.hsl,i.gray.hwb=function(e){return[0,100,e[0]]},i.gray.cmyk=function(e){return[0,0,0,e[0]]},i.gray.lab=function(e){return[e[0],0,0]},i.gray.hex=function(e){let t=255&Math.round(e[0]/100*255),r=((t<<16)+(t<<8)+t).toString(16).toUpperCase();return"000000".substring(r.length)+r},i.rgb.gray=function(e){return[(e[0]+e[1]+e[2])/3/255*100]}},51757:function(e,t,r){let n=r(49387),a=r(23203),i={};Object.keys(n).forEach(e=>{i[e]={},Object.defineProperty(i[e],"channels",{value:n[e].channels}),Object.defineProperty(i[e],"labels",{value:n[e].labels});let t=a(e);Object.keys(t).forEach(r=>{let n=t[r];i[e][r]=function(e){let t=function(...t){let r=t[0];if(null==r)return r;r.length>1&&(t=r);let n=e(t);if("object"==typeof n)for(let e=n.length,t=0;t<e;t++)n[t]=Math.round(n[t]);return n};return"conversion"in e&&(t.conversion=e.conversion),t}(n),i[e][r].raw=function(e){let t=function(...t){let r=t[0];return null==r?r:(r.length>1&&(t=r),e(t))};return"conversion"in e&&(t.conversion=e.conversion),t}(n)})}),e.exports=i},23203:function(e,t,r){let n=r(49387);e.exports=function(e){let t=function(e){let t=function(){let e={},t=Object.keys(n);for(let r=t.length,n=0;n<r;n++)e[t[n]]={distance:-1,parent:null};return e}(),r=[e];for(t[e].distance=0;r.length;){let e=r.pop(),a=Object.keys(n[e]);for(let n=a.length,i=0;i<n;i++){let n=a[i],o=t[n];-1===o.distance&&(o.distance=t[e].distance+1,o.parent=e,r.unshift(n))}}return t}(e),r={},a=Object.keys(t);for(let e=a.length,i=0;i<e;i++){let e=a[i];null!==t[e].parent&&(r[e]=function(e,t){let r=[t[e].parent,e],a=n[t[e].parent][e],i=t[e].parent;for(;t[i].parent;)r.unshift(t[i].parent),a=function(e,t){return function(r){return t(e(r))}}(n[t[i].parent][i],a),i=t[i].parent;return a.conversion=r,a}(e,t))}return r}},66119:function(e){"use strict";e.exports={aliceblue:[240,248,255],antiquewhite:[250,235,215],aqua:[0,255,255],aquamarine:[127,255,212],azure:[240,255,255],beige:[245,245,220],bisque:[255,228,196],black:[0,0,0],blanchedalmond:[255,235,205],blue:[0,0,255],blueviolet:[138,43,226],brown:[165,42,42],burlywood:[222,184,135],cadetblue:[95,158,160],chartreuse:[127,255,0],chocolate:[210,105,30],coral:[255,127,80],cornflowerblue:[100,149,237],cornsilk:[255,248,220],crimson:[220,20,60],cyan:[0,255,255],darkblue:[0,0,139],darkcyan:[0,139,139],darkgoldenrod:[184,134,11],darkgray:[169,169,169],darkgreen:[0,100,0],darkgrey:[169,169,169],darkkhaki:[189,183,107],darkmagenta:[139,0,139],darkolivegreen:[85,107,47],darkorange:[255,140,0],darkorchid:[153,50,204],darkred:[139,0,0],darksalmon:[233,150,122],darkseagreen:[143,188,143],darkslateblue:[72,61,139],darkslategray:[47,79,79],darkslategrey:[47,79,79],darkturquoise:[0,206,209],darkviolet:[148,0,211],deeppink:[255,20,147],deepskyblue:[0,191,255],dimgray:[105,105,105],dimgrey:[105,105,105],dodgerblue:[30,144,255],firebrick:[178,34,34],floralwhite:[255,250,240],forestgreen:[34,139,34],fuchsia:[255,0,255],gainsboro:[220,220,220],ghostwhite:[248,248,255],gold:[255,215,0],goldenrod:[218,165,32],gray:[128,128,128],green:[0,128,0],greenyellow:[173,255,47],grey:[128,128,128],honeydew:[240,255,240],hotpink:[255,105,180],indianred:[205,92,92],indigo:[75,0,130],ivory:[255,255,240],khaki:[240,230,140],lavender:[230,230,250],lavenderblush:[255,240,245],lawngreen:[124,252,0],lemonchiffon:[255,250,205],lightblue:[173,216,230],lightcoral:[240,128,128],lightcyan:[224,255,255],lightgoldenrodyellow:[250,250,210],lightgray:[211,211,211],lightgreen:[144,238,144],lightgrey:[211,211,211],lightpink:[255,182,193],lightsalmon:[255,160,122],lightseagreen:[32,178,170],lightskyblue:[135,206,250],lightslategray:[119,136,153],lightslategrey:[119,136,153],lightsteelblue:[176,196,222],lightyellow:[255,255,224],lime:[0,255,0],limegreen:[50,205,50],linen:[250,240,230],magenta:[255,0,255],maroon:[128,0,0],mediumaquamarine:[102,205,170],mediumblue:[0,0,205],mediumorchid:[186,85,211],mediumpurple:[147,112,219],mediumseagreen:[60,179,113],mediumslateblue:[123,104,238],mediumspringgreen:[0,250,154],mediumturquoise:[72,209,204],mediumvioletred:[199,21,133],midnightblue:[25,25,112],mintcream:[245,255,250],mistyrose:[255,228,225],moccasin:[255,228,181],navajowhite:[255,222,173],navy:[0,0,128],oldlace:[253,245,230],olive:[128,128,0],olivedrab:[107,142,35],orange:[255,165,0],orangered:[255,69,0],orchid:[218,112,214],palegoldenrod:[238,232,170],palegreen:[152,251,152],paleturquoise:[175,238,238],palevioletred:[219,112,147],papayawhip:[255,239,213],peachpuff:[255,218,185],peru:[205,133,63],pink:[255,192,203],plum:[221,160,221],powderblue:[176,224,230],purple:[128,0,128],rebeccapurple:[102,51,153],red:[255,0,0],rosybrown:[188,143,143],royalblue:[65,105,225],saddlebrown:[139,69,19],salmon:[250,128,114],sandybrown:[244,164,96],seagreen:[46,139,87],seashell:[255,245,238],sienna:[160,82,45],silver:[192,192,192],skyblue:[135,206,235],slateblue:[106,90,205],slategray:[112,128,144],slategrey:[112,128,144],snow:[255,250,250],springgreen:[0,255,127],steelblue:[70,130,180],tan:[210,180,140],teal:[0,128,128],thistle:[216,191,216],tomato:[255,99,71],turquoise:[64,224,208],violet:[238,130,238],wheat:[245,222,179],white:[255,255,255],whitesmoke:[245,245,245],yellow:[255,255,0],yellowgreen:[154,205,50]}},87866:function(e,t,r){"use strict";function n(e){var t=e.toString(16);return 1===t.length?"0"+t:t}function a(e){return"#"+e.map(n).join("")}function i(e,t,r){for(var n=0;n<r.length;n++)if(function(e,t,r){switch(r.length){case 3:if(255!==e[t+3]||e[t]===r[0]&&e[t+1]===r[1]&&e[t+2]===r[2])return!0;break;case 4:if(e[t+3]&&r[3]?e[t]===r[0]&&e[t+1]===r[1]&&e[t+2]===r[2]&&e[t+3]===r[3]:e[t+3]===r[3])return!0;break;case 5:if(function(e,t,r){var n=r[0],a=r[1],i=r[2],l=r[3],s=r[4],u=e[t+3],c=o(u,l,s);return l?!!(!u&&c||o(e[t],n,s)&&o(e[t+1],a,s)&&o(e[t+2],i,s)&&c):c}(e,t,r))return!0;break;default:return!1}}(e,t,r[n]))return!0;return!1}function o(e,t,r){return e>=t-r&&e<=t+r}function l(e,t,r){for(var n={},a=r.dominantDivider||24,o=r.ignoredColor,l=r.step,s=[0,0,0,0,0],u=0;u<t;u+=l){var c=e[u],h=e[u+1],d=e[u+2],g=e[u+3];if(!(o&&i(e,u,o))){var f=Math.round(c/a)+","+Math.round(h/a)+","+Math.round(d/a);n[f]?n[f]=[n[f][0]+c*g,n[f][1]+h*g,n[f][2]+d*g,n[f][3]+g,n[f][4]+1]:n[f]=[c*g,h*g,d*g,g,1],s[4]<n[f][4]&&(s=n[f])}}var b=s[0],m=s[1],p=s[2],v=s[3],y=s[4];return v?[Math.round(b/v),Math.round(m/v),Math.round(p/v),Math.round(v/y)]:r.defaultColor}function s(e,t,r){for(var n=0,a=0,o=0,l=0,s=0,u=r.ignoredColor,c=r.step,h=0;h<t;h+=c){var d=e[h+3],g=e[h]*d,f=e[h+1]*d,b=e[h+2]*d;!(u&&i(e,h,u))&&(n+=g,a+=f,o+=b,l+=d,s++)}return l?[Math.round(n/l),Math.round(a/l),Math.round(o/l),Math.round(l/s)]:r.defaultColor}function u(e,t,r){for(var n=0,a=0,o=0,l=0,s=0,u=r.ignoredColor,c=r.step,h=0;h<t;h+=c){var d=e[h],g=e[h+1],f=e[h+2],b=e[h+3];!(u&&i(e,h,u))&&(n+=d*d*b,a+=g*g*b,o+=f*f*b,l+=b,s++)}return l?[Math.round(Math.sqrt(n/l)),Math.round(Math.sqrt(a/l)),Math.round(Math.sqrt(o/l)),Math.round(l/s)]:r.defaultColor}function c(e){return h(e,"defaultColor",[0,0,0,0])}function h(e,t,r){return void 0===e[t]?r:e[t]}function d(e){return"undefined"!=typeof HTMLCanvasElement&&e instanceof HTMLCanvasElement?"canvas":f&&e instanceof OffscreenCanvas?"offscreencanvas":"undefined"!=typeof ImageBitmap&&e instanceof ImageBitmap?"imagebitmap":e.src}function g(e){return"undefined"!=typeof HTMLImageElement&&e instanceof HTMLImageElement}r.d(t,{Z:function(){return v}});var f="undefined"!=typeof OffscreenCanvas,b="undefined"==typeof window;function m(e){return Error("FastAverageColor: "+e)}function p(e,t){t||console.error(e)}var v=function(){function e(){this.canvas=null,this.ctx=null}return e.prototype.getColorAsync=function(e,t){if(!e)return Promise.reject(m("call .getColorAsync() without resource"));if("string"==typeof e){if("undefined"==typeof Image)return Promise.reject(m("resource as string is not supported in this environment"));var r=new Image;return r.crossOrigin=t&&t.crossOrigin||"",r.src=e,this.bindImageEvents(r,t)}if(g(e)&&!e.complete)return this.bindImageEvents(e,t);var n=this.getColor(e,t);return n.error?Promise.reject(n.error):Promise.resolve(n)},e.prototype.getColor=function(e,t){var r,n,a,i,o,l,s,u,v=c(t=t||{});if(!e){var y=m("call .getColor() without resource");return p(y,t.silent),this.prepareResult(v,y)}var M=(r=function(e){if(g(e)){var t=e.naturalWidth,r=e.naturalHeight;return e.naturalWidth||-1===e.src.search(/\.svg(\?|$)/i)||(t=r=100),{width:t,height:r}}return"undefined"!=typeof HTMLVideoElement&&e instanceof HTMLVideoElement?{width:e.videoWidth,height:e.videoHeight}:{width:e.width,height:e.height}}(e),a=h(n=t,"left",0),i=h(n,"top",0),o=h(n,"width",r.width),l=h(n,"height",r.height),s=o,u=l,"precision"===n.mode||(o>l?u=Math.round((s=100)/(o/l)):s=Math.round((u=100)/(l/o)),(s>o||u>l||s<10||u<10)&&(s=o,u=l)),{srcLeft:a,srcTop:i,srcWidth:o,srcHeight:l,destWidth:s,destHeight:u});if(!M.srcWidth||!M.srcHeight||!M.destWidth||!M.destHeight){var y=m('incorrect sizes for resource "'.concat(d(e),'"'));return p(y,t.silent),this.prepareResult(v,y)}if(!this.canvas&&(this.canvas=b?f?new OffscreenCanvas(1,1):null:document.createElement("canvas"),!this.canvas)){var y=m("OffscreenCanvas is not supported in this browser");return p(y,t.silent),this.prepareResult(v,y)}if(!this.ctx){if(this.ctx=this.canvas.getContext("2d",{willReadFrequently:!0}),!this.ctx){var y=m("Canvas Context 2D is not supported in this browser");return p(y,t.silent),this.prepareResult(v)}this.ctx.imageSmoothingEnabled=!1}this.canvas.width=M.destWidth,this.canvas.height=M.destHeight;try{this.ctx.clearRect(0,0,M.destWidth,M.destHeight),this.ctx.drawImage(e,M.srcLeft,M.srcTop,M.srcWidth,M.srcHeight,0,0,M.destWidth,M.destHeight);var k=this.ctx.getImageData(0,0,M.destWidth,M.destHeight).data;return this.prepareResult(this.getColorFromArray4(k,t))}catch(r){var y=m("security error (CORS) for resource ".concat(d(e),".\nDetails: https://developer.mozilla.org/en/docs/Web/HTML/CORS_enabled_image"));return p(y,t.silent),t.silent||console.error(r),this.prepareResult(v,y)}},e.prototype.getColorFromArray4=function(e,t){t=t||{};var r,n,a=e.length,i=c(t);if(a<4)return i;var o=4*(t.step||1);switch(t.algorithm||"sqrt"){case"simple":r=s;break;case"sqrt":r=u;break;case"dominant":r=l;break;default:throw m("".concat(t.algorithm," is unknown algorithm"))}return r(e,a-a%4,{defaultColor:i,ignoredColor:(n=t.ignoredColor)?Array.isArray(n[0])?n:[n]:[],step:o,dominantDivider:t.dominantDivider})},e.prototype.prepareResult=function(e,t){var r=e.slice(0,3),n=[e[0],e[1],e[2],e[3]/255],i=(299*e[0]+587*e[1]+114*e[2])/1e3<128;return{value:[e[0],e[1],e[2],e[3]],rgb:"rgb("+r.join(",")+")",rgba:"rgba("+n.join(",")+")",hex:a(r),hexa:a(e),isDark:i,isLight:!i,error:t}},e.prototype.destroy=function(){this.canvas&&(this.canvas.width=1,this.canvas.height=1,this.canvas=null),this.ctx=null},e.prototype.bindImageEvents=function(e,t){var r=this;return new Promise(function(n,a){var i=function(){s();var i=r.getColor(e,t);i.error?a(i.error):n(i)},o=function(){s(),a(m('Error loading image "'.concat(e.src,'"')))},l=function(){s(),a(m('Image "'.concat(e.src,'" loading aborted')))},s=function(){e.removeEventListener("load",i),e.removeEventListener("error",o),e.removeEventListener("abort",l)};e.addEventListener("load",i),e.addEventListener("error",o),e.addEventListener("abort",l)})},e}()}}]);