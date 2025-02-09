"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9194],{89194:function(e,t,r){r.d(t,{K:function(){return n}});var o=r(28294);class s{constructor(e){this._options=e,this._requestMessageId=0,this._requestHandlers=new Map,this._requestHandlerAbortControllers=new Map,this._notificationHandlers=new Map,this._responseHandlers=new Map,this._progressHandlers=new Map,this.setNotificationHandler(o.MH,e=>{let t=this._requestHandlerAbortControllers.get(e.params.requestId);null==t||t.abort(e.params.reason)}),this.setNotificationHandler(o.gD,e=>{this._onprogress(e)}),this.setRequestHandler(o.EO,e=>({}))}async connect(e){this._transport=e,this._transport.onclose=()=>{this._onclose()},this._transport.onerror=e=>{this._onerror(e)},this._transport.onmessage=e=>{"method"in e?"id"in e?this._onrequest(e):this._onnotification(e):this._onresponse(e)},await this._transport.start()}_onclose(){var e;let t=this._responseHandlers;this._responseHandlers=new Map,this._progressHandlers.clear(),this._transport=void 0,null===(e=this.onclose)||void 0===e||e.call(this);let r=new o.yp(o.jK.ConnectionClosed,"Connection closed");for(let e of t.values())e(r)}_onerror(e){var t;null===(t=this.onerror)||void 0===t||t.call(this,e)}_onnotification(e){var t;let r=null!==(t=this._notificationHandlers.get(e.method))&&void 0!==t?t:this.fallbackNotificationHandler;void 0!==r&&Promise.resolve().then(()=>r(e)).catch(e=>this._onerror(Error(`Uncaught error in notification handler: ${e}`)))}_onrequest(e){var t,r;let s=null!==(t=this._requestHandlers.get(e.method))&&void 0!==t?t:this.fallbackRequestHandler;if(void 0===s){null===(r=this._transport)||void 0===r||r.send({jsonrpc:"2.0",id:e.id,error:{code:o.jK.MethodNotFound,message:"Method not found"}}).catch(e=>this._onerror(Error(`Failed to send an error response: ${e}`)));return}let n=new AbortController;this._requestHandlerAbortControllers.set(e.id,n),Promise.resolve().then(()=>s(e,{signal:n.signal})).then(t=>{var r;if(!n.signal.aborted)return null===(r=this._transport)||void 0===r?void 0:r.send({result:t,jsonrpc:"2.0",id:e.id})},t=>{var r,s;if(!n.signal.aborted)return null===(r=this._transport)||void 0===r?void 0:r.send({jsonrpc:"2.0",id:e.id,error:{code:Number.isSafeInteger(t.code)?t.code:o.jK.InternalError,message:null!==(s=t.message)&&void 0!==s?s:"Internal error"}})}).catch(e=>this._onerror(Error(`Failed to send response: ${e}`))).finally(()=>{this._requestHandlerAbortControllers.delete(e.id)})}_onprogress(e){let{progress:t,total:r,progressToken:o}=e.params,s=this._progressHandlers.get(Number(o));if(void 0===s){this._onerror(Error(`Received a progress notification for an unknown token: ${JSON.stringify(e)}`));return}s({progress:t,total:r})}_onresponse(e){let t=e.id,r=this._responseHandlers.get(Number(t));if(void 0===r){this._onerror(Error(`Received a response for an unknown message ID: ${JSON.stringify(e)}`));return}this._responseHandlers.delete(Number(t)),this._progressHandlers.delete(Number(t)),r("result"in e?e:new o.yp(e.error.code,e.error.message,e.error.data))}get transport(){return this._transport}async close(){var e;await (null===(e=this._transport)||void 0===e?void 0:e.close())}request(e,t,r){return new Promise((s,n)=>{var i,a,l,u;let d;if(!this._transport){n(Error("Not connected"));return}(null===(i=this._options)||void 0===i?void 0:i.enforceStrictCapabilities)===!0&&this.assertCapabilityForMethod(e.method),null===(a=null==r?void 0:r.signal)||void 0===a||a.throwIfAborted();let c=this._requestMessageId++,p={...e,jsonrpc:"2.0",id:c};(null==r?void 0:r.onprogress)&&(this._progressHandlers.set(c,r.onprogress),p.params={...e.params,_meta:{progressToken:c}}),this._responseHandlers.set(c,e=>{var o;if(void 0!==d&&clearTimeout(d),null===(o=null==r?void 0:r.signal)||void 0===o||!o.aborted){if(e instanceof Error)return n(e);try{let r=t.parse(e.result);s(r)}catch(e){n(e)}}});let h=e=>{var t;this._responseHandlers.delete(c),this._progressHandlers.delete(c),null===(t=this._transport)||void 0===t||t.send({jsonrpc:"2.0",method:"cancelled",params:{requestId:c,reason:String(e)}}).catch(e=>this._onerror(Error(`Failed to send cancellation: ${e}`))),n(e)};null===(l=null==r?void 0:r.signal)||void 0===l||l.addEventListener("abort",()=>{var e;void 0!==d&&clearTimeout(d),h(null===(e=null==r?void 0:r.signal)||void 0===e?void 0:e.reason)});let z=null!==(u=null==r?void 0:r.timeout)&&void 0!==u?u:6e4;d=setTimeout(()=>h(new o.yp(o.jK.RequestTimeout,"Request timed out",{timeout:z})),z),this._transport.send(p).catch(e=>{void 0!==d&&clearTimeout(d),n(e)})})}async notification(e){if(!this._transport)throw Error("Not connected");this.assertNotificationCapability(e.method);let t={...e,jsonrpc:"2.0"};await this._transport.send(t)}setRequestHandler(e,t){let r=e.shape.method.value;this.assertRequestHandlerCapability(r),this._requestHandlers.set(r,(r,o)=>Promise.resolve(t(e.parse(r),o)))}removeRequestHandler(e){this._requestHandlers.delete(e)}setNotificationHandler(e,t){this._notificationHandlers.set(e.shape.method.value,r=>Promise.resolve(t(e.parse(r))))}removeNotificationHandler(e){this._notificationHandlers.delete(e)}}class n extends s{constructor(e,t){super(t),this._clientInfo=e,this._capabilities=t.capabilities}assertCapability(e,t){var r;if(!(null===(r=this._serverCapabilities)||void 0===r?void 0:r[e]))throw Error(`Server does not support ${e} (required for ${t})`)}async connect(e){await super.connect(e);try{let e=await this.request({method:"initialize",params:{protocolVersion:o.P7,capabilities:this._capabilities,clientInfo:this._clientInfo}},o.EE);if(void 0===e)throw Error(`Server sent invalid initialize result: ${e}`);if(!o.e5.includes(e.protocolVersion))throw Error(`Server's protocol version is not supported: ${e.protocolVersion}`);this._serverCapabilities=e.capabilities,this._serverVersion=e.serverInfo,await this.notification({method:"notifications/initialized"})}catch(e){throw this.close(),e}}getServerCapabilities(){return this._serverCapabilities}getServerVersion(){return this._serverVersion}assertCapabilityForMethod(e){var t,r,o,s,n;switch(e){case"logging/setLevel":if(!(null===(t=this._serverCapabilities)||void 0===t?void 0:t.logging))throw Error(`Server does not support logging (required for ${e})`);break;case"prompts/get":case"prompts/list":if(!(null===(r=this._serverCapabilities)||void 0===r?void 0:r.prompts))throw Error(`Server does not support prompts (required for ${e})`);break;case"resources/list":case"resources/templates/list":case"resources/read":case"resources/subscribe":case"resources/unsubscribe":if(!(null===(o=this._serverCapabilities)||void 0===o?void 0:o.resources))throw Error(`Server does not support resources (required for ${e})`);if("resources/subscribe"===e&&!this._serverCapabilities.resources.subscribe)throw Error(`Server does not support resource subscriptions (required for ${e})`);break;case"tools/call":case"tools/list":if(!(null===(s=this._serverCapabilities)||void 0===s?void 0:s.tools))throw Error(`Server does not support tools (required for ${e})`);break;case"completion/complete":if(!(null===(n=this._serverCapabilities)||void 0===n?void 0:n.prompts))throw Error(`Server does not support prompts (required for ${e})`)}}assertNotificationCapability(e){var t;if("notifications/roots/list_changed"===e&&!(null===(t=this._capabilities.roots)||void 0===t?void 0:t.listChanged))throw Error(`Client does not support roots list changed notifications (required for ${e})`)}assertRequestHandlerCapability(e){switch(e){case"sampling/createMessage":if(!this._capabilities.sampling)throw Error(`Client does not support sampling capability (required for ${e})`);break;case"roots/list":if(!this._capabilities.roots)throw Error(`Client does not support roots capability (required for ${e})`)}}async ping(e){return this.request({method:"ping"},o.Zs,e)}async complete(e,t){return this.request({method:"completion/complete",params:e},o.Bi,t)}async setLoggingLevel(e,t){return this.request({method:"logging/setLevel",params:{level:e}},o.Zs,t)}async getPrompt(e,t){return this.request({method:"prompts/get",params:e},o.Go,t)}async listPrompts(e,t){return this.request({method:"prompts/list",params:e},o.ev,t)}async listResources(e,t){return this.request({method:"resources/list",params:e},o.Ol,t)}async listResourceTemplates(e,t){return this.request({method:"resources/templates/list",params:e},o.CD,t)}async readResource(e,t){return this.request({method:"resources/read",params:e},o.vg,t)}async subscribeResource(e,t){return this.request({method:"resources/subscribe",params:e},o.Zs,t)}async unsubscribeResource(e,t){return this.request({method:"resources/unsubscribe",params:e},o.Zs,t)}async callTool(e,t=o.GR,r){return this.request({method:"tools/call",params:e},t,r)}async listTools(e,t){return this.request({method:"tools/list",params:e},o.Gd,t)}async sendRootsListChanged(){return this.notification({method:"notifications/roots/list_changed"})}}},28294:function(e,t,r){r.d(t,{Bi:function(){return ej},CD:function(){return O},EE:function(){return w},EO:function(){return E},GR:function(){return el},Gd:function(){return ea},Go:function(){return eo},M$:function(){return eu},MH:function(){return x},Ol:function(){return V},P7:function(){return i},Zs:function(){return _},b5:function(){return ez},e5:function(){return a},ev:function(){return Q},gD:function(){return R},jK:function(){return s},kO:function(){return ev},vg:function(){return G},yp:function(){return eE}});var o,s,n=r(97712);let i="2024-11-05",a=[i,"2024-10-07"],l=n.z.union([n.z.string(),n.z.number().int()]),u=n.z.string(),d=n.z.object({_meta:n.z.optional(n.z.object({progressToken:n.z.optional(l)}).passthrough())}).passthrough(),c=n.z.object({method:n.z.string(),params:n.z.optional(d)}),p=n.z.object({_meta:n.z.optional(n.z.object({}).passthrough())}).passthrough(),h=n.z.object({method:n.z.string(),params:n.z.optional(p)}),z=n.z.object({_meta:n.z.optional(n.z.object({}).passthrough())}).passthrough(),m=n.z.union([n.z.string(),n.z.number().int()]),g=n.z.object({jsonrpc:n.z.literal("2.0"),id:m}).merge(c).strict(),b=n.z.object({jsonrpc:n.z.literal("2.0")}).merge(h).strict(),v=n.z.object({jsonrpc:n.z.literal("2.0"),id:m,result:z}).strict();(o=s||(s={}))[o.ConnectionClosed=-1]="ConnectionClosed",o[o.RequestTimeout=-2]="RequestTimeout",o[o.ParseError=-32700]="ParseError",o[o.InvalidRequest=-32600]="InvalidRequest",o[o.MethodNotFound=-32601]="MethodNotFound",o[o.InvalidParams=-32602]="InvalidParams",o[o.InternalError=-32603]="InternalError";let f=n.z.object({jsonrpc:n.z.literal("2.0"),id:m,error:n.z.object({code:n.z.number().int(),message:n.z.string(),data:n.z.optional(n.z.unknown())})}).strict();n.z.union([g,b,v,f]);let _=z.strict(),x=h.extend({method:n.z.literal("notifications/cancelled"),params:p.extend({requestId:m,reason:n.z.string().optional()})}),y=n.z.object({name:n.z.string(),version:n.z.string()}).passthrough(),j=n.z.object({experimental:n.z.optional(n.z.object({}).passthrough()),sampling:n.z.optional(n.z.object({}).passthrough()),roots:n.z.optional(n.z.object({listChanged:n.z.optional(n.z.boolean())}).passthrough())}).passthrough(),q=c.extend({method:n.z.literal("initialize"),params:d.extend({protocolVersion:n.z.string(),capabilities:j,clientInfo:y})}),C=n.z.object({experimental:n.z.optional(n.z.object({}).passthrough()),logging:n.z.optional(n.z.object({}).passthrough()),prompts:n.z.optional(n.z.object({listChanged:n.z.optional(n.z.boolean())}).passthrough()),resources:n.z.optional(n.z.object({subscribe:n.z.optional(n.z.boolean()),listChanged:n.z.optional(n.z.boolean())}).passthrough()),tools:n.z.optional(n.z.object({listChanged:n.z.optional(n.z.boolean())}).passthrough())}).passthrough(),w=z.extend({protocolVersion:n.z.string(),capabilities:C,serverInfo:y}),H=h.extend({method:n.z.literal("notifications/initialized")}),E=c.extend({method:n.z.literal("ping")}),k=n.z.object({progress:n.z.number(),total:n.z.optional(n.z.number())}).passthrough(),R=h.extend({method:n.z.literal("notifications/progress"),params:p.merge(k).extend({progressToken:l})}),I=c.extend({params:d.extend({cursor:n.z.optional(u)}).optional()}),T=z.extend({nextCursor:n.z.optional(u)}),$=n.z.object({uri:n.z.string(),mimeType:n.z.optional(n.z.string())}).passthrough(),M=$.extend({text:n.z.string()}),N=$.extend({blob:n.z.string().base64()}),S=n.z.object({uri:n.z.string(),name:n.z.string(),description:n.z.optional(n.z.string()),mimeType:n.z.optional(n.z.string())}).passthrough(),P=n.z.object({uriTemplate:n.z.string(),name:n.z.string(),description:n.z.optional(n.z.string()),mimeType:n.z.optional(n.z.string())}).passthrough(),F=I.extend({method:n.z.literal("resources/list")}),V=T.extend({resources:n.z.array(S)}),L=I.extend({method:n.z.literal("resources/templates/list")}),O=T.extend({resourceTemplates:n.z.array(P)}),A=c.extend({method:n.z.literal("resources/read"),params:d.extend({uri:n.z.string()})}),G=z.extend({contents:n.z.array(n.z.union([M,N]))}),K=h.extend({method:n.z.literal("notifications/resources/list_changed")}),D=c.extend({method:n.z.literal("resources/subscribe"),params:d.extend({uri:n.z.string()})}),Z=c.extend({method:n.z.literal("resources/unsubscribe"),params:d.extend({uri:n.z.string()})}),B=h.extend({method:n.z.literal("notifications/resources/updated"),params:p.extend({uri:n.z.string()})}),J=n.z.object({name:n.z.string(),description:n.z.optional(n.z.string()),required:n.z.optional(n.z.boolean())}).passthrough(),U=n.z.object({name:n.z.string(),description:n.z.optional(n.z.string()),arguments:n.z.optional(n.z.array(J))}).passthrough(),W=I.extend({method:n.z.literal("prompts/list")}),Q=T.extend({prompts:n.z.array(U)}),X=c.extend({method:n.z.literal("prompts/get"),params:d.extend({name:n.z.string(),arguments:n.z.optional(n.z.record(n.z.string()))})}),Y=n.z.object({type:n.z.literal("text"),text:n.z.string()}).passthrough(),ee=n.z.object({type:n.z.literal("image"),data:n.z.string().base64(),mimeType:n.z.string()}).passthrough(),et=n.z.object({type:n.z.literal("resource"),resource:n.z.union([M,N])}).passthrough(),er=n.z.object({role:n.z.enum(["user","assistant"]),content:n.z.union([Y,ee,et])}).passthrough(),eo=z.extend({description:n.z.optional(n.z.string()),messages:n.z.array(er)}),es=h.extend({method:n.z.literal("notifications/prompts/list_changed")}),en=n.z.object({name:n.z.string(),description:n.z.optional(n.z.string()),inputSchema:n.z.object({type:n.z.literal("object"),properties:n.z.optional(n.z.object({}).passthrough())}).passthrough()}).passthrough(),ei=I.extend({method:n.z.literal("tools/list")}),ea=T.extend({tools:n.z.array(en)}),el=z.extend({content:n.z.array(n.z.union([Y,ee,et])),isError:n.z.boolean().default(!1).optional()}),eu=el.or(z.extend({toolResult:n.z.unknown()})),ed=c.extend({method:n.z.literal("tools/call"),params:d.extend({name:n.z.string(),arguments:n.z.optional(n.z.record(n.z.unknown()))})}),ec=h.extend({method:n.z.literal("notifications/tools/list_changed")}),ep=n.z.enum(["debug","info","notice","warning","error","critical","alert","emergency"]),eh=c.extend({method:n.z.literal("logging/setLevel"),params:d.extend({level:ep})}),ez=h.extend({method:n.z.literal("notifications/message"),params:p.extend({level:ep,logger:n.z.optional(n.z.string()),data:n.z.unknown()})}),em=n.z.object({name:n.z.string().optional()}).passthrough(),eg=n.z.object({hints:n.z.optional(n.z.array(em)),costPriority:n.z.optional(n.z.number().min(0).max(1)),speedPriority:n.z.optional(n.z.number().min(0).max(1)),intelligencePriority:n.z.optional(n.z.number().min(0).max(1))}).passthrough(),eb=n.z.object({role:n.z.enum(["user","assistant"]),content:n.z.union([Y,ee])}).passthrough(),ev=c.extend({method:n.z.literal("sampling/createMessage"),params:d.extend({messages:n.z.array(eb),systemPrompt:n.z.optional(n.z.string()),includeContext:n.z.optional(n.z.enum(["none","thisServer","allServers"])),temperature:n.z.optional(n.z.number()),maxTokens:n.z.number().int(),stopSequences:n.z.optional(n.z.array(n.z.string())),metadata:n.z.optional(n.z.object({}).passthrough()),modelPreferences:n.z.optional(eg)})}),ef=z.extend({model:n.z.string(),stopReason:n.z.optional(n.z.enum(["endTurn","stopSequence","maxTokens"]).or(n.z.string())),role:n.z.enum(["user","assistant"]),content:n.z.discriminatedUnion("type",[Y,ee])}),e_=n.z.object({type:n.z.literal("ref/resource"),uri:n.z.string()}).passthrough(),ex=n.z.object({type:n.z.literal("ref/prompt"),name:n.z.string()}).passthrough(),ey=c.extend({method:n.z.literal("completion/complete"),params:d.extend({ref:n.z.union([ex,e_]),argument:n.z.object({name:n.z.string(),value:n.z.string()}).passthrough()})}),ej=z.extend({completion:n.z.object({values:n.z.array(n.z.string()).max(100),total:n.z.optional(n.z.number().int()),hasMore:n.z.optional(n.z.boolean())}).passthrough()}),eq=n.z.object({uri:n.z.string().startsWith("file://"),name:n.z.optional(n.z.string())}).passthrough(),eC=c.extend({method:n.z.literal("roots/list")}),ew=z.extend({roots:n.z.array(eq)}),eH=h.extend({method:n.z.literal("notifications/roots/list_changed")});n.z.union([E,q,ey,eh,X,W,F,L,A,D,Z,ed,ei]),n.z.union([x,R,H,eH]),n.z.union([_,ef,ew]),n.z.union([E,ev,eC]),n.z.union([x,R,ez,B,K,ec,es]),n.z.union([_,w,ej,eo,Q,V,O,G,el,ea]);class eE extends Error{constructor(e,t,r){super(`MCP error ${e}: ${t}`),this.code=e,this.data=r}}}}]);