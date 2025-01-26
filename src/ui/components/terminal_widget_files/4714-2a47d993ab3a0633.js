"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[4714],{51230:function(a,e,r){r.d(e,{Nq:function(){return o},rg:function(){return l}});var t=r(7653);let n=(0,t.createContext)(null);function l({clientId:a,nonce:e,onScriptLoadSuccess:r,onScriptLoadError:l,children:o}){let i=function(a={}){let{nonce:e,onScriptLoadSuccess:r,onScriptLoadError:n}=a,[l,o]=(0,t.useState)(!1),i=(0,t.useRef)(r);i.current=r;let j=(0,t.useRef)(n);return j.current=n,(0,t.useEffect)(()=>{let a=document.createElement("script");return a.src="https://accounts.google.com/gsi/client",a.async=!0,a.defer=!0,a.nonce=e,a.onload=()=>{var a;o(!0),null===(a=i.current)||void 0===a||a.call(i)},a.onerror=()=>{var a;o(!1),null===(a=j.current)||void 0===a||a.call(j)},document.body.appendChild(a),()=>{document.body.removeChild(a)}},[e]),l}({nonce:e,onScriptLoadSuccess:r,onScriptLoadError:l}),j=(0,t.useMemo)(()=>({clientId:a,scriptLoadedSuccessfully:i}),[a,i]);return t.createElement(n.Provider,{value:j},o)}function o({flow:a="implicit",scope:e="",onSuccess:r,onError:l,onNonOAuthError:o,overrideScope:i,state:j,...c}){let{clientId:H,scriptLoadedSuccessfully:V}=function(){let a=(0,t.useContext)(n);if(!a)throw Error("Google OAuth components must be used within GoogleOAuthProvider");return a}(),h=(0,t.useRef)(),u=(0,t.useRef)(r);u.current=r;let s=(0,t.useRef)(l);s.current=l;let d=(0,t.useRef)(o);d.current=o,(0,t.useEffect)(()=>{var r;if(!V)return;let t="implicit"===a?"initTokenClient":"initCodeClient",n=null===(r=null==window?void 0:window.google)||void 0===r?void 0:r.accounts.oauth2[t]({client_id:H,scope:i?e:`openid profile email ${e}`,callback:a=>{var e,r;if(a.error)return null===(e=s.current)||void 0===e?void 0:e.call(s,a);null===(r=u.current)||void 0===r||r.call(u,a)},error_callback:a=>{var e;null===(e=d.current)||void 0===e||e.call(d,a)},state:j,...c});h.current=n},[H,V,a,e,j]);let p=(0,t.useCallback)(a=>{var e;return null===(e=h.current)||void 0===e?void 0:e.requestAccessToken(a)},[]),v=(0,t.useCallback)(()=>{var a;return null===(a=h.current)||void 0===a?void 0:a.requestCode()},[]);return"implicit"===a?p:v}},40152:function(a,e,r){r.d(e,{O:function(){return p}});var t=r(29758),n=r(7653),l=r(64864);let o=new Map([["bold",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M228,104a12,12,0,0,1-24,0V69l-59.51,59.51a12,12,0,0,1-17-17L187,52H152a12,12,0,0,1,0-24h64a12,12,0,0,1,12,12Zm-44,24a12,12,0,0,0-12,12v64H52V84h64a12,12,0,0,0,0-24H48A20,20,0,0,0,28,80V208a20,20,0,0,0,20,20H176a20,20,0,0,0,20-20V140A12,12,0,0,0,184,128Z"})})],["duotone",t.j.jsxs(t.j.Fragment,{children:[t.j.jsx("path",{d:"M184,80V208a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V80a8,8,0,0,1,8-8H176A8,8,0,0,1,184,80Z",opacity:"0.2"}),t.j.jsx("path",{d:"M224,104a8,8,0,0,1-16,0V59.32l-66.33,66.34a8,8,0,0,1-11.32-11.32L196.68,48H152a8,8,0,0,1,0-16h64a8,8,0,0,1,8,8Zm-40,24a8,8,0,0,0-8,8v72H48V80h72a8,8,0,0,0,0-16H48A16,16,0,0,0,32,80V208a16,16,0,0,0,16,16H176a16,16,0,0,0,16-16V136A8,8,0,0,0,184,128Z"})]})],["fill",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M192,136v72a16,16,0,0,1-16,16H48a16,16,0,0,1-16-16V80A16,16,0,0,1,48,64h72a8,8,0,0,1,0,16H48V208H176V136a8,8,0,0,1,16,0Zm32-96a8,8,0,0,0-8-8H152a8,8,0,0,0-5.66,13.66L172.69,72l-42.35,42.34a8,8,0,0,0,11.32,11.32L184,83.31l26.34,26.35A8,8,0,0,0,224,104Z"})})],["light",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M222,104a6,6,0,0,1-12,0V54.49l-69.75,69.75a6,6,0,0,1-8.48-8.48L201.51,46H152a6,6,0,0,1,0-12h64a6,6,0,0,1,6,6Zm-38,26a6,6,0,0,0-6,6v72a2,2,0,0,1-2,2H48a2,2,0,0,1-2-2V80a2,2,0,0,1,2-2h72a6,6,0,0,0,0-12H48A14,14,0,0,0,34,80V208a14,14,0,0,0,14,14H176a14,14,0,0,0,14-14V136A6,6,0,0,0,184,130Z"})})],["regular",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M224,104a8,8,0,0,1-16,0V59.32l-66.33,66.34a8,8,0,0,1-11.32-11.32L196.68,48H152a8,8,0,0,1,0-16h64a8,8,0,0,1,8,8Zm-40,24a8,8,0,0,0-8,8v72H48V80h72a8,8,0,0,0,0-16H48A16,16,0,0,0,32,80V208a16,16,0,0,0,16,16H176a16,16,0,0,0,16-16V136A8,8,0,0,0,184,128Z"})})],["thin",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M220,104a4,4,0,0,1-8,0V49.66l-73.16,73.17a4,4,0,0,1-5.66-5.66L206.34,44H152a4,4,0,0,1,0-8h64a4,4,0,0,1,4,4Zm-36,28a4,4,0,0,0-4,4v72a4,4,0,0,1-4,4H48a4,4,0,0,1-4-4V80a4,4,0,0,1,4-4h72a4,4,0,0,0,0-8H48A12,12,0,0,0,36,80V208a12,12,0,0,0,12,12H176a12,12,0,0,0,12-12V136A4,4,0,0,0,184,132Z"})})]]);var i=Object.defineProperty,j=Object.defineProperties,c=Object.getOwnPropertyDescriptors,H=Object.getOwnPropertySymbols,V=Object.prototype.hasOwnProperty,h=Object.prototype.propertyIsEnumerable,u=(a,e,r)=>e in a?i(a,e,{enumerable:!0,configurable:!0,writable:!0,value:r}):a[e]=r,s=(a,e)=>{for(var r in e||(e={}))V.call(e,r)&&u(a,r,e[r]);if(H)for(var r of H(e))h.call(e,r)&&u(a,r,e[r]);return a},d=(a,e)=>j(a,c(e));let p=(0,n.forwardRef)((a,e)=>t.j.jsx(l.Z,d(s({ref:e},a),{weights:o})));p.displayName="ArrowSquareOut"},45785:function(a,e,r){r.d(e,{C:function(){return p}});var t=r(29758),n=r(7653),l=r(64864);let o=new Map([["bold",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M216,28H88A12,12,0,0,0,76,40V76H40A12,12,0,0,0,28,88V216a12,12,0,0,0,12,12H168a12,12,0,0,0,12-12V180h36a12,12,0,0,0,12-12V40A12,12,0,0,0,216,28ZM156,204H52V100H156Zm48-48H180V88a12,12,0,0,0-12-12H100V52H204Z"})})],["duotone",t.j.jsxs(t.j.Fragment,{children:[t.j.jsx("path",{d:"M216,40V168H168V88H88V40Z",opacity:"0.2"}),t.j.jsx("path",{d:"M216,32H88a8,8,0,0,0-8,8V80H40a8,8,0,0,0-8,8V216a8,8,0,0,0,8,8H168a8,8,0,0,0,8-8V176h40a8,8,0,0,0,8-8V40A8,8,0,0,0,216,32ZM160,208H48V96H160Zm48-48H176V88a8,8,0,0,0-8-8H96V48H208Z"})]})],["fill",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M216,32H88a8,8,0,0,0-8,8V80H40a8,8,0,0,0-8,8V216a8,8,0,0,0,8,8H168a8,8,0,0,0,8-8V176h40a8,8,0,0,0,8-8V40A8,8,0,0,0,216,32Zm-8,128H176V88a8,8,0,0,0-8-8H96V48H208Z"})})],["light",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M216,34H88a6,6,0,0,0-6,6V82H40a6,6,0,0,0-6,6V216a6,6,0,0,0,6,6H168a6,6,0,0,0,6-6V174h42a6,6,0,0,0,6-6V40A6,6,0,0,0,216,34ZM162,210H46V94H162Zm48-48H174V88a6,6,0,0,0-6-6H94V46H210Z"})})],["regular",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M216,32H88a8,8,0,0,0-8,8V80H40a8,8,0,0,0-8,8V216a8,8,0,0,0,8,8H168a8,8,0,0,0,8-8V176h40a8,8,0,0,0,8-8V40A8,8,0,0,0,216,32ZM160,208H48V96H160Zm48-48H176V88a8,8,0,0,0-8-8H96V48H208Z"})})],["thin",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M216,36H88a4,4,0,0,0-4,4V84H40a4,4,0,0,0-4,4V216a4,4,0,0,0,4,4H168a4,4,0,0,0,4-4V172h44a4,4,0,0,0,4-4V40A4,4,0,0,0,216,36ZM164,212H44V92H164Zm48-48H172V88a4,4,0,0,0-4-4H92V44H212Z"})})]]);var i=Object.defineProperty,j=Object.defineProperties,c=Object.getOwnPropertyDescriptors,H=Object.getOwnPropertySymbols,V=Object.prototype.hasOwnProperty,h=Object.prototype.propertyIsEnumerable,u=(a,e,r)=>e in a?i(a,e,{enumerable:!0,configurable:!0,writable:!0,value:r}):a[e]=r,s=(a,e)=>{for(var r in e||(e={}))V.call(e,r)&&u(a,r,e[r]);if(H)for(var r of H(e))h.call(e,r)&&u(a,r,e[r]);return a},d=(a,e)=>j(a,c(e));let p=(0,n.forwardRef)((a,e)=>t.j.jsx(l.Z,d(s({ref:e},a),{weights:o})));p.displayName="Copy"},20387:function(a,e,r){r.d(e,{K:function(){return p}});var t=r(29758),n=r(7653),l=r(64864);let o=new Map([["bold",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M100,148a12,12,0,0,1-12,12H64a12,12,0,0,1,0-24H88A12,12,0,0,1,100,148Zm144-32v60a20,20,0,0,1-20,20H140v28a12,12,0,0,1-24,0V196H32a20,20,0,0,1-20-20V116A64.07,64.07,0,0,1,76,52h80V24a12,12,0,0,1,12-12h32a12,12,0,0,1,0,24H180V52A64.07,64.07,0,0,1,244,116ZM116,172V116a40,40,0,0,0-80,0v56Zm104-56a40,40,0,0,0-40-40v68a12,12,0,0,1-24,0V76H125.93A63.7,63.7,0,0,1,140,116v56h80Z"})})],["duotone",t.j.jsxs(t.j.Fragment,{children:[t.j.jsx("path",{d:"M232,116v60a8,8,0,0,1-8,8H128V116A52,52,0,0,0,76,64H180A52,52,0,0,1,232,116Z",opacity:"0.2"}),t.j.jsx("path",{d:"M104,152a8,8,0,0,1-8,8H56a8,8,0,0,1,0-16H96A8,8,0,0,1,104,152Zm136-36v60a16,16,0,0,1-16,16H136v32a8,8,0,0,1-16,0V192H32a16,16,0,0,1-16-16V116A60.07,60.07,0,0,1,76,56h76V24a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H168V56h12A60.07,60.07,0,0,1,240,116ZM120,176V116a44,44,0,0,0-88,0v60Zm104-60a44.05,44.05,0,0,0-44-44H168v72a8,8,0,0,1-16,0V72H116.75A59.86,59.86,0,0,1,136,116v60h88Z"})]})],["fill",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M104,152a8,8,0,0,1-8,8H56a8,8,0,0,1,0-16H96A8,8,0,0,1,104,152ZM168,32h24a8,8,0,0,0,0-16H160a8,8,0,0,0-8,8V56h16Zm72,84v60a16,16,0,0,1-16,16H136v32a8,8,0,0,1-16,0V192H32a16,16,0,0,1-16-16V116A60.07,60.07,0,0,1,76,56h76v88a8,8,0,0,0,16,0V56h12A60.07,60.07,0,0,1,240,116Zm-120,0a44,44,0,0,0-88,0v60h88Z"})})],["light",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M102,152a6,6,0,0,1-6,6H56a6,6,0,0,1,0-12H96A6,6,0,0,1,102,152Zm136-36v60a14,14,0,0,1-14,14H134v34a6,6,0,0,1-12,0V190H32a14,14,0,0,1-14-14V116A58.07,58.07,0,0,1,76,58h78V24a6,6,0,0,1,6-6h32a6,6,0,0,1,0,12H166V58h14A58.07,58.07,0,0,1,238,116ZM122,178V116a46,46,0,0,0-92,0v60a2,2,0,0,0,2,2Zm104-62a46.06,46.06,0,0,0-46-46H166v74a6,6,0,0,1-12,0V70H111.29A57.93,57.93,0,0,1,134,116v62h90a2,2,0,0,0,2-2Z"})})],["regular",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M104,152a8,8,0,0,1-8,8H56a8,8,0,0,1,0-16H96A8,8,0,0,1,104,152Zm136-36v60a16,16,0,0,1-16,16H136v32a8,8,0,0,1-16,0V192H32a16,16,0,0,1-16-16V116A60.07,60.07,0,0,1,76,56h76V24a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H168V56h12A60.07,60.07,0,0,1,240,116ZM120,176V116a44,44,0,0,0-88,0v60Zm104-60a44.05,44.05,0,0,0-44-44H168v72a8,8,0,0,1-16,0V72H116.75A59.86,59.86,0,0,1,136,116v60h88Z"})})],["thin",t.j.jsx(t.j.Fragment,{children:t.j.jsx("path",{d:"M100,152a4,4,0,0,1-4,4H56a4,4,0,0,1,0-8H96A4,4,0,0,1,100,152Zm136-36v60a12,12,0,0,1-12,12H132v36a4,4,0,0,1-8,0V188H32a12,12,0,0,1-12-12V116A56.06,56.06,0,0,1,76,60h80V24a4,4,0,0,1,4-4h32a4,4,0,0,1,0,8H164V60h16A56.06,56.06,0,0,1,236,116ZM124,180V116a48,48,0,0,0-96,0v60a4,4,0,0,0,4,4Zm104-64a48.05,48.05,0,0,0-48-48H164v76a4,4,0,0,1-8,0V68H104.82A56,56,0,0,1,132,116v64h92a4,4,0,0,0,4-4Z"})})]]);var i=Object.defineProperty,j=Object.defineProperties,c=Object.getOwnPropertyDescriptors,H=Object.getOwnPropertySymbols,V=Object.prototype.hasOwnProperty,h=Object.prototype.propertyIsEnumerable,u=(a,e,r)=>e in a?i(a,e,{enumerable:!0,configurable:!0,writable:!0,value:r}):a[e]=r,s=(a,e)=>{for(var r in e||(e={}))V.call(e,r)&&u(a,r,e[r]);if(H)for(var r of H(e))h.call(e,r)&&u(a,r,e[r]);return a},d=(a,e)=>j(a,c(e));let p=(0,n.forwardRef)((a,e)=>t.j.jsx(l.Z,d(s({ref:e},a),{weights:o})));p.displayName="Mailbox"}}]);