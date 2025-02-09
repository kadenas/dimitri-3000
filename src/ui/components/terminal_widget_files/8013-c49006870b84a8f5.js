"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[8013],{78013:function(e,t,s){s.d(t,{LayoutWithSidebar:function(){return th}});var n=s(27573),a=s(76335),i=s(61925),l=s(88075),r=s(85565),d=s(51571),o=s(82880),c=s(17886),u=s(6734),x=s(35018),m=s(90026);function h(){let e=(0,r._)(["\n  border\n  rounded-full\n  px-2\n  font-medium\n  text-sm\n  flex\n  gap-1\n  items-center\n  select-none\n"]);return h=function(){return e},e}let f=o.q.div(h()),p=e=>{let{envToDisplay:t}=e;switch(t){case"dev":return(0,n.jsx)("span",{className:"bg-accent-main-900 text-accent-main-100",children:"dev"});case"staging":return(0,n.jsx)("span",{className:"bg-accent-pro-900 text-accent-pro-100",children:"staging"})}},j=e=>{let t,{envToDisplay:s,concise:a=!1,appLayer:i}=e;switch(i){case"frontend":t=(0,n.jsx)(x.s,{size:a?12:16,weight:"bold"});break;case"backend":t=(0,n.jsx)(m.v,{size:a?12:16,weight:"bold"})}switch(s){case"staging":return(0,n.jsxs)(f,{className:"border-accent-pro-100 bg-accent-pro-900 text-accent-pro-000",children:[t,a?"St":"Staging"]});case"dev":return(0,n.jsxs)(f,{className:"border-accent-main-100 bg-accent-main-900 text-accent-main-000",children:[t,"Dev"]})}},g=e=>{let{concise:t=!1}=e,{backendPrivateApiUrl:s}=(0,d.m)(),a=(0,u.cm)()?"staging":(0,u.yG)()?"dev":void 0,i="dev"!==a?a:s.includes("staging")?"staging":"dev";return a&&i?a===i?(0,n.jsx)(c.u,{tooltipContent:(0,n.jsxs)("span",{children:["Both FE and BE are in ",(0,n.jsx)(p,{envToDisplay:a})]}),side:"bottom",children:(0,n.jsx)("div",{className:"pb-2",children:(0,n.jsx)(j,{envToDisplay:a})})}):(0,n.jsxs)("div",{className:"inline-flex cursor-default items-center gap-1 pb-2",children:[(0,n.jsx)(c.u,{tooltipContent:(0,n.jsxs)("span",{children:["Frontend: ",(0,n.jsx)(p,{envToDisplay:a})]}),side:"bottom",children:(0,n.jsx)("div",{children:(0,n.jsx)(j,{envToDisplay:a,concise:t,appLayer:"frontend"})})}),(0,n.jsx)(c.u,{tooltipContent:(0,n.jsxs)("span",{children:["Backend: ",(0,n.jsx)(p,{envToDisplay:i})]}),side:"bottom",children:(0,n.jsx)("div",{children:(0,n.jsx)(j,{envToDisplay:i,concise:t,appLayer:"backend"})})})]}):void 0};var v=s(11096),b=s(58396);let y=e=>{let{size:t}=e,{account:s}=(0,l.t)(),a=(0,l.ZJ)();return(0,n.jsx)(b.M,{account:s||null,size:t,variant:a?"pro":"default"})};var w=s(99663),N=s(4713),k=s(5942),M=s(20880),C=s(69454),_=s(31702),Z=s(35675),z=s(95859),E=s(57908),P=s(3095),S=s(87659),F=s(93124),O=s(91237),T=s(5891),L=s(2275),D=s(44846),J=s(67754),A=s(7653),U=s(92082);let R=e=>{let{openNewChatModal:t}=e,s=(0,J.useRouter)(),{value:n}=(0,D.F)("new_chat_modal"),a=(0,A.useCallback)(()=>{n?t():s.push("/new")},[t,s,n]);return(0,L.H9)(L.LT.cmdK,a),(0,A.useEffect)(()=>{let e=e=>{var t;let s=(0,T.V5)()?e.metaKey:e.ctrlKey;(null===(t=e.key)||void 0===t?void 0:t.toLowerCase())==="k"&&s&&(e.preventDefault(),a())};return document.addEventListener("keydown",e),()=>document.removeEventListener("keydown",e)},[a]),null},X=()=>{let[e,t]=(0,A.useState)(!1);return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(R,{openNewChatModal:()=>t(!0)}),(0,n.jsx)(U.e,{isOpen:e,onClose:()=>t(!1)})]})};var B=s(69602),H=s(46326),q=s(3982);function I(){let e=(0,r._)(["\n  border\n  rounded-full\n  px-2\n  font-medium\n  text-sm\n  flex\n  gap-1\n  items-center\n  select-none\n"]);return I=function(){return e},e}let K=o.q.div(I()),V=()=>{let{isEnabled:e,comparativeModel:t}=(0,i.uD)(),s=(0,q.O_)();return e&&s&&t?(0,n.jsx)(c.u,{tooltipContent:(0,n.jsx)("span",{className:"bg-accent-danger-900 text-accent-danger-100",children:(0,n.jsx)(F.Z,{defaultMessage:"Comparing responses against {model}",id:"OfXPOA+l9o",values:{model:t}})}),side:"bottom",children:(0,n.jsxs)(K,{children:[(0,n.jsx)(H.M,{size:12,weight:"bold"}),(0,n.jsx)(F.Z,{defaultMessage:"comparing",id:"dzOqyR/+PE"})]})}):null};var W=s(23489),Q=s(21468),Y=s(83925);let G=()=>{var e;let{isEnabled:t,comparativeModel:s,setComparativeModel:a}=(0,i.uD)(),{activeModelOptions:l}=(0,W.u)(),r=(0,O.Z)(),d=(0,Q.z$)(),o=(0,A.useCallback)(e=>{let t=e.target.value;a(t),t?d.track({event_key:"hfi.comparative_model.selected",model_name:t,last_model_name:s}):d.track({event_key:"hfi.comparative_model.selection_cleared",last_model_name:s})},[a,d,s]),u=(0,q.O_)();if(!t||!u)return null;let x=s?null===(e=l.find(e=>{let{model:t}=e;return t===s}))||void 0===e?void 0:e.name:null;return(0,n.jsx)(c.u,{tooltipContent:(0,n.jsx)("span",{children:x?(0,n.jsx)(F.Z,{defaultMessage:"Comparing responses against {modelName} ({comparativeModel})",id:"kkDOlLJzfz",values:{modelName:x,comparativeModel:s}}):(0,n.jsx)(F.Z,{defaultMessage:"Not comparing against another model",id:"X1vvySTCxK"})}),side:"bottom",children:(0,n.jsx)("div",{className:"w-full mb-1 flex flex-col",children:(0,n.jsxs)(Y.P,{id:"comparative-model-selector",className:"text-xs inline-block",size:"sm",value:s||"",onChange:o,label:r.formatMessage({defaultMessage:"HFI comparison",id:"L8Eovm+sfw"}),children:[(0,n.jsx)("option",{value:"",children:(0,n.jsx)(F.Z,{defaultMessage:"none",id:"q5Op6V1w7b"})}),l.map(e=>{let{model:t,name:s}=e;return(0,n.jsx)("option",{value:t,children:s},t)})]})})})};var $=s(17718),ee=s(11907),et=s(15437),es=s(61814),en=s(67736),ea=s(95014),ei=s(40152),el=s(99728),er=s(35747),ed=s(87846),eo=s(14120),ec=s(10751),eu=s.n(ec),ex=s(28986),em=s(48644),eh=s(79843),ef=s(59038),ep=s(85571),ej=s(24912);let eg=()=>{let{mode:e,setMode:t}=(0,eh.F)();return(0,A.useEffect)(()=>{(0,L.hd)()},[e]),(0,n.jsxs)(es.Vy,{children:[(0,n.jsxs)(es.WR,{className:"text-sm",children:[(0,n.jsx)(F.Z,{defaultMessage:"Appearance",id:"2GURQYNPp3"}),"\xa0",(0,n.jsx)(ea.T,{size:16})]}),(0,n.jsx)(es.nI,{children:(0,n.jsxs)(es.A2,{sideOffset:4,children:[(0,n.jsxs)(es.hP,{onSelect:()=>t("auto"),children:[(0,n.jsxs)("div",{className:"flex items-center gap-2 pr-4 text-sm",children:[(0,n.jsx)(ef.u,{size:16}),"\xa0",(0,n.jsx)(F.Z,{defaultMessage:"System",id:"+CwN9C/QFk"})]}),"auto"===e?(0,n.jsx)(er.J,{size:16}):(0,n.jsx)("div",{className:"h-4 w-4"})]}),(0,n.jsxs)(es.hP,{onSelect:()=>t("light"),children:[(0,n.jsxs)("div",{className:"flex items-center gap-2 text-sm",children:[(0,n.jsx)(ep.k,{size:16}),"\xa0",(0,n.jsx)(F.Z,{defaultMessage:"Light",id:"3cc4CtJM5h"})]}),"light"===e?(0,n.jsx)(er.J,{size:16}):(0,n.jsx)("div",{className:"h-4 w-4"})]}),(0,n.jsxs)(es.hP,{onSelect:()=>t("dark"),children:[(0,n.jsxs)("div",{className:"flex items-center gap-2 text-sm",children:[(0,n.jsx)(ej.J,{size:16}),"\xa0",(0,n.jsx)(F.Z,{defaultMessage:"Dark",id:"tOdNiYuuag"})]}),"dark"===e?(0,n.jsx)(er.J,{size:16}):(0,n.jsx)("div",{className:"h-4 w-4"})]})]})})]})};var ev=s(30247),eb=(s(79791),s(71854));function ey(){let e=(0,r._)(["fixed top-2.5 right-3.5 z-10 flex flex-row items-center gap-2"]);return ey=function(){return e},e}function ew(){let e=(0,r._)(["\n  border\n  border-accent-pro-200\n  bg-accent-pro-900\n  rounded-lg\n  mt-1\n  mb-2\n  mx-2\n  py-2\n  px-3\n"]);return ew=function(){return e},e}function eN(e){var t;let{onOpenChange:s}=e,i=(0,O.Z)(),{track:r}=(0,Q.z$)(),{account:o}=(0,l.t)(),{openConsentBanner:c}=(0,et.C)(),u=null==o?void 0:o.memberships.map(e=>e.organization),x=null==u?void 0:u.some(e=>e.capabilities.includes("api")),m=Object.keys(null===(t=(0,em.useConfig)("fp_menu").config)||void 0===t?void 0:t.get("features",{})).length>0,{openModal:h}=(0,a.h)(),f=(0,d.m)(),{value:p}=(0,D.F)("conversation_export"),{value:j}=(0,D.F)("claude_ai_intercom"),g=(0,ex.o)(),b=(0,l.Cf)(),w=(0,n.jsxs)(v.z,{variant:"unstyled",size:"unset",className:"border-0.5 border-border-300 hover:border-border-200 group relative z-[1] w-full overflow-hidden rounded-lg !px-2.5 !py-2 !text-left","data-testid":"user-menu-button",children:[(0,n.jsx)("div",{className:"from-bg-500/0 to-bg-500/40 absolute inset-0 bg-gradient-to-b opacity-70 transition-opacity group-hover:opacity-100"}),(0,n.jsxs)("div",{className:"relative z-[5] flex w-full items-center gap-1.5",children:[(0,n.jsx)(y,{size:"sm"}),(0,n.jsx)("div",{className:"min-w-0 flex-1 truncate text-sm",children:null==o?void 0:o.email_address}),(0,n.jsx)(en.p,{size:12})]})]});return(0,n.jsx)(n.Fragment,{children:(0,n.jsxs)(es.Lt,{matchTriggerWidth:!0,align:"end",unstyledTrigger:!0,trigger:w,onOpenChange:e=>{null==s||s(e)},className:"w-72",children:[(0,n.jsx)(ek,{}),m&&(0,n.jsx)(es.hP,{onSelect:()=>{r({event_key:"claudeai.settings.preview_feature.opened",source:"user_menu"}),h()},className:"text-sm",children:(0,n.jsx)(F.Z,{defaultMessage:"Feature Preview",id:"FfkUr6izJa"})}),(0,n.jsx)(es.u2,{}),(0,n.jsxs)(es.Vy,{children:[(0,n.jsxs)(es.WR,{className:"text-sm",children:[(0,n.jsx)(F.Z,{defaultMessage:"Learn more",id:"TdTXXf940t"}),"\xa0",(0,n.jsx)(ea.T,{size:16})]}),(0,n.jsx)(es.nI,{children:(0,n.jsxs)(es.A2,{sideOffset:4,children:[(0,n.jsx)(e_,{name:i.formatMessage({defaultMessage:"About Anthropic",id:"Cm+OGj8nZs"}),path:"/"}),(0,n.jsx)(es.u2,{}),!b&&(0,n.jsx)(e_,{name:i.formatMessage({defaultMessage:"Consumer Terms",id:"vPzYLV3Pyi"}),path:"/legal/consumer-terms"}),(0,n.jsx)(e_,{name:i.formatMessage({defaultMessage:"Usage Policy",id:"oio2A03CTj"}),path:"/legal/aup"}),(0,n.jsx)(e_,{name:i.formatMessage({defaultMessage:"Privacy Policy",id:"vx0nkZ8xpy"}),path:"/legal/privacy"}),(0,n.jsx)(es.hP,{asChild:!0,children:(0,n.jsx)("button",{className:"w-full text-left text-sm",onClick:c,children:(0,n.jsx)(F.Z,{defaultMessage:"Your Privacy Choices",id:"Hty8P+F08/"})})})]})})]}),x&&(0,n.jsx)(n.Fragment,{children:(0,n.jsx)(es.hP,{asChild:!0,children:(0,n.jsxs)(S.default,{href:f.consoleAbsoluteUrl,target:"_blank",className:"text-sm",children:[(0,n.jsx)(F.Z,{defaultMessage:"API Console",id:"CfiNwKIPP1"}),"\xa0",(0,n.jsx)(ei.O,{})]})})}),j&&(0,n.jsx)(es.hP,{onSelect:()=>{r({event_key:"claudeai.get_help.clicked"}),g.update({hideDefaultLauncher:!1}),g.show()},className:"text-sm intercom-launcher",children:(0,n.jsx)(F.Z,{defaultMessage:"Get help",id:"9OuUCLqQgd"})}),(0,n.jsx)(es.hP,{asChild:!0,children:(0,n.jsxs)(S.default,{href:"https://support.anthropic.com/",target:"_blank",className:"text-sm",onClick:()=>{r({event_key:"claudeai.support.opened"})},children:[j?(0,n.jsx)(F.Z,{defaultMessage:"Help Center",id:"HtSDycElXb"}):(0,n.jsx)(F.Z,{defaultMessage:"Help & Support",id:"Uf3+S6hwtD"}),"\xa0",(0,n.jsx)(ei.O,{})]})}),(0,n.jsx)(es.hP,{asChild:!0,children:(0,n.jsxs)(S.default,{href:"https://claude.ai/download",target:"_blank",className:"text-sm",children:[(0,n.jsx)(F.Z,{defaultMessage:"Download Apps",id:"jI7JVSAJpx"}),"\xa0",(0,n.jsx)(ei.O,{})]})}),(0,n.jsx)(es.u2,{}),p&&(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(es.hP,{asChild:!0,children:(0,n.jsx)(ev.Jh,{})}),(0,n.jsx)(es.u2,{})]}),"",(0,n.jsx)(es.hP,{asChild:!0,children:(0,n.jsx)(S.default,{href:"/logout",className:"text-sm",children:(0,n.jsx)(F.Z,{defaultMessage:"Log Out",id:"H0JBH6xAVJ"})})})]})})}let ek=()=>{let{account:e}=(0,l.t)(),t=(0,A.useMemo)(()=>{var t;return null!==(t=null==e?void 0:e.memberships.map(e=>e.organization))&&void 0!==t?t:[]},[e]),s=(0,A.useMemo)(()=>eu()(t.filter(e=>e.capabilities.includes("chat")),e=>!e.capabilities.includes("raven"),"name"),[t]),a=s.some(e=>e.capabilities.includes("raven"));return(0,n.jsx)(n.Fragment,{children:e&&(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(es.HF,{className:"text-sm pb-2 overflow-ellipsis truncate",children:null==e?void 0:e.email_address}),s.map(e=>(0,n.jsx)(eM,{org:e,hasTeam:a},e.uuid)),(0,n.jsx)(eZ,{orgs:s}),(0,n.jsx)(es.u2,{}),(0,n.jsx)(es.hP,{asChild:!0,"data-testid":"user-menu-settings",children:(0,n.jsx)(S.default,{href:"/settings/profile",className:"text-sm",children:(0,n.jsx)(F.Z,{defaultMessage:"Settings",id:"D3idYvSLF9"})})}),(0,n.jsx)(eg,{})]})})},eM=e=>{let{org:t,hasTeam:s}=e,a=(0,O.Z)(),{switchAndRefresh:i}=(0,ee.z6)(),{activeOrganization:r}=(0,l.t)(),d=(0,l.gQ)(t),o=(0,J.usePathname)(),c=d?"Enterprise":t.capabilities.includes("raven")?"Team":t.capabilities.includes("claude_pro")?"Pro":"Free",u=t.uuid===(null==r?void 0:r.uuid),x=t.capabilities.includes("raven")?t.name:a.formatMessage({defaultMessage:"Personal",id:"NDx+B0BTac"}),m=(0,n.jsx)(n.Fragment,{children:(0,n.jsxs)("div",{className:"flex items-center gap-2 w-full",children:[(0,n.jsx)(eC,{org:t}),(0,n.jsxs)("div",{className:"flex flex-col overflow-hidden grow",children:[(0,n.jsx)("span",{className:"truncate text-text-100 text-sm",children:x}),(0,n.jsxs)("div",{className:"text-xs",children:[(0,n.jsx)("span",{className:"text-text-300",children:(0,n.jsx)(F.Z,{defaultMessage:"{plan} plan",id:"oK+PGPHfhv",values:{plan:c}})}),"Free"===c&&u&&s&&(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(el.o,{size:12,className:"inline"}),(0,n.jsx)(S.default,{href:"/upgrade",className:"text-accent-pro-100 hover font-medium transition-all",children:(0,n.jsx)(F.Z,{defaultMessage:"Upgrade",id:"0h/lPMeYkq"})})]})]})]}),t.uuid===(null==r?void 0:r.uuid)&&(0,n.jsx)(er.J,{weight:"bold",className:"flex-shrink-0 text-accent-main-100 h-4 w-4"})]})});return u?(0,n.jsx)(es.AZ,{children:m}):(0,n.jsx)(es.hP,{onSelect:()=>{o.startsWith("/chat/")?i(t.uuid,"/chats"):i(t.uuid)},children:m})},eC=e=>{let{org:t}=e,s=t.capabilities.includes("raven")||t.capabilities.includes("claude_pro")?"bg-accent-pro-100":"bg-text-400",a=t.capabilities.includes("raven")?(0,n.jsx)(ed.$,{size:16}):(0,n.jsx)(eo.n,{size:16});return(0,n.jsx)("div",{className:(0,E.Z)(s,"flex-shrink-0 text-oncolor-100 flex h-7 w-7 items-center justify-center rounded-full"),children:a})},e_=e=>{let{name:t,path:s}=e,{websiteBaseUrl:a}=(0,d.m)();return(0,n.jsx)(es.hP,{asChild:!0,children:(0,n.jsxs)(S.default,{href:"".concat(a).concat(s),target:"_blank",className:"text-sm",children:[t,(0,n.jsx)(ei.O,{})]})})};o.q.div(ey());let eZ=e=>{let{orgs:t}=e,s=(0,l.Sl)(),a=(0,A.useMemo)(()=>t.some(e=>e.capabilities.includes("claude_pro")),[t]);return t.some(e=>e.capabilities.includes("raven"))||a&&!s?null:(0,n.jsxs)(ez,{children:[(0,n.jsx)("p",{className:"text-text-300 text-sm",children:a?(0,n.jsx)(F.Z,{defaultMessage:"Claude's better with your teammates.",id:"JmpPbizrjQ"}):(0,n.jsx)(F.Z,{defaultMessage:"Get more from Claude with Pro or Team plans.",id:"uME1B4Y8Ek"})}),(0,n.jsx)(S.default,{href:"/upgrade",className:"text-accent-pro-000 text-sm font-medium",children:a?(0,n.jsx)(F.Z,{defaultMessage:"Add Team Plan",id:"Va+Jw/hdxd"}):(0,n.jsx)(F.Z,{defaultMessage:"Upgrade Plan",id:"8Wfi094ofM"})})]})},ez=o.q.div(ew());var eE=s(96742);function eP(e){let{type:t,href:s,onClick:a=()=>void 0,className:i,children:l}=e,r=(0,J.usePathname)();return(0,n.jsx)(S.default,{className:(0,E.Z)("hover:bg-bg-400 group -mx-1.5 flex items-center gap-1 rounded-md px-1.5 py-1 transition-colors duration-200",("chat"===t||"project"===t)&&"font-tiempos text-text-200 text-sm",r===s&&"bg-bg-400",i),href:s,onClick:a,children:"link"===t?(0,n.jsx)(n.Fragment,{children:l}):(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(()=>"project"===t?(0,n.jsx)(k.j,{size:16,className:"shrink-0 translate-y-px"}):"chat"===t?(0,n.jsx)(eE.J,{size:14,className:"shrink-0"}):void 0,{}),(0,n.jsx)("div",{className:"min-w-0 truncate",children:l})]})})}var eS=s(91014),eF=s(63226);function eO(){let{track:e}=(0,Q.z$)(),{data:t,isLoading:s}=(0,eS.QR)({limit:8,offset:0});if(!s)return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)("h3",{className:"text-text-300 mb-1 mt-1 text-sm font-medium",children:(0,n.jsx)(F.Z,{defaultMessage:"Recents",id:"wA4FIMmtlS"})}),(null==t?void 0:t.length)===0?(0,n.jsx)("div",{className:"border-border-300 text-text-500 rounded-lg border border-dashed px-3 py-8 text-center text-xs",children:(0,n.jsx)(F.Z,{defaultMessage:"Start your first conversation with Claude",id:"8ncY+fezs4"})}):(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)("ul",{className:"flex flex-col gap-0.5",children:null==t?void 0:t.map(t=>(0,n.jsx)("li",{children:(0,n.jsx)(eP,{type:"chat",href:"/chat/".concat(t.uuid),onClick:()=>{e({event_key:"claudeai.conversation.recent.opened",conversation_uuid:t.uuid})},children:t.name?t.name:(0,n.jsx)(F.Z,{defaultMessage:"(New chat)",id:"iFmsJKMEi2"})})},t.uuid))}),(0,n.jsxs)(S.default,{href:"/recents",className:"text-text-300 hover:text-text-200 -ml-px mt-2 flex items-center gap-1 text-sm",children:[(0,n.jsx)(F.Z,{defaultMessage:"View all",id:"pFK6bJU0EM"}),(0,n.jsx)(eF.o,{size:12,className:"translate-y-px"})]})]})]})}var eT=s(27957);function eL(){let e=(0,B.U)(),{data:t,isLoading:s}=(0,eT.bQ)(),{data:a,isLoading:i}=(0,eS.cj)();if(e&&s||i)return;let l=null!=a?a:[],r=null!=t?t:[],d=!(null==r?void 0:r.length)&&!(null==l?void 0:l.length),o=(0,n.jsx)("div",{className:"border-border-300 text-text-500 rounded-lg border border-dashed px-3 py-8 text-center text-xs",children:e?(0,n.jsx)(F.Z,{defaultMessage:"Star projects and chats you use often",id:"ySSiOyaLgB"}):(0,n.jsx)(F.Z,{defaultMessage:"Star chats you use often",id:"CTXuzagSvL"})});return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)("h3",{className:"text-text-300 mb-1 flex items-center gap-1.5 text-sm font-medium",children:(0,n.jsx)(F.Z,{defaultMessage:"Starred",id:"V7cUPvWFo3"})}),d?o:(0,n.jsxs)("ul",{className:"-mx-1.5 flex flex-1 flex-col gap-0.5 overflow-y-auto px-1.5",children:[r.map(e=>(0,n.jsx)("li",{children:(0,n.jsx)(eP,{type:"project",href:"/project/".concat(e.uuid),children:e.name})},e.uuid)),l.map(e=>(0,n.jsx)("li",{children:(0,n.jsx)(eP,{type:"chat",href:"/chat/".concat(e.uuid),children:e.name})},e.uuid))]})]})}var eD=s(84115),eJ=s(57713),eA=s.n(eJ);let eU=(e,t)=>{let[s,n]=(0,eD.nh)(eb.cn.SIDEBAR_PINNED,!1),[a,i]=(0,A.useState)(s),l=(0,A.useCallback)(e=>{n(e),i(e),d(!1)},[n]),[r,d]=(0,A.useState)(!1),{width:o=0}=(0,q.iP)(),c=o<768;(0,A.useEffect)(()=>{s&&i(!c)},[c,s]);let u=(0,A.useRef)(0),x=(0,A.useRef)(null),[m,h]=(0,A.useState)(0);return(0,A.useEffect)(()=>{let n=eR(e),l=eR(t),d=e=>{if(!s&&!r&&!c){let{clientX:t}=e,s=(a?l:n)+12,r=a||t<u.current;if(t>s){let e=1-(t-s)/(window.outerWidth/3);h(e=eA()(e,0,1))}let d=t<=s&&r;d?(x.current&&(clearTimeout(x.current),x.current=null),i(!0)):a&&!x.current&&(x.current=setTimeout(()=>{i(d)},250)),u.current=t}},o=()=>{h(0),u.current=0,s||(x.current=setTimeout(()=>{i(!1)},500))};return document.addEventListener("mousemove",d),document.addEventListener("mouseleave",o),()=>{x.current&&(clearTimeout(x.current),x.current=null),document.removeEventListener("mousemove",d),document.removeEventListener("mouseleave",o)}},[r,a,s,i,e,t,c]),{isExpanded:a,setIsExpanded:i,isPinnedExpanded:s,setIsPinnedExpanded:l,hasDropdownOpen:r,setHasDropdownOpen:d,isMobile:c,gradientAffordanceOpacity:m}};function eR(e){return parseFloat(e.replace("rem",""))*parseFloat(window.getComputedStyle(document.documentElement).fontSize)}let eX="4.5rem",eB="18rem";function eH(e){let{isExpanded:t,isPinnedExpanded:s,setHasDropdownOpen:a}=e,i=(0,B.U)();return(0,n.jsxs)(P.E.div,{initial:s?"enter":"initial",animate:t?"enter":"initial",className:(0,E.Z)("flex flex-col min-h-0 h-full",!t&&"pointer-events-none opacity-0"),children:[(0,n.jsxs)("div",{className:"overflow-y-auto overflow-x-hidden flex flex-col gap-4 px-3 -mx-3 pb-2 pt-3 h-full u-hidden-scrollbar",style:{maskImage:"linear-gradient(180deg, rgba(0, 0, 0, 0) 0, rgba(0, 0, 0, 1) 0.75rem, rgba(0, 0, 0, 1) calc(100% - 1.5rem), rgba(0, 0, 0, 0) 100%)"},children:[(0,n.jsxs)(P.E.ul,{variants:eV,className:"flex flex-col gap-px",children:[(0,n.jsx)("li",{children:(0,n.jsxs)(eP,{type:"link",href:"/new",className:"text-accent-main-000",children:[(0,n.jsx)($.jU,{className:"shrink-0"}),(0,n.jsx)(F.Z,{defaultMessage:"Start new chat",id:"KcA+xo4hhh"})]})}),i&&(0,n.jsx)("li",{children:(0,n.jsxs)(eP,{type:"link",href:"/projects",className:"text-text-100",children:[(0,n.jsx)(k.j,{size:16,className:"translate-y-[0.5px]"}),(0,n.jsx)(F.Z,{defaultMessage:"Projects",id:"UxTJRaKagI"})]})})]},"main-nav"),(0,n.jsx)(P.E.div,{variants:eV,className:"flex min-h-0 flex-col min-h-min",children:(0,n.jsx)(eL,{})},"starred"),(0,n.jsx)(P.E.div,{className:"flex-1 pb-3",variants:eV,children:(0,n.jsx)(eO,{})},"recents")]}),(0,n.jsxs)(P.E.div,{variants:eW,className:"flex flex-col",children:[(0,n.jsxs)("div",{className:"flex flex-col space-y-1 z-0",children:[(0,n.jsx)(G,{}),(0,n.jsx)(g,{})]}),(0,n.jsx)("div",{className:"translate-y-0 px-2",children:(0,n.jsx)(e$,{})}),(0,n.jsx)(eN,{onOpenChange:e=>null==a?void 0:a(e)}),(0,n.jsxs)("div",{className:"mt-2 flex items-center justify-between pl-1.5 pr-1",children:[(0,n.jsx)("div",{className:"text-text-400 translate-y-[0.5px]",children:(0,n.jsx)(w.V,{size:15})}),(0,n.jsxs)("a",{href:"https://support.anthropic.com/en/",target:"_blank",className:"text-text-300 flex translate-x-0 items-center gap-1 text-xs hover:underline",children:[(0,n.jsx)(M.H,{size:14}),(0,n.jsx)(F.Z,{defaultMessage:"Help & support",id:"t/Ekfe9gAS"})]})]})]},"user-menu")]})}function eq(){let e=(0,O.Z)(),{isExpanded:t,setIsExpanded:s,isPinnedExpanded:a,setIsPinnedExpanded:i,setHasDropdownOpen:l,isMobile:r,gradientAffordanceOpacity:d}=eU(eX,eB);return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(X,{}),(0,n.jsxs)(P.E.nav,{variants:eI,initial:a?"pinnedExpanded":"collapsed",animate:a?"pinnedExpanded":"collapsed",className:"z-sidebar h-screen max-md:pointer-events-none max-md:fixed",onClick:()=>{r?t&&!l&&s(!1):s(!0)},"data-testid":"menu-sidebar",children:[(0,n.jsx)("div",{className:(0,E.Z)("pointer-events-auto absolute left-2 top-3 md:hidden",t&&"opacity-0"),children:(0,n.jsx)(v.z,{size:"icon_sm",variant:"ghost",onClick:()=>s(!0),children:(0,n.jsx)(eG,{})})}),(0,n.jsxs)(P.E.div,{style:{width:eB},className:(0,E.Z)("fixed bottom-0 left-0 top-0 px-3 pb-4 pt-2.5",t?"pointer-events-auto":"pointer-events-none"),children:[!a&&(0,n.jsx)("div",{style:{opacity:t?0:d,width:eB,transform:"translate3d(0,0,0)",backfaceVisibility:"hidden"},className:"from-bg-500/40 to-bg-500/0 fixed left-0 top-0 h-full bg-gradient-to-r to-80% transition-opacity max-md:hidden"}),(0,n.jsx)(P.E.div,{variants:eK,initial:t?"expanded":"collapsed",animate:t?"expanded":"collapsed",transition:{type:"spring",stiffness:900,damping:50,mass:1},style:{width:eB,transform:"translate3d(0,0,0)"},className:(0,E.Z)("from-bg-300/70 to-bg-400/70 border-r-0.5 border-border-300 absolute left-0 overflow-hidden bg-gradient-to-b backdrop-blur",a?"bottom-0 top-0":"shadow-level-1 border-t-0.5 border-b-0.5 bottom-1 top-1 rounded-r-xl")}),(0,n.jsxs)(P.E.div,{initial:a?"enter":"initial",animate:t?"enter":"initial",className:(0,E.Z)("flex h-full flex-col",!t&&"pointer-events-none"),children:[(0,n.jsxs)("div",{className:"-mr-1 flex translate-y-px items-center",children:[(0,n.jsx)(eY,{isExpanded:t}),(0,n.jsxs)(P.E.div,{className:(0,E.Z)(!t&&"pointer-events-none"),variants:eQ,children:[(0,n.jsx)(v.z,{variant:"ghost",size:"icon_sm",className:"md:hidden",onClick:()=>s(!1),children:(0,n.jsx)(_.X,{size:16})}),(0,n.jsx)("div",{className:"max-md:hidden",children:(0,n.jsx)(c.u,{side:"right",tooltipContent:a?e.formatMessage({defaultMessage:"Unpin sidebar",id:"GY942ifhuL"}):e.formatMessage({defaultMessage:"Pin sidebar",id:"CbhFihKPdw"}),children:(0,n.jsx)(v.z,{variant:"ghost",size:"icon_sm",onClick:()=>i(!a),"data-testid":"pin-sidebar-toggle",children:a?(0,n.jsx)(Z.l,{size:16}):(0,n.jsx)(C.g,{size:16})})})})]})]}),(0,n.jsx)(eH,{isExpanded:t,isPinnedExpanded:a,setHasDropdownOpen:l})]}),!t&&(0,n.jsxs)("div",{className:"absolute bottom-4 flex items-start flex-col gap-10 max-md:hidden",children:[(0,n.jsxs)(P.E.div,{initial:{opacity:0,translateX:"4px"},animate:{opacity:1,translateX:"0px"},transition:{duration:.15},children:[(0,n.jsx)(V,{}),(0,n.jsx)(g,{concise:!0})]}),(0,n.jsxs)("div",{className:"flex flex-col items-center gap-4 max-md:hidden",children:[(0,n.jsx)("div",{className:"-translate-y-[0.5px]",children:(0,n.jsx)(y,{size:"sm"})}),(0,n.jsx)(P.E.div,{initial:{opacity:0,translateX:"4px"},animate:{opacity:1,translateX:"0px"},transition:{duration:.15},className:"text-text-400 relative flex h-4 w-4 items-center justify-center",children:(0,n.jsx)("button",{onClick:()=>s(!0),"aria-label":e.formatMessage({defaultMessage:"open sidebar",id:"aBWlDf2ISA"}),"aria-pressed":t?"true":"false",children:(0,n.jsx)(z.z,{})})})]})]})]})]})]})}let eI={collapsed:{width:eX},pinnedExpanded:{width:eB},transition:{type:"spring",stiffness:1e3,damping:100,mass:1}},eK={collapsed:{opacity:0,translateX:"-25%",transition:{opacity:{duration:.1},translateX:{duration:.5}}},expanded:{opacity:1,translateX:"0%"}},eV={initial:{opacity:0,translateX:"-15%",filter:"blur(2px)",transition:{opacity:{duration:.05}}},enter:{opacity:1,translateX:"0%",filter:"blur(0px)",transition:{translateX:{type:"spring",stiffness:1e3,damping:50,mass:1}}}},eW={initial:{opacity:0,translateX:"-10px",transition:{duration:.05}},enter:{opacity:1,translateX:"0px",transition:{opacity:{duration:0},type:"spring",stiffness:1e3,damping:50,mass:1}}},eQ={initial:{opacity:0,scale:.95,translateX:"-6px",transition:{opacity:{duration:.05}}},enter:{opacity:1,scale:1,translateX:"0px"}};function eY(e){let{isExpanded:t}=e;return(0,n.jsx)("div",{className:(0,E.Z)("ml-px flex h-9 flex-1 items-center leading-none",!t&&"max-md:pointer-events-none max-md:opacity-0"),children:(0,n.jsxs)(S.default,{href:"/new",children:[(0,n.jsx)(N.l,{className:(0,E.Z)("h-4 flex-shrink-0",t?"text-text-100":"text-text-300")}),""]})})}function eG(e){let{size:t=24}=e;return(0,n.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:t,height:t,fill:"currentColor",viewBox:"0 0 32 32",children:(0,n.jsx)("path",{d:"M26 16a1 1 0 0 1-1 1H5a1 1 0 0 1 0-2h20a1 1 0 0 1 1 1ZM5 9h18a1 1 0 1 0 0-2H5a1 1 0 0 0 0 2Zm16 14H5a1 1 0 0 0 0 2h16a1 1 0 0 0 0-2Z"})})}function e$(){let{activeOrganization:e}=(0,l.t)(),t=(0,l.Cf)(),s=(0,l.ZJ)(),a=!s&&!t,i=t&&!!(null==e?void 0:e.name);return(0,n.jsxs)("div",{className:(0,E.Z)("font-tiempos border-0.5 rounded-t-md border-b-0 bg-gradient-to-b p-1 text-center text-xs",a?"from-bg-200 to-bg-200/5 text-text-300 bg-bg-300 border-border-300":"text-accent-pro-000 from-accent-pro-100/0 to-accent-pro-100/5 border-accent-pro-200/50"),children:[t&&(i?e.name:(0,n.jsx)(F.Z,{defaultMessage:"Team",id:"wsUmh9XWBm"})),s&&(0,n.jsx)(F.Z,{defaultMessage:"Professional plan",id:"hephW2Q72r"}),a&&(0,n.jsx)(F.Z,{defaultMessage:"Free plan",id:"B+7815cfpz"})]})}var e0=s(63610);function e1(){let e=(0,r._)(["\n  gap-3\n  ","\n"]);return e1=function(){return e},e}function e2(){let e=(0,r._)(['\n  text-text-200\n  shadow-inset-border-0.5\n  shadow-border-300\n  data-[state="checked"]:text-accent-secondary-000\n  data-[state="checked"]:shadow-inset-border\n  data-[state="checked"]:shadow-accent-secondary-200\n  transition-all\n  group/card\n  text-left\n  font-styrene\n  rounded-lg\n  px-4\n  py-3\n']);return e2=function(){return e},e}(0,o.q)(e0.fC)(e1(),e=>{let{full:t}=e;return t?"grid\n      grid-flow-col\n      auto-cols-fr":"flex"}),(0,o.q)(e0.ck)(e2());var e5=s(74651);s(23428);var e3=s(1489),e4=s(73567),e6=s(42443),e7=s(85409),e8=s(29620),e9=s(71233),te=s(65880),tt=s(2282);function ts(){let e=(0,r._)(["\n  max-w-full\n  mb-3\n  pb-1\n  pl-1\n  pr-1\n  min-w-[180px]\n  md:mb-0\n  md:p-0\n  [&::-webkit-scrollbar]:bg-transparent\n  [&::-webkit-scrollbar]:h-[4px]\n  [&::-webkit-scrollbar-thumb]:bg-[rgba(0,0,0,0.15)]\n  [&::-webkit-scrollbar-thumb]:rounded-[100px]\n"]);return ts=function(){return e},e}function tn(){let e=(0,r._)(["\n  relative\n  border\n  border-border-300\n  rounded-xl\n  overflow-hidden\n"]);return tn=function(){return e},e}function ta(){let e=(0,r._)(["\n  font-styrene-display\n  font-medium\n  tracking-tighter\n  leading-[0.9em]\n  text-xl]\n"]);return ta=function(){return e},e}function ti(){let e=(0,r._)(["\n  font-styrene\n  text-text-300\n  text-md]\n"]);return ti=function(){return e},e}function tl(){var e;let t=null===(e=(0,em.useConfig)("fp_menu").config)||void 0===e?void 0:e.get("features",{}),s=(0,tt.i)(),n=(0,B.U)(),{value:a,source:i}=(0,e6.h)({}),l={...t};s&&delete l.preview_feature_uses_artifacts,a&&"experiment"===i&&delete l.enabled_artifacts_attachments,n||delete l.preview_feature_uses_harmony;let r=Object.keys(l).length>0;return{features:l,hasFeatures:r}}let tr=()=>{var e,t,s,i,r,d,o,c,u,x,m,h;let f=(0,O.Z)(),{isOpen:p,activeFeatureKey:j,closeModal:g,setActiveFeatureKey:v}=(0,a.h)(),{track:b}=(0,Q.z$)(),{account:y}=(0,l.t)(),{mutate:w}=(0,e4.Ck)(),{features:N,hasFeatures:k}=tl(),{value:M}=(0,D.F)("force_harmony"),{value:C,source:_}=(0,e6.h)(null!==(x=null==y?void 0:y.settings)&&void 0!==x?x:{}),[Z,z]=(0,A.useState)(!1);(0,A.useEffect)(()=>{j&&j in N||!k||v(Object.keys(N)[0])},[N,k,j,v]),(0,A.useEffect)(()=>{if(!Z)return;let e=setTimeout(()=>{z(!1)},7e3);return()=>{clearTimeout(e)}},[Z]);let E=!!j&&null!==(m=null==y?void 0:null===(e=y.settings)||void 0===e?void 0:e[j])&&void 0!==m&&m;"preview_feature_uses_harmony"===j&&M&&(E=!0),"enabled_artifacts_attachments"===j&&"flag"===_&&C&&(E=!0);let P="preview_feature_uses_harmony"===j&&M;return(0,n.jsxs)(e5.u_,{modalSize:"xl",isOpen:p,onClose:g,hasCloseButton:!0,title:f.formatMessage({defaultMessage:"Feature Preview",id:"FfkUr6izJa"}),icon:(0,n.jsx)(e8.G,{size:"24"}),children:[(0,n.jsx)("div",{className:"text-text-400 text-sm",children:(0,n.jsx)(F.Z,{defaultMessage:"Preview and provide feedback on upcoming enhancements to our platform. Please note: experimental features might influence Claude's behavior and some interactions may differ from the standard experience.",id:"nRjeQQ1Gbi"})}),(0,n.jsx)("div",{className:"border-border-300 mt-4 flex flex-col items-stretch gap-4 md:flex-row",children:k&&j?(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(to,{children:(0,n.jsx)("ul",{className:"flex gap-1 md:flex-col flex-wrap",children:Object.keys(N).map(e=>{var t;return(0,n.jsx)(td,{isCurrentButton:e===j,onClick:()=>v(e),children:null===(t=N[e])||void 0===t?void 0:t.title},e)})})}),(0,n.jsx)(tc,{children:(0,n.jsxs)("div",{className:"h-auto overflow-y-auto md:h-[27em]",children:[(null===(s=N[j])||void 0===s?void 0:null===(t=s.image)||void 0===t?void 0:t.src)&&(0,n.jsx)(te.default,{src:null!==(h=null===(r=N[j])||void 0===r?void 0:null===(i=r.image)||void 0===i?void 0:i.src)&&void 0!==h?h:"",style:{width:"100%",height:"auto"},width:null===(d=N[j])||void 0===d?void 0:d.image.width,height:null===(o=N[j])||void 0===o?void 0:o.image.height,alt:f.formatMessage({defaultMessage:"Preview image of feature",id:"6VliGZPeZA"})}),(0,n.jsxs)("div",{className:"border-border-300 border-t p-4",children:[(0,n.jsxs)("div",{className:"mb-3 flex w-full items-center justify-between",children:[(0,n.jsx)("h3",{className:"font-styrene-display text-lg font-medium",children:null===(c=N[j])||void 0===c?void 0:c.title}),(0,n.jsx)("label",{className:"flex justify-between gap-2",children:(0,n.jsxs)("div",{className:"flex cursor-pointer gap-2 self-center",children:[(0,n.jsx)("span",{className:"text-text-000 self-center text-xs",children:E?(0,n.jsx)(F.Z,{defaultMessage:"On",id:"Zh+5A6yahu"}):(0,n.jsx)(F.Z,{defaultMessage:"Off",id:"OvzONl52rs"})}),(0,n.jsx)(e7.Z,{disabled:P,checked:E,onChange:()=>{y&&j&&(z(!0),b({event_key:"claudeai.settings.preview_feature.toggled",account_uuid:y.uuid,feature_id:j,action:!0===E?"disable":"enable"}),w({...y.settings,[j]:!E}))}},"activeFeatureKey")]})})]}),(0,n.jsx)("p",{className:"text-text-300 text-sm",children:null===(u=N[j])||void 0===u?void 0:u.description})]})]})})]}):(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(tu,{children:(0,n.jsx)(F.Z,{defaultMessage:"No Features Available",id:"BZgwb1vh3U"})}),(0,n.jsx)(tx,{children:(0,n.jsx)(F.Z,{defaultMessage:"There are no features available to preview.",id:"j2ZCZOmEcz"})})]})}),Z&&(0,n.jsxs)("div",{className:"text-accent-secondary-100 bg-bg-100 mt-3 flex items-center justify-center gap-1 rounded-md px-2 py-1 text-xs",children:[(0,n.jsx)(e9.f,{}),"\xa0",(0,n.jsx)(F.Z,{defaultMessage:"Settings will apply to future conversations",id:"jJr0uk3TyA"})]})]})},td=(0,A.forwardRef)((e,t)=>{let{children:s,isCurrentButton:a,onClick:i}=e;return(0,n.jsx)("li",{children:(0,n.jsx)("button",{ref:t,onClick:i,className:(0,E.Z)(a?"bg-bg-400 font-medium":"hover:bg-bg-300","block w-full whitespace-nowrap rounded-full px-5 py-2 text-left transition-colors ease-in-out active:scale-95"),children:s})})});td.displayName="SidebarButton";let to=o.q.nav(ts()),tc=o.q.div(tn()),tu=o.q.h2(ta()),tx=o.q.h3(ti()),tm=()=>{let{features:e}=tl();return Object.keys(e).length>0?(0,n.jsx)(tr,{}):null};function th(e){let{children:t}=e;return(0,n.jsx)("div",{className:"flex min-h-screen w-full",children:(0,n.jsx)(a.b,{children:(0,n.jsx)(i.s4,{children:(0,n.jsxs)(e3.Q,{children:[(0,n.jsx)(tm,{}),"",(0,n.jsx)(eq,{}),(0,n.jsx)("div",{className:"min-h-full w-full min-w-0 flex-1",children:t})]})})})})}},92082:function(e,t,s){s.d(t,{Y:function(){return h},e:function(){return m}});var n=s(27573),a=s(65930),i=s(88075),l=s(11096),r=s(74651),d=s(17886),o=s(7653),c=s(85338),u=s(50987),x=s(17718);let m=e=>{let{isOpen:t,onClose:s}=e,{account:l}=(0,i.t)(),d=(0,a.w)();return((0,o.useEffect)(()=>{let e=e=>{"Escape"===e.key&&t&&(e.preventDefault(),s())};return t&&document.addEventListener("keydown",e),()=>{document.removeEventListener("keydown",e)}},[t,s]),l)?(0,n.jsx)(r.u_,{isOpen:t,onClose:s,modalSize:"xl",backgroundColor:"bg-transparent",className:"!shadow-none border-none !p-0",children:(0,n.jsx)(u.x,{willRedirectOnSubmit:!0,onCreate:async e=>(s(),await d(e)),children:(0,n.jsx)(c.x,{placement:"modal",accountSettings:l.settings})})}):null},h=()=>{let[e,t]=(0,o.useState)(!1);return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(d.u,{tooltipContent:"New chat",side:"bottom",children:(0,n.jsx)(l.z,{size:"icon",option:"rounded",onClick:()=>t(!0),children:(0,n.jsx)(x.jU,{width:20,height:20})})}),(0,n.jsx)(m,{isOpen:e,onClose:()=>t(!1)})]})}},61925:function(e,t,s){s.d(t,{s4:function(){return c},uD:function(){return o}});var n=s(27573),a=s(23489),i=s(20504),l=s(44846),r=s(7653);let d=(0,r.createContext)({comparativeModel:"",isEnabled:!1,setComparativeModel:()=>{throw Error("Not initialized")}}),o=()=>{let e=(0,r.useContext)(d);if(!e)throw Error("useHfiFeedbackConfig must be used within a HfiFeedbackConfigProvider");return e},c=e=>{let{children:t}=e,{value:s}=(0,l.F)("show_hfi_feedback_ui"),o=(0,a.u)().activeModelOptions.map(e=>e.model),[c,u,x]=(0,i.R)("hfi:comparativeModel","");(0,r.useEffect)(()=>{c&&!o.includes(c)&&x()},[o,x,c]);let m=(0,r.useMemo)(()=>({isEnabled:s,comparativeModel:c,setComparativeModel:e=>{e&&o.includes(e)?u(e):x()}}),[s,c,o,x,u]);return(0,n.jsx)(d.Provider,{value:m,children:t})}},30247:function(e,t,s){s.d(t,{Dy:function(){return h},Jh:function(){return x}});var n=s(85565),a=s(27573),i=s(91014),l=s(82880),r=s(11096),d=s(7653),o=s(93124);function c(){let e=(0,n._)(["\n  w-full\n  text-left\n  text-sm\n  disabled:pointer-events-none\n  disabled:shadow-none\n  disabled:drop-shadow-none"]);return c=function(){return e},e}let u=e=>{let{data:t}=(0,i.QR)(),[s,n]=(0,d.useState)([]),[a,l]=(0,d.useState)(null),[r,o]=(0,d.useState)([]),{data:c,error:u}=(0,i._C)(null!=a?a:"");return(0,d.useEffect)(()=>{if(!t)return;if(c&&c.uuid===a)s.some(e=>e.uuid===c.uuid)||n(e=>[...e,c]);else{if(!u)return;o(e=>[...e,a])}let i=t.find(e=>!s.some(t=>t.uuid===e.uuid)&&!r.includes(e.uuid));i?l(i.uuid):e(s)},[c,u,r,a,s,t,e]),{totalConversations:null==t?void 0:t.length,numExported:s.length,numFailed:r.length,startExporting:()=>{t&&t.length&&l(t[0].uuid)}}},x=(0,d.forwardRef)((e,t)=>{let[s,n]=(0,d.useState)(!1),[i,l]=(0,d.useState)(null),{totalConversations:r,numExported:c,numFailed:x,startExporting:h}=u(e=>{n(!1),l(JSON.stringify(e,null,2))});return s?(0,a.jsx)(m,{ref:t,disabled:!0,...e,children:x>0?(0,a.jsx)(o.Z,{defaultMessage:"Exporting: {numExported} / {totalConversations} ({numFailed} failed)",id:"hKNwlNeKOf",values:{numExported:c,totalConversations:r,numFailed:x}}):(0,a.jsx)(o.Z,{defaultMessage:"Exporting: {numExported} / {totalConversations}",id:"EAIBTT4RJD",values:{numExported:c,totalConversations:r}})}):i?(0,a.jsx)(m,{ref:t,...e,onClick:()=>{let e=new Blob([i],{type:"application/json"}),t=URL.createObjectURL(e),s=document.createElement("a");s.href=t,s.download="conversations.json",s.click()},children:(0,a.jsx)(o.Z,{defaultMessage:"Download Conversations",id:"4L07zIpdIw"})}):(0,a.jsx)(m,{ref:t,...e,onClick:()=>{n(!0),h()},children:(0,a.jsx)(o.Z,{defaultMessage:"Export all conversations",id:"mVqNYWmNHv"})})});x.displayName="ExportConversationsWidget";let m=l.q.button(c()),h=e=>{let{conversationUUID:t}=e,{data:s}=(0,i.Rq)(t);return(0,a.jsx)(r.z,{variant:"outline",size:"sm",onClick:()=>{let e=new Blob([JSON.stringify(s,null,2)],{type:"application/json"}),t=URL.createObjectURL(e),n=document.createElement("a");n.href=t,n.download="conversation.json",n.click()},children:(0,a.jsx)(o.Z,{defaultMessage:"Download Conversation",id:"LuAMejyuTp"})})}},58396:function(e,t,s){s.d(t,{M:function(){return i}});var n=s(27573),a=s(18793);let i=e=>{var t,s,i;let{account:l,size:r,variant:d}=e,o=null!==(i=null!==(s=null!==(t=null==l?void 0:l.full_name)&&void 0!==t?t:null==l?void 0:l.display_name)&&void 0!==s?s:null==l?void 0:l.email_address)&&void 0!==i?i:"";return(0,n.jsx)(a.q,{name:o,size:r,variant:d})}}}]);