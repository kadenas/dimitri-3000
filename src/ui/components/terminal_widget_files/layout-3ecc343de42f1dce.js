(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[283],{47801:function(e,t,n){Promise.resolve().then(n.bind(n,72606))},72606:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return o}});var r=n(27573),u=n(27920),a=n(78013);function o(e){let{children:t}=e;return(0,r.jsx)(u.hH,{children:(0,r.jsx)(a.LayoutWithSidebar,{children:t})})}},11907:function(e,t,n){"use strict";n.d(t,{K5:function(){return p},Ql:function(){return E},Z1:function(){return y},_A:function(){return C},nJ:function(){return _},rN:function(){return w},wy:function(){return S},z6:function(){return g}});var r=n(51571),u=n(10398),a=n(88075),o=n(24658),c=n(19486),i=n(62627),s=n(71854),l=n(44846);n(73571);var f=n(67754),d=n(7653),h=n(73567),m=n(37727);let g=()=>{let e=(0,f.useRouter)(),t=(0,u.f)();return{refresh:()=>{e.refresh()},switchAndRefresh:(e,n)=>{t.set(s.cn.LAST_ACTIVE_ORG,e),n?location.pathname=n:location.reload()}}},v=e=>{let{account:t}=(0,a.t)();return t&&((0,i.wJ)({account:t,isClaudeDot:e})||(0,i.c6)(t,e))?"/onboarding":t&&(0,i.kK)(t,e)?"/invites":t&&(0,i.D_)(t,e)?"/create":e?"/new":"/dashboard"};function p(e){let{value:t}=(0,l.F)("show_affirmative_consent"),{value:n}=(0,l.F)("show_affirmative_consent_for_privacy_policy");return(0,d.useMemo)(()=>[...t===e?["aup","consumer-terms"]:[],...n===e?["privacy"]:[]],[n,t,e])}let w=(e,t,n)=>{let r=(0,c.q)(),{mutateAsync:u}=(0,h.k7)();return(0,d.useCallback)(async()=>{if(!e||!r||0===t.length)return;let a=t.map(e=>({document_id:"v3:".concat(e,":").concat(r[e]),accepted_via_checkbox:n}));await u({acceptances:a})},[e,r,t,u,n])},C=(e,t)=>{let{account:n,refetch:r,setActiveOrganizationUUID:u}=(0,a.t)(),[c,i]=(0,d.useState)(!1),[s,l]=(0,d.useState)(!1),f=_(),{addSuccess:m}=(0,o.e)(),{data:g}=(0,h.gq)(e);return(0,d.useEffect)(()=>{n&&c&&s&&(t?t(f):f())},[s,f,c,n,t]),(0,d.useCallback)(async()=>{i(!0),await r(),(null==g?void 0:g.organization_uuid)&&(u(g.organization_uuid),m("Successfully joined ".concat(g.organization_name))),l(!0)},[g,m,r,u])},_=function(){let e=arguments.length>0&&void 0!==arguments[0]&&arguments[0],t=(0,f.useSearchParams)().get("returnTo"),n=S(e);return(0,d.useCallback)(()=>{n(t)},[n,t])},S=function(){let e=arguments.length>0&&void 0!==arguments[0]&&arguments[0],{account:t}=(0,a.t)(),[n,u]=(0,d.useState)(!1),o=(0,f.useRouter)(),[c,i]=(0,d.useState)(null),s=(0,f.usePathname)(),l=(0,f.useSearchParams)(),h=(0,r.Z)(),g=v(h);return(0,d.useEffect)(()=>{(n||e)&&!t&&o.push((0,m.C2)(s,l.toString()))},[t,o,n,e,s,l]),(0,d.useEffect)(()=>{if(n&&t){let e=(0,m.eX)(t,c,g,h);o.push(e)}},[t,o,n,c,g,h]),(0,d.useCallback)(e=>{e&&i(e),u(!0)},[])};function y(){let[e,t]=(0,d.useState)(!1);return{getRecaptchaToken:(0,d.useCallback)(async(e,n)=>(t(!0),new Promise((r,u)=>{if("undefined"==typeof grecaptcha)return t(!1),u(Error("Recaptcha failed to load"));grecaptcha.enterprise.ready(()=>{grecaptcha.enterprise.execute(e,{action:n}).then(e=>{r(e),t(!1)},e=>{t(!1),u(e)})})})),[]),isLoading:e}}function E(e){let[t,n]=(0,d.useState)(!1);(0,d.useEffect)(()=>{if(!t){let t=setInterval(()=>{window.grecaptcha&&(n(!0),e())},10);return()=>clearInterval(t)}},[t,n,e])}},37727:function(e,t,n){"use strict";n.d(t,{$6:function(){return c},C2:function(){return a},G9:function(){return o},eX:function(){return u},kY:function(){return i}});var r=n(62627);let u=(e,t,n,u)=>{if(!t||!t.startsWith("/"))return n;if((0,r.cG)(e,u)){let e=new URLSearchParams({returnTo:t});return"".concat(n,"?").concat(e.toString())}return o(t)},a=function(e,t){let n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"/login",r=arguments.length>3&&void 0!==arguments[3]?arguments[3]:{},u="".concat(e,"?").concat(t),a=new URLSearchParams(r);return a.append("returnTo",u),"".concat(n,"?").concat(a.toString())};function o(e){let t=new URL(e,"http://example.com");return t.pathname+t.search}function c(e){return e.reduce((e,t)=>{let n=localStorage.getItem(t);return null!==n&&e.push([t,n]),e},[])}function i(e){e.forEach(e=>{let[t,n]=e;localStorage.setItem(t,n)})}},15437:function(e,t,n){"use strict";n.d(t,{C:function(){return m},ConsentProvider:function(){return h}});var r=n(27573),u=n(79791),a=n(33293),o=n(30298),c=n(71854),i=n(90345),s=n.n(i),l=n(7653),f=n(69850);let d=(0,l.createContext)({showConsentBanner:!1,openConsentBanner:s(),preferences:f.iw,savePreferences:s()}),h=e=>{let{children:t,requiresExplicitConsent:n}=e,[i,s,h]=(0,u.D)(c.cn.CONSENT_PREFERENCES,n?f.iw:f.DF),[m,g]=(0,l.useState)(n&&!h),v=(0,l.useCallback)(e=>{s(e),(0,a.HF)(e),g(!1),o.u.updateCategories(e)},[s,g]);return(0,r.jsx)(d.Provider,{value:{showConsentBanner:m,openConsentBanner:()=>g(!0),preferences:i,savePreferences:v},children:t})};function m(){return(0,l.useContext)(d)}},79791:function(e,t,n){"use strict";n.d(t,{D:function(){return o}});var r=n(13623),u=n(7653),a=n(10398);function o(e,t){let n=(0,a.f)(),[o,c]=(0,u.useState)(()=>!!n.get(e)),[i,s]=(0,u.useState)(()=>{try{let r=n.get(e);return r?JSON.parse(r):t}catch(n){return(0,r.Tb)(n,{extra:{message:"Malformed JSON cookie",cookieKey:e}}),t}});return[i,(0,u.useCallback)(t=>{n.set(e,JSON.stringify(t)),s(t),c(!0)},[n,e]),o]}},33293:function(e,t,n){"use strict";n.d(t,{HF:function(){return a},bq:function(){return u}});var r=n(13623);let u=function(e){for(var t=arguments.length,n=Array(t>1?t-1:0),u=1;u<t;u++)n[u-1]=arguments[u];try{"function"==typeof window.gtag&&gtag(e,...n)}catch(e){(0,r.Tb)(e)}},a=e=>{u("consent","update",o(e))},o=e=>({ad_personalization:e.marketing?"granted":"denied",ad_user_data:e.marketing?"granted":"denied",ad_storage:e.marketing?"granted":"denied",analytics_storage:e.analytics?"granted":"denied",functionality_storage:"granted",personalization_storage:"granted",security_storage:"granted"})},19486:function(e,t,n){"use strict";n.d(t,{LegalDocsProvider:function(){return o},q:function(){return c}});var r=n(27573),u=n(7653);let a=(0,u.createContext)(void 0),o=e=>{let{value:t,children:n}=e;return(0,r.jsx)(a.Provider,{value:t,children:n})};function c(){return(0,u.useContext)(a)}},99663:function(e,t,n){"use strict";n.d(t,{V:function(){return u}});var r=n(27573);function u(e){let{size:t=16}=e;return(0,r.jsx)("svg",{width:t,height:t,viewBox:"0 0 28 28",fill:"currentColor",xmlns:"http://www.w3.org/2000/svg",children:(0,r.jsx)("path",{d:"M20 4h-4.3l7.7 19.5h4.2L20 4ZM7.6 4 0 23.5h4.3L6 19.4h8l1.6 4h4.3L12.1 4H7.7Zm-.4 11.8 2.6-6.9 2.7 6.9H7.3Z"})})}},42152:function(e,t,n){"use strict";n.d(t,{f:function(){return c},m:function(){return i}});var r=n(27573),u=n(71233),a=n(21484),o=n(7653);function c(e){let{didCopy:t,...n}=e;return t?(0,r.jsx)(u.f,{...n}):(0,r.jsx)(a.T,{...n})}function i(e){let[t,n]=(0,o.useState)(!1);return{didCopy:t,copyToClipboard:(0,o.useCallback)(t=>{let r="string"==typeof t?t:e;navigator.clipboard.writeText(r.trim()).then(()=>{n(!0),setTimeout(()=>n(!1),2e3)}).catch(e=>console.log("Something went wrong",e))},[e])}}},79843:function(e,t,n){"use strict";n.d(t,{ThemeProvider:function(){return l},F:function(){return g}});var r=n(27573),u=n(10398),a=n(20504),o=n(71854),c=n(7653);let i="(prefers-color-scheme: dark)",s=(0,c.createContext)(void 0);function l(e){let{initialTheme:t,children:n}=e,[o,l]=(0,c.useState)(t),h=(0,u.f)(),[m,g]=(0,a.R)("userThemeMode","auto");(0,c.useEffect)(()=>f(o),[o]),(0,c.useEffect)(()=>d(m,h),[h,m]);let v=(0,c.useCallback)(()=>d(m,h),[h,m]);return(0,c.useEffect)(()=>{if("auto"!==m)return;let e=window.matchMedia(i);return e.addEventListener("change",v),()=>e.removeEventListener("change",v)},[m,v]),(0,r.jsx)(s.Provider,{value:{theme:o,mode:m,setMode:g,setTheme:l},children:n})}let f=e=>{"undefined"!=typeof document&&(document.documentElement.dataset.theme=e,h())},d=(e,t)=>{if("undefined"==typeof document)return;let n=m(e);t.set(o.cn.COLOR_MODE,n),document.documentElement.dataset.mode=n,h()},h=()=>{let[e,t,n]=getComputedStyle(document.documentElement).getPropertyValue("--bg-200").split(" "),r="hsl(".concat(e,",").concat(t,",").concat(n,")"),u=document.querySelector('meta[name="theme-color"]');u||((u=document.createElement("meta")).setAttribute("name","theme-color"),document.head.appendChild(u)),u.setAttribute("content",r)},m=e=>{var t;return"auto"!==e?e:(null===(t=window)||void 0===t?void 0:t.matchMedia(i).matches)?"dark":"light"},g=()=>{let e=(0,c.useContext)(s);if(void 0===e)throw Error("useTheme must be used within a ThemeProvider");return e}}},function(e){e.O(0,[4507,2044,9906,7611,5469,395,6659,4164,3124,3982,4128,9095,1359,8566,9261,6572,6088,2898,622,56,2177,6192,7712,2237,126,6398,9194,2862,6291,7991,2679,2545,4501,8039,1014,5667,9136,4293,2274,5765,6010,7718,8013,1293,1362,693,1744],function(){return e(e.s=47801)}),_N_E=e.O()}]);