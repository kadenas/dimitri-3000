"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[8474],{77508:function(e,n,t){t.d(n,{X:function(){return o}});var r=t(27573),a=t(57908),s=t(3095);let o=e=>{let{label:n,checked:t,onChange:o,disabled:l=!1,hideLabel:i,className:d,testId:c,...u}=e;return(0,r.jsxs)("label",{className:"select-none inline-flex align-top items-center gap-2 cursor-pointer",children:[(0,r.jsxs)("div",{className:"relative",children:[(0,r.jsx)("input",{type:"checkbox",className:"sr-only peer",checked:t,onChange:()=>{},onClick:e=>{o&&o(e.currentTarget.checked,e.shiftKey)},disabled:l,...u}),(0,r.jsx)("div",{className:(0,a.Z)("w-6 h-6 overflow-hidden flex items-center justify-center border rounded transition-colors duration-100 ease-in-out peer-focus-visible:ring-1 ring-offset-2 ring-offset-bg-300 ring-accent-main-100",t?"bg-accent-secondary-000 border-accent-secondary-000":"bg-bg-000 border-border-200 hover:border-border-100",l?"opacity-50 cursor-not-allowed":"cursor-pointer",d),"data-testid":c,children:t&&(0,r.jsx)("svg",{className:"w-4 h-4 text-oncolor-100",viewBox:"0 0 20 20",fill:"none",children:(0,r.jsx)(s.E.path,{d:"M3.5 10L8 14.5L17 5.5",stroke:"currentColor",strokeWidth:"2",strokeLinecap:"round",initial:{pathLength:0},animate:{pathLength:1},transition:{type:"spring",stiffness:280,damping:25}})})})]}),(0,r.jsx)("span",{className:(0,a.Z)(l?"text-text-500":"text-text-100",i&&"sr-only"),children:n})]})}},58845:function(e,n,t){t.d(n,{K:function(){return u},_:function(){return c}});var r=t(27573),a=t(57908),s=t(32288),o=t.n(s),l=t(51585),i=t.n(l),d=t(7653);let c=e=>{let{label:n,id:t,className:s}=e;return n?(0,r.jsx)("label",{htmlFor:t,className:(0,a.Z)("text-text-200 mb-1 block text-sm font-medium",s),children:n}):null},u=e=>{let{label:n,id:t}=e;return(0,d.useMemo)(()=>t||(n&&"string"==typeof n?i()("".concat(o()(n),"_")):i()()),[n,t])}},50725:function(e,n,t){t.d(n,{Q:function(){return o}});var r=t(27573),a=t(58845),s=t(64429);function o(e){let{placeholder:n="Select",options:t,selected:o,onSelect:l,avoidCollisions:i=!1,id:d,label:c,align:u,className:b,textClassName:m,checkboxStyle:x="round",scroll:p,size:f,type:g,disabled:h,testId:v,matchWidth:y}=e,w=(0,a.K)({id:d,label:c});return(0,r.jsxs)(r.Fragment,{children:[c&&(0,r.jsx)(a._,{label:c,id:w}),(0,r.jsx)(s.fC,{label:(null==o?void 0:o.label)||n,avoidCollisions:i,align:u,className:b,scroll:p,size:f,type:g,disabled:h,testId:v,matchWidth:y,children:t.map(e=>{let{key:n,label:t,description:a,disabled:i}=e;return(0,r.jsx)(s.ck,{label:t,description:a,onSelect:()=>l(e),checkboxStyle:x,textClassName:m,closeOnSelect:!0,checked:(null==o?void 0:o.key)===n,size:f,disabled:i},n)})})]})}},83925:function(e,n,t){t.d(n,{P:function(){return i}});var r=t(27573),a=t(58845),s=t(65517),o=t(7653);let l=(0,s.j)("block\n  text-text-200\n  py-0\n  transition-colors\n  focus:ring-accent-main-200\n  focus:border-accent-main-200",{variants:{size:{sm:"h-8 pl-3 pr-8 text-sm tracking-tight rounded-md",normal:"h-9 pl-3 pr-6.5 rounded-lg",lg:"h-11 pl-4 pr-6.5 rounded-[0.6rem]"},variant:{outline:"bg-bg-000 border border-border-200 hover:border-border-100 shadow bg-bg-000",ghost:"bg-transparent border-none shadow-none cursor-pointer",danger:"bg-danger-900 text-danger-100 shadow border-danger-200 hover:border-danger-200 focus:border-danger-200"}},defaultVariants:{size:"normal",variant:"outline"}}),i=(0,o.forwardRef)((e,n)=>{let{size:t,variant:s,className:o,label:i,id:d,...c}=e,u=(0,a.K)({id:d,label:i});return(0,r.jsxs)(r.Fragment,{children:[i&&(0,r.jsx)(a._,{label:i,id:u}),(0,r.jsx)("select",{id:u,ref:n,className:l({size:t,className:o,variant:s}),...c})]})});i.displayName="Select"},64429:function(e,n,t){t.d(n,{ck:function(){return h},fC:function(){return w}});var r=t(85565),a=t(27573),s=t(82880),o=t(35747),l=t(67736),i=t(19570),d=t(30581),c=t(89628),u=t(65517),b=t(57908);function m(){let e=(0,r._)(["\n  grow\n  shrink\n  pr-2\n  basis-0\n"]);return m=function(){return e},e}function x(){let e=(0,r._)(["\n  w-3 h-3 opacity-50 justify-center items-center inline-flex\n"]);return x=function(){return e},e}function p(e){let{checked:n}=e;return(0,a.jsxs)("div",{className:"relative h-4 w-4",children:[(0,a.jsx)("div",{className:(0,b.Z)("bg-bg-700 absolute left-0 top-0 h-4 w-4 rounded-full border",n?"border-text-100":"border-border-100")}),n&&(0,a.jsx)("div",{className:"bg-text-100 absolute left-1 top-1 h-2 w-2 rounded-full"})]})}function f(e){let{checked:n}=e;return(0,a.jsx)("div",{className:"inline-flex h-5 w-5 items-center justify-center gap-2.5",children:n?(0,a.jsx)("div",{className:"bg-text-100 text-bg-100 inline-flex h-4 w-4 items-center justify-center rounded text-lg",children:(0,a.jsx)(o.J,{size:12})}):(0,a.jsx)("div",{className:"bg-bg-300 border-border-200 h-4 w-4 rounded border"})})}t(7653);let g=(0,u.j)("\n  self-stretch\n  px-2\n  py-3\n  rounded\n  cursor-pointer\n  justify-start\n  overflow-hidden\n  text-ellipsis\n  text-text-100\n  grid\n  grid-cols-[minmax(0,_1fr)_auto]\n  inline-flex\n  gap-4\n  items-center\n  outline-none\n  select-none\n  hover:bg-bg-500\n  hover:text-text-000\n  [&[data-disabled]]:opacity-50\n  [&[data-disabled]]:bg-bg-100\n  [&[data-disabled]]:cursor-default\n",{variants:{size:{sm:"text-xs",md:"text-sm",lg:""}},defaultVariants:{size:"md"}});function h(e){let{label:n,checked:t,description:r,checkboxStyle:s,textClassName:o,closeOnSelect:l,onSelect:d,size:c="md",...u}=e;return(0,a.jsxs)(i.ck,{className:g({size:c}),onSelect:e=>{d(),l||e.preventDefault()},...u,children:[(0,a.jsxs)("div",{className:"flex shrink grow basis-0 flex-col justify-start gap-1",children:[(0,a.jsx)("div",{className:(0,b.Z)("font-normal",o),children:n}),r&&(0,a.jsx)("div",{className:(0,b.Z)("text-text-300 text-xs",o),children:r})]}),s&&("square"===s?(0,a.jsx)(f,{checked:t}):(0,a.jsx)(p,{checked:t}))]})}let v=(0,u.j)("transition-colors\n  justify-between\n  items-center\n  inline-flex\n  text-left\n  text-text-100\n  hover:border-border-100\n  border\n  border-border-200/30\n  [&[data-disabled]]:opacity-50\n  [&[data-disabled]]:cursor-not-allowed\n  [&[data-disabled]]:!text-text-500\n  focus:ring-accent-main-200\n  focus:ring-1\n  focus:outline-none",{variants:{size:{sm:"h-8 rounded-md px-3 text-xs",md:"h-9 px-3 py-2 rounded-lg text-sm",lg:"h-11 px-3 rounded-[0.6rem]"},type:{primary:"bg-bg-000 border-border-200",secondary:"bg-bg-500 border-border-300",ghost:"text-text-200 transition-all active:bg-bg-400 hover:bg-bg-300 hover:text-text-100"}},defaultVariants:{size:"md",type:"primary"}}),y=(0,u.j)("z-dropdown\n  flex\n  flex-col\n  border-0.5\n  border-border-300\n  rounded-lg\n  text-text-200\n  shadow-element",{variants:{size:{sm:"min-w-[13rem]",md:"min-w-[15rem]",lg:"min-w-[18rem]"},type:{primary:"bg-bg-000",secondary:"bg-bg-200",ghost:"bg-bg-200"},overflow:{scroll:"max-h-[16rem]",expand:""}},defaultVariants:{size:"md",type:"primary",overflow:"expand"}});function w(e){let{label:n,avoidCollisions:t,align:r="start",scroll:s=!0,sideOffset:o,children:u,className:b,disabled:m=!1,size:x="md",type:p="primary",testId:f,id:g,matchWidth:h}=e;return(0,a.jsxs)(i.fC,{children:[(0,a.jsx)(i.xz,{asChild:!0,disabled:m,children:(0,a.jsxs)("button",{id:g,className:v({size:x,type:p,className:b}),"data-testid":f,children:[(0,a.jsx)(j,{children:n}),(0,a.jsx)(N,{children:(0,a.jsx)(l.p,{})})]})}),(0,a.jsx)(i.Uv,{children:(0,a.jsx)(d.M,{trapped:!1,children:(0,a.jsx)(i.VY,{sideOffset:null!=o?o:4,className:y({size:x,type:p,overflow:s?"scroll":"expand"}),style:{width:h?"var(--radix-dropdown-menu-trigger-width)":void 0},avoidCollisions:t,align:r,asChild:!0,children:s?(0,a.jsxs)(c.fC,{className:"w-[100%] overflow-hidden",type:"auto",children:[(0,a.jsx)(c.l_,{className:"inline-flex max-h-[16rem] w-[100%] items-start justify-start gap-2 p-2",role:"menu",children:(0,a.jsx)("div",{className:"flex shrink grow basis-0 flex-col items-start justify-start",children:u})}),(0,a.jsx)(c.LW,{className:"h-[100%] w-2",orientation:"vertical",children:(0,a.jsx)(c.bU,{className:"bg-bg-200 rounded-full"})}),(0,a.jsx)(c.Ns,{className:"ScrollAreaCorner"})]}):(0,a.jsx)("div",{className:"flex shrink grow basis-0 flex-col items-start justify-start p-2",children:u})})})})]})}let j=s.q.div(m()),N=s.q.div(x())},63074:function(e,n,t){t.d(n,{o:function(){return u}});var r=t(27573);function a(e){return n=>{e.forEach(e=>{"function"==typeof e?e(n):null!==e&&(e.current=n)})}}var s=t(65517),o=t(57908),l=t(7653),i=t(72459),d=t(58845);let c=(0,s.j)("bg-bg-000\n  border\n  border-border-200\n  hover:border-border-100\n  transition-colors\n  placeholder:text-text-500\n  focus:border-accent-secondary-100\n  focus-within:!border-accent-secondary-100\n  focus:ring-0\n  focus:outline-none\n  disabled:cursor-not-allowed\n  disabled:opacity-50",{variants:{size:{default:"h-9 px-3 py-2 rounded-lg",sm:"h-8 rounded-md px-3 text-xs",lg:"h-11 px-3 rounded-[0.6rem]"},error:{true:"!border-danger-200/50 hover:!border-danger-200/90 focus:!border-danger-200"}},defaultVariants:{size:"default"}}),u=(0,l.forwardRef)((e,n)=>{let{autoFocus:t,className:s,id:u,label:b,secondaryLabel:m,size:x="default",error:p,type:f,value:g,currencySymbol:h="$",labelClassName:v,onChange:y,onValueChange:w,automaticallyFocusAndSelect:j,prepend:N,append:k,..._}=e,z=(0,o.Z)(c({size:x,error:p,className:s}),s),C=(0,d.K)({id:u,label:b}),Z=(0,l.useRef)(null);(0,l.useEffect)(()=>{if(j){var e,n;null===(e=Z.current)||void 0===e||e.focus(),null===(n=Z.current)||void 0===n||n.select()}},[]);let{defaultValue:S,step:V,...F}=_,E="currency"!==f&&!(N||k);return(0,r.jsxs)(r.Fragment,{children:[b&&(0,r.jsx)(d._,{label:b,id:C,className:v}),(N||k)&&(0,r.jsxs)("div",{className:(0,o.Z)(z,"inline-flex cursor-text items-stretch gap-2"),onClick:()=>{var e;return null===(e=Z.current)||void 0===e?void 0:e.focus()},children:[N&&(0,r.jsx)("div",{className:"flex items-center",children:N}),(0,r.jsx)("input",{id:C,autoFocus:t,type:f,className:"w-full placeholder:text-text-500 m-0 bg-transparent p-0 focus:outline-none focus:ring-0 disabled:cursor-not-allowed disabled:opacity-50",ref:a([n,Z]),value:g,onChange:e=>{null==y||y(e),null==w||w(e.target.value)},..._}),k&&(0,r.jsx)("div",{className:(0,o.Z)("flex items-center","default"===x&&"-mr-2","sm"===x&&"-mr-2","lg"===x&&"-mr-1.5"),children:k})]}),"currency"===f&&(0,r.jsx)(i.Z,{id:C,ref:n,autoFocus:t,prefix:h,placeholder:h,className:z,value:g,onValueChange:e=>null==w?void 0:w(e),allowDecimals:!1,...F}),E&&(0,r.jsx)("input",{id:C,autoFocus:t,type:f,className:z,ref:a([n,Z]),value:g,onChange:e=>{null==y||y(e),null==w||w(e.target.value)},..._}),m&&(0,r.jsx)("div",{className:"text-text-400 mt-1 text-sm",children:m})]})});u.displayName="TextInput"},70443:function(e,n,t){t.d(n,{NU:function(){return i},Q:function(){return d.Q},sY:function(){return b},Ph:function(){return m.P},Kx:function(){return f},oi:function(){return g.o}}),t(77508);var r=t(27573),a=t(58845),s=t(64429),o=t(7653);function l(e){return 0===e.length?"Select":1===e.length?"1 item":"".concat(e.length," items")}function i(e){let{labelFn:n=l,options:t,onSelect:a,size:i,type:d}=e,[c,u]=(0,o.useState)(()=>new Set),b=(0,o.useMemo)(()=>Object.fromEntries(t.map(e=>[e.key,e])),[t]),m=(0,o.useMemo)(()=>[...c].map(e=>b[e]),[c,b]);return(0,r.jsx)(s.fC,{label:n(m),avoidCollisions:!1,size:i,type:d,children:t.map(e=>{let{key:n,label:t}=e;return(0,r.jsx)(s.ck,{label:t,onSelect:()=>{let n=new Set(c);n.has(e.key)?n.delete(e.key):n.add(e.key),null==a||a([...n].map(e=>b[e])),u(n)},checkboxStyle:"square",closeOnSelect:!1,checked:c.has(e.key),size:i},n)})})}var d=t(50725),c=t(61756),u=t(57908);let b=e=>{let{size:n="base",options:t,onSelect:a,initialKey:s,testId:l}=e,[i,d]=(0,o.useState)(s);return(0,r.jsx)(c.fC,{type:"single",value:i,className:"bg-bg-300 border-bg-300 inline-flex rounded-full border cursor-pointer",onValueChange:e=>{""!==e&&(d(e),null==a||a(e))},onClick:()=>{if(2===t.length){let e=t.findIndex(e=>e.key===i),n=t[0===e?1:0].key;d(n),null==a||a(n)}},children:t.map(e=>(0,r.jsx)(c.ck,{value:e.key,className:(0,u.Z)('text-text-500 data-[state="on"]:text-text-100 border-0.5 data-[state="on"]:bg-bg-100 data-[state="on"]:border-border-300 flex items-center rounded-full border-transparent font-medium',"sm"===n&&"gap-1 px-2.5 text-xs","md"===n&&"gap-1 py-1 pl-2.5 pr-2.5 text-xs","base"===n&&"gap-1.5 py-2 pl-3 pr-3 text-sm"),"data-testid":"".concat(l,"-").concat(e.key),children:e.label},e.key))})};var m=t(83925),x=t(84921);let p=(0,t(65517).j)("bg-bg-000\n  border\n  border-border-200\n  p-3\n  leading-5\n  rounded-lg\n  transition-colors\n  hover:not-read-only:border-border-100\n  placeholder:text-text-500\n  focus:border-accent-secondary-100\n  focus:ring-0\n  focus:outline-none\n  disabled:cursor-not-allowed\n  disabled:opacity-50\n  read-only:opacity-50\n  whitespace-pre-wrap\n  resize-none\n  row-start-1\n  row-end-2\n  col-start-1\n  col-end-2\n  ",{variants:{},defaultVariants:{}}),f=(0,o.forwardRef)((e,n)=>{let{id:t,className:s,rows:o,minRows:l,label:i,insetLabel:d,value:c,labelClassName:b,error:m,onChange:f,onValueChange:g,customScrollbar:h,...v}=e,y=(0,a.K)({id:t,label:i}),w=(0,u.Z)(p({className:s}),d&&"pt-7",h&&x.X,m&&"!border-danger-200/50 hover:!border-danger-200/90 focus:!border-danger-200");return(0,r.jsxs)("div",{className:"group relative",children:[(0,r.jsx)(()=>i?(0,r.jsx)(a._,{label:i,id:y,className:(0,u.Z)(b,d&&"!text-text-400 absolute left-3 top-2 !text-xs !font-bold")}):null,{}),(0,r.jsxs)("div",{className:"grid",children:[!o&&(0,r.jsx)(()=>(0,r.jsxs)("div",{"aria-hidden":"true",className:(0,u.Z)(w,"pointer-events-none invisible"),children:[c," "]}),{}),(0,r.jsx)("textarea",{id:y,ref:n,className:w,rows:l||o,value:c,onChange:e=>{null==f||f(e),null==g||g(e.target.value)},"data-1p-ignore":!0,...v})]}),m&&"string"==typeof m&&(0,r.jsx)("div",{className:"bg-danger-100 text-oncolor-100 absolute bottom-0 right-0 rounded-ee-lg rounded-ss-md px-1.5 py-1 text-right text-xs font-medium",children:m})]})});f.displayName="TextArea";var g=t(63074)},84921:function(e,n,t){t.d(n,{X:function(){return r}});let r="\n  overflow-x-visible\n  overflow-y-auto\n  scroll-pb-6\n  min-h-[0px]\n  [scrollbar-color:hsl(var(--text-500))]\n  scroll-smooth\n  overscroll-contain\n  [-webkit-overflow-scrolling:touch]\n  [&::-webkit-scrollbar]:mt-4\n  [&::-webkit-scrollbar]:w-[0.25rem]\n  [&::-webkit-scrollbar-track]:bg-transparent\n  [&::-webkit-scrollbar-track]:my-1\n  [&::-webkit-scrollbar-thumb]:rounded-[1em]\n  [&::-webkit-scrollbar-thumb]:border-[0.25rem]\n  [&::-webkit-scrollbar-thumb]:border-transparent\n  [&::-webkit-scrollbar-thumb]:bg-clip-padding\n  [&::-webkit-scrollbar-thumb]:bg-text-500/80\n  [&::-webkit-scrollbar-thumb:hover]:bg-text-500\n  [&.has-bottom-scroll]:[mask-image:linear-gradient(to_top,rgba(0,0,0,0)_0%,_rgba(0,0,0,1)_3%)]\n  "},82880:function(e,n,t){t.d(n,{q:function(){return o}});var r=t(57908),a=t(7653);function s(e){return function(n){for(var t=arguments.length,s=Array(t>1?t-1:0),o=1;o<t;o++)s[o-1]=arguments[o];let l=n.map(e=>e.replace(/\n/g,"").trim()),i=a.forwardRef((n,t)=>{let{className:o,...i}=n,d=s.map(e=>"function"==typeof e?e(n):e);return a.createElement(e,{...i,ref:t,className:(0,r.Z)(l,d,"string"==typeof o?o:"")})});return i.displayName="string"==typeof e?e:e.displayName,i}}function o(e){return s(e)}o.a=s("a"),o.aside=s("aside"),o.button=s("button"),o.main=s("main"),o.div=s("div"),o.form=s("form"),o.nav=s("nav"),o.fieldset=s("fieldset"),o.header=s("header"),o.h1=s("h1"),o.h2=s("h2"),o.h3=s("h3"),o.h4=s("h4"),o.h5=s("h5"),o.th=s("th"),o.td=s("td"),o.input=s("input"),o.label=s("label"),o.p=s("p"),o.section=s("section"),o.span=s("span"),o.li=s("li")},11096:function(e,n,t){t.d(n,{z:function(){return c}});var r=t(27573),a=t(41464),s=t(65517),o=t(57908),l=t(87659),i=t(7653);let d=(0,s.j)("inline-flex\n  items-center\n  justify-center\n  relative\n  shrink-0\n  ring-offset-2\n  ring-offset-bg-300\n  ring-accent-main-100\n  focus-visible:outline-none\n  focus-visible:ring-1\n  disabled:pointer-events-none\n  disabled:opacity-50\n  disabled:shadow-none\n  disabled:drop-shadow-none",{variants:{variant:{primary:"\n          bg-accent-main-100\n          bg-gradient-to-r\n          from-accent-main-100\n          via-accent-main-200/50\n          to-accent-main-200\n          bg-[length:200%_100%]\n          hover:bg-right\n          active:bg-accent-main-000\n          border-0.5\n          border-border-300\n          text-oncolor-100\n          font-medium\n          font-styrene\n          drop-shadow-sm\n          transition-all\n          shadow-[inset_0_0.5px_0px_rgba(255,255,0,0.15)]\n          [text-shadow:_0_1px_2px_rgb(0_0_0_/_10%)]\n          active:shadow-[inset_0_1px_6px_rgba(0,0,0,0.2)]\n          hover:from-accent-main-200\n          hover:to-accent-main-200",flat:"bg-accent-main-100\n          text-oncolor-100\n          font-medium\n          font-styrene\n          transition-colors\n          hover:bg-accent-main-200",secondary:"\n          bg-[radial-gradient(ellipse,_var(--tw-gradient-stops))]\n          from-bg-500/10\n          from-50%\n          to-bg-500/30\n          border-0.5\n          border-border-400\n          font-medium\n          font-styrene\n          text-text-100/90\n          transition-colors\n          active:bg-bg-500/50\n          hover:text-text-000\n          hover:bg-bg-500/60",outline:"border-1.5\n          font-medium\n          font-styrene\n          bg-transparent\n          text-text-200\n          transition-colors\n          hover:text-text-100\n          hover:bg-bg-400\n          hover:border-bg-400",ghost:"text-text-200\n          border-transparent\n          transition-colors\n          font-styrene\n          active:bg-bg-400\n          hover:bg-bg-500/40\n          hover:text-text-100",underline:"opacity-80\n          transition-all\n          active:scale-[0.985]\n          hover:opacity-100\n          hover:underline\n          underline-offset-3",danger:"bg-danger-100\n          text-oncolor-100\n          font-medium\n          font-styrene\n          transition-colors\n          hover:bg-danger-200",unstyled:""},size:{default:"h-9 px-4 py-2 rounded-lg min-w-[5rem] active:scale-[0.985] whitespace-nowrap",sm:"h-8 rounded-md px-3 text-xs min-w-[4rem] active:scale-[0.985] whitespace-nowrap",lg:"h-11 rounded-[0.6rem] px-5 min-w-[6rem] active:scale-[0.985] whitespace-nowrap",icon:"h-9 w-9 rounded-md active:scale-95 shrink-0",icon_xs:"h-6 w-6 rounded-md active:scale-95",icon_sm:"h-8 w-8 rounded-md active:scale-95",icon_lg:"h-11 w-11 rounded-[0.6rem] active:scale-95",inline:"px-0.5 rounded-[0.25rem]",unset:""},option:{rounded:"!rounded-full",prepend:"",append:""},state:{active:""}},compoundVariants:[{size:"default",option:"prepend",class:"pl-2 pr-3 gap-1"},{size:"lg",option:"prepend",class:"pl-2.5 pr-3.5 gap-1"},{size:"sm",option:"prepend",class:" pl-2 pr-2.5 gap-1"},{size:"default",option:"append",class:"pl-3 pr-2 gap-1"},{size:"lg",option:"append",class:"pl-3.5 pr-2.5 gap-1"},{size:"sm",option:"append",class:"pl-2.5 pr-2 gap-1"},{variant:"ghost",state:"active",class:"!bg-bg-400"}],defaultVariants:{variant:"primary",size:"default"}}),c=(0,i.forwardRef)((e,n)=>{let{className:t,variant:s,size:i,option:c,loading:u,href:b,target:m,prepend:x,append:p,state:f,disabled:g,children:h,type:v="button",...y}=e;x&&(c="prepend"),p&&(c="append");let w=(0,o.Z)(d({variant:s,size:i,option:c,state:f,className:t}),u&&"text-transparent ![text-shadow:_none]"),j=(0,r.jsxs)(r.Fragment,{children:[u&&(0,r.jsx)("div",{className:(0,o.Z)("absolute inset-0 flex items-center justify-center",s&&"primary"!==s&&"flat"!==s&&"danger"!==s?"text-text-200":"text-oncolor-100"),children:(0,r.jsx)(a.g,{size:"sm",inheritColor:!0})}),x,h,p]});return b?(0,r.jsx)(l.default,{href:b,target:m||"_self",className:w,"aria-label":y["aria-label"],children:j}):(0,r.jsx)("button",{className:w,ref:n,disabled:g||u,type:v,...y,children:j})});c.displayName="Button"},41464:function(e,n,t){t.d(n,{g:function(){return s}});var r=t(27573),a=t(57908);let s=(0,t(7653).memo)(function(e){let{size:n="md",fullscreen:t=!1,inheritColor:s}=e;return(0,r.jsx)("div",{className:(0,a.Z)(t?"fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2":"m-auto"),children:(0,r.jsx)("div",{className:(0,a.Z)("sm"===n&&"h-4 w-4 border-2","md"===n&&"h-20 w-20 border-8",s?"border-current":"border-border-200","text-secondary inline-block animate-spin rounded-full border-solid border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"),role:"status",children:(0,r.jsx)("span",{className:"sr-only",children:"Loading..."})})})})}}]);