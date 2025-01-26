"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[4293],{64655:function(e,t,n){n.d(t,{HN:function(){return u},SE:function(){return s},Tx:function(){return l}});var r=n(89992),i=n(88075),a=n(49793),o=n(26821),c=n(27957);let u=(e,t)=>{let{account:n,activeOrganization:u}=(0,i.t)(),s=t===(null==n?void 0:n.uuid),l=null==u?void 0:u.uuid,d=(0,o.useQueryClient)(),f=(0,c.Gm)();return(0,r.uC)(()=>"/api/organizations/".concat(l,"/projects/").concat(e,"/accounts/").concat(t),"PUT",{onSuccess:()=>{d.invalidateQueries({queryKey:[a.l3,{projectUuid:e}]}),s&&(f(e),d.invalidateQueries({queryKey:[a.VH,{orgUUID:l}]}),d.invalidateQueries({queryKey:[a.tv,{orgUUID:l}]}))}})},s=function(e){let t=!(arguments.length>1)||void 0===arguments[1]||arguments[1],{activeOrganization:n}=(0,i.t)(),o=null==n?void 0:n.uuid;return(0,r.WE)("/api/organizations/".concat(o,"/projects/").concat(e,"/accounts"),{queryKey:[a.l3,{projectUuid:e}],enabled:!!(t&&n&&e),staleTime:0})},l=e=>{let{activeOrganization:t}=(0,i.t)(),n=null==t?void 0:t.uuid,c=(0,o.useQueryClient)();return(0,r.uC)(t=>"/api/organizations/".concat(n,"/projects/").concat(e,"/accounts/").concat(t.accountUuid),"PUT",{onSuccess:()=>{c.invalidateQueries({queryKey:[a.l3,{projectUuid:e}]})},transformVariables:e=>({role:e.role})})}},48970:function(e,t,n){n.d(t,{ER:function(){return f},Kf:function(){return s},Zy:function(){return y},h4:function(){return p},i9:function(){return u},op:function(){return h},pK:function(){return m},tR:function(){return l},u3:function(){return d}});var r=n(89992),i=n(88075),a=n(65490),o=n(49793),c=n(26821);let u="[ANT ONLY] synced_resources.txt";function s(e){let{activeOrganization:t}=(0,i.t)(),n=null==t?void 0:t.uuid,{data:a,...c}=(0,r.WE)("/api/organizations/".concat(n,"/projects/").concat(e,"/docs"),{queryKey:[o.zy,{orgUuid:n,projectUuid:e}],enabled:!!t&&!!e});return{data:null==a?void 0:a.filter(e=>{let{file_name:t,content:n}=e;return t.length>0&&n.length>0}).filter(e=>{let{file_name:t}=e;return t!==u}),unfilteredData:a,...c}}let l=e=>{let{projectUuid:t,docUuid:n}=e,{activeOrganization:c}=(0,i.t)(),u=null==c?void 0:c.uuid;return(0,r.WE)("/api/organizations/".concat(u,"/projects/").concat(t,"/docs/").concat(n),{queryKey:[o.tt,{orgUuid:u,projectUuid:t,docUuid:n}],enabled:!!c,staleTime:0,meta:{noToast:e=>e instanceof a.Hx&&404===e.statusCode}})};function d(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},{activeOrganization:n}=(0,i.t)(),a=null==n?void 0:n.uuid,u=(0,c.useQueryClient)();return(0,r.uC)(()=>"/api/organizations/".concat(a,"/projects/").concat(e,"/docs"),"POST",{enabled:!!e,onSuccess:function(){for(var n,r=arguments.length,i=Array(r),c=0;c<r;c++)i[c]=arguments[c];u.invalidateQueries({queryKey:[o.zy,{orgUuid:a,projectUuid:e}]}),u.invalidateQueries({queryKey:[o.n$,{orgUuid:a}]}),u.invalidateQueries({queryKey:[o.VH,{orgUUID:a}]}),null===(n=t.onSuccess)||void 0===n||n.call(t,...i)},onError:function(){for(var e,n=arguments.length,r=Array(n),i=0;i<n;i++)r[i]=arguments[i];null===(e=t.onError)||void 0===e||e.call(t,...r)}})}function f(e){let{activeOrganization:t}=(0,i.t)(),n=null==t?void 0:t.uuid,a=(0,c.useQueryClient)();return(0,r.Ne)(t=>"/api/organizations/".concat(n,"/projects/").concat(e,"/docs/").concat(t.docUuid),"DELETE",(e,t)=>t?t.filter(t=>t.uuid!==e.docUuid):t,{queryKey:[o.zy,{orgUuid:n,projectUuid:e}],enabled:!!e,onSuccess:(t,r)=>{a.invalidateQueries({queryKey:[o.tt,{orgUuid:n,projectUuid:e,docUuid:r.docUuid}]}),a.invalidateQueries({queryKey:[o.zy,{orgUuid:n,projectUuid:e}]}),a.invalidateQueries({queryKey:[o.n$,{orgUuid:n}]}),a.invalidateQueries({queryKey:[o.VH,{orgUUID:n}]})}})}let h=e=>{let{activeOrganization:t}=(0,i.t)(),n=null==t?void 0:t.uuid,a=(0,c.useQueryClient)();return(0,r.Ne)(()=>"/api/organizations/".concat(n,"/projects/").concat(e,"/docs/delete_many"),"POST",(e,t)=>t?t.filter(t=>!e.doc_uuids.includes(t.uuid)):t,{queryKey:[o.zy,{orgUuid:n,projectUuid:e}],enabled:!!e,onSuccess:(t,r)=>{for(let t of r.doc_uuids)a.invalidateQueries({queryKey:[o.tt,{orgUuid:n,projectUuid:e,docUuid:t}]});a.invalidateQueries({queryKey:[o.zy,{orgUuid:n,projectUuid:e}]}),a.invalidateQueries({queryKey:[o.n$,{orgUuid:n}]}),a.invalidateQueries({queryKey:[o.VH,{orgUUID:n}]})}})};function y(e){let{activeOrganization:t}=(0,i.t)(),n=null==t?void 0:t.uuid,a=(0,c.useQueryClient)();return(0,r.Ne)(t=>"/api/organizations/".concat(n,"/projects/").concat(e,"/docs/").concat(t.docUuid),"PUT",(e,t)=>t?t.map(t=>t.uuid===e.docUuid?{...t,...e}:t):t,{queryKey:[o.zy,{orgUuid:n,projectUuid:e}],enabled:!!e,onSuccess:(t,r)=>{a.invalidateQueries({queryKey:[o.tt,{orgUuid:n,projectUuid:e,docUuid:r.docUuid}]}),a.invalidateQueries({queryKey:[o.zy,{orgUuid:n,projectUuid:e}]}),a.invalidateQueries({queryKey:[o.n$,{orgUuid:n}]}),a.invalidateQueries({queryKey:[o.VH,{orgUUID:n}]})}})}function p(e){let{activeOrganization:t}=(0,i.t)(),n=null==t?void 0:t.uuid,a=(0,c.useQueryClient)();return(0,r.Ne)(()=>"/api/organizations/".concat(n,"/projects/").concat(e,"/files/delete_many"),"POST",(e,t)=>t?t.filter(t=>!e.file_uuids.includes(t.file_uuid)):t,{queryKey:[o.jb,{orgUuid:n,projectUuid:e}],enabled:!!e,onSuccess:()=>{a.invalidateQueries({queryKey:[o.jb,{orgUuid:n,projectUuid:e}]}),a.invalidateQueries({queryKey:[o.n$,{orgUuid:n}]}),a.invalidateQueries({queryKey:[o.VH,{orgUUID:n}]})}})}function m(e){let{activeOrganization:t}=(0,i.t)(),n=null==t?void 0:t.uuid;return(0,r.WE)("/api/organizations/".concat(n,"/projects/").concat(e,"/files"),{queryKey:[o.jb,{orgUuid:n,projectUuid:e}],enabled:!!t&&!!e})}},93456:function(e,t,n){n.d(t,{M:function(){return h},Y:function(){return y}});var r=n(27573),i=n(20504),a=n(90345),o=n.n(a),c=n(67754),u=n(7653);function s(e,t){switch(t.type){case"DRAW_SVG":return{...e,selectedItem:{type:"svg",data:t.svg}};case"CLOSE_CHAT_SIDEBAR":return{...e,isChatSidebarOpen:!1};case"OPEN_CHAT_SIDEBAR":return{...e,isChatSidebarOpen:!0};case"SELECT_ATTACHMENT":return{...e,selectedItem:{type:"attachment",attachment:t.attachment}};case"SELECT_ARTIFACT":return{...e,selectedItem:{type:"artifact",id:t.id,versionUUID:t.versionUUID}};case"SELECT_DOC":return{...e,selectedItem:{type:"doc",id:t.id}};case"SELECT_SYNCED_DIRECTORY":return{...e,selectedItem:{type:"syncedDirectory",id:t.id}};case"CLEAR_SELECTED":return{...e,selectedItem:null,activeMessageUUID:void 0};case"SET_ACTIVE_MESSAGE_UUID":return{...e,activeMessageUUID:t.uuid};case"UPDATE_ARTIFACTS":return{...e,artifacts:t.artifacts};case"UPDATE_ATTACHMENTS":return{...e,attachments:t.attachments};case"UPDATE_FILES":return{...e,files:t.files};case"UPDATE_SYNC_SOURCES":return{...e,syncSources:t.syncSources};case"UPDATE_DOC_UPDATES":return{...e,docUpdates:t.updates};case"UPDATE_FILE_EDITS":return{...e,fileEdits:t.edits};default:return e}}let l={selectedItem:null,artifacts:{},attachments:[],files:[],syncSources:[],docUpdates:[],fileEdits:new Map,isChatSidebarOpen:!1,activeMessageUUID:void 0,conversationUUID:void 0},d={chatResourceState:l,dispatchChatResource:o()},f=(0,u.createContext)(d);function h(e){let{children:t,conversationUUID:n}=e,a=function(e){let t=!!(0,c.useSearchParams)().get("controls")&&!(window.matchMedia&&window.matchMedia("(max-width: 767px)").matches),[n]=(0,i.R)("".concat(e,":chatControlsSidebarIsOpen"),t);return n}(n),[o,d]=(0,u.useReducer)(s,{...l,isChatSidebarOpen:a,conversationUUID:n});return(0,r.jsx)(f.Provider,{value:{chatResourceState:o,dispatchChatResource:d},children:t})}function y(){return(0,u.useContext)(f)}},74293:function(e,t,n){n.d(t,{r:function(){return v},s:function(){return w}});var r=n(27573),i=n(21468),a=n(32751),o=n(1984),c=n(37772),u=n.n(c),s=n(90345),l=n.n(s),d=n(7653),f=n(93456),h=n(51087);let y=(0,d.createContext)(null),p={getInstance:()=>void 0,setBaseContent:l(),flagForDeletion:l(),getCurrentContent:()=>void 0,hasUnsavedChanges:()=>!1,registerEditor:l(),unregisterEditor:l(),setMergeState:()=>l(),subscribeToMergeStateChanges:()=>l(),acceptAllChanges:l(),rejectAllChanges:l(),deactivateChangesMode:l(),activeEditors:[],changesMode:!1},m=(e,t)=>{var n,r;let i=null===(r=(0,o.Sk)(e.state))||void 0===r?void 0:null===(n=r.chunks)||void 0===n?void 0:n[0];return!!i&&("accept"===t?o.bN:o.A)(e,i.fromB)};function v(e){let{children:t}=e,{track:n}=(0,i.z$)(),{openedFiles:o}=(0,h.b)(),{dispatchChatResource:c}=(0,f.Y)(),s=(0,d.useRef)(new Map),l=(0,d.useRef)(new Set),p=(0,d.useCallback)((e,t)=>{s.current.set(e,{view:t})},[]),v=(0,d.useCallback)(e=>{s.current.delete(e)},[]),w=(0,d.useCallback)((e,t)=>{let n=s.current.get(e);if(!n){a.v("Attempted to update unknown editor: ".concat(e));return}s.current.set(e,{...n,...t})},[]),g=(0,d.useCallback)((e,t)=>w(e,{baseContent:t}),[w]),E=(0,d.useCallback)(e=>w(e,{filePendingDeletion:!0}),[w]),C=(0,d.useCallback)((e,t)=>{w(e,{mergeState:t}),l.current.forEach(n=>n(e,t))},[w]),U=(0,d.useCallback)(e=>(l.current.add(e),()=>{l.current.delete(e)}),[]),S=(0,d.useCallback)(e=>s.current.get(e),[]),[I,_]=(0,d.useState)([]),[b,T]=(0,d.useState)(!1),D=(0,d.useCallback)(()=>{c({type:"UPDATE_FILE_EDITS",edits:new Map}),T(!1)},[c]);(0,d.useEffect)(()=>{I.length&&T(!0)},[I]),(0,d.useEffect)(()=>(_(o.filter(e=>{var t;let n=S(e);return!!n&&(null===(t=n.mergeState)||void 0===t?void 0:t.isActive)&&!!n.view})),U((e,t)=>{_(n=>{var r;let i=n.includes(e),a=t.isActive&&!!(null===(r=S(e))||void 0===r?void 0:r.view);return i===a?n:a?[...n,e]:n.filter(t=>t!==e)})})),[o,U,S,b]);let j=(0,d.useCallback)(()=>{I.forEach(e=>{var t;let n=null===(t=S(e))||void 0===t?void 0:t.view;if(n)for(;m(n,"accept"););}),n({event_key:"harmony.suggestion.accepted"})},[I,n,S]),x=(0,d.useCallback)(()=>{I.forEach(e=>{var t;let r=null===(t=S(e))||void 0===t?void 0:t.view;if(r){for(;m(r,"reject"););C(e,{isActive:!1}),n({event_key:"harmony.suggestion.rejected"})}})},[I,n,S,C]),A=(0,d.useCallback)(e=>{var t,n;return null===(n=S(e))||void 0===n?void 0:null===(t=n.view)||void 0===t?void 0:t.state.doc.toString()},[S]),P=(0,d.useCallback)(e=>{var t;let n=A(e);return u()(n)&&n!==(null===(t=S(e))||void 0===t?void 0:t.baseContent)},[A,S]),M=(0,d.useMemo)(()=>({getInstance:S,setBaseContent:g,flagForDeletion:E,getCurrentContent:A,hasUnsavedChanges:P,registerEditor:p,unregisterEditor:v,setMergeState:C,subscribeToMergeStateChanges:U,acceptAllChanges:j,rejectAllChanges:x,deactivateChangesMode:D,activeEditors:I,changesMode:b}),[S,g,E,A,P,p,v,C,U,j,x,D,I,b]);return(0,r.jsx)(y.Provider,{value:M,children:t})}function w(){return(0,d.useContext)(y)||p}},65380:function(e,t,n){n.d(t,{KA:function(){return s},Nc:function(){return u},YB:function(){return c},b8:function(){return a},h4:function(){return o}});var r=n(35567),i=n.n(r);function a(e,t){return i()(e,t)}function o(e){let t=[],n=0;for(let[r,i]of e)0!==r&&t.push({op:r,pos:n,text:i}),-1!==r&&(n+=i.length);return t}function c(e){if(!Array.isArray(e))throw Error("Input must be an array");e.forEach((e,t)=>{if(!("object"==typeof e&&null!==e&&"op"in e&&"number"==typeof e.op))throw Error("Invalid change object at index ".concat(t));if(1!==e.op&&-1!==e.op)throw Error("Invalid 'op' value at index ".concat(t));if("number"!=typeof e.pos||!Number.isInteger(e.pos))throw Error("Invalid 'pos' value at index ".concat(t));if("string"!=typeof e.text)throw Error("Invalid 'text' value at index ".concat(t))})}function u(e,t){return function(e,t){let n=e,r=0;for(let e of t){let t=e.pos+r;1===e.op?(n=n.slice(0,t)+e.text+n.slice(t),r+=e.text.length):-1===e.op&&(n=n.slice(0,t)+n.slice(t+e.text.length),r-=e.text.length)}return n}(e,t.map(e=>({op:-e.op,pos:e.pos,text:e.text})).reverse())}function s(e){for(let[t]of e)if(0!==t)return!1;return!0}},2550:function(e,t,n){function r(e){var t;return(null===(t=e.mergeState)||void 0===t?void 0:t.isActive)?e.mergeState.diffSource:e.view.state.doc.toString()}function i(e){return r(e)!==e.baseContent}n.d(t,{li:function(){return r},oI:function(){return i}}),n(65380)},3909:function(e,t,n){n.d(t,{G:function(){return a}});var r=n(68068),i=n.n(r);function a(e){return i().createHash("sha256").update(e.trim()).digest("hex").slice(0,6)}},95950:function(e,t,n){n.d(t,{Y:function(){return u}});var r=n(88075),i=n(44846),a=n(48644),o=n(64655),c=n(27957);let u=e=>{var t;let{account:n}=(0,r.t)(),{value:u}=(0,i.F)("force_harmony"),{data:s,isLoading:l}=(0,c.Yc)(e),{data:d,isLoading:f}=(0,o.SE)(e||""),h=null!==(t=null==d?void 0:d.some(e=>e.account.uuid===(null==n?void 0:n.uuid)&&"user"===e.role))&&void 0!==t&&t,y="showDirectoryPicker"in window&&"FileSystemHandle"in window,p=(0,a.useConfig)("harmony").config;return{userHasHarmony:y&&((null==n?void 0:n.settings.preview_feature_uses_harmony)||u)&&(null==p?void 0:p.get("harmonize",!1)),projectHasHarmony:!l&&!f&&h&&!!(null==s?void 0:s.is_harmony_project),config:p}}},51087:function(e,t,n){n.d(t,{C:function(){return E},b:function(){return C}});var r=n(27573),i=n(7653),a=n(90345),o=n.n(a);let c=(0,i.createContext)(null),u={openedFiles:[],projectDocs:[],files:[],setFiles:o(),projectUuid:"",syncedDirectories:[],setSyncedDirectories:o()};function s(e){let{children:t,onLoad:n}=e;return(0,i.useEffect)(n,[n]),(0,r.jsx)(c.Provider,{value:u,children:t})}var l=n(32751),d=n(20053),f=n.n(d),h=n(3982),y=n(48970),p=n(769),m=n(12063),v=n(1373);function w(e){let{children:t,onLoad:n,projectUuid:a}=e,{isLoading:o,unfilteredData:u=[]}=(0,y.Kf)(a),[s,d]=(0,i.useState)([]),[w,g]=(0,i.useState)([]),E=(0,i.useMemo)(()=>[...(function(e,t){let n=new Map,r=t.filter(v.IQ).map(e=>e.uri);if(!r.length)return n;for(let t of r){let r=new Set;for(let n of e){if(!(0,v.Wx)(n.file_name))continue;let{projectUuid:e,directoryUuid:i}=(0,v.Xp)(n.file_name),a=(0,v.Xp)(t);e===a.projectUuid&&i===a.directoryUuid&&r.add(n.file_name)}n.set(t,r)}return n})(u,s).values()].flatMap(e=>[...e]),[u,s]);(0,i.useEffect)(()=>{(0,p.Zz)(a).then(g).catch(e=>l.v("Harmony: Error initializing synced directories from IndexedDB",e))},[a]);let{mutateAsync:C}=(0,y.u3)(a),{mutateAsync:U}=(0,y.Zy)(a),{mutateAsync:S}=(0,y.ER)(a),I=(0,i.useCallback)(()=>{(0,m.tt)(a,o,s,u,C,U,S).then(e=>{e&&(f()(s,e.updatedFiles)||(d(e.updatedFiles),l.f("Harmony: Resynced ".concat(e.updatedFiles.filter(v.zE).length," files in ").concat(e.updatedFiles.filter(v.IQ).length," directories")),n()))}).catch(e=>l.v("Harmony: Error during resync:",e))},[a,o,s,u,C,U,S,n]);(0,i.useEffect)(I,[I]),(0,h.Yz)(I,3e4);let _=(0,i.useMemo)(()=>({projectUuid:a,openedFiles:E,projectDocs:u,files:s,setFiles:d,syncedDirectories:w,setSyncedDirectories:g}),[a,E,u,s,w,g]);return(0,r.jsx)(c.Provider,{value:_,children:t})}var g=n(95950);function E(e){let{children:t,onLoad:n,projectUuid:i}=e,{userHasHarmony:a}=(0,g.Y)(i);return a?(0,r.jsx)(w,{onLoad:n,projectUuid:i,children:t}):(0,r.jsx)(s,{onLoad:n,children:t})}function C(){return(0,i.useContext)(c)||u}},769:function(e,t,n){n.d(t,{Gz:function(){return h},U4:function(){return y},Zz:function(){return d},sN:function(){return f},y3:function(){return p}});var r=n(32751),i=n(71994),a=n(1373);let o="directories",c="projectUuid",u=null;async function s(){return u||new Promise((e,t)=>{let n=indexedDB.open("harmony",1);n.onerror=()=>t(n.error),n.onsuccess=()=>{(u=n.result).onerror=e=>{r.v("Database error:",e)},u.onclose=()=>{u=null},e(u)},n.onupgradeneeded=e=>{e.target.result.createObjectStore(o,{keyPath:"uuid"}).createIndex(c,"projectUuid",{unique:!1})}})}function l(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"readonly";if(!u)throw Error("Database not initialized");return u.transaction(o,e)}async function d(e){await s();let t=l("readonly").objectStore(o).index(c);return new Promise((n,r)=>{let i=t.getAll(e);i.onerror=()=>r(i.error),i.onsuccess=()=>{n(i.result.map(e=>({...e,uri:(0,a.cT)(e)})))}})}async function f(e){await s();let t=l("readonly").objectStore(o);return new Promise((n,r)=>{let i=t.get(e);i.onerror=()=>r(i.error),i.onsuccess=()=>{if(i.result){let e=i.result;n({...e,uri:(0,a.cT)(e)})}else n(null)}})}async function h(e){await s();let t={...e,uuid:(0,i.H)()};return new Promise((e,n)=>{let i=l("readwrite").objectStore(o).add(t);i.onerror=()=>n(i.error),i.onsuccess=()=>{let n=(0,a.cT)(t);e({...t,uri:n}),r.f("Harmony: Synced directory added to IndexedDB",t)}})}async function y(e){return await s(),new Promise((t,n)=>{let r=l("readwrite").objectStore(o).put(e);r.onerror=()=>n(r.error),r.onsuccess=()=>t()})}async function p(e){return await s(),new Promise((t,n)=>{let r=l("readwrite").objectStore(o).delete(e);r.onerror=()=>n(r.error),r.onsuccess=()=>t()})}},12063:function(e,t,n){n.d(t,{Jl:function(){return y},wC:function(){return E},T7:function(){return S},bE:function(){return f},lz:function(){return U},xF:function(){return m},Zn:function(){return C},cM:function(){return g},tt:function(){return I},KT:function(){return h},ec:function(){return p}});var r=n(32751),i=n(20053),a=n.n(i),o=n(48970),c=n(65380),u=n(2550),s=n(3909),l=n(769),d=n(1373);async function f(e){let t=await (0,l.Zz)(e);return await (0,d.C7)(t)}async function h(e,t,r){let i=arguments.length>3&&void 0!==arguments[3]&&arguments[3],a=arguments.length>4&&void 0!==arguments[4]&&arguments[4],o=await Promise.all(t.filter(d.zE).map(async t=>({path:t.uri,content:await y(e,t.uri)})));return new Promise((e,t)=>{let c=new Worker(n.tu(new URL(n.p+n.u(6269),n.b))),u=setTimeout(()=>{t(Error("Search timeout"))},3e4),s=()=>{c.terminate(),clearTimeout(u)};c.onerror=e=>{s(),t(e)};let l=[];c.onmessage=t=>{let{type:n,results:r}=t.data;l.push(...r),"complete"===n&&(s(),e(l))},c.postMessage({files:o,searchTerm:r,isRegex:i,caseSensitive:a})})}async function y(e,t){return(await (0,d.pJ)(e,t)).text}async function p(e,t,n,i,a,o){let s=await (0,l.Zz)(t),f=Array.from(new Set([...e])).map(async e=>{if((0,d.Wx)(e))try{let t=o(e),l=t?(0,u.li)(t):void 0,d=t?t.baseContent:void 0;if(void 0===d||void 0===l){let t=await y(s,e);if(!l){if(null===t){r.v(Error("File content not found for ".concat(e)));return}return await v(n,i,a,e,t,[])}return await v(n,i,a,e,l,(0,c.b8)(t||"",l))}let f=(0,c.b8)(d,l);return await v(n,i,a,e,l,f)}catch(t){r.v("Error processing file ".concat(e,":"),t)}});await Promise.all(f)}async function m(e,t,n,r,i){let a=await y(e,i);if(null===a)throw Error("File content not found for ".concat(i));if(new TextEncoder().encode(a).length>102400)throw Error("File ".concat(i," is too large and will degrade the experience. Pass a specific view_range when using the view tool for this file."));return await v(t,n,r,i,a)}async function v(e,t,n,r,i,a){let o=e.find(e=>e.file_name===r);if(o&&function(e){let t=arguments.length>1&&void 0!==arguments[1]&&arguments[1],n=e.match(/<content>([\s\S]*)<\/content>/),r=n&&n[1]?n[1].trim():e;if(t){let t=e.match(/<changes>(.*?)<\/changes>/);if(t&&t[1]){let e=JSON.parse(t[1]);(0,c.YB)(e),r=(0,c.Nc)(r,e)}}return r}(o.content)===i)return o;let u=function(e,t){let n=(0,s.G)(e),r=void 0!==t&&!(0,c.KA)(t);return"\n<metadata>\n<file_hash>".concat(n,"</file_hash>\n<file_state>\n  ").concat(r&&void 0!==t?"\n  <status>includes_unsaved_changes</status>\n  <message>This content includes modifications since it was last synchronized. You can and should continue to suggest changes using write or replace operations. Your suggestions will be applied to the latest version of the file. THIS IS THE MOST UP TO DATE VERSION OF THE FILE.</message>\n  <changes>".concat(JSON.stringify((0,c.h4)(t)),"</changes>\n"):"<status>synced</status>","\n</file_state>\n</metadata>\n<content>").concat(e,"</content>\n").trim()}(i,a);return o?await n({docUuid:o.uuid,content:u}):await t({file_name:r,content:u})}async function w(e,t,n,i,a){if(0===e.length){let e=t.find(e=>e.file_name===o.i9);e&&await a({docUuid:e.uuid});return}let c=JSON.stringify(e.map(e=>e.uri),null,2).split("\n"),u=c.slice(0,50).join("\n"),s=c.length-50,l="<synced_resources>\n".concat(u,"\n").concat(s>0?"\n... plus ".concat(s," additional files."):"","\n</synced_resources>"),d=t.filter(e=>e.file_name===o.i9);if(d.length>0){let[e,...n]=d;if(n.length>0&&r.f("Harmony: Cleaning up ".concat(n.length," extra project docs")),await Promise.all(n.map(e=>g(t,e.file_name,a))),e.content===l){r.f("Harmony: Project doc already up to date",e.uuid);return}await i({docUuid:e.uuid,content:l}),r.f("Harmony: Updated project doc",e.uuid)}else{let e=await n({file_name:o.i9,content:l});r.f("Harmony: Created project doc",e.uuid)}}async function g(e,t,n){let r=e.find(e=>e.file_name===t);r&&await n({docUuid:r.uuid})}async function E(e,t,n,r){let{projectUuid:i,directoryUuid:a}=(0,d.Xp)(r),o=(0,d.wq)(e,i,a);for(let e of(await (0,l.y3)(a),t.filter(e=>U(e,o))))await n({docUuid:e.uuid});return e.filter(e=>e!==o)}async function C(e,t,n){let r=await (0,d.mf)(e,null!=n?n:[]);return await (0,l.Gz)({projectUuid:t,root:r,ignorePatterns:null!=n?n:[],lastUpdated:Date.now()})}function U(e,t){if(!(0,d.Wx)(e.file_name))return!1;let{projectUuid:n,directoryUuid:r}=(0,d.Xp)(t.uri),{projectUuid:i,directoryUuid:a}=(0,d.Xp)(e.file_name);return n===i&&r===a}function S(e){let t=e.split("/"),n=t[t.length-1],r=t[t.length-2];return""===n||"."===n?"".concat(r,"/"):n}async function I(e,t,n,r,i,o,c){if(!e||t)return;let u=await (0,l.Zz)(e),s=await (0,d.C7)(u);if(!a()(n.map(e=>e.uri),s.map(e=>e.uri))){for(let e of u)e.root.descendants.some(t=>t.lastModified>e.lastUpdated)&&await (0,l.U4)({...e,lastUpdated:Date.now()});return await w(s,r,i,o,c),{updatedFiles:s}}}},1373:function(e,t,n){n.d(t,{O:function(){return g},cn:function(){return m},_I:function(){return v},wq:function(){return U},sy:function(){return S},IQ:function(){return E},zE:function(){return C},Wx:function(){return R},C7:function(){return w},mf:function(){return D},Xp:function(){return M},pJ:function(){return f},cT:function(){return _},NC:function(){return h}});var r=n(49456),i=n(32751),a=n(36758);class o{static getInstance(){return o.instance||(o.instance=new o),o.instance}getCacheKey(e,t){return"".concat(e.name,"-").concat(t)}isPermissionExpired(e){return Date.now()-e>this.CACHE_DURATION}async checkPermission(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"read",n=this.getCacheKey(e,t),r=this.permissionCache.get(n);if(r&&!this.isPermissionExpired(r.timestamp))return"granted"===r.state;try{if("queryPermission"in e){let r=await e.queryPermission({mode:t});if("granted"===r)return this.permissionCache.set(n,{state:"granted",timestamp:Date.now(),mode:t}),!0}if("requestPermission"in e){let r=await e.requestPermission({mode:t});return"granted"===r&&this.permissionCache.set(n,{state:r,timestamp:Date.now(),mode:t}),"granted"===r}return this.permissionCache.set(n,{state:"granted",timestamp:Date.now(),mode:t}),!0}catch(e){return i.v("Permission check failed:",e),!1}}constructor(){this.permissionCache=new Map,this.CACHE_DURATION=36e5}}let c=o.getInstance();async function u(e,t){return c.checkPermission(e,t)}var s=n(46385).Buffer;let l="inode/directory";async function d(e,t){let n=await e.getFile();return{handle:e,path:"".concat(t,"/").concat(n.name),lastModified:n.lastModified}}async function f(e,t){let n,i;let{directory:a,file:o}=S(e,t);if(!o)throw Error("File not found: ".concat(t));let c=await o.handle.getFile(),u=null;try{u=await (0,r.CL)(c),i=c.type||"text/plain"}catch(t){let e=await c.arrayBuffer();n=e.byteLength>1048576?"[File truncated due to size]":s.from(e).toString("base64"),i=c.type||"application/octet-stream"}return{uri:I(a,o),mimeType:i,text:u,blob:n}}async function h(e,t){if(!await u(e.handle,"readwrite"))throw Error("Permission denied");let n=await e.handle.getFile();try{await (0,r.CL)(n)}catch(e){throw Error("Cannot write to non-text files")}let a=await e.handle.createWritable();try{await a.write(t)}finally{await a.close()}i.f("Harmony: Wrote file ".concat(e.path," to local file system")),e.lastModified=Date.now()}async function y(e,t){try{return await e.getDirectoryHandle(t,{create:!0})}catch(e){throw Error("Failed to create directory ".concat(t))}}async function p(e,t){let n=e;for(let e=0;e<t.length-1;e++)n=await y(n,t[e]);return n}async function m(e,t,n){let{pathComponents:r}=q(t);if(!await u(e.root.handle,"readwrite"))throw Error("Permission denied");let i=await p(e.root.handle,r),a=r[r.length-1];try{let t={handle:await i.getFileHandle(a,{create:!0}),path:"".concat(e.root.name,"/").concat(r.join("/")),lastModified:Date.now()};return await h(t,n),e.root.descendants.push(t),!0}catch(e){throw Error("Failed to create file ".concat(t," - ").concat(e))}}async function v(e,t){let{pathComponents:n}=q(t);if(!await u(e.root.handle,"readwrite"))throw Error("Permission denied to delete file in the directory");let r=await p(e.root.handle,n),i=n[n.length-1];try{return await r.removeEntry(i),e.root.descendants=e.root.descendants.filter(t=>t.path!=="".concat(e.root.name,"/").concat(n.join("/"))),!0}catch(e){throw Error("Failed to delete file ".concat(i))}}async function w(e){return(await Promise.all(e.map(g))).flat()}async function g(e){try{if(await u(e.root.handle,"read")){let t=await j(e);t&&(e.root=t.updatedDirectoryRoot)}}catch(t){i.v("Harmony: Could not resync ".concat(e.uuid),t)}let t=e.root.descendants.map(t=>({uri:I(e,t)}));return t.unshift({uri:_(e),mimeType:l}),t}function E(e){return e.mimeType===l}function C(e){return!E(e)}function U(e,t,n){let r=e.find(e=>e.projectUuid===t&&e.uuid===n);if(!r)throw Error("Resource not found: ".concat(t,"/").concat(n));return r}function S(e,t){let{projectUuid:n,directoryUuid:r,pathComponents:i}=M(t),a=U(e,n,r);try{let e=function(e,t){let n="".concat(e.root.name,"/").concat(t.join("/")),r=e.root.descendants.find(e=>e.path===n);if(!r)throw Error("File not found: ".concat(n));return r}(a,i);return{directory:a,file:e}}catch(e){return{directory:a,file:null}}}function I(e,t){let n=t.path.split("/").map(encodeURIComponent);return"file://".concat(e.projectUuid,"/").concat(e.uuid,"/")+n.join("/")}function _(e){return"file://".concat(e.projectUuid,"/").concat(e.uuid,"/").concat(encodeURIComponent(e.root.name),"/")}async function b(e,t,n,r){let i=n.flatMap(e=>{if(""===(e=e.trim())||e.startsWith("#"))return[];let t=e.startsWith("!");return t&&(e=e.slice(1)),(e=e.replace(/^\//,"")).endsWith("/")&&(e+="*"),t?["!".concat(e)]:[e]}),o=[],c=[[e,t]];for(;c.length>0;){let[e,n]=c.shift();for await(let u of e.values()){if(o.length>=r)throw Error("Maximum number of files (".concat(r,") exceeded"));if(u.name.startsWith(".")&&".gitignore"!==u.name)continue;let e="".concat(n,"/").concat(u.name),s=e.slice(t.length+1);if(!i.some(e=>(0,a.s7)(s,e,{dot:!0,matchBase:!0}))){if("file"===u.kind){let e=await d(u,n);o.push(e)}else c.push([u,e])}}}return o}async function T(e){try{let t=await e.getFileHandle(".gitignore",{create:!1}),n=await t.getFile();return(await n.text()).split("\n").filter(e=>""!==e.trim()&&!e.startsWith("#"))}catch(e){return[]}}async function D(e,t){let n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:2500;try{let r=[...await T(e),...t],i=await b(e,e.name,r,n);return{handle:e,name:e.name,descendants:i}}catch(e){if(e instanceof Error&&e.message.includes("Maximum number of files"))throw Error("The size of this directory may cause performance degradation. Please choose a smaller directory.");throw e}}async function j(e){let t;let n=e.root;try{t=await D(e.root.handle,e.ignorePatterns)}catch(e){return null}let r=x(n.descendants),i=x(t.descendants),a=[];for(let[e,t]of r.entries()){let n=i.get(e);if(void 0===n){a.push({type:"removed",file:t});continue}n.lastModified!==t.lastModified&&a.push({type:"modified",file:n}),i.delete(e)}for(let e of i.values())a.push({type:"added",file:e});return{updatedDirectoryRoot:t,fileChanges:a}}function x(e){let t=new Map;for(let n of e)t.set(n.path,n);return t}let A=new Map,P=(e,t)=>{A.size>=1e3&&Array.from(A.keys()).slice(0,Math.floor(200)).forEach(e=>A.delete(e)),A.set(e,t)};function M(e){if(A.has(e))return A.get(e);if(!e||""===e.trim())throw Error("Invalid URI: URI is undefined or empty");if(!e.startsWith("file://"))throw Error('Invalid URI: Must start with "file://"');let t=new URL(e),n=t.host,[r,i,a,...o]=t.pathname.split("/").map(decodeURIComponent);if(!(n&&o.length))throw Error("Invalid URI: Missing required components");let c={projectUuid:n,directoryUuid:i,directoryName:a,pathComponents:o};return P(e,c),c}function R(e){try{return M(e),!0}catch(e){return!1}}function q(e){if(!e||""===e.trim())throw Error("Invalid URI: URI is undefined or empty");if(!e.startsWith("file://"))throw Error('Invalid URI: Must start with "file://"');try{let t=new URL(e),n=t.host,[r,i,a,...o]=t.pathname.split("/").map(decodeURIComponent);if(!n||!i||!a)throw Error("Invalid URI: Missing required components");return{projectUuid:n,directoryUuid:i,directoryName:a,pathComponents:o}}catch(e){throw Error("Invalid URI: ".concat(e.message))}}},32751:function(e,t,n){function r(){for(var e=arguments.length,t=Array(e),n=0;n<e;n++)t[n]=arguments[n]}function i(){for(var e=arguments.length,t=Array(e),n=0;n<e;n++)t[n]=arguments[n]}n.d(t,{f:function(){return r},v:function(){return i}})}}]);