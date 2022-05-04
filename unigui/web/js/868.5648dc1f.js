"use strict";(self["webpackChunkuniqua"]=self["webpackChunkuniqua"]||[]).push([[868],{1868:(e,t,a)=>{a.r(t),a.d(t,{default:()=>Dt});var l=a(3673),o=a(2323);const s=(0,l._)("div",{class:"q-pa-lg"},null,-1);function n(e,t,a,n,i,d){const r=(0,l.up)("q-item-label"),c=(0,l.up)("q-tab"),u=(0,l.up)("q-tabs"),h=(0,l.up)("q-toolbar"),p=(0,l.up)("q-header"),m=(0,l.up)("zone"),g=(0,l.up)("q-page"),f=(0,l.up)("q-page-container"),w=(0,l.up)("q-layout");return(0,l.wg)(),(0,l.j4)(w,{view:"lHh Lpr lFf"},{default:(0,l.w5)((()=>[(0,l.Wm)(p,{elevated:""},{default:(0,l.w5)((()=>[(0,l.Wm)(h,null,{default:(0,l.w5)((()=>[(0,l.Wm)(r,{class:"text-h5"},{default:(0,l.w5)((()=>[(0,l.Uk)((0,o.zw)(e.screen.header?e.screen.header:""),1)])),_:1}),s,(0,l.Wm)(u,{class:"text-teal",align:"center","inline-label":"",dense:"",modelValue:e.tab,"onUpdate:modelValue":t[0]||(t[0]=t=>e.tab=t),style:{float:"center"}},{default:(0,l.w5)((()=>[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.menu,(t=>((0,l.wg)(),(0,l.j4)(c,{class:"justify-center text-white shadow-2",name:t.name,icon:t.icon,label:t.name,onClick:a=>e.tabclick(t.name)},null,8,["name","icon","label","onClick"])))),256))])),_:1},8,["modelValue"])])),_:1})])),_:1}),(0,l.Wm)(f,null,{default:(0,l.w5)((()=>[(0,l.Wm)(g,{class:"flex q-pa-sm justify-center centers"},{default:(0,l.w5)((()=>[(0,l.Wm)(m,{data:e.screen.blocks},null,8,["data"])])),_:1})])),_:1})])),_:1})}a(71);function i(e,t,a,s,n,i){const d=(0,l.up)("q-icon"),r=(0,l.up)("q-item-section"),c=(0,l.up)("q-item-label"),u=(0,l.up)("q-item");return(0,l.wg)(),(0,l.j4)(u,{clickable:"",tag:"a",target:"_blank",onClick:e.send},{default:(0,l.w5)((()=>[(0,l.Wm)(r,{avatar:""},{default:(0,l.w5)((()=>[(0,l.Wm)(d,{name:e.icon},null,8,["name"])])),_:1}),(0,l.Wm)(r,null,{default:(0,l.w5)((()=>[(0,l.Wm)(c,null,{default:(0,l.w5)((()=>[(0,l.Uk)((0,o.zw)(e.name),1)])),_:1})])),_:1})])),_:1},8,["onClick"])}var d;a(7070),a(6226),a(1598),a(7098);const r="ws://35.172.48.116:8281/";let c=null,u={},h=!0;const p=136,m=400,g=`height: ${p}px; width: ${m}px`,f={},w={},y=["error","progress","warning","info"];function b(e){d=new WebSocket(e.localServer?"ws://localhost:8000/":r),d.onopen=()=>e.statusConnect=!0,d.onmessage=t=>{h&&console.log("socket message",t.data),e.processMessage(JSON.parse(t.data))},d.onerror=t=>e.error(t),d.onclose=t=>{t.wasClean?e.info("Connection closed and was clean."):e.error("Connection suddenly closed!"),e.statusConnect=!1,h&&console.info("close code : "+t.code+" reason: "+t.reason)},c=e}function k(e){console.log("sended",e),d.send(JSON.stringify(e))}let v,C=0;function q(e){for(var t in e)e.hasOwnProperty(t)&&delete e[t]}function x(e,t,a,l="?"){let o=++C,s=[e.pdata.name,e.data.name,l,t,o];k(s),u[o]=a}function j(){q(f),q(w)}function S(e,t){Object.assign(e.data,t),e.updated=t.value,e.value=t.value}function Z(e){if(e.multi)for(let[t,a]of e.update.entries())if(a.length>1){a.reverse();let l=a.join("@"),o=w[l];S(o,e.data[t])}else{let l=f[a[0]];Object.assign(l.data,e.data[t])}else{let t,a=e.update;if(a.length>1){a.reverse();let e=a.join("@");t=w[e]}else t=f[a[0]];S(t,e.data)}}function A(e){typeof e.answer==String?c.showError():u[e.id](e.answer),delete u[e.id]}function M(e){let t=[];for(let l of e)l instanceof Array?t.push(l):t.push([l]);let a=t.shift();return t.reduce(((e,t)=>e.flatMap((e=>t.map((t=>e instanceof Array?[...e,t]:[e,t]))))),a)}const D={childList:!0,subtree:!0};function W(){v=new MutationObserver(_.debounce($,200,{leading:!1})),v.observe(c.$el,D)}function $(){v&&(v.disconnect(),v=null),h&&console.log("------------------recalc design");const e=H(),t=Q();for(let[a,l]of Object.entries(e)){let e=w[a];const o=t[a];let s,n=e.geom().el,i=e.pdata?e.pdata.name:e.name,d=f[i];for(let t of d.data.childs)if(Array.isArray(t)){if(t.find((t=>t.name==e.data.name))){let e=t[t.length-1],a=`${e.name}@${i}`;s=w[a];break}}else if(t.name==e.data.name){s=e;break}let r=d.$el.getBoundingClientRect().right-(s?s.geom().right:e.geom().right)-10;d.data.width&&(r=d.data.width-n.clientWidth-o),h&&console.log(e.name,`h=${n.clientHeight}, deltaH=${l}, deltaW=${o}, height: ${n.clientHeight+l}px;             width: ${n.clientWidth}px;`);let c=a.startsWith("_scroll@")?e.geom().inner.clientHeight:n.clientHeight;e.styleSize=`height: ${c+l}px; width: ${n.clientWidth+o+r}px;`}}function H(){const e=c.screen.blocks;let t=window.innerHeight;t-=10;let a={},l=new Map;for(let o of e){const e=[];let s=o instanceof Array?M(o):[o];for(let a of s){let o=Array.isArray(a),s=o?a[a.length-1]:a,n=f[s.name].$el,i=n.getBoundingClientRect().bottom;if(i!=t){const n=[];for(let[e,t]of Object.entries(w))if(t.expanding){let[i,d]=e.split("@");if(o?a.find((e=>e.name==d)):a.name==d){let e=!0;const a=t.geom();if(d==s.name)for(let[o,s]of n.entries()){let i=s.geom();if(s!==t&&i.top==a.top){i.scrollHeight<a.scrollHeight&&(n[o]=t),e=!1,l.set(t.fullname,s.fullname);break}}e&&n.push(t)}}n.length&&e.push([t-i,n])}}for(let[t,l]of e){l.sort(((e,t)=>e.geom().scrollHeight<t.geom().scrollHeight));let e=l.length,o=l[e-1];for(let s of l){let l=a[s.fullname];if(!l){const l=s.geom();if(o!==s&&l.scrollHeight<t/e){const t=l.scrollHeight-l.inner.clientHeight;a[s.fullname]=t,e--}else a[s.fullname]=t/e}}}}for(let[o,s]of l.entries())s in a?a[o]=a[s]:a[s]=a[o];return a}function Q(){const e=c.screen.blocks;let t=window.innerWidth-30,a=[],l={};for(let n of e)if(0==a.length)if(Array.isArray(n))for(let e of n)a.push(Array.isArray(e)?e:[e]);else a=[[n]];else{let e=[];if(Array.isArray(n))for(let t of n)for(let l of a)e.push(Array.isArray(t)?l.concat(t):[...l,t]);else for(let t of a)e.push([...t,n]);a=e}const o=[];let s=new Map;for(let n of a){let e=Array.isArray(n)?n[n.length-1]:n,a=f[e.name].$el.getBoundingClientRect().right;e=Array.isArray(n)?n[0]:n;let l=f[e.name].$el.getBoundingClientRect().left,i=t-a+l-10;const d=[];for(let[t,o]of Object.entries(w))if(o.expanding){let e=t.split("@")[1];if(n.find((t=>t.name==e))){let e=!0,t=o.geom().left;for(let[a,l]of d.entries())if(l!==o&&l.geom().left==t){l.geom().scrollWidth<o.geom().scrollWidth?(d[a]=o,s.set(l.fullname,o.fullname)):s.set(o.fullname,l.fullname),e=!1;break}e&&d.push(o)}}d.length&&o.push([i,d])}for(let[n,i]of o){i.sort(((e,t)=>e.geom().scrollWidth-t.geom().scrollWidth));let e=i.length;for(let t of i){let a=l[t.fullname];if(void 0===a)if(t.geom().scrollWidth-t.geom().el.clientWidth<n/e){const a=t.geom().scrollWidth-t.geom().el.clientWidth+35;l[t.fullname]=Math.floor(a),e--,n-=a}else l[t.fullname]=Math.floor(n/e)}}for(let[n,i]of s.entries())i in l?l[n]=l[i]:l[i]=l[n];return l}const z=(0,l.aZ)({name:"menubar",methods:{send(){k(["root",this.name])}},props:{name:{type:String,required:!0},icon:{type:String,default:""}}});var V=a(4260),O=a(3414),U=a(2035),P=a(4554),T=a(2350),I=a(7518),K=a.n(I);const R=(0,V.Z)(z,[["render",i]]),L=R;K()(z,"components",{QItem:O.Z,QItemSection:U.Z,QIcon:P.Z,QItemLabel:T.Z});const E={key:0,class:"row q-col-gutter-sm q-py-sm"},B={class:"q-col-gutter-sm q-py-sm"},F={key:0,class:"column q-col-gutter-sm q-py-sm"};function Y(e,t,a,o,s,n){const i=(0,l.up)("zone",!0),d=(0,l.up)("block");return e.data instanceof Array?((0,l.wg)(),(0,l.iD)("div",E,[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.data,(e=>((0,l.wg)(),(0,l.iD)("div",B,[e instanceof Array?((0,l.wg)(),(0,l.iD)("div",F,[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e,(e=>((0,l.wg)(),(0,l.j4)(i,{data:e},null,8,["data"])))),256))])):((0,l.wg)(),(0,l.j4)(d,{key:1,data:e},null,8,["data"]))])))),256))])):((0,l.wg)(),(0,l.j4)(d,{key:1,data:e.data},null,8,["data"]))}const N={class:"row"},J={key:2,class:"q-ma-sm",style:{"font-size":"18px"}},X=["data","pdata"],G={key:0,class:"row"},ee=["data","pdata"],te={key:0,class:"row"};function ae(e,t,a,s,n,i){const d=(0,l.up)("element"),r=(0,l.up)("q-icon"),c=(0,l.up)("q-scroll-area"),u=(0,l.up)("q-card");return(0,l.wg)(),(0,l.j4)(u,{class:"my-card q-ma-xs"},{default:(0,l.w5)((()=>[(0,l._)("div",N,[e.data.logo?((0,l.wg)(),(0,l.j4)(d,{key:0,data:e.data.logo,pdata:e.data},null,8,["data","pdata"])):e.data.icon?((0,l.wg)(),(0,l.j4)(r,{key:1,size:"sm",name:e.data.icon},null,8,["name"])):(0,l.kq)("",!0),"_"!=e.name[0]?((0,l.wg)(),(0,l.iD)("p",J,(0,o.zw)(e.name),1)):(0,l.kq)("",!0),((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.data.top_childs,(t=>((0,l.wg)(),(0,l.j4)(d,{class:"q-ma-xs",data:t,pdata:e.data},null,8,["data","pdata"])))),256))]),e.data.scroll?((0,l.wg)(),(0,l.j4)(c,{key:0,style:(0,o.j5)(e.styleSize),"thumb-style":e.thumbStyle,"bar-style":e.barStyle},{default:(0,l.w5)((()=>[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.data.childs,(t=>((0,l.wg)(),(0,l.iD)("div",{class:"column",data:t,pdata:e.data},[t instanceof Array?((0,l.wg)(),(0,l.iD)("div",G,[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(t,(t=>((0,l.wg)(),(0,l.j4)(d,{class:"q-ma-xs",data:t,pdata:e.data},null,8,["data","pdata"])))),256))])):((0,l.wg)(),(0,l.j4)(d,{key:1,class:"q-ma-xs",data:t,pdata:e.data},null,8,["data","pdata"]))],8,X)))),256))])),_:1},8,["style","thumb-style","bar-style"])):((0,l.wg)(!0),(0,l.iD)(l.HY,{key:1},(0,l.Ko)(e.data.childs,(t=>((0,l.wg)(),(0,l.iD)("div",{class:"column",data:t,pdata:e.data},[t instanceof Array?((0,l.wg)(),(0,l.iD)("div",te,[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(t,(t=>((0,l.wg)(),(0,l.j4)(d,{class:"q-ma-xs",data:t,pdata:e.data},null,8,["data","pdata"])))),256))])):((0,l.wg)(),(0,l.j4)(d,{key:1,class:"q-ma-xs",data:t,pdata:e.data},null,8,["data","pdata"]))],8,ee)))),256))])),_:1})}var le=a(8880);const oe=e=>((0,l.dD)("data-v-218719a8"),e=e(),(0,l.Cn)(),e),se=["input-style"],ne=["width","height"],ie=["src"],de={key:13,class:"web-camera-container"},re={class:"camera-button"},ce={key:0},ue={key:1},he={class:"camera-loading"},pe=oe((()=>(0,l._)("ul",{class:"loader-circle"},[(0,l._)("li"),(0,l._)("li"),(0,l._)("li")],-1))),me=[pe],ge=["height"],fe=["height"],we={key:1,class:"camera-shoot"},ye=oe((()=>(0,l._)("img",{src:"https://img.icons8.com/material-outlined/50/000000/camera--v2.png"},null,-1))),be=[ye],ke={key:2,class:"camera-download"};function ve(e,t,a,s,n,i){const d=(0,l.up)("q-icon"),r=(0,l.up)("q-img"),c=(0,l.up)("q-badge"),u=(0,l.up)("q-select"),h=(0,l.up)("q-toggle"),p=(0,l.up)("q-btn-toggle"),m=(0,l.up)("utable"),g=(0,l.up)("q-input"),f=(0,l.up)("q-tree"),w=(0,l.up)("q-scroll-area"),y=(0,l.up)("q-separator"),b=(0,l.up)("q-uploader"),k=(0,l.up)("q-btn");return"image"==e.type?((0,l.wg)(),(0,l.j4)(r,{key:0,src:e.data.name,"spinner-color":"blue",onClick:(0,le.iM)(e.switchValue,["stop"]),fit:"cover",style:(0,o.j5)(e.elemSize)},{default:(0,l.w5)((()=>[e.data.header?((0,l.wg)(),(0,l.iD)("div",{key:0,class:"absolute-bottom-right text-subtitle2 custom-caption",onClick:t[0]||(t[0]=(0,le.iM)(((...t)=>e.lens&&e.lens(...t)),["stop"]))},(0,o.zw)(e.data.header),1)):(0,l.kq)("",!0),e.value?((0,l.wg)(),(0,l.j4)(d,{key:1,class:"absolute all-pointer-events",size:"32px",name:"check_circle",color:"gray",style:{"font-size":"2em",top:"8px",left:"8px"}})):(0,l.kq)("",!0)])),_:1},8,["src","onClick","style"])):"select"==e.type?((0,l.wg)(),(0,l.j4)(u,{key:1,"transition-show":"flip-up","transition-hide":"flip-down",dense:"",modelValue:e.value,"onUpdate:modelValue":t[1]||(t[1]=t=>e.value=t),options:e.data.options},(0,l.Nv)({_:2},[e.showname?{name:"prepend",fn:(0,l.w5)((()=>[(0,l.Wm)(c,{color:"secondary"},{default:(0,l.w5)((()=>[(0,l.Uk)((0,o.zw)(e.name),1)])),_:1})]))}:void 0]),1032,["modelValue","options"])):"switch"==e.type?((0,l.wg)(),(0,l.j4)(h,{key:2,modelValue:e.value,"onUpdate:modelValue":t[2]||(t[2]=t=>e.value=t),color:"primary",label:e.nameLabel,"left-label":""},null,8,["modelValue","label"])):"radio"==e.type?((0,l.wg)(),(0,l.j4)(p,{key:3,push:"","no-caps":"",width:"400px",modelValue:e.value,"onUpdate:modelValue":t[3]||(t[3]=t=>e.value=t),options:e.data.options.map((e=>({label:e,value:e})))},{default:(0,l.w5)((()=>[e.showname?((0,l.wg)(),(0,l.j4)(c,{key:0,color:"secondary"},{default:(0,l.w5)((()=>[(0,l.Uk)((0,o.zw)(e.name),1)])),_:1})):(0,l.kq)("",!0)])),_:1},8,["modelValue","options"])):"table"==e.type?((0,l.wg)(),(0,l.j4)(m,{key:4,data:e.data,pdata:e.pdata,styleSize:e.styleSize},null,8,["data","pdata","styleSize"])):"edit"==e.type?((0,l.wg)(),(0,l.j4)(g,{key:5,modelValue:e.value,"onUpdate:modelValue":t[4]||(t[4]=t=>e.value=t),label:e.name,ref:"inputRef",autogrow:e.data.autogrow,dense:"",onKeyup:(0,le.D2)(e.pressedEnter,["enter"]),readonly:!1===e.data.edit},null,8,["modelValue","label","autogrow","onKeyup","readonly"])):"autoedit"==e.type?((0,l.wg)(),(0,l.j4)(u,{key:6,dense:"",modelValue:e.value,"onUpdate:modelValue":t[5]||(t[5]=t=>e.value=t),"use-input":"","hide-selected":"",borderless:"",outlined:"","hide-bottom-space":"","fill-input":"","input-debounce":"0",options:e.options,onFilter:e.complete,label:e.name,onKeyup:(0,le.D2)(e.pressedEnter,["enter"])},null,8,["modelValue","options","onFilter","label","onKeyup"])):"tree"==e.type||"list"==e.type?((0,l.wg)(),(0,l.j4)(w,{key:7,style:(0,o.j5)(e.styleSize),"thumb-style":e.thumbStyle,"bar-style":e.barStyle},{default:(0,l.w5)((()=>[(0,l.Wm)(f,{nodes:e.treeNodes,selected:e.value,"onUpdate:selected":t[6]||(t[6]=t=>e.value=t),"node-key":"label","default-expand-all":"","selected-color":"blue-10"},null,8,["nodes","selected"])])),_:1},8,["style","thumb-style","bar-style"])):"docviewer"==e.type?(0,l.wy)(((0,l.wg)(),(0,l.iD)("textarea",{key:8,class:"textarea","onUpdate:modelValue":t[7]||(t[7]=t=>e.value=t),filled:"",type:"textarea","input-style":e.styleSize},null,8,se)),[[le.nr,e.value]]):"line"==e.type?((0,l.wg)(),(0,l.j4)(y,{key:9,color:"green"})):"video"==e.type?((0,l.wg)(),(0,l.iD)("video",{key:10,width:e.data.width,height:e.data.height,controls:""},[(0,l._)("source",{src:e.data.src,type:"video/mp4"},null,8,ie)],8,ne)):"gallery"==e.type?((0,l.wg)(),(0,l.j4)(b,{key:11,label:e.name,"auto-upload":"",thumbnails:"",url:"http://localhost:8000",onUploaded:e.updateDom,onAdded:e.onAdded,style:{height:"40px","max-height":"40px"},ref:"uploaderRef",flat:""},null,8,["label","onUploaded","onAdded"])):"gimages"==e.type?((0,l.wg)(),(0,l.j4)(b,{key:12,label:e.name,"auto-upload":"",thumbnails:"",url:"http://localhost:8000",onUploaded:e.updateDom,onAdded:e.onAdded,ref:"uploaderRef",flat:""},null,8,["label","onUploaded","onAdded"])):"camera"==e.type?((0,l.wg)(),(0,l.iD)("div",de,[(0,l._)("div",re,[(0,l._)("button",{class:(0,o.C_)(["button is-rounded",{"is-primary":!e.isCameraOpen,"is-danger":e.isCameraOpen}]),type:"button",onClick:t[8]||(t[8]=(...t)=>e.toggleCamera&&e.toggleCamera(...t))},[e.isCameraOpen?((0,l.wg)(),(0,l.iD)("span",ue,"Close Camera")):((0,l.wg)(),(0,l.iD)("span",ce,"Open Camera"))],2)]),(0,l.wy)((0,l._)("div",he,me,512),[[le.F8,e.isCameraOpen&&e.isLoading]]),e.isCameraOpen?(0,l.wy)(((0,l.wg)(),(0,l.iD)("div",{key:0,class:(0,o.C_)(["camera-box",{flash:e.isShotPhoto}])},[(0,l._)("div",{class:(0,o.C_)(["camera-shutter",{flash:e.isShotPhoto}])},null,2),(0,l.wy)((0,l._)("video",{ref:"camera",width:450,height:337.5,autoplay:""},null,8,ge),[[le.F8,!e.isPhotoTaken]]),(0,l.wy)((0,l._)("canvas",{id:"photoTaken",ref:"canvas",width:450,height:337.5},null,8,fe),[[le.F8,e.isPhotoTaken]])],2)),[[le.F8,!e.isLoading]]):(0,l.kq)("",!0),e.isCameraOpen&&!e.isLoading?((0,l.wg)(),(0,l.iD)("div",we,[(0,l._)("button",{class:"button",type:"button",onClick:t[9]||(t[9]=(...t)=>e.takePhoto&&e.takePhoto(...t))},be)])):(0,l.kq)("",!0),e.isPhotoTaken&&e.isCameraOpen?((0,l.wg)(),(0,l.iD)("div",ke,[(0,l.Wm)(k,{onClick:e.downloadImage,label:"Send"},null,8,["onClick"])])):(0,l.kq)("",!0)])):""!=e.showname?((0,l.wg)(),(0,l.j4)(k,{key:14,"no-caps":"",label:e.name,icon:e.data.icon,onClick:e.sendValue},null,8,["label","icon","onClick"])):((0,l.wg)(),(0,l.j4)(k,{key:15,"no-caps":"",dense:"",icon:e.data.icon,onClick:e.sendValue},null,8,["icon","onClick"]))}const Ce={key:0},qe={class:"row"},_e=(0,l.Uk)("Show selected"),xe=(0,l.Uk)("Deselect all"),je=(0,l.Uk)("Delete selected"),Se=(0,l.Uk)("Multi-single select mode"),Ze=(0,l.Uk)("Edit mode"),Ae=(0,l.Uk)("Add a new row"),Me=(0,l.Uk)("Draw the chart"),De=["onClick"];function We(e,t,a,s,n,i){const d=(0,l.up)("q-icon"),r=(0,l.up)("q-input"),c=(0,l.up)("q-tooltip"),u=(0,l.up)("q-btn"),h=(0,l.up)("q-th"),p=(0,l.up)("q-tr"),m=(0,l.up)("q-checkbox"),g=(0,l.up)("q-select"),f=(0,l.up)("q-td"),w=(0,l.up)("q-table");return(0,l.wg)(),(0,l.j4)(w,{class:"my-sticky-virtscroll-table","virtual-scroll":"",dense:"",style:(0,o.j5)(e.styleSize),flat:"",filter:e.search,ref:"table",virtualScrollSliceSize:"60","rows-per-page-options":[0],"virtual-scroll-sticky-size-start":48,"row-key":"iiid",title:e.name,rows:e.rows,columns:e.columns,selection:e.singleMode?"single":"multiple",selected:e.selected,"onUpdate:selected":t[1]||(t[1]=t=>e.selected=t)},{"top-right":(0,l.w5)((()=>[!1!==e.data.tools?((0,l.wg)(),(0,l.iD)("div",Ce,[(0,l._)("div",qe,[(0,l.Wm)(r,{modelValue:e.search,"onUpdate:modelValue":t[0]||(t[0]=t=>e.search=t),label:"Search",dense:""},{prepend:(0,l.w5)((()=>[(0,l.Wm)(d,{name:"search"})])),_:1},8,["modelValue"]),(0,l._)("div",null,[(0,l.Wm)(u,{dense:"",rounded:"",icon:"select_all","no-caps":"",onClick:e.showSelected},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[_e])),_:1})])),_:1},8,["onClick"]),(0,l.Wm)(u,{dense:"",rounded:"",icon:"deselect","no-caps":"",onClick:e.deselectAll},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[xe])),_:1})])),_:1},8,["onClick"]),"delete"in e.data?((0,l.wg)(),(0,l.j4)(u,{key:0,dense:"",rounded:"",icon:"delete_forever","no-caps":"",onClick:e.delSelected},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[je])),_:1})])),_:1},8,["onClick"])):(0,l.kq)("",!0),!1!==e.data.multimode?((0,l.wg)(),(0,l.j4)(u,{key:1,dense:"",rounded:"",icon:e.singleMode?"looks_one":"grain","no-caps":"",onClick:e.switchMode},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[Se])),_:1})])),_:1},8,["icon","onClick"])):(0,l.kq)("",!0),e.editable?((0,l.wg)(),(0,l.j4)(u,{key:2,dense:"",rounded:"",icon:e.editMode?"cancel":"edit","no-caps":"",onClick:e.switchEdit},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[Ze])),_:1})])),_:1},8,["icon","onClick"])):(0,l.kq)("",!0),e.editable&&"append"in e.data?((0,l.wg)(),(0,l.j4)(u,{key:3,dense:"",rounded:"",icon:"add","no-caps":"",onClick:e.append},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[Ae])),_:1})])),_:1},8,["onClick"])):(0,l.kq)("",!0),"view"in e.data?((0,l.wg)(),(0,l.j4)(u,{key:4,dense:"",rounded:"",icon:"insights","no-caps":"",onClick:e.chart},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[Me])),_:1})])),_:1},8,["onClick"])):(0,l.kq)("",!0)])])])):(0,l.kq)("",!0)])),header:(0,l.w5)((e=>[(0,l.Wm)(p,{props:e},{default:(0,l.w5)((()=>[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.cols,(t=>((0,l.wg)(),(0,l.j4)(h,{class:"text-italic text-purple",key:t.name,props:e},{default:(0,l.w5)((()=>[(0,l.Uk)((0,o.zw)(t.label),1)])),_:2},1032,["props"])))),128))])),_:2},1032,["props"])])),body:(0,l.w5)((t=>[(0,l.Wm)(p,{props:t,onClick:e=>t.selected=!t.selected},{default:(0,l.w5)((()=>[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.columns,((a,s)=>((0,l.wg)(),(0,l.j4)(f,{key:a.name,props:t},{default:(0,l.w5)((()=>["boolean"==typeof t.row[a.name]?((0,l.wg)(),(0,l.j4)(m,{key:0,modelValue:t.row[a.name],"onUpdate:modelValue":[e=>t.row[a.name]=e,l=>e.change_switcher(t.row,a.name,s)],dense:"",disable:!e.editMode},null,8,["modelValue","onUpdate:modelValue","disable"])):e.editMode&&"complete"in e.data&&s==e.cedit&&e.redit==t.row.iiid?((0,l.wg)(),(0,l.j4)(g,{key:1,dense:"","model-value":t.row[a.name],"use-input":"","hide-selected":"","fill-input":"",autofocus:"",outlined:"",borderless:"",onInputValue:e.change,"hide-dropdown-icon":"","input-debounce":"0",options:e.options,onFilter:e.complete,onKeydown:e.keyInput},null,8,["model-value","onInputValue","options","onFilter","onKeydown"])):e.editMode&&s==e.cedit&&e.redit==t.row.iiid?((0,l.wg)(),(0,l.j4)(r,{key:2,modelValue:t.row[a.name],"onUpdate:modelValue":[e=>t.row[a.name]=e,e.change],dense:"",onKeydown:e.keyInput,autofocus:""},null,8,["modelValue","onUpdate:modelValue","onKeydown"])):((0,l.wg)(),(0,l.iD)("div",{key:3,onClick:a=>e.select(t.row.iiid,s)},(0,o.zw)(t.row[a.name]),9,De))])),_:2},1032,["props"])))),128))])),_:2},1032,["props","onClick"])])),_:1},8,["style","filter","title","rows","columns","selection","selected"])}var $e=a(1959);const He=(0,l.aZ)({name:"utable",setup(e){const{data:t,pdata:a}=(0,$e.BK)(e);let o=(0,l.Fl)((()=>{let e=[],a=t.value;const l=a.headers,o=l.length,s=a.rows,n=s.length;for(var i=0,d=0;d<n;d++){const t={},a=s[d];for(var r=0;r<o;r++)t[l[r]]=a[r];t.iiid=o==a.length?i:a[a.length-1],e.push(t),i++}return e})),s=()=>{let e=t.value;return null===e.value?[]:Array.isArray(e.value)?e.value.map((e=>o.value[e])):[o.value[e.value]]},n=s(),i=(0,$e.iH)(n),d=(0,$e.iH)(!Array.isArray(t.value.value)),r=(e,l)=>{k([a.value.name,t.value.name,e,l])},c=(0,l.Fl)((()=>d.value?i.value.length>0?i.value[0].iiid:null:i.value.map((e=>e.iiid)))),u=(0,l.Fl)((()=>t.value.value));return(0,l.YP)(o,((e,t)=>{i.value=s(),n=i.value})),(0,l.YP)(t,((e,a)=>{h&&console.log("data update",a.name),i.value=s(),n=i.value,d.value=!Array.isArray(t.value.value)})),(0,l.YP)(i,(e=>{n!==i.value&&(n=i.value,r("=",c.value))})),{rows:o,value:c,selected:i,singleMode:d,sendMessage:r,datavalue:u}},data(){return{search:"",editMode:!1,options:[],cedit:null}},methods:{select(e,t){this.editMode&&(this.cedit=t,h&&console.log("selected",e,this.cedit))},change_switcher(e,t,a){if(console.log(e,t,a,e[t]),this.editMode){this.cedit=a;const l=e.iiid;let o=this.data.rows;o[l][a]=e[t],this.sendMessage("#",[e[t],[l,a]])}},change(e){if(h&&console.log("changed",this.data.headers[this.cedit],e),this.editMode&&this.selected.length){const t=this.selected[0].iiid;let a=this.rows;a[t][this.data.headers[this.cedit]]=e,this.sendMessage("#",[e,[t,this.cedit]])}},keyInput(e){if("Control"!=e.key)switch(h&&console.log("keypress",e),e.key){case"Enter":"update"in this.data&&this.sendMessage("->",[this.data.rows[this.redit][this.cedit],[this.redit,this.cedit]]);break;case"Escape":this.switchEdit();break;case"ArrowLeft":if(e.ctrlKey)for(let e=this.cedit-1;e>=0;e--){let t=typeof this.data.rows[this.redit][e];if("string"==t||"number"==t){this.cedit=e;break}}break;case"ArrowRight":if(e.ctrlKey)for(let e=this.cedit+1;e<this.data.rows[this.redit].length;e++){let t=typeof this.data.rows[this.redit][e];if("string"==t||"number"==t){this.cedit=e;break}}break;case"ArrowUp":if(e.ctrlKey&&this.redit>0){let e=this.redit-1,t=typeof this.data.rows[e][this.cedit];"string"!=t&&"number"!=t||(this.selected=[this.rows[e]])}break;case"ArrowDown":if(e.ctrlKey&&this.redit+1<this.rows.length){let e=this.redit+1,t=typeof this.data.rows[e][this.cedit];"string"!=t&&"number"!=t||(this.selected=[this.rows[e]])}break}},complete(e,t,a){x(this,[e,[this.redit,this.cedit]],(e=>t((()=>{this.options=e}))))},append(){let e=this.data.rows,t=e.length,a=this;x(this,[t,this.search],(function(l){if(!Array.isArray(l))return c.error(l);h&&console.log("added row",l),a.search="",e.push(l),setTimeout((()=>{let e=a.rows;a.select(e[t],0),a.showSelected()}),100)}),"+")},showSelected(){let e=this.$refs.table;this.selected&&e.scrollTo(e.computedRows.findIndex((e=>e===this.selected[0])))},deselectAll(){this.selected=[],this.sendMessage("=",this.value)},chart(){},switchMode(){this.singleMode=!this.singleMode,this.singleMode&&this.selected.length>1&&this.selected.splice(1)},switchEdit(){this.editMode=!this.editMode,this.sendMessage("!",this.editMode),this.editMode&&!this.singleMode&&this.switchMode()},delSelected(){if(!this.selected.length)return void c.error("Rows are not selected!");this.sendMessage("-",this.value);let e=this.data.rows;if(this.singleMode)e.splice(this.selected[0].iiid,1);else{this.selected.length>1&&this.selected.sort(((e,t)=>t.iiid-e.iiid));for(let t of this.selected)e.splice(t.iiid,1)}this.selected=[]}},computed:{redit(){return console.log("redit",this.editMode&&this.selected.length?this.selected[0].iiid:null),this.editMode&&this.selected.length?this.selected[0].iiid:null},editable(){return 0!=this.data["edit"]},name(){return"_"==this.data.name?"":this.data.name},columns(){return this.data.headers.map((e=>({name:e,label:e,align:"left",sortable:!0,field:e})))}},props:{data:Object,pdata:Object,styleSize:String}});var Qe=a(4993),ze=a(4842),Ve=a(8240),Oe=a(8870),Ue=a(8186),Pe=a(2414),Te=a(3884),Ie=a(5735),Ke=a(7208);const Re=(0,V.Z)(He,[["render",We]]),Le=Re;function Ee(e){let t=new FormData;t.append("image",e);let a=new XMLHttpRequest;a.open("POST","http://localhost:8000",!0),a.onload=function(){200===this.status?console.log(this.response):console.error(a)},a.send(t)}K()(He,"components",{QTable:Qe.Z,QInput:ze.Z,QIcon:P.Z,QBtn:Ve.Z,QTooltip:Oe.Z,QTr:Ue.Z,QTh:Pe.Z,QTd:Te.Z,QCheckbox:Ie.Z,QSelect:Ke.Z});const Be=(0,l.aZ)({name:"element",components:{utable:Le},methods:{log(e){console.log(e)},onAdded(e){0!==e.length&&(0!==this.fileArr.length?(this.$refs.uploaderRef.removeFile(this.fileArr[0]),this.fileArr.splice(0,1,e[0])):this.fileArr.push(e[0]))},sendMessage(e,t){k([this.pdata["name"],this.data["name"],e,t])},pressedEnter(){"update"in this.data&&this.sendMessage("->",this.value)},updateDom(e){let t=e.files.length;t&&(this.sendMessage("=",e.files[t-1].name),$())},sendValue(){this.sendMessage("=",this.value)},switchValue(){this.value=!this.value},setValue(e){console.log(e),this.value=e},complete(e,t,a){this.value=e,x(this,e,(e=>t((()=>{this.options=e}))))},lens(){c.lens(this.data)},toggleCamera(){this.isCameraOpen?(this.isCameraOpen=!1,this.isPhotoTaken=!1,this.isShotPhoto=!1,this.stopCameraStream()):(this.isCameraOpen=!0,this.createCameraElement())},createCameraElement(){this.isLoading=!0;const e=window.constraints={audio:!1,video:!0};navigator.mediaDevices.getUserMedia(e).then((e=>{this.isLoading=!1,this.$refs.camera.srcObject=e})).catch((e=>{this.isLoading=!1,alert("May the browser didn't support or there is some errors.")}))},stopCameraStream(){let e=this.$refs.camera.srcObject.getTracks();e.forEach((e=>{e.stop()}))},takePhoto(){if(!this.isPhotoTaken){this.isShotPhoto=!0;const e=50;setTimeout((()=>{this.isShotPhoto=!1}),e)}this.isPhotoTaken=!this.isPhotoTaken;const e=this.$refs.canvas.getContext("2d");e.drawImage(this.$refs.camera,0,0,450,337.5)},downloadImage(){document.getElementById("downloadPhoto"),document.getElementById("photoTaken").toBlob(Ee,"image/jpeg")},geom(){const e="clientHeight"in this.$el?this.$el:this.$el.nextElementSibling,t=e.querySelector("table"==this.type?".scroll":".q-tree"),a=e.getBoundingClientRect();return{el:e,inner:t,left:a.left,right:a.right,top:a.top,scrollHeight:t.scrollHeight,scrollWidth:t.scrollWidth}}},mounted(){w[this.fullname]=this,h&&console.log("mounted",this.fullname)},data(){return{value:this.data.value,styleSize:g,options:[],thumbStyle:{right:"4px",borderRadius:"7px",backgroundColor:"#027be3",width:"4px",opacity:.75},barStyle:{right:"2px",borderRadius:"9px",backgroundColor:"#027be3",width:"8px",opacity:.2},updated:"#027be3sds",isCameraOpen:!1,isPhotoTaken:!1,isShotPhoto:!1,isLoading:!1,link:"#",fileArr:[]}},computed:{elemSize(){let e="";return this.data.width&&(e=`width : ${this.data.width}px`),this.data.height&&(""!=e&&(e+="; "),e+=`height: ${this.data.height}px`),console.log(e),""==e?g:e},name(){return this.data.name},fullname(){return`${this.data.name}@${this.pdata.name}`},showname(){return"_"!=this.data.name[0]},nameLabel(){return this.data.label?this.data.label:"_"!=this.data.name[0]?this.data.name:""},text(){return this.data.text},expanding(){let e=this.type;return"tree"==e||"table"==e||"list"==e},selection(){return this.data.selection},icon(){return this.data.icon},type(){var e=this.data.type;if(e)return e;const t=this.data,a=t.options;return a?a.length>3?"select":"radio":t.headers?"table":(e=typeof this.value,"number"==e||"string"==e?void 0!==t.complete?"autoedit":"edit":"boolean"==e?"switch":"button")},treeNodes(){var e=[];if("list"==this.type)return this.data.options.map((e=>({label:e,children:[]})));for(var t=[],a=0;a<this.data.options.length;a++){var l=this.data.options[a][0].toString(),o=0;for(let e of l){if(e.toLowerCase()!=e.toUpperCase())break;o++}var s={label:l.substr(o),children:[]};while(t.length>o)t.pop();t.length?t[t.length-1].children.push(s):e.push(s),t.push(s)}return e}},props:{data:{type:Object,required:!0},pdata:{type:Object,required:!0}},watch:{value(e,t){e!==this.updated&&(h&&console.log("value changed",e,t),this.sendValue(),this.updated=e)},selection(e){h&&console.log("selection changed",e,this.$refs.inputRef),Array.isArray(e)||(e=[0,0]);let t=this.$refs.inputRef.$el;t.focus();let a=t.getElementsByTagName("textarea");0==a.length&&(a=t.getElementsByTagName("input")),a[0].setSelectionRange(e[0],e[1])},data(e,t){h&&console.log("data update",this.fullname,t.name),this.expanding&&(this.styleSize=g),this.value=this.data.value,this.updated=this.value,w[this.fullname]=this}}});var Fe=a(4027),Ye=a(9721),Ne=a(8886),Je=a(8761),Xe=a(7704),Ge=a(5551),et=a(5869),tt=a(3768);const at=(0,V.Z)(Be,[["render",ve],["__scopeId","data-v-218719a8"]]),lt=at;K()(Be,"components",{QImg:Fe.Z,QIcon:P.Z,QSelect:Ke.Z,QBadge:Ye.Z,QToggle:Ne.Z,QBtnToggle:Je.Z,QInput:ze.Z,QScrollArea:Xe.Z,QTree:Ge.Z,QSeparator:et.Z,QUploader:tt.Z,QBtn:Ve.Z});const ot=(0,l.aZ)({name:"block",components:{element:lt},data(){return{styleSize:g,thumbStyle:{right:"4px",borderRadius:"7px",backgroundColor:"#027be3",width:"4px",opacity:.75},barStyle:{right:"2px",borderRadius:"9px",backgroundColor:"#027be3",width:"8px",opacity:.2}}},methods:{log(){console.log(Object.keys(f).length,this.name,this.$el.getBoundingClientRect())},geom(){let e="clientHeight"in this.$el?this.$el:this.$el.nextElementSibling;const t=e.querySelector(".q-scrollarea"),a=e.getBoundingClientRect();return{el:e,inner:t,left:a.left,right:a.right,top:a.top,scrollHeight:window.innerHeight,scrollWidth:window.innerWidth}}},mounted(){f[this.name]=this,this.expanding&&(w[this.fullname]=this)},computed:{name(){return this.data.name},fullname(){return`_scroll@${this.name}`},icon(){return this.data.icon},expanding(){return this.data.scroll}},props:{data:{type:Object,required:!0}},watch:{data(e){h&&console.log("data update",this.name),this.styleSize=g,f[this.name]=this,this.expanding&&(w[this.fullname]=this)}}});var st=a(151);const nt=(0,V.Z)(ot,[["render",ae]]),it=nt;K()(ot,"components",{QCard:st.Z,QIcon:P.Z,QScrollArea:Xe.Z});const dt=(0,l.aZ)({name:"zone",components:{block:it},props:{data:Object}}),rt=(0,V.Z)(dt,[["render",Y]]),ct=rt,ut={class:"row q-gutter-sm row-md"};function ht(e,t,a,s,n,i){const d=(0,l.up)("block"),r=(0,l.up)("q-space"),c=(0,l.up)("q-btn"),u=(0,l.up)("q-card"),h=(0,l.up)("q-dialog");return(0,l.wg)(),(0,l.j4)(h,{ref:"dialog",onHide:i.onDialogHide},{default:(0,l.w5)((()=>[(0,l.Wm)(u,{class:"q-dialog-plugin q-pa-md items-start q-gutter-md",bordered:"",style:(0,o.j5)(a.data.internal?"width: 800px; max-width: 80vw;":"")},{default:(0,l.w5)((()=>[a.data?((0,l.wg)(),(0,l.j4)(d,{key:0,data:a.data},null,8,["data"])):(0,l.kq)("",!0),(0,l._)("div",ut,[(0,l.Wm)(r),((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(a.buttons,(e=>((0,l.wg)(),(0,l.j4)(c,{class:"col-md-3",label:e,color:a.buttons[0]==e?"primary":"secondary",onClick:t=>i.sendMessage(e)},null,8,["label","color","onClick"])))),256))])])),_:1},8,["style"])])),_:1},8,["onHide"])}const pt={props:{data:Object,buttons:Array},components:{block:it},emits:["ok","hide"],methods:{show(){this.$refs.dialog.show()},sendMessage(e){this.data.internal||k([this.data["name"],e]),this.hide()},hide(){this.$refs.dialog.hide()},onDialogHide(){this.$emit("hide")},onOKClick(){this.$emit("ok"),this.hide()},onCancelClick(){this.hide()}}};var mt=a(6778),gt=a(2025);const ft=(0,V.Z)(pt,[["render",ht]]),wt=ft;K()(pt,"components",{QDialog:mt.Z,QCard:st.Z,QSpace:gt.Z,QBtn:Ve.Z});a(8603);var yt=!0;let bt=null;const kt=(0,l.aZ)({name:"MainLayout",data(){return{leftDrawerOpen:!1,menu:[],tab:"",localServer:!0,statusConnect:!1,screen:{blocks:[]},prevHeight:0}},components:{menubar:L,zone:ct},created(){b(this)},unmounted(){window.removeEventListener("resize",this.onResize)},methods:{toggleLeftDrawer(){this.leftDrawerOpen=!this.leftDrawerOpen},tabclick(e){k(["root",e])},onResize(e){const t=e.currentTarget.innerHeight;this.prevHeight!=t&&(h&&console.log("window has been resized",t,window.innerHeight),this.prevHeight=t,$())},lens(e){let t={title:"Photo lens",message:e.text,cancel:!0,persistent:!0,component:wt},{height:a,...l}=e;l.width=750;let o={name:`Picture lens of ${e.name}`,top_childs:[],childs:[l],internal:!0};t.componentProps={data:o,buttons:["Close"]},this.$q.dialog(t)},notify(e,t){let a=t,l={message:e,type:t,position:"top",icon:a};"progress"==t?null==bt?(l={group:!1,timeout:0,spinner:!0,type:"info",message:e||"Progress..",position:"top",color:"secondary"},bt=this.$q.notify(l)):null==e?(bt(),bt=null):(l={caption:e},bt(l)):("error"==t&&l.type,this.$q.notify(l))},error(e){this.notify(e,"error")},info(e){this.notify(e,"info")},processMessage(e){if(yt)yt=!1,this.menu=e[0].map((e=>({name:e[0],icon:e[1],order:e[2]}))),this.screen=e[1],this.tab=this.screen.name,h&&console.log("init loading..");else if("screen"==e.type)j(),W(),this.screen=e;else if("dialog"==e.type){let t={title:e.name,message:e.text,cancel:!0,persistent:!0};e.content&&(t.component=wt,t.componentProps={data:e.content,buttons:e.buttons}),this.$q.dialog(t).onOk((()=>{k(["root",!0])})).onCancel((()=>{k(["root",!1])}))}else if(e.hasOwnProperty("answer"))A(e);else{e.update&&Z(e);let t=!1;for(let a of y)a in e&&(this.notify(e[a],a),t=!0);t||e.update||(this.error("Invalid data came from the server! Look the console."),console.log(`Invalid data came from the server! ${e}`))}bt&&!e.progress&&this.notify(null,"progress")}},mounted(){W(),window.addEventListener("resize",this.onResize)},beforeUpdate(){h&&(console.log("before updated"),console.log($()))}});var vt=a(9214),Ct=a(3812),qt=a(9570),_t=a(7547),xt=a(3269),jt=a(2901),St=a(7011),Zt=a(2652),At=a(4379);const Mt=(0,V.Z)(kt,[["render",n]]),Dt=Mt;K()(kt,"components",{QLayout:vt.Z,QHeader:Ct.Z,QToolbar:qt.Z,QBtn:Ve.Z,QItemLabel:T.Z,QTabs:_t.Z,QTab:xt.Z,QDrawer:jt.Z,QList:St.Z,QPageContainer:Zt.Z,QPage:At.Z})}}]);