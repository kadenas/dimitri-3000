"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[8930],{5990:function(e,t,s){s.d(t,{H:function(){return r}});var n=s(27573),i=s(17886),a=s(87659),l=s(93124);function r(e){let{children:t}=e;return(0,n.jsx)(i.u,{tooltipContent:(0,n.jsxs)("div",{className:"max-w-48 p-1",children:[(0,n.jsx)("p",{className:"mb-2 whitespace-break-spaces text-xs tracking-tight",children:(0,n.jsx)(l.Z,{defaultMessage:"This is an example project. Create a new project to work with your own documents.",id:"aod9/juMdU"})}),(0,n.jsx)(a.default,{href:"/projects/create",className:"text-accent-secondary-200 text-xs tracking-tight",children:(0,n.jsx)(l.Z,{defaultMessage:"Create new project",id:"a7FtAnfVfj"})})]}),children:t})}},52433:function(e,t,s){s.d(t,{W:function(){return h}});var n=s(27573),i=s(24658),a=s(70443),l=s(11096),r=s(74651),o=s(44846),d=s(87659),c=s(7653),u=s(91237),g=s(93124),x=s(27957);function h(e){let{isOpen:t,onClose:s,project:h}=e,m=(0,u.Z)(),[f,p]=(0,c.useState)(h.prompt_template),[j,v]=(0,c.useState)(!1),{value:y}=(0,o.F)("claudeai_custom_styles"),{value:w}=(0,o.F)("claude_ai_cayenne"),{addError:b}=(0,i.e)(),{mutateAsync:N}=(0,x.dY)(h.uuid),M=async()=>{v(!0);try{await N({prompt_template:f}),s(),v(!1)}catch(e){b(m.formatMessage({defaultMessage:"Error saving instructions, please try again later",id:"WL3FdCcP2y"})),v(!1)}},S=h.prompt_template.length>0&&0===f.length,C=w?(0,n.jsx)(g.Z,{defaultMessage:"This will work alongside <link>user preferences</link> and the selected style in a chat.",values:{link:e=>(0,n.jsx)(d.default,{className:"hover:underline",href:"/settings/profile",children:e})},id:"NlixH3av58"}):(0,n.jsx)(g.Z,{defaultMessage:"This will work alongside the selected style in a chat.",id:"rptxrPz/Y3"});return(0,n.jsxs)(r.u_,{isOpen:t,onClose:s,modalSize:"lg",children:[(0,n.jsxs)("div",{className:"flex flex-col gap-1",children:[(0,n.jsx)("h2",{className:"font-styrene-display text-xl font-medium",children:(0,n.jsx)(g.Z,{defaultMessage:"Set project instructions",id:"+On7CFwfGv"})}),(0,n.jsxs)("p",{className:"text-text-300 text-sm",children:[(0,n.jsx)(g.Z,{defaultMessage:"Provide Claude with relevant instructions and information for chats within {projectName}.",id:"NM6ePuQ0y+",values:{projectName:h.name}}),"\xa0",y&&C]})]}),(0,n.jsx)("div",{className:"mb-6 mt-3",children:(0,n.jsx)(a.Kx,{value:f,onChange:e=>p(e.target.value),placeholder:m.formatMessage({defaultMessage:"Think step by step and show reasoning for complex problems. Use specific examples.",id:"j554E3Ar1K"})+"\n\n"+m.formatMessage({defaultMessage:"Break down large tasks and ask clarifying questions when needed.",id:"H/tJ47E9to"})+"\n\n"+m.formatMessage({defaultMessage:"Use Artifacts only for web apps and code demos.",id:"U50hIJOW7M"})+"\n\n"+m.formatMessage({defaultMessage:"When giving feedback, explain thought process and highlight issues and opportunities.",id:"f2YGj7vTV3"}),minRows:8,required:!0,customScrollbar:!0,className:"max-h-60"})}),(0,n.jsxs)("div",{className:"mt-2 flex justify-end gap-2",children:[(0,n.jsx)(l.z,{variant:"secondary",onClick:s,children:(0,n.jsx)(g.Z,{defaultMessage:"Cancel",id:"47FYwba+bI"})}),(0,n.jsx)(l.z,{loading:j,disabled:h.prompt_template===f,onClick:()=>{M()},children:S?(0,n.jsx)(g.Z,{defaultMessage:"Clear Instructions",id:"irlLU/gWty"}):(0,n.jsx)(g.Z,{defaultMessage:"Save Instructions",id:"ctY95GUX+w"})})]})]})}},69576:function(e,t,s){s.d(t,{U:function(){return J}});var n=s(27573),i=s(24658),a=s(11096),l=s(12068),r=s(99694),o=s(71473),d=s(98599),c=s(62124),u=s(3095),g=s(7653),x=s(93124),h=s(48970),m=s(6274),f=s(86825),p=s(48814),j=s(17886),v=s(95166),y=s(11050),w=s(57908),b=s(82177),N=s(91237);let M=e=>{let{file:t,canEditKnowledgeBase:s,isLoading:i,deleteFile:l,shouldHideDeleteButton:r,relativeFileLength:o,compressButton:d}=e,c=(0,N.Z)(),u="created_at"in t?t.created_at:null;return(0,n.jsxs)("div",{className:(0,w.Z)("group flex items-center gap-2 rounded-lg py-0.5 transition-colors lg:-ml-1.5 lg:-mr-1 lg:p-1",s&&"lg:hover:bg-bg-300"),children:[(0,n.jsx)(f.mB,{file:t,size:"xs"}),(0,n.jsxs)("div",{className:"min-w-0 flex-1",children:[(0,n.jsx)("div",{className:"mb-0.5 mt-1 line-clamp-1 break-all text-sm",children:(0,f.a9)(t.file_name)}),(0,n.jsxs)("div",{className:"text-text-400 flex items-center gap-1 text-xs",children:[!!u&&(0,n.jsx)(p.i,{datetime:b.ou.fromISO(u),locale:c.locale}),!!o&&(0,n.jsxs)(n.Fragment,{children:[!!u&&(0,n.jsx)(n.Fragment,{children:(0,n.jsx)("span",{className:"text-text-500/50 text-[6px]",children:"•"})}),o]})]})]}),s&&(0,n.jsx)("div",{className:(0,w.Z)("transition-opacity group-has-[:focus-visible]/row:opacity-100 group-hover:opacity-100",i?"opacity-100":"lg:opacity-0"),children:i?(0,n.jsx)(v.U,{className:"animate-spin",size:18}):(0,n.jsxs)("div",{className:(0,w.Z)("transition-opacity",r?"opacity-0":"opacity-100"),children:[d,(0,n.jsx)(j.u,{tooltipContent:c.formatMessage({defaultMessage:"Remove",id:"G/yZLul6P1"}),children:(0,n.jsx)(a.z,{size:"icon_sm",variant:"ghost",disabled:i||r,onClick:l,"aria-label":c.formatMessage({defaultMessage:"Remove from project knowledge",id:"eRF6oJ+Cb5"}),children:(0,n.jsx)(y.r,{size:16})})})]})})]})},S=e=>{let{doc:t,canEditKnowledgeBase:s,shouldHideDeleteButton:i=!1,compressButton:a}=e,{mutate:l,isPending:r}=(0,h.ER)(t.project_uuid),o=(0,g.useMemo)(()=>(function(e){let t={2e4:"Large file",6e4:"Very large file"},s=e.length,n=Object.keys(t).reverse();for(let e=0;e<n.length;e++)if(s>parseInt(n[e]))return t[n[e]]})(t.content),[t]),d=(0,g.useMemo)(()=>new TextEncoder().encode(t.content).length,[t]);return(0,n.jsx)(M,{file:{created_at:t.created_at,file_name:t.file_name,file_size:d,file_type:"",extracted_content:t.content},canEditKnowledgeBase:s,isLoading:r,shouldHideDeleteButton:i,relativeFileLength:o,deleteFile:()=>l({docUuid:t.uuid}),compressButton:a})},C=e=>{let{file:t,projectUuid:s,canEditKnowledgeBase:i,shouldHideDeleteButton:a=!1}=e,{mutate:l,isPending:r}=(0,h.h4)(s);return(0,n.jsx)(M,{file:t,canEditKnowledgeBase:i,isLoading:r,shouldHideDeleteButton:a,deleteFile:()=>l({file_uuids:[t.file_uuid]})})};var k=s(33435),E=s(55722),U=s(2906),Z=s(50513),_=s(76009),D=s(62973),I=s(72500),z=s(96100),F=s(958),P=s(23428),T=s(35934),A=s(57385),O=s(13143),L=s(85285),G=s(84001),R=s(13789);function B(e){let{uri:t,isError:s,isLink:i=!1}=e;return(0,n.jsx)(G.$,{uri:t,isError:s,isLink:i,useDocumentHook:P.gQ,getDocumentUrl:R.v,defaultErrorTitle:"Outline"})}var H=s(65291);function K(e){let{projectUuid:t,syncSource:s,isActionsHidden:i,canEditKnowledgeBase:a}=e,l=(0,T.mo)(),[o,d]=(0,g.useState)(!1),{type:c,status:{state:u,current_file_count:h},config:m}=s,f=(0,_.ir)(u);return(0,n.jsxs)("div",{className:(0,w.Z)("group flex flex-row items-center gap-2 rounded-lg px-0  lg:-ml-1.5 lg:-mr-1 lg:p-1 transition relative",a&&"lg:hover:bg-bg-300"),children:[(0,n.jsxs)("div",{className:"flex-1 inline-flex items-center gap-2",children:[(0,n.jsx)("div",{className:(0,w.Z)("relative inline-flex items-center shrink-0 justify-center h-10 w-10 m-0.5 border-0.5 border-border-300 rounded-lg",a&&"group-hover:border-border-200 group-hover:bg-bg-200"),children:(0,n.jsx)(Z.j0,{type:c,size:24,variant:Z.cT.DOCS,isError:f})}),(0,n.jsxs)("div",{children:[(0,n.jsx)("span",{className:"text-sm line-clamp-1 break-all",children:c===r.Fg.GITHUB?(0,n.jsx)(L.d,{config:m,isError:f}):c===r.Fg.GDRIVE?(0,n.jsx)(A.C,{uri:m.uri,isError:f,isLink:u!==r.co.UNAUTHENTICATED}):c===r.Fg.OUTLINE?(0,n.jsx)(B,{uri:m.outline_uri,isError:f,isLink:u!==r.co.UNAUTHENTICATED}):null}),(0,n.jsxs)("div",{className:"flex flex-row gap-1 text-xs text-text-400",children:[(0,n.jsx)("span",{className:"line-clamp-1",children:(0,n.jsx)(H.w,{syncSource:s})}),!!h&&(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)("span",{className:"text-text-500/50 text-[6px] hidden sm:inline",children:(0,n.jsx)(n.Fragment,{children:"•"})}),(0,n.jsx)("span",{className:"hidden sm:inline",children:(0,n.jsx)(x.Z,{defaultMessage:"{count, plural, one {# file} other {# files}}",id:"Lf81FX5U/k",values:{count:h}})})]})]})]})]}),!i&&(0,n.jsx)(q,{isError:f,canRefresh:s.type===r.Fg.GITHUB,onEdit:s.type===r.Fg.GITHUB?()=>d(!0):void 0,projectUuid:t,syncSource:s}),s.type===r.Fg.GITHUB&&(0,n.jsx)(O.U,{isOpen:o,onClose:()=>d(!1),tokenLimit:l,projectUuid:t,syncSource:s})]})}function q(e){let{isError:t,canRefresh:s,onEdit:l,projectUuid:r,syncSource:o}=e,{mutateAsync:d}=(0,m.zB)(r),c=(0,N.Z)(),{isUpdating:u,isFailing:x,handleUpdate:h}=function(e){let{projectUuid:t,syncSource:s}=e,[n,a]=(0,g.useState)(!1),{addSuccess:l}=(0,i.e)(),r=(0,N.Z)(),{mutate:o}=(0,m.l2)(t,{onSuccess:()=>{l(r.formatMessage({defaultMessage:"Update enqueued",id:"1w/eI79UGE"}))}});(0,g.useEffect)(()=>{a(!1)},[s.status]);let d=(0,P.sf)(s)||n,c=(0,P.xm)(s),u=(0,g.useCallback)(()=>{d||(a(!0),o({sync_source_uuid:s.uuid,sync_source_config:s.config}))},[d,o,s.config,s.uuid]);return{isUpdating:d,isFailing:c,handleUpdate:u}}({projectUuid:r,syncSource:o});return(0,n.jsxs)("div",{className:(0,w.Z)("h-full lg:pl-4 lg:absolute flex items-center lg:pr-2 right-0 rounded-md lg:bg-gradient-to-l from-bg-200 from-80% group-hover:from-bg-300 transition-all lg:opacity-0 group-hover:opacity-100 group-has-[:focus-visible]/row:opacity-100",u&&"lg:opacity-100"),children:[!t&&s&&(0,n.jsx)(j.u,{tooltipContent:u?c.formatMessage({defaultMessage:"Syncing...",id:"S92mvo6R0o"}):x?c.formatMessage({defaultMessage:"Sync failed. Click to retry",id:"zOAqlyzs1U"}):c.formatMessage({defaultMessage:"Sync now",id:"SwsYB/OerA"}),children:(0,n.jsx)(a.z,{variant:"ghost",size:"icon_sm",onClick:h,children:u?(0,n.jsx)(D.t,{className:"animate-spin"}):x?(0,n.jsx)(I.v,{}):(0,n.jsx)(D.t,{})})}),!t&&l&&(0,n.jsx)(j.u,{tooltipContent:c.formatMessage({defaultMessage:"Configure files",id:"rAV3qK0Jqb"}),children:(0,n.jsx)(a.z,{variant:"ghost",size:"icon_sm",onClick:l,children:(0,n.jsx)(z.X,{})})}),(0,n.jsx)(j.u,{tooltipContent:c.formatMessage({defaultMessage:"Remove",id:"G/yZLul6P1"}),children:(0,n.jsx)(a.z,{variant:"ghost",size:"icon_sm",onClick:()=>d(o.uuid),children:(0,n.jsx)(F.r,{})})})]})}s(88075);var V=s(98219);let W="project_syncs",Y="project_docs",X="project_linked_files";function J(e){let{project:t,canEditKnowledgeBase:s=!1,isUploadingDoc:i=!1,isUploadingDriveSync:r=!1,isUploadingOutlineSync:d=!1,isUploadingGithubSync:g=!1,setIsUploadingDoc:h,setIsUploadingDriveSync:m,setIsUploadingOutlineSync:f,setIsUploadingGithubSync:p,maxItems:j,onViewAll:v,onClickProjectDoc:y}=e,{githubSyncSources:w,driveSyncSources:b,outlineSyncSources:N,projectDocs:M,linkedFiles:k,isFetchingKnowledge:E,knowledgeCount:Z}=$({projectUuid:t.uuid,maxItems:j}),{isDeleting:_,selectedItems:D,handleSelect:I,selectAllItems:z,isInSelectionMode:F,toggleSelectMode:P,handleDeleteSelected:T}=ee({githubSyncSources:w,driveSyncSources:b,outlineSyncSources:N,projectDocs:M,linkedFiles:k,projectUuid:t.uuid,isEnabled:s});Q({clearUploadingState:()=>null==h?void 0:h(!1),numItems:M.length+k.length}),Q({clearUploadingState:()=>null==p?void 0:p(!1),numItems:w.length}),Q({clearUploadingState:()=>null==m?void 0:m(!1),numItems:b.length}),Q({clearUploadingState:()=>null==f?void 0:f(!1),numItems:N.length});let A={isInSelectionMode:F,canEditKnowledgeBase:s},O=new Set(D.map(e=>{let{uuid:t}=e;return t}));return E?(0,n.jsx)(l.g,{height:65,className:"opacity-25 rounded-lg mb-3 mt-3"}):0===Z?(0,n.jsx)(et,{canEditKnowledgeBase:s}):(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(c.M,{children:s&&(0,n.jsx)(u.E.div,{initial:{opacity:0,height:0},animate:{opacity:1,height:"auto"},children:(0,n.jsx)(V.n,{projectUuid:t.uuid})})}),(0,n.jsx)("ul",{className:"flex flex-col py-1",children:(0,n.jsxs)(c.M,{initial:!1,children:[(0,n.jsx)(en,{isShown:r},"drive-skeleton-loader"),b.map(e=>(0,n.jsx)(es,{isSelected:O.has(e.uuid),...A,handleSelect:(t,s)=>I({uuid:e.uuid,type:W},t,s),children:(0,n.jsx)(K,{projectUuid:t.uuid,syncSource:e,canEditKnowledgeBase:s,isActionsHidden:F||!s})},e.uuid)),(0,n.jsx)(en,{isShown:d},"outline-skeleton-loader"),N.map(e=>(0,n.jsx)(es,{isSelected:O.has(e.uuid),...A,handleSelect:(t,s)=>I({uuid:e.uuid,type:W},t,s),children:(0,n.jsx)(K,{projectUuid:t.uuid,syncSource:e,canEditKnowledgeBase:s,isActionsHidden:F||!s})},e.uuid)),(0,n.jsx)(en,{isShown:g},"github-skeleton-loader"),w.map(e=>(0,n.jsx)(es,{isSelected:O.has(e.uuid),...A,handleSelect:(t,s)=>I({uuid:e.uuid,type:W},t,s),children:(0,n.jsx)(K,{projectUuid:t.uuid,syncSource:e,canEditKnowledgeBase:s,isActionsHidden:F||!s})},e.uuid)),(0,n.jsx)(en,{isShown:i},"doc-skeleton-loader"),M.map(e=>(0,n.jsx)(es,{isSelected:O.has(e.uuid),...A,handleSelect:(t,s)=>I({uuid:e.uuid,type:Y},t,s),className:y?"cursor-pointer":void 0,handleClick:()=>null==y?void 0:y(e.uuid),children:(0,n.jsx)(S,{doc:e,canEditKnowledgeBase:s,shouldHideDeleteButton:F,compressButton:void 0})},e.uuid)),k.map(e=>(0,n.jsx)(es,{isSelected:O.has(e.file_uuid),...A,handleSelect:(t,s)=>I({uuid:e.file_uuid,type:X},t,s),children:(0,n.jsx)(C,{file:e,projectUuid:t.uuid,canEditKnowledgeBase:s,shouldHideDeleteButton:F})},e.file_uuid)),(0,n.jsx)(c.M,{children:F&&(0,n.jsx)(u.E.div,{initial:{opacity:0,height:0},animate:{opacity:1,height:"auto"},exit:{opacity:0,height:0},className:"ml-auto",children:(0,n.jsx)("div",{className:"flex mt-3 gap-2 justify-end",children:(0,n.jsx)(U.J,{isLoading:_,numSelected:D.length,totalNumItems:Z,handleSelectAll:z,handleCancel:()=>P(!1),handleDeleteSelected:T})})},"item-management-menu")})]})}),!!v&&!!j&&Z>j&&(0,n.jsx)("div",{children:(0,n.jsxs)(a.z,{variant:"unstyled",onClick:v,className:"hover:text-text-000 hover:underline !px-0 text-sm",children:[(0,n.jsx)(x.Z,{defaultMessage:"View all {count} files",id:"b36mSZ46cW",values:{count:Z}}),(0,n.jsx)(o.o,{size:16,className:"inline-block pl-1"})]})})]})}let Q=e=>{let{clearUploadingState:t,numItems:s}=e,n=(0,g.useRef)(s);(0,g.useEffect)(()=>{s>n.current&&t(),n.current=s},[s,t])},$=e=>{let{projectUuid:t,maxItems:s}=e,{data:n=[],isLoading:i}=(0,h.Kf)(t),a=[...n],{data:l=[],isLoading:o}=(0,m.yg)(t),{data:d=[]}=(0,h.pK)(t),c=[...d],u=l.filter(e=>{let{type:t}=e;return t===r.Fg.GDRIVE}),g=l.filter(e=>{let{type:t}=e;return t===r.Fg.OUTLINE}),x=l.filter(e=>{let{type:t}=e;return t===r.Fg.GITHUB});if(s){let e=s;[u,g,x,a,c].forEach(t=>{t.splice(e),e=Math.max(0,e-t.length)})}let f=[a,l,c].reduce((e,t)=>{var s;return e+(null!==(s=null==t?void 0:t.length)&&void 0!==s?s:0)},0);return{driveSyncSources:u,outlineSyncSources:g,githubSyncSources:x,projectDocs:a,linkedFiles:c,isFetchingKnowledge:i||o,knowledgeCount:f}},ee=e=>{let{githubSyncSources:t,driveSyncSources:s,outlineSyncSources:n,projectDocs:a,linkedFiles:l,projectUuid:r,isEnabled:o}=e,d=s.map(e=>{let{uuid:t}=e;return{type:W,uuid:t}}).concat(t.map(e=>{let{uuid:t}=e;return{type:W,uuid:t}})).concat(n.map(e=>{let{uuid:t}=e;return{type:W,uuid:t}})).concat(a.map(e=>{let{uuid:t}=e;return{type:Y,uuid:t}})).concat(l.map(e=>{let{file_uuid:t}=e;return{type:X,uuid:t}})),{selectedItems:c,handleSelect:u,selectAllItems:g,isInSelectionMode:x,toggleSelectMode:f}=(0,k.M)(d,!o),{addError:p}=(0,i.e)(),{mutateAsync:j,isPending:v}=(0,m.IP)(r),{mutateAsync:y,isPending:w}=(0,h.op)(r),{mutateAsync:b,isPending:N}=(0,h.h4)(r),M=async()=>{let e=c.filter(e=>{let{type:t}=e;return t===Y}),t=c.filter(e=>{let{type:t}=e;return t===W}),s=c.filter(e=>{let{type:t}=e;return t===X});f(!1);try{await Promise.all([e.length?y({doc_uuids:e.map(e=>{let{uuid:t}=e;return t})}):Promise.resolve(),t.length?j({sync_source_uuids:t.map(e=>{let{uuid:t}=e;return t})}):Promise.resolve(),s.length?b({file_uuids:s.map(e=>{let{uuid:t}=e;return t})}):Promise.resolve()])}catch(e){p("Something went wrong while deleting. Refresh the page and try again")}};return{isDeleting:w||v||N,selectedItems:c,handleSelect:u,selectAllItems:g,isInSelectionMode:x,toggleSelectMode:f,handleDeleteSelected:M}},et=e=>{let{canEditKnowledgeBase:t}=e;return(0,n.jsxs)("div",{className:"bg-bg-500/10 text-text-400 mb-1 mt-2 flex w-full flex-col items-center gap-3 rounded-lg px-6 pb-10 pt-8 text-center text-sm",children:[(0,n.jsx)(d.g,{size:36,weight:"thin"}),t?(0,n.jsx)(x.Z,{defaultMessage:"No knowledge added yet. Add PDFs, documents, or other text to the project knowledge base that Claude will reference in every project conversation.",id:"j7/C6AKAfW"}):(0,n.jsx)(x.Z,{defaultMessage:"No knowledge added yet.",id:"frsVQgI4+c"})]})};function es(e){let{handleSelect:t,isSelected:s,isInSelectionMode:i,canEditKnowledgeBase:a,className:l,handleClick:r,children:o}=e;return(0,n.jsx)(u.E.li,{initial:{height:0,opacity:0},exit:{height:0,opacity:0},animate:{height:"auto",opacity:1},children:(0,n.jsx)(E.f,{itemName:"content",isSelected:s,checkboxOffset:"-left-4",isInSelectionMode:i,hiddenAndDisabled:!a,handleSelect:t,children:(0,n.jsx)("div",{className:l,onClick:r,children:o})})})}function en(e){let{isShown:t}=e;return t?(0,n.jsx)(u.E.li,{className:"flex items-center overflow-hidden",initial:{height:0,opacity:0},animate:{height:"3rem",opacity:1},children:(0,n.jsxs)("div",{className:"flex flex-row items-center gap-2 w-full",children:[(0,n.jsx)(l.g,{className:"opacity-25 rounded-lg h-48 shrink-0",height:40,width:40}),(0,n.jsxs)("div",{className:"flex flex-col w-full gap-1",children:[(0,n.jsx)(l.g,{className:"opacity-25 rounded-lg",height:12,width:"50%"}),(0,n.jsx)(l.g,{className:"opacity-25 rounded-lg",height:12,width:"90%"})]})]})},0):null}},98219:function(e,t,s){s.d(t,{n:function(){return G},l:function(){return F}});var n=s(27573),i=s(98635),a=s(49456),l=s(88075),r=s(24658),o=s(70443),d=s(11096),c=s(61814),u=s(74651),g=s(17886),x=s(50513),h=s(84115),m=s(49793),f=s(99694),p=s(84344),j=s(47787),v=s(95014),y=s(90067),w=s(72834),b=s(26821),N=s(57908),M=s(7653),S=s(91237),C=s(93124),k=s(48970),E=s(27957),U=s(23428),Z=s(35934),_=s(5990),D=s(40047),I=s(13143),z=s(64965);s(12068),s(6274);let F=e=>{let{projectUuid:t,isStarterProject:s,isUploading:o,setIsUploadingDoc:d,setIsUploadingGithubSync:c,setIsUploadingDriveSync:u,setIsUploadingOutlineSync:g}=e,{activeOrganization:x}=(0,l.t)(),h=null==x?void 0:x.uuid,f=(0,S.Z)(),p=(0,M.useRef)(null),[j,v]=(0,M.useState)(""),[y,w]=(0,M.useState)(""),[N,_]=(0,M.useState)(!1),[D,z]=(0,M.useState)(!1),[F,T]=(0,M.useState)(!1),{addError:A}=(0,r.e)(),{mutateAsync:O}=(0,k.u3)(t,{onError:()=>d(!1)}),{data:G}=(0,E.Yc)(t),{isGithubAuthenticated:R,initGithubAuth:B}=(0,U.Yn)({callerIdentifier:"project",toggleGithubModalOpen:z}),H=(0,U.P8)(),{isOutlineAuthenticated:K}=(0,U.vc)(),q=(0,U.J$)(),V=(0,U.E4)(),W=(0,Z.nR)(t),Y=(0,Z.mo)(),X=(null!=W?W:0)>Y,J=(0,b.useQueryClient)(),Q=(0,M.useCallback)(async(e,s)=>{for(let t of e)await O({file_name:t.file_name,content:t.extracted_content});s.length&&J.invalidateQueries({queryKey:[m.jb,{orgUuid:h,projectUuid:t}]})},[O,h,t,J]),$=(0,a.eh)(),{handleUpload:ee}=(0,i.Vn)({imagesEnabled:!1,blobFileUploadsEnabled:$,rasterizePdfUploadsEnabled:!1,onUploadComplete:async function(){for(var e=arguments.length,t=Array(e),s=0;s<e;s++)t[s]=arguments[s];await Q(...t)},onError:()=>{d(!1)},projectUuid:t}),et=(0,M.useCallback)(async e=>{let t=e.target.files;t&&(d(!0),await ee(Array.from(t),Y-(null!=W?W:0)),d(!1)),e.target.value=""},[ee,d,W,Y]),es=async()=>{try{_(!1),d(!0),await O({file_name:y,content:j}),w(""),v("")}catch(e){d(!1),A(f.formatMessage({defaultMessage:"Error saving text content",id:"9U64gLEIVo"}))}};return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)("input",{"data-testid":"project-doc-upload",ref:p,type:"file",className:"hidden",accept:(0,a.tB)({imagesEnabled:!1,outOfContextFilesEnabled:$}).join(","),onChange:et,multiple:!0}),(0,n.jsx)(P,{projectUuid:t,shouldShowGithubSyncSource:H,shouldShowDriveSyncSource:V,shouldShowOutlineSyncSource:q,handleGithubClick:()=>{if(R){z(!0);return}B()},handleOutlineClick:()=>{K?T(!0):A((0,n.jsxs)("div",{className:"flex flex-col items-start",children:[(0,n.jsx)("div",{children:(0,n.jsx)(C.Z,{defaultMessage:"You need to connect to Outline before using this feature.",id:"PejG+e4wN5"})}),(0,n.jsx)("button",{onClick:()=>{window.location.href="/settings/profile"},className:"mt-2 underline",children:(0,n.jsx)(C.Z,{defaultMessage:"Connect to Outline",id:"m1DuTWXorQ"})})]}))},handleFileUploadClick:()=>{p.current&&p.current.click()},handleTextContentClick:()=>_(!0),isPrivateProject:!!(null==G?void 0:G.is_private),isStarterProject:s,isOverProjectKnowledgeLimit:X,isLoading:o,setIsUploadingDriveSync:u}),(0,n.jsx)(L,{isOpen:N,onClose:()=>_(!1),title:y,setTitle:w,content:j,setContent:v,onSave:es}),H&&(0,n.jsx)(I.U,{isOpen:D,onClose:()=>z(!1),projectUuid:t,tokenLimit:Y,setIsUploadingGithubSync:c}),q&&""]})},P=e=>{let{projectUuid:t,shouldShowGithubSyncSource:s,shouldShowDriveSyncSource:i,handleGithubClick:a,handleFileUploadClick:l,handleTextContentClick:r,isPrivateProject:o,isStarterProject:d,isOverProjectKnowledgeLimit:u,isLoading:g,shouldShowOutlineSyncSource:x,handleOutlineClick:h,setIsUploadingDriveSync:m}=e,[j,v]=(0,M.useState)(!1),[w,b]=(0,M.useState)(!1),N=i||s,{isDriveAuthenticated:S,initDriveAuth:k,handleDriveTrigger:E,shouldShowDriveSearchEnablementModal:Z}=(0,U.nC)({callerIdentifier:"project",handleAuthSuccess:e=>{v(e),e?setTimeout(()=>{b(e)},100):b(e)}}),_=S&&o&&!Z;return(0,n.jsxs)(c.Lt,{align:"end",unstyledTrigger:!0,trigger:(0,n.jsx)(T,{isStarterProject:d,isOverProjectKnowledgeLimit:u,isLoading:g}),open:j,onOpenChange:v,children:[(0,n.jsx)(c.hP,{onClick:l,className:"text-left",children:(0,n.jsxs)("div",{className:"flex items-center gap-2",children:[(0,n.jsx)(y.p,{size:16}),(0,n.jsx)(C.Z,{defaultMessage:"Upload from device",id:"vMaZk5Jcnv"})]})}),(0,n.jsx)(c.hP,{onClick:r,className:"text-left",children:(0,n.jsxs)("div",{className:"flex items-center gap-2",children:[(0,n.jsx)(p.P,{size:16}),(0,n.jsx)(C.Z,{defaultMessage:"Add text content",id:"G7XW3Mvn8X"})]})}),N?(0,n.jsx)(c.u2,{}):null,s&&(0,n.jsx)(A,{type:f.Fg.GITHUB,isPrivateProject:o,onClick:a}),i&&(0,n.jsx)(O,{projectUuid:t,isPrivateProject:o,setIsUploadingDriveSync:m,isOpen:w,setIsOpen:b,closeWholeDropdown:()=>{b(!1),v(!1)},showGoogleDriveSubDropdown:_,handleGoogleDriveButtonClick:()=>{!_&&o&&(S?E():k())}}),x&&(0,n.jsx)(A,{type:f.Fg.OUTLINE,isPrivateProject:o,onClick:h})]})},T=(0,M.forwardRef)((e,t)=>{let{isStarterProject:s,isOverProjectKnowledgeLimit:i,isLoading:a,...l}=e,r=(0,n.jsx)(d.z,{...l,ref:t,className:"!text-accent-secondary-100 gap-1.5 !rounded-lg flex items-center -mr-2 px-2 py-1 text-sm font-medium tracking-tight",variant:"ghost",size:"inline",disabled:s||i||a,loading:a,prepend:(0,n.jsx)(j.v,{size:16,weight:"bold"}),children:(0,n.jsx)(C.Z,{defaultMessage:"Add Content",id:"66s1201qd9"})});return s?(0,n.jsx)(_.H,{children:(0,n.jsx)("div",{children:r})}):i?(0,n.jsx)(g.u,{side:"bottom",tooltipContent:(0,n.jsx)(C.Z,{defaultMessage:"Project knowledge at capacity. Remove an existing file in order to add to knowledge",id:"g3hx72ya32"}),children:(0,n.jsx)("div",{children:r})}):r});T.displayName="ProjectDocUploaderDropdownTrigger";let A=e=>{let{type:t,isPrivateProject:s,isSubTrigger:i=!1,isSubDropdownOpen:a=!1,onClick:l}=e,r=i?c.WR:c.hP,o=(0,n.jsxs)(r,{onClick:l,onPointerLeave:e=>{i&&a&&e.preventDefault()},onPointerMove:e=>{i&&a&&e.preventDefault()},disabled:!s,className:"text-left",children:[(0,n.jsxs)("div",{className:"flex items-center gap-2",children:[(0,n.jsx)(x.j0,{type:t,size:16}),(0,D.DH)(t)]}),i&&(0,n.jsx)(v.T,{size:16})]});return s?o:(0,n.jsx)(g.u,{side:"left",tooltipContent:(0,n.jsx)(C.Z,{defaultMessage:"Only accessible from private projects",id:"lNrma+LwGe"}),children:(0,n.jsx)("div",{children:o})})},O=e=>{let{projectUuid:t,isPrivateProject:s,setIsUploadingDriveSync:i,isOpen:a,setIsOpen:l,closeWholeDropdown:r,showGoogleDriveSubDropdown:o,handleGoogleDriveButtonClick:d}=e;return o?(0,n.jsxs)(c.Vy,{open:a,onOpenChange:l,children:[(0,n.jsx)(A,{type:f.Fg.GDRIVE,isPrivateProject:s,isSubTrigger:!0,isSubDropdownOpen:a}),(0,n.jsx)(c.nI,{children:(0,n.jsx)(z.C,{projectUuid:t,isSubDropdown:!0,setIsUploadingDriveSync:i,isOpen:a,setIsOpen:l,closeWholeDropdown:r,shouldAddSyncUponPaste:!0})})]}):(0,n.jsx)(A,{type:f.Fg.GDRIVE,isPrivateProject:s,onClick:d})},L=e=>{let{isOpen:t,onClose:s,title:i,setTitle:a,content:l,setContent:r,onSave:c}=e,g=(0,S.Z)(),x=(0,M.useRef)(null);return(0,h.pp)({shouldFocus:t,target:x}),(0,n.jsx)(u.u_,{isOpen:t,onClose:s,modalSize:"xl",className:"p-7 pt-6",children:(0,n.jsxs)("form",{onSubmit:e=>{e.preventDefault(),""!==i.trim()&&""!==l.trim()&&c()},children:[(0,n.jsx)("h2",{className:"font-tiempos mb-3 text-xl",children:(0,n.jsx)(C.Z,{defaultMessage:"Add text content",id:"G7XW3Mvn8X"})}),(0,n.jsx)(o.oi,{ref:x,placeholder:g.formatMessage({defaultMessage:"Name your content",id:"C7Sx4g/l21"}),className:"mb-2 w-full",size:"lg",label:(0,n.jsx)(C.Z,{defaultMessage:"Title",id:"9a9+wwWy4u"}),value:i,onChange:e=>a(e.target.value),required:!0}),(0,n.jsx)(o.Kx,{placeholder:g.formatMessage({defaultMessage:"Type or paste in content...",id:"f5RDuqxeT2"}),label:g.formatMessage({defaultMessage:"Content",id:"Jq3FDzj0/T"}),minRows:12,value:l,onChange:e=>r(e.target.value),required:!0,className:"max-h-[50vh] overflow-y-auto"}),(0,n.jsxs)("div",{className:"mt-4 flex justify-end gap-2",children:[(0,n.jsx)(d.z,{variant:"secondary",onClick:e=>{e.preventDefault(),s()},children:(0,n.jsx)(C.Z,{defaultMessage:"Cancel",id:"47FYwba+bI"})}),(0,n.jsx)(d.z,{type:"submit",children:(0,n.jsx)(C.Z,{defaultMessage:"Add Content",id:"66s1201qd9"})})]})]})})},G=e=>{let{size:t="default",projectUuid:s,tooltipContent:i}=e,a=(0,Z.nR)(s),l=(0,Z.mo)();if(!a)return null;let r=Math.ceil(a/l*100),o=r>80&&r<100,c=r>=100;return(0,n.jsxs)("div",{className:(0,N.Z)("default"===t?"mt-3":"flex items-center gap-3"),children:[(0,n.jsx)("div",{className:(0,N.Z)("bg-bg-300 rounded-full p-0.5","small"===t&&"w-24"),children:(0,n.jsx)("div",{style:{width:"".concat(Math.min(100,r),"%")},className:(0,N.Z)("h-1 rounded-full transition-all",!o&&!c&&"bg-accent-secondary-100",o&&"bg-warning-orange",c&&"bg-danger-100")})}),(0,n.jsxs)("div",{className:(0,N.Z)("flex gap-2 items-center text-xs","default"===t&&"mt-2"),children:[(0,n.jsx)("div",{className:(0,N.Z)("flex-1",r<100&&"text-text-400",r>=100&&"text-danger-100 font-medium"),children:(0,n.jsx)(C.Z,{defaultMessage:"{pctUsed}% of knowledge capacity used",id:"2JyXZfrx4Q",values:{pctUsed:r}})}),(0,n.jsx)(g.u,{className:"text-center mt-0.5",side:"left",tooltipContent:null!=i?i:(0,n.jsx)(C.Z,{defaultMessage:"Project knowledge is currently limited to Claude's maximum context window size.",id:"zmLdyOeio5"}),children:(0,n.jsx)("div",{className:"flex items-center",children:(0,n.jsx)(d.z,{size:"unset",variant:"ghost",href:"https://support.anthropic.com/en/articles/9517075-what-are-projects",target:"_blank",className:"rounded-full",children:(0,n.jsx)(w.k,{size:16})})})})]}),r>=100&&(0,n.jsx)("div",{className:"text-text-400 text-xs",children:(0,n.jsx)(C.Z,{defaultMessage:"Remove an existing file in order to add to knowledge",id:"mSQjDnX2IA"})})]})}},40047:function(e,t,s){s.d(t,{DH:function(){return i}});var n=s(99694);let i=e=>{switch(e){case n.Fg.GITHUB:return"GitHub";case n.Fg.GDRIVE:return"Google Drive";case n.Fg.OUTLINE:return"Outline"}}},33435:function(e,t,s){s.d(t,{M:function(){return i}});var n=s(7653);let i=(e,t)=>{let[s,i]=(0,n.useState)(!1),[a,l]=(0,n.useState)([]),r=(s,n)=>{t||l(t=>{if(!n||0===Object.keys(t).length)return[...t,s];let i=t[Object.keys(t).length-1],a=e.findIndex(e=>{let{uuid:t,type:s}=e;return t===i.uuid&&s===i.type});if(-1===a)return[...t,s];let l=e.findIndex(e=>{let{uuid:t}=e;return t===s.uuid}),r=e.slice(Math.min(a+1,l),Math.max(a-1,l)+1),o=t.map(e=>{let{uuid:t}=e;return t});return[...t,...r.filter(e=>{let{uuid:t}=e;return -1===o.indexOf(t)})]})},o=e=>{t||l(t=>t.filter(t=>{let{uuid:s,type:n}=t;return s!==e.uuid||n!==e.type}))};return(0,n.useEffect)(()=>{i(a.length>0)},[a]),{selectedItems:a,handleSelect:(e,s,n)=>{t||(s?r(e,n):o(e))},selectAllItems:()=>{t||l(e)},isInSelectionMode:!t&&s,toggleSelectMode:e=>{i(e),e||l([])}}}},55722:function(e,t,s){s.d(t,{f:function(){return r}});var n=s(27573),i=s(77508),a=s(17886),l=s(57908);function r(e){let{itemName:t,isInSelectionMode:s,isSelected:r,handleSelect:o,checkboxOffset:d,children:c,hiddenAndDisabled:u=!1}=e;return(0,n.jsxs)("div",{className:"relative group/row",children:[u?null:(0,n.jsx)("div",{className:(0,l.Z)("p-1 absolute z-10 top-1/2 -translate-y-1/2 -translate-x-1/2 transition duration-100 ",d,!s&&" opacity-0 scale-75 group-has-[:focus-visible]/row:opacity-100 group-has-[:focus-visible]/row:scale-100 group-hover/row:opacity-100 group-hover/row:scale-100"),children:(0,n.jsx)(a.u,{tooltipContent:r?"Deselect ".concat(t):"Select ".concat(t),className:"pointer-events-none",children:(0,n.jsx)("div",{children:(0,n.jsx)(i.X,{disabled:u,checked:r,onChange:o,label:"Select ".concat(t),hideLabel:!0})})})}),c]})}},2906:function(e,t,s){s.d(t,{J:function(){return l}});var n=s(27573),i=s(11096);s(7653);var a=s(93124);let l=e=>{let{isLoading:t,numSelected:s,totalNumItems:l,handleSelectAll:r,handleCancel:o,handleDeleteSelected:d}=e;return(0,n.jsxs)(n.Fragment,{children:[s<l&&(0,n.jsx)(i.z,{variant:"underline",className:"text-sm rounded-md text-accent-secondary-000 mr-2 !opacity-100 h-8",size:"unset",onClick:r,children:(0,n.jsx)(a.Z,{defaultMessage:"Select all",id:"94Fg25VD0N"})}),(0,n.jsx)(i.z,{size:"sm",variant:"secondary",onClick:o,children:(0,n.jsx)(a.Z,{defaultMessage:"Cancel",id:"47FYwba+bI"})}),(0,n.jsx)(i.z,{size:"sm",variant:"danger",disabled:0===s,onClick:d,loading:t,children:(0,n.jsx)(a.Z,{defaultMessage:"Delete <hidden>{space}Selected</hidden>",id:"QE60Po3yK8",values:{space:(0,n.jsx)(n.Fragment,{children:"\xa0"}),hidden:e=>(0,n.jsxs)("span",{className:"max-sm:hidden",children:[" ",e]})}})})]})}},85285:function(e,t,s){s.d(t,{d:function(){return a}});var n=s(27573),i=s(93124);function a(e){let{isError:t,config:s}=e;return t?(0,n.jsx)(i.Z,{defaultMessage:"GitHub",id:"wO9wb5D8Fn"}):(0,n.jsxs)("p",{children:[s.owner,(0,n.jsx)("span",{className:"opacity-25 px-0.5",children:"/"}),s.repo,(0,n.jsx)("span",{className:"border-0.5 bg-bg-200 font-mono text-text-300 border-border-200 px-0.5 rounded ml-1.5 text-xs hidden sm:inline",children:s.branch})]})}},65291:function(e,t,s){s.d(t,{w:function(){return g}});var n=s(27573),i=s(48814),a=s(17886),l=s(76009),r=s(99694),o=s(82177),d=s(91237),c=s(93124),u=s(23428);function g(e){let{syncSource:t}=e,s=(0,d.Z)(),g=(0,u.lP)(),{state:x,last_synced_at:h}=t.status;switch(x){case r.co.CREATED:case r.co.PENDING:case r.co.UPDATING:return(0,n.jsx)("span",{children:(0,n.jsx)(c.Z,{defaultMessage:"Syncing...",id:"S92mvo6R0o"})});case r.co.FAILED:case r.co.UPDATE_FAILED:return(0,n.jsx)("span",{className:"text-danger-100",children:(0,n.jsx)(c.Z,{defaultMessage:"Failed",id:"vXCeIi67rj"})});case r.co.READY:return h?(0,n.jsx)("span",{children:(0,n.jsx)(c.Z,{defaultMessage:"Last synced {relativeTime}",id:"bHMcz2sr6C",values:{relativeTime:(0,n.jsx)(i.i,{datetime:o.ou.fromISO(h),locale:s.locale})}})}):(0,n.jsx)("span",{children:(0,n.jsx)(c.Z,{defaultMessage:"Ready",id:"IZFEUgrg25"})});case r.co.UNAUTHENTICATED:return(0,n.jsx)("span",{className:"text-danger-100",children:(0,n.jsx)(c.Z,{defaultMessage:"You are not authenticated. <button>Authenticate</button>",id:"dRMzxrur9L",values:{button:e=>(0,n.jsx)("button",{className:"underline",onClick:()=>g(t.type),children:e})}})});case r.co.ACCESS_DENIED:return(0,n.jsx)("span",{className:"text-danger-100",children:(0,n.jsx)(c.Z,{defaultMessage:"Access denied, request via {source}",id:"iZUStU5eYI",values:{source:l.X_[t.type]}})});case r.co.DISABLED:return(0,n.jsx)(a.u,{tooltipContent:l.p5,children:(0,n.jsx)("span",{className:"text-danger-100",children:(0,n.jsx)(c.Z,{defaultMessage:"Content not accessible",id:"IPK01iLM7n"})})})}}},22161:function(e,t,s){s.d(t,{p:function(){return d}});var n=s(27573),i=s(11096),a=s(74651),l=s(57908);let r=s(7653).forwardRef((e,t)=>{let{value:s,className:i}=e,a=Math.round(100*Math.min(Math.max(s,0),1));return(0,n.jsx)("div",{ref:t,role:"progressbar","aria-valuenow":a,"aria-valuemin":0,"aria-valuemax":100,className:(0,l.Z)("w-full h-1 bg-bg-400 rounded-full overflow-hidden",i),children:(0,n.jsx)("div",{className:"h-full bg-accent-main-100 rounded-full transition-all duration-300 ease-in-out",style:{width:"".concat(a,"%")}})})});r.displayName="Progress";var o=s(62973);let d=e=>{let{isOpen:t=!1,onClose:s,onConfirm:l,modalTitle:d="Delete chat?",modalText:c="Are you sure you want to delete this chat?",isDeleting:u=!1,progress:g=0}=e;return(0,n.jsxs)(a.u_,{title:d,isOpen:t,onClose:s,children:[(0,n.jsx)("div",{className:"mt-1 mb-2",children:c}),u&&g>0&&(0,n.jsx)(r,{value:g}),(0,n.jsxs)(a.dm,{children:[(0,n.jsx)(i.z,{variant:"danger","data-testid":"delete-modal-confirm",onClick:l,disabled:u,children:u?(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(o.t,{className:"inline-block mr-1 animate-spin",size:14}),"Deleting..."]}):"Delete"}),(0,n.jsx)(i.z,{variant:"secondary",onClick:s,children:"Cancel"})]})]})}},33293:function(e,t,s){s.d(t,{HF:function(){return a},bq:function(){return i}});var n=s(13623);let i=function(e){for(var t=arguments.length,s=Array(t>1?t-1:0),i=1;i<t;i++)s[i-1]=arguments[i];try{"function"==typeof window.gtag&&gtag(e,...s)}catch(e){(0,n.Tb)(e)}},a=e=>{i("consent","update",l(e))},l=e=>({ad_personalization:e.marketing?"granted":"denied",ad_user_data:e.marketing?"granted":"denied",ad_storage:e.marketing?"granted":"denied",analytics_storage:e.analytics?"granted":"denied",functionality_storage:"granted",personalization_storage:"granted",security_storage:"granted"})},48814:function(e,t,s){s.d(t,{i:function(){return r}});var n=s(27573),i=s(82177),a=s(17886);let l={timeZoneName:"short",...i.ou.DATETIME_MED};function r(e){let{datetime:t,locale:s}=e;return(0,n.jsx)(a.u,{delayDuration:700,side:"bottom",tooltipContent:t.toLocaleString(l),children:(0,n.jsx)("span",{children:t.toRelative({locale:s})})})}},42152:function(e,t,s){s.d(t,{f:function(){return r},m:function(){return o}});var n=s(27573),i=s(71233),a=s(21484),l=s(7653);function r(e){let{didCopy:t,...s}=e;return t?(0,n.jsx)(i.f,{...s}):(0,n.jsx)(a.T,{...s})}function o(e){let[t,s]=(0,l.useState)(!1);return{didCopy:t,copyToClipboard:(0,l.useCallback)(t=>{let n="string"==typeof t?t:e;navigator.clipboard.writeText(n.trim()).then(()=>{s(!0),setTimeout(()=>s(!1),2e3)}).catch(e=>console.log("Something went wrong",e))},[e])}}}}]);