"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[1867],{61867:function(e,t,n){n.d(t,{FO:function(){return g},N7:function(){return y},O3:function(){return S},P2:function(){return z},TD:function(){return C},Wy:function(){return x},q2:function(){return b},to:function(){return a},vr:function(){return h}});var o,a,r=n(15489),c=n(97712),s=n(3286);(o=a||(a={})).ReadyForContent="anthropic.claude.usercontent.sandbox.ReadyForContent",o.SetContent="anthropic.claude.usercontent.sandbox.SetContent",o.GetFile="anthropic.claude.usercontent.sandbox.GetFile",o.SendConversationMessage="anthropic.claude.usercontent.sandbox.SendConversationMessage",o.RunCode="anthropic.claude.usercontent.sandbox.RunCode",o.ClaudeCompletion="anthropic.claude.usercontent.sandbox.ClaudeCompletion",o.ReportError="anthropic.claude.usercontent.sandbox.ReportError",o.GetScreenshot="anthropic.claude.usercontent.sandbox.GetScreenshot",o.BroadcastContentSize="anthropic.claude.usercontent.sandbox.BroadcastContentSize";let i=c.z.object({type:c.z.literal("UnsupportedImports"),unsupportedModules:c.z.array(c.z.string()),nonExistentIcons:c.z.array(c.z.string())}),u=c.z.object({type:c.z.literal("RuntimeError"),message:c.z.string()}),d=c.z.object({type:c.z.literal("FileNotFound"),fileName:c.z.string()}),l=c.z.object({type:c.z.literal("ClaudeCompletionError"),message:c.z.string()}),p=c.z.discriminatedUnion("type",[i,u,d,l]);c.z.object({code:c.z.string()});let h=c.z.object({status:c.z.enum(["success","error"]),result:c.z.string().optional(),logs:c.z.array(c.z.string()),error:c.z.string().optional()}),m={"anthropic.claude.usercontent.sandbox.SetContent":{requestSchema:s.Zq.extend({method:c.z.literal("anthropic.claude.usercontent.sandbox.SetContent"),payload:c.z.strictObject({"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.SandboxContent"),content:c.z.string(),type:c.z.nativeEnum(r.JP),watchContentSize:c.z.boolean().optional()})}),responseSchema:s.AY,alwaysPermitted:!1},"anthropic.claude.usercontent.sandbox.ReadyForContent":{requestSchema:s.Zq.extend({method:c.z.literal("anthropic.claude.usercontent.sandbox.ReadyForContent"),payload:c.z.strictObject({"@type":c.z.literal("type.googleapis.com/google.protobuf.Empty")})}),responseSchema:s.AY,alwaysPermitted:!0},"anthropic.claude.usercontent.sandbox.BroadcastContentSize":{requestSchema:s.Zq.extend({method:c.z.literal("anthropic.claude.usercontent.sandbox.BroadcastContentSize"),payload:c.z.strictObject({"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.BroadcastContentSizePayload"),height:c.z.number(),width:c.z.number()})}),responseSchema:s.AY,alwaysPermitted:!1},"anthropic.claude.usercontent.sandbox.GetFile":{requestSchema:s.Zq.extend({method:c.z.literal("anthropic.claude.usercontent.sandbox.GetFile"),payload:c.z.strictObject({key:c.z.string(),"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.GetFileRequest")})}),responseSchema:s.Tk.extend({payload:c.z.strictObject({value:c.z.instanceof(Uint8Array).nullable(),"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.GetFileResponse")})}),alwaysPermitted:!1},"anthropic.claude.usercontent.sandbox.SendConversationMessage":{requestSchema:s.Zq.extend({method:c.z.literal("anthropic.claude.usercontent.sandbox.SendConversationMessage"),payload:c.z.strictObject({message:c.z.string(),messageType:c.z.enum(["text","error"]),"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.SendConversationMessageRequest")})}),responseSchema:s.AY,alwaysPermitted:!1},"anthropic.claude.usercontent.sandbox.RunCode":{requestSchema:s.Zq.extend({method:c.z.literal("anthropic.claude.usercontent.sandbox.RunCode"),payload:c.z.strictObject({code:c.z.string(),"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.RunCodeRequest")})}),responseSchema:s.Tk.extend({payload:c.z.strictObject({"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.RunCodeResponse")}).merge(h)}),alwaysPermitted:!1},"anthropic.claude.usercontent.sandbox.ClaudeCompletion":{requestSchema:s.Zq.extend({method:c.z.literal("anthropic.claude.usercontent.sandbox.ClaudeCompletion"),payload:c.z.strictObject({prompt:c.z.string(),"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.ClaudeCompletionRequest")})}),responseSchema:s.Tk.extend({payload:c.z.strictObject({completion:c.z.string().nullable(),"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.ClaudeCompletionResponse")})}),alwaysPermitted:!1},"anthropic.claude.usercontent.sandbox.ReportError":{requestSchema:s.Zq.extend({method:c.z.literal("anthropic.claude.usercontent.sandbox.ReportError"),payload:c.z.strictObject({"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.ReportErrorRequest"),error:p})}),responseSchema:s.AY,alwaysPermitted:!0},"anthropic.claude.usercontent.sandbox.GetScreenshot":{requestSchema:s.Zq.extend({method:c.z.literal("anthropic.claude.usercontent.sandbox.GetScreenshot"),payload:c.z.strictObject({"@type":c.z.literal("type.googleapis.com/google.protobuf.Empty")})}),responseSchema:s.Tk.extend({payload:c.z.strictObject({screenshot:c.z.string().nullable(),"@type":c.z.literal("type.googleapis.com/anthropic.claude.usercontent.sandbox.GetScreenshotResponse")})}),alwaysPermitted:!1}},z=c.z.enum(["anthropic.claude.usercontent.sandbox.ReadyForContent","anthropic.claude.usercontent.sandbox.GetFile","anthropic.claude.usercontent.sandbox.SendConversationMessage","anthropic.claude.usercontent.sandbox.ClaudeCompletion","anthropic.claude.usercontent.sandbox.ReportError","anthropic.claude.usercontent.sandbox.BroadcastContentSize"]),b=c.z.discriminatedUnion("method",[m["anthropic.claude.usercontent.sandbox.ReadyForContent"].requestSchema,m["anthropic.claude.usercontent.sandbox.GetFile"].requestSchema,m["anthropic.claude.usercontent.sandbox.SendConversationMessage"].requestSchema,m["anthropic.claude.usercontent.sandbox.ClaudeCompletion"].requestSchema,m["anthropic.claude.usercontent.sandbox.ReportError"].requestSchema,m["anthropic.claude.usercontent.sandbox.BroadcastContentSize"].requestSchema]),g=c.z.union([s.AY,m["anthropic.claude.usercontent.sandbox.GetFile"].responseSchema,m["anthropic.claude.usercontent.sandbox.SendConversationMessage"].responseSchema,m["anthropic.claude.usercontent.sandbox.ClaudeCompletion"].responseSchema]),x=c.z.enum(["anthropic.claude.usercontent.sandbox.SetContent","anthropic.claude.usercontent.sandbox.RunCode","anthropic.claude.usercontent.sandbox.GetScreenshot"]),y=c.z.discriminatedUnion("method",[m["anthropic.claude.usercontent.sandbox.SetContent"].requestSchema,m["anthropic.claude.usercontent.sandbox.RunCode"].requestSchema,m["anthropic.claude.usercontent.sandbox.GetScreenshot"].requestSchema]),S=c.z.union([m["anthropic.claude.usercontent.sandbox.SetContent"].responseSchema,m["anthropic.claude.usercontent.sandbox.RunCode"].responseSchema,m["anthropic.claude.usercontent.sandbox.GetScreenshot"].responseSchema]),C=Object.entries(m).filter(e=>{let[t,n]=e;return!0===n.alwaysPermitted}).map(e=>{let[t,n]=e;return t})},3286:function(e,t,n){n.d(t,{AY:function(){return i},D7:function(){return u},Kj:function(){return s},Tk:function(){return c},Zq:function(){return r},qV:function(){return a},v8:function(){return d}});var o=n(97712);let a=o.z.object({channel:o.z.enum(["request","response"]),requestId:o.z.string()}).passthrough(),r=a.strict().extend({channel:o.z.literal("request"),method:o.z.string(),payload:o.z.strictObject({"@type":o.z.string()})}),c=a.extend({channel:o.z.literal("response"),status:o.z.number().int().min(100).max(599),payload:o.z.strictObject({"@type":o.z.string()}).passthrough()}).passthrough(),s=c.extend({status:o.z.number().int().min(400).max(599),payload:o.z.strictObject({"@type":o.z.literal("type.googleapis.com/anthropic.claude.usercontent.ErrorResponse"),error:o.z.string()})}),i=c.extend({payload:o.z.strictObject({"@type":o.z.literal("type.googleapis.com/google.protobuf.Empty")})}),u={"@type":"type.googleapis.com/google.protobuf.Empty"},d=e=>({"@type":"type.googleapis.com/anthropic.claude.usercontent.ErrorResponse",error:e})},15489:function(e,t,n){n.d(t,{JP:function(){return a},KD:function(){return r}});var o,a,r,c=n(97712);(o=a||(a={})).Text="text/plain",o.Markdown="text/markdown",o.Html="text/html",o.Code="application/vnd.ant.code",o.Svg="image/svg+xml",o.Mermaid="application/vnd.ant.mermaid",o.React="application/vnd.ant.react",(r||(r={})).Repl="application/vnd.ant.repl";let s=c.z.string().nullish().transform(e=>null!=e?e:void 0);c.z.object({version_uuid:s,command:c.z.enum(["create","update","rewrite"]).optional().catch(void 0),id:s,title:s,type:c.z.nativeEnum(a).optional().catch(void 0),language:s,content:s,old_str:s,new_str:s});let i="antArtifact",u="<".concat(i,"(?:\\s+([^>]*)>|(?!>)\\S*)"),d="</".concat(i,">");RegExp("".concat(u,"([\\s\\S]*?)(?:").concat(d,"|$)"),"g"),RegExp("".concat(u,"[\\s\\S]*?(?:").concat(d,"|$)"),"g");let l="antThinking",p="<".concat(l,">");RegExp("".concat(p,"[\\s\\S]*?(?:</").concat(l,">|$)"),"g")}}]);