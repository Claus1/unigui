"use strict";(globalThis["webpackChunkuniqua"]=globalThis["webpackChunkuniqua"]||[]).push([[544],{7544:(e,t,a)=>{a.r(t),a.d(t,{default:()=>Zt});var l=a(3673),s=a(2323);const o=(0,l._)("div",{class:"q-pa-lg"},null,-1);function n(e,t,a,n,i,d){const r=(0,l.up)("q-item-label"),c=(0,l.up)("q-tab"),h=(0,l.up)("q-tabs"),u=(0,l.up)("q-toolbar"),p=(0,l.up)("q-header"),g=(0,l.up)("zone"),m=(0,l.up)("q-page"),f=(0,l.up)("q-page-container"),w=(0,l.up)("q-layout");return(0,l.wg)(),(0,l.j4)(w,{view:"lHh Lpr lFf"},{default:(0,l.w5)((()=>[(0,l.Wm)(p,{elevated:""},{default:(0,l.w5)((()=>[(0,l.Wm)(u,null,{default:(0,l.w5)((()=>[(0,l.Wm)(r,{class:"text-h5"},{default:(0,l.w5)((()=>[(0,l.Uk)((0,s.zw)(e.screen.header?e.screen.header:""),1)])),_:1}),o,(0,l.Wm)(h,{class:"text-teal",align:"center","inline-label":"",dense:"",modelValue:e.tab,"onUpdate:modelValue":t[0]||(t[0]=t=>e.tab=t),style:{float:"center"}},{default:(0,l.w5)((()=>[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.menu,(t=>((0,l.wg)(),(0,l.j4)(c,{class:"justify-center text-white shadow-2",name:t.name,icon:t.icon,label:t.name,onClick:a=>e.tabclick(t.name)},null,8,["name","icon","label","onClick"])))),256))])),_:1},8,["modelValue"])])),_:1})])),_:1}),(0,l.Wm)(f,null,{default:(0,l.w5)((()=>[(0,l.Wm)(m,{class:"flex q-pa-sm justify-center centers"},{default:(0,l.w5)((()=>[(0,l.Wm)(g,{data:e.screen.blocks},null,8,["data"])])),_:1})])),_:1})])),_:1})}a(71);function i(e,t,a,o,n,i){const d=(0,l.up)("q-icon"),r=(0,l.up)("q-item-section"),c=(0,l.up)("q-item-label"),h=(0,l.up)("q-item");return(0,l.wg)(),(0,l.j4)(h,{clickable:"",tag:"a",target:"_blank",onClick:e.send},{default:(0,l.w5)((()=>[(0,l.Wm)(r,{avatar:""},{default:(0,l.w5)((()=>[(0,l.Wm)(d,{name:e.icon},null,8,["name"])])),_:1}),(0,l.Wm)(r,null,{default:(0,l.w5)((()=>[(0,l.Wm)(c,null,{default:(0,l.w5)((()=>[(0,l.Uk)((0,s.zw)(e.name),1)])),_:1})])),_:1})])),_:1},8,["onClick"])}var d,r=a(698),c=a(8603),h=a.n(c);let u=null,p={},g=!0;const m=136,f=400,w=`height: ${m}px; width: ${f}px`,y={},b={},k=["error","progress","warning","info"];function v(e){d=new WebSocket("ws://localhost:8000/ws"),d.onopen=()=>e.statusConnect=!0,d.onmessage=t=>{g&&console.log("socket message",t.data),e.processMessage(JSON.parse(t.data))},d.onerror=t=>e.error(t),d.onclose=t=>{t.wasClean?e.info("Connection closed and was clean."):e.error("Connection suddenly closed!"),e.statusConnect=!1,g&&console.info("close code : "+t.code+" reason: "+t.reason)},u=e}function q(e){console.log("sended",e),d.send(JSON.stringify(e))}let C,_=0;function x(e){for(var t in e)e.hasOwnProperty(t)&&delete e[t]}function S(e,t,a,l="?"){let s=++_,o=[e.pdata.name,e.data.name,l,t,s];q(o),p[s]=a}function j(){x(y),x(b)}function A(e,t){Object.assign(e.data,t),e.updated=t.value,e.value=t.value}function Z(e){if(e.multi)for(let[t,a]of e.update.entries())if(a.length>1){a.reverse();let l=a.join("@"),s=b[l];A(s,e.data[t])}else{let l=y[a[0]];Object.assign(l.data,e.data[t])}else{let t,a=e.update;if(a.length>1){a.reverse();let e=a.join("@");t=b[e]}else t=y[a[0]];A(t,e.data),1==a.length&&h().delay($,200,t)}}function M(e){typeof e.answer==String?u.showError():p[e.id](e.answer),delete p[e.id]}function D(e){let t=[];for(let l of e)l instanceof Array?t.push(l):t.push([l]);let a=t.shift();return t.reduce(((e,t)=>e.flatMap((e=>t.map((t=>e instanceof Array?[...e,t]:[e,t]))))),a)}let z=h().debounce($,200);const Q={childList:!0,subtree:!0,attributes:!0};function W(){C&&(C.disconnect(),C=null),C=new MutationObserver(z),C.observe(u.$el,Q)}function $(e){Array.isArray(e)&&(e=null),C&&(C.disconnect(),C=null),g&&console.log("------------------recalc design");const t=V(e),a=O(e);for(let[l,s]of Object.entries(t)){let e=b[l];const[t,o]=a[l];let n,i=e.geom().el,d=e.pdata?e.pdata.name:e.name,r=y[d];for(let a of r.data.childs)if(Array.isArray(a)){if(a.find((t=>t.name==e.data.name))){let e=a[a.length-1],t=`${e.name}@${d}`;n=b[t];break}}else if(a.name==e.data.name){n=e;break}let c=r.data.width?r.data.width-i.clientWidth-t:r.$el.getBoundingClientRect().right-(n?n.geom().right:e.geom().right);c/=o;let h=l.startsWith("_scroll@")?e.geom().inner.clientHeight:i.clientHeight;e.styleSize=`height: ${h+s}px; width: ${i.clientWidth+c+t}px;`}}function V(e){const t=u.screen.blocks;let a=window.innerHeight;a-=10;let l={},s=new Map,o={};for(let[d,r]of Object.entries(y))o[r.name]=r.$el.getBoundingClientRect().height;let n=[];for(let d of t){const e=[];let t=d instanceof Array,i=t?D(d):[[d]];for(let a of i){let e=0;for(let t of a)e+=o[t.name]+8;n.push([e,a])}n.sort(((e,t)=>e[0]>t[0]?-1:e[0]==t[0]?0:1));for(let l of n){let t=l[1];(0,r.hu)(Array.isArray(t));const o=[];for(let[e,a]of Object.entries(b))if(a.expanding_height){let[l,n]=e.split("@");if(t.find((e=>e.name==n))){let e=!0;const t=a.geom();for(let[l,n]of o.entries()){let i=n.geom();if(n!==a&&i.top==t.top){i.scrollHeight<t.scrollHeight&&(o[l]=a),e=!1,s.set(a.fullname,n.fullname);break}}e&&o.push(a)}}o.length&&e.push([a-l[0]-64,o])}for(let[a,s]of e){s.sort(((e,t)=>e.geom().scrollHeight<t.geom().scrollHeight));let e=s.length;for(let t of s)t.fullname in l&&(e--,a-=l[t.fullname]);for(let t of s)t.fullname in l||("docviewer"==t.type?l[t.fullname]=a/e+4:l[t.fullname]=a/e)}}let i=Array.from(s.entries());i.sort(((e,t)=>e[0]in l||e[1]in l?-1:1));for(let[d,r]of i)r in l?l[d]=l[r]:l[r]=l[d];return l}function O(e){e=null;const t=e?[e]:u.screen.blocks;let a=window.innerWidth-30,l=[],s={};for(let i of t)if(0==l.length)if(Array.isArray(i))for(let e of i)l.push(Array.isArray(e)?e:[e]);else l=[[i]];else{let e=[];if(Array.isArray(i))for(let t of i)for(let a of l)e.push(Array.isArray(t)?a.concat(t):[...a,t]);else for(let t of l)e.push([...t,i]);l=e}l.sort(((e,t)=>e.length>t.length?-1:e.length==t.length?0:1));const o=[];let n=new Map;for(let i of l){let e=Array.isArray(i)?i[i.length-1]:i,t=y[e.name].$el.getBoundingClientRect().right;e=Array.isArray(i)?i[0]:i;let l=y[e.name].$el.getBoundingClientRect().left,s=a-t+l-10;const d=[];for(let[a,o]of Object.entries(b))if(o.expanding_width){let e=a.split("@")[1];if(i.find((t=>t.name==e))){let e=!0,t=o.geom().left;for(let[a,l]of d.entries())if(l!==o&&l.geom().left==t){l.geom().scrollWidth<o.geom().scrollWidth?(d[a]=o,n.set(l.fullname,o.fullname)):n.set(o.fullname,l.fullname),e=!1;break}e&&d.push(o)}}d.length&&o.push([s,d])}for(let[i,d]of o){d.sort(((e,t)=>e.geom().scrollWidth-t.geom().scrollWidth));let e=d.length,t={};for(let a of d){let l=s[a.fullname];l&&(e--,i-=l[0]/l[1]);let o=a.pdata?a.pdata.name:a.name;t[o]?t[o]++:t[o]=1}for(let a of d){let l=s[a.fullname];if(void 0===l){let l=a.pdata?a.pdata.name:a.name;s[a.fullname]=[Math.floor(i/e),t[l]]}}}for(let[i,d]of n.entries())d in s?s[i]=s[d]:s[d]=s[i];return s}const E=(0,l.aZ)({name:"menubar",methods:{send(){q(["root",this.name])}},props:{name:{type:String,required:!0},icon:{type:String,default:""}}});var H=a(4260),U=a(3414),P=a(2035),T=a(4554),I=a(2350),N=a(7518),R=a.n(N);const K=(0,H.Z)(E,[["render",i]]),L=K;R()(E,"components",{QItem:U.Z,QItemSection:P.Z,QIcon:T.Z,QItemLabel:I.Z});const B={key:0,class:"row q-col-gutter-sm q-py-sm"},Y={class:"q-col-gutter-sm q-py-sm"},F={key:0,class:"column q-col-gutter-sm q-py-sm"};function J(e,t,a,s,o,n){const i=(0,l.up)("zone",!0),d=(0,l.up)("block");return e.data instanceof Array?((0,l.wg)(),(0,l.iD)("div",B,[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.data,(e=>((0,l.wg)(),(0,l.iD)("div",Y,[e instanceof Array?((0,l.wg)(),(0,l.iD)("div",F,[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e,(e=>((0,l.wg)(),(0,l.j4)(i,{data:e},null,8,["data"])))),256))])):((0,l.wg)(),(0,l.j4)(d,{key:1,data:e},null,8,["data"]))])))),256))])):((0,l.wg)(),(0,l.j4)(d,{key:1,data:e.data},null,8,["data"]))}const G={class:"row"},X={key:2,class:"q-ma-sm",style:{"font-size":"18px"}},ee=["data","pdata"],te={key:0,class:"row"},ae=["data","pdata"],le={key:0,class:"row"};function se(e,t,a,o,n,i){const d=(0,l.up)("element"),r=(0,l.up)("q-icon"),c=(0,l.up)("q-scroll-area"),h=(0,l.up)("q-card");return(0,l.wg)(),(0,l.j4)(h,{class:"my-card q-ma-xs"},{default:(0,l.w5)((()=>[(0,l._)("div",G,[e.data.logo?((0,l.wg)(),(0,l.j4)(d,{key:0,data:e.data.logo,pdata:e.data},null,8,["data","pdata"])):e.data.icon?((0,l.wg)(),(0,l.j4)(r,{key:1,size:"sm",name:e.data.icon},null,8,["name"])):(0,l.kq)("",!0),"_"!=e.name[0]?((0,l.wg)(),(0,l.iD)("p",X,(0,s.zw)(e.name),1)):(0,l.kq)("",!0),((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.data.top_childs,(t=>((0,l.wg)(),(0,l.j4)(d,{class:"q-ma-xs",data:t,pdata:e.data},null,8,["data","pdata"])))),256))]),e.data.scroll?((0,l.wg)(),(0,l.j4)(c,{key:0,style:(0,s.j5)(e.styleSize),"thumb-style":e.thumbStyle,"bar-style":e.barStyle},{default:(0,l.w5)((()=>[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.data.childs,(t=>((0,l.wg)(),(0,l.iD)("div",{class:"column",data:t,pdata:e.data},[t instanceof Array?((0,l.wg)(),(0,l.iD)("div",te,[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(t,(t=>((0,l.wg)(),(0,l.j4)(d,{class:"q-ma-xs",data:t,pdata:e.data},null,8,["data","pdata"])))),256))])):((0,l.wg)(),(0,l.j4)(d,{key:1,class:"q-ma-xs",data:t,pdata:e.data},null,8,["data","pdata"]))],8,ee)))),256))])),_:1},8,["style","thumb-style","bar-style"])):((0,l.wg)(!0),(0,l.iD)(l.HY,{key:1},(0,l.Ko)(e.data.childs,(t=>((0,l.wg)(),(0,l.iD)("div",{class:"column",data:t,pdata:e.data},[t instanceof Array?((0,l.wg)(),(0,l.iD)("div",le,[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(t,(t=>((0,l.wg)(),(0,l.j4)(d,{class:"q-ma-xs",data:t,pdata:e.data},null,8,["data","pdata"])))),256))])):((0,l.wg)(),(0,l.j4)(d,{key:1,class:"q-ma-xs",data:t,pdata:e.data},null,8,["data","pdata"]))],8,ae)))),256))])),_:1})}var oe=a(8880);const ne=e=>((0,l.dD)("data-v-424a81a0"),e=e(),(0,l.Cn)(),e),ie=["width","height"],de=["src"],re={key:15,class:"web-camera-container"},ce={class:"camera-button"},he={key:0},ue={key:1},pe={class:"camera-loading"},ge=ne((()=>(0,l._)("ul",{class:"loader-circle"},[(0,l._)("li"),(0,l._)("li"),(0,l._)("li")],-1))),me=[ge],fe=["height"],we=["height"],ye={key:1,class:"camera-shoot"},be=ne((()=>(0,l._)("img",{src:"https://img.icons8.com/material-outlined/50/000000/camera--v2.png"},null,-1))),ke=[be],ve={key:2,class:"camera-download"};function qe(e,t,a,o,n,i){const d=(0,l.up)("q-icon"),r=(0,l.up)("q-img"),c=(0,l.up)("q-badge"),h=(0,l.up)("q-select"),u=(0,l.up)("q-checkbox"),p=(0,l.up)("q-toggle"),g=(0,l.up)("q-btn-toggle"),m=(0,l.up)("utable"),f=(0,l.up)("q-input"),w=(0,l.up)("q-tree"),y=(0,l.up)("q-scroll-area"),b=(0,l.up)("q-separator"),k=(0,l.up)("q-uploader"),v=(0,l.up)("ugraph"),q=(0,l.up)("q-btn");return"image"==e.type?((0,l.wg)(),(0,l.j4)(r,{key:0,src:e.data.name,"spinner-color":"blue",onClick:(0,oe.iM)(e.switchValue,["stop"]),fit:"cover",style:(0,s.j5)(e.elemSize)},{default:(0,l.w5)((()=>[e.data.header?((0,l.wg)(),(0,l.iD)("div",{key:0,class:"absolute-bottom-right text-subtitle2 custom-caption",onClick:t[0]||(t[0]=(0,oe.iM)(((...t)=>e.lens&&e.lens(...t)),["stop"]))},(0,s.zw)(e.data.header),1)):(0,l.kq)("",!0),e.value?((0,l.wg)(),(0,l.j4)(d,{key:1,class:"absolute all-pointer-events",size:"32px",name:"check_circle",color:"gray",style:{"font-size":"2em",top:"8px",left:"8px"}})):(0,l.kq)("",!0)])),_:1},8,["src","onClick","style"])):"select"==e.type?((0,l.wg)(),(0,l.j4)(h,{key:1,"transition-show":"flip-up","transition-hide":"flip-down",dense:"",modelValue:e.value,"onUpdate:modelValue":t[1]||(t[1]=t=>e.value=t),options:e.data.options},(0,l.Nv)({_:2},[e.showname?{name:"prepend",fn:(0,l.w5)((()=>[(0,l.Wm)(c,{color:"secondary"},{default:(0,l.w5)((()=>[(0,l.Uk)((0,s.zw)(e.name),1)])),_:1})])),key:"0"}:void 0]),1032,["modelValue","options"])):"check"==e.type?((0,l.wg)(),(0,l.j4)(u,{key:2,"left-label":"",modelValue:e.value,"onUpdate:modelValue":t[2]||(t[2]=t=>e.value=t),label:e.nameLabel,"checked-icon":"task_alt","unchecked-icon":"highlight_off"},null,8,["modelValue","label"])):"switch"==e.type?((0,l.wg)(),(0,l.j4)(p,{key:3,modelValue:e.value,"onUpdate:modelValue":t[3]||(t[3]=t=>e.value=t),color:"primary",label:e.nameLabel,"left-label":""},null,8,["modelValue","label"])):"radio"==e.type?((0,l.wg)(),(0,l.j4)(g,{key:4,push:"","no-caps":"",width:"400px",modelValue:e.value,"onUpdate:modelValue":t[4]||(t[4]=t=>e.value=t),options:e.data.options.map((e=>({label:e,value:e})))},{default:(0,l.w5)((()=>[e.showname?((0,l.wg)(),(0,l.j4)(c,{key:0,color:"secondary"},{default:(0,l.w5)((()=>[(0,l.Uk)((0,s.zw)(e.name),1)])),_:1})):(0,l.kq)("",!0)])),_:1},8,["modelValue","options"])):"table"==e.type?((0,l.wg)(),(0,l.j4)(m,{key:5,data:e.data,pdata:e.pdata,styleSize:e.styleSize},null,8,["data","pdata","styleSize"])):"edit"==e.type?((0,l.wg)(),(0,l.j4)(f,{key:6,modelValue:e.value,"onUpdate:modelValue":t[5]||(t[5]=t=>e.value=t),label:e.name,ref:"inputRef",autogrow:e.data.autogrow,dense:"",onKeyup:(0,oe.D2)(e.pressedEnter,["enter"]),readonly:!1===e.data.edit},null,8,["modelValue","label","autogrow","onKeyup","readonly"])):"autoedit"==e.type?((0,l.wg)(),(0,l.j4)(h,{key:7,dense:"",modelValue:e.value,"onUpdate:modelValue":t[6]||(t[6]=t=>e.value=t),"use-input":"","hide-selected":"",borderless:"",outlined:"","hide-bottom-space":"","fill-input":"","input-debounce":"0",options:e.options,onFilter:e.complete,label:e.name,onKeyup:(0,oe.D2)(e.pressedEnter,["enter"])},null,8,["modelValue","options","onFilter","label","onKeyup"])):"tree"==e.type||"list"==e.type?((0,l.wg)(),(0,l.j4)(y,{key:8,style:(0,s.j5)(e.styleSize),"thumb-style":e.thumbStyle,"bar-style":e.barStyle},{default:(0,l.w5)((()=>[(0,l.Wm)(w,{nodes:e.treeNodes,selected:e.value,"onUpdate:selected":t[7]||(t[7]=t=>e.value=t),"node-key":"label","default-expand-all":"","selected-color":"blue-10"},null,8,["nodes","selected"])])),_:1},8,["style","thumb-style","bar-style"])):"docviewer"==e.type?(0,l.wy)(((0,l.wg)(),(0,l.iD)("textarea",{key:9,class:"textarea","onUpdate:modelValue":t[8]||(t[8]=t=>e.value=t),filled:"",type:"textarea",style:(0,s.j5)(e.elemSize)},null,4)),[[oe.nr,e.value]]):"line"==e.type?((0,l.wg)(),(0,l.j4)(b,{key:10,color:"green"})):"video"==e.type?((0,l.wg)(),(0,l.iD)("video",{width:e.data.width,height:e.data.height,key:e.data.src,controls:""},[(0,l._)("source",{src:e.data.src,type:"video/mp4"},null,8,de)],8,ie)):"gallery"==e.type?((0,l.wg)(),(0,l.j4)(k,{key:12,label:e.name,"auto-upload":"",thumbnails:"",url:"http://localhost:8000",onUploaded:e.updateDom,onAdded:e.onAdded,style:(0,s.j5)(e.elemSize),ref:"uploaderRef",flat:""},null,8,["label","onUploaded","onAdded","style"])):"gimages"==e.type?((0,l.wg)(),(0,l.j4)(k,{key:13,label:e.name,"auto-upload":"",thumbnails:"",url:"http://localhost:8000",onUploaded:e.updateDom,onAdded:e.onAdded,ref:"uploaderRef",flat:""},null,8,["label","onUploaded","onAdded"])):"graph"==e.type?((0,l.wg)(),(0,l.j4)(v,{key:14,data:e.data,pdata:e.pdata,styleSize:e.elemSize},null,8,["data","pdata","styleSize"])):"camera"==e.type?((0,l.wg)(),(0,l.iD)("div",re,[(0,l._)("div",ce,[(0,l._)("button",{class:(0,s.C_)(["button is-rounded",{"is-primary":!e.isCameraOpen,"is-danger":e.isCameraOpen}]),type:"button",onClick:t[9]||(t[9]=(...t)=>e.toggleCamera&&e.toggleCamera(...t))},[e.isCameraOpen?((0,l.wg)(),(0,l.iD)("span",ue,"Close Camera")):((0,l.wg)(),(0,l.iD)("span",he,"Open Camera"))],2)]),(0,l.wy)((0,l._)("div",pe,me,512),[[oe.F8,e.isCameraOpen&&e.isLoading]]),e.isCameraOpen?(0,l.wy)(((0,l.wg)(),(0,l.iD)("div",{key:0,class:(0,s.C_)(["camera-box",{flash:e.isShotPhoto}])},[(0,l._)("div",{class:(0,s.C_)(["camera-shutter",{flash:e.isShotPhoto}])},null,2),(0,l.wy)((0,l._)("video",{ref:"camera",width:450,height:337.5,autoplay:""},null,8,fe),[[oe.F8,!e.isPhotoTaken]]),(0,l.wy)((0,l._)("canvas",{id:"photoTaken",ref:"canvas",width:450,height:337.5},null,8,we),[[oe.F8,e.isPhotoTaken]])],2)),[[oe.F8,!e.isLoading]]):(0,l.kq)("",!0),e.isCameraOpen&&!e.isLoading?((0,l.wg)(),(0,l.iD)("div",ye,[(0,l._)("button",{class:"button",type:"button",onClick:t[10]||(t[10]=(...t)=>e.takePhoto&&e.takePhoto(...t))},ke)])):(0,l.kq)("",!0),e.isPhotoTaken&&e.isCameraOpen?((0,l.wg)(),(0,l.iD)("div",ve,[(0,l.Wm)(q,{onClick:e.downloadImage,label:"Send"},null,8,["onClick"])])):(0,l.kq)("",!0)])):""!=e.showname?((0,l.wg)(),(0,l.j4)(q,{key:16,"no-caps":"",label:e.name,icon:e.data.icon,onClick:e.sendValue},null,8,["label","icon","onClick"])):((0,l.wg)(),(0,l.j4)(q,{key:17,"no-caps":"",dense:"",icon:e.data.icon,onClick:e.sendValue},null,8,["icon","onClick"]))}const Ce={key:0},_e={class:"row"},xe=["onClick"];function Se(e,t,a,o,n,i){const d=(0,l.up)("q-icon"),r=(0,l.up)("q-input"),c=(0,l.up)("q-tooltip"),h=(0,l.up)("q-btn"),u=(0,l.up)("q-th"),p=(0,l.up)("q-tr"),g=(0,l.up)("q-checkbox"),m=(0,l.up)("q-select"),f=(0,l.up)("q-td"),w=(0,l.up)("q-table");return(0,l.wg)(),(0,l.j4)(w,{class:"my-sticky-virtscroll-table","virtual-scroll":"",dense:"",style:(0,s.j5)(e.styleSize),flat:"",filter:e.search,ref:"table",virtualScrollSliceSize:"60","rows-per-page-options":[0],"virtual-scroll-sticky-size-start":48,"row-key":"iiid",title:e.name,rows:e.rows,columns:e.columns,selection:e.singleMode?"single":"multiple",selected:e.selected,"onUpdate:selected":t[1]||(t[1]=t=>e.selected=t)},{"top-right":(0,l.w5)((()=>[!1!==e.data.tools?((0,l.wg)(),(0,l.iD)("div",Ce,[(0,l._)("div",_e,[(0,l.Wm)(r,{modelValue:e.search,"onUpdate:modelValue":t[0]||(t[0]=t=>e.search=t),label:"Search",dense:""},{prepend:(0,l.w5)((()=>[(0,l.Wm)(d,{name:"search"})])),_:1},8,["modelValue"]),(0,l._)("div",null,[(0,l.Wm)(h,{dense:"",rounded:"",icon:"select_all","no-caps":"",onClick:e.showSelected},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[(0,l.Uk)("Show selected")])),_:1})])),_:1},8,["onClick"]),(0,l.Wm)(h,{dense:"",rounded:"",icon:"deselect","no-caps":"",onClick:e.deselectAll},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[(0,l.Uk)("Deselect all")])),_:1})])),_:1},8,["onClick"]),"delete"in e.data?((0,l.wg)(),(0,l.j4)(h,{key:0,dense:"",rounded:"",icon:"delete_forever","no-caps":"",onClick:e.delSelected},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[(0,l.Uk)("Delete selected")])),_:1})])),_:1},8,["onClick"])):(0,l.kq)("",!0),!1!==e.data.multimode?((0,l.wg)(),(0,l.j4)(h,{key:1,dense:"",rounded:"",icon:e.singleMode?"looks_one":"grain","no-caps":"",onClick:e.switchMode},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[(0,l.Uk)("Multi-single select mode")])),_:1})])),_:1},8,["icon","onClick"])):(0,l.kq)("",!0),e.editable?((0,l.wg)(),(0,l.j4)(h,{key:2,dense:"",rounded:"",icon:e.editMode?"cancel":"edit","no-caps":"",onClick:e.switchEdit},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[(0,l.Uk)("Edit mode")])),_:1})])),_:1},8,["icon","onClick"])):(0,l.kq)("",!0),e.editable&&"append"in e.data?((0,l.wg)(),(0,l.j4)(h,{key:3,dense:"",rounded:"",icon:"add","no-caps":"",onClick:e.append},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[(0,l.Uk)("Add a new row")])),_:1})])),_:1},8,["onClick"])):(0,l.kq)("",!0),"view"in e.data?((0,l.wg)(),(0,l.j4)(h,{key:4,dense:"",rounded:"",icon:"insights","no-caps":"",onClick:e.chart},{default:(0,l.w5)((()=>[(0,l.Wm)(c,{class:"text-body2"},{default:(0,l.w5)((()=>[(0,l.Uk)("Draw the chart")])),_:1})])),_:1},8,["onClick"])):(0,l.kq)("",!0)])])])):(0,l.kq)("",!0)])),header:(0,l.w5)((e=>[(0,l.Wm)(p,{props:e},{default:(0,l.w5)((()=>[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.cols,(t=>((0,l.wg)(),(0,l.j4)(u,{class:"text-italic text-purple",key:t.name,props:e},{default:(0,l.w5)((()=>[(0,l.Uk)((0,s.zw)(t.label),1)])),_:2},1032,["props"])))),128))])),_:2},1032,["props"])])),body:(0,l.w5)((t=>[(0,l.Wm)(p,{props:t,onClick:e=>t.selected=!t.selected},{default:(0,l.w5)((()=>[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(e.columns,((a,o)=>((0,l.wg)(),(0,l.j4)(f,{key:a.name,props:t},{default:(0,l.w5)((()=>["boolean"==typeof t.row[a.name]?((0,l.wg)(),(0,l.j4)(g,{key:0,modelValue:t.row[a.name],"onUpdate:modelValue":[e=>t.row[a.name]=e,l=>e.change_switcher(t.row,a.name,o)],dense:"",disable:!e.editMode},null,8,["modelValue","onUpdate:modelValue","disable"])):e.editMode&&"complete"in e.data&&o==e.cedit&&e.redit==t.row.iiid?((0,l.wg)(),(0,l.j4)(m,{key:1,dense:"","model-value":t.row[a.name],"use-input":"","hide-selected":"","fill-input":"",autofocus:"",outlined:"",borderless:"",onInputValue:e.change,"hide-dropdown-icon":"","input-debounce":"0",options:e.options,onFilter:e.complete,onKeydown:e.keyInput},null,8,["model-value","onInputValue","options","onFilter","onKeydown"])):e.editMode&&o==e.cedit&&e.redit==t.row.iiid?((0,l.wg)(),(0,l.j4)(r,{key:2,modelValue:t.row[a.name],"onUpdate:modelValue":[e=>t.row[a.name]=e,e.change],dense:"",onKeydown:e.keyInput,autofocus:""},null,8,["modelValue","onUpdate:modelValue","onKeydown"])):((0,l.wg)(),(0,l.iD)("div",{key:3,onClick:a=>e.select(t.row.iiid,o)},(0,s.zw)(t.row[a.name]),9,xe))])),_:2},1032,["props"])))),128))])),_:2},1032,["props","onClick"])])),_:1},8,["style","filter","title","rows","columns","selection","selected"])}var je=a(1959);const Ae=(0,l.aZ)({name:"utable",setup(e){const{data:t,pdata:a}=(0,je.BK)(e);let s=(0,l.Fl)((()=>{let e=[],a=t.value;const l=a.headers,s=l.length,o=a.rows,n=o.length;for(var i=0,d=0;d<n;d++){const t={},a=o[d];for(var r=0;r<s;r++)t[l[r]]=a[r];t.iiid=s==a.length?i:a[a.length-1],e.push(t),i++}return e})),o=()=>{let e=t.value;return null===e.value?[]:Array.isArray(e.value)?e.value.map((e=>s.value[e])):[s.value[e.value]]},n=o(),i=(0,je.iH)(n),d=(0,je.iH)(!Array.isArray(t.value.value)),r=(e,l)=>{q([a.value.name,t.value.name,e,l])},c=(0,l.Fl)((()=>d.value?i.value.length>0?i.value[0].iiid:null:i.value.map((e=>e.iiid)))),h=(0,l.Fl)((()=>t.value.value));return(0,l.YP)(s,((e,t)=>{i.value=o(),n=i.value})),(0,l.YP)(t,((e,a)=>{g&&console.log("data update",a.name),i.value=o(),n=i.value,d.value=!Array.isArray(t.value.value)})),(0,l.YP)(i,(e=>{n!==i.value&&(n=i.value,r("=",c.value))})),{rows:s,value:c,selected:i,singleMode:d,sendMessage:r,datavalue:h}},data(){return{search:"",editMode:!1,options:[],cedit:null}},methods:{select(e,t){this.editMode&&(this.cedit=t,g&&console.log("selected",e,this.cedit))},change_switcher(e,t,a){if(console.log(e,t,a,e[t]),this.editMode){this.cedit=a;const l=e.iiid;let s=this.data.rows;s[l][a]=e[t],this.sendMessage("#",[e[t],[l,a]])}},change(e){if(g&&console.log("changed",this.data.headers[this.cedit],e),this.editMode&&this.selected.length){const t=this.selected[0].iiid;let a=this.rows;a[t][this.data.headers[this.cedit]]=e,this.sendMessage("#",[e,[t,this.cedit]])}},keyInput(e){if("Control"!=e.key)switch(g&&console.log("keypress",e),e.key){case"Enter":"update"in this.data&&this.sendMessage("->",[this.data.rows[this.redit][this.cedit],[this.redit,this.cedit]]);break;case"Escape":this.switchEdit();break;case"ArrowLeft":if(e.ctrlKey)for(let e=this.cedit-1;e>=0;e--){let t=typeof this.data.rows[this.redit][e];if("string"==t||"number"==t){this.cedit=e;break}}break;case"ArrowRight":if(e.ctrlKey)for(let e=this.cedit+1;e<this.data.rows[this.redit].length;e++){let t=typeof this.data.rows[this.redit][e];if("string"==t||"number"==t){this.cedit=e;break}}break;case"ArrowUp":if(e.ctrlKey&&this.redit>0){let e=this.redit-1,t=typeof this.data.rows[e][this.cedit];"string"!=t&&"number"!=t||(this.selected=[this.rows[e]])}break;case"ArrowDown":if(e.ctrlKey&&this.redit+1<this.rows.length){let e=this.redit+1,t=typeof this.data.rows[e][this.cedit];"string"!=t&&"number"!=t||(this.selected=[this.rows[e]])}break}},complete(e,t,a){S(this,[e,[this.redit,this.cedit]],(e=>t((()=>{this.options=e}))))},append(){let e=this.data.rows,t=e.length,a=this;S(this,[t,this.search],(function(l){if(!Array.isArray(l))return u.error(l);g&&console.log("added row",l),a.search="",e.push(l),setTimeout((()=>{let e=a.rows;a.select(e[t],0),a.showSelected()}),100)}),"+")},showSelected(){let e=this.$refs.table;this.selected&&e.scrollTo(e.computedRows.findIndex((e=>e===this.selected[0])))},deselectAll(){this.selected=[],this.sendMessage("=",this.value)},chart(){},switchMode(){this.singleMode=!this.singleMode,this.singleMode&&this.selected.length>1&&this.selected.splice(1)},switchEdit(){this.editMode=!this.editMode,this.sendMessage("!",this.editMode),this.editMode&&!this.singleMode&&this.switchMode()},delSelected(){if(!this.selected.length)return void u.error("Rows are not selected!");this.sendMessage("-",this.value);let e=this.data.rows;if(this.singleMode)e.splice(this.selected[0].iiid,1);else{this.selected.length>1&&this.selected.sort(((e,t)=>t.iiid-e.iiid));for(let t of this.selected)e.splice(t.iiid,1)}this.selected=[]}},computed:{redit(){return console.log("redit",this.editMode&&this.selected.length?this.selected[0].iiid:null),this.editMode&&this.selected.length?this.selected[0].iiid:null},editable(){return 0!=this.data["edit"]},name(){return"_"==this.data.name?"":this.data.name},columns(){return this.data.headers.map((e=>({name:e,label:e,align:"left",sortable:!0,field:e})))}},props:{data:Object,pdata:Object,styleSize:String}});var Ze=a(9267),Me=a(4842),De=a(2165),ze=a(8870),Qe=a(8186),We=a(2414),$e=a(3884),Ve=a(5735),Oe=a(7208);const Ee=(0,H.Z)(Ae,[["render",Se]]),He=Ee;function Ue(e,t,a,o,n,i){const d=(0,l.up)("v-edge-label"),r=(0,l.up)("v-network-graph");return(0,l.wg)(),(0,l.j4)(r,{nodes:e.nodes,edges:e.edges,style:(0,s.j5)(e.styleSize),configs:e.configs,"selected-edges":e.selectedEdges,"onUpdate:selectedEdges":t[0]||(t[0]=t=>e.selectedEdges=t),"selected-nodes":e.selectedNodes,"onUpdate:selectedNodes":t[1]||(t[1]=t=>e.selectedNodes=t)},{"edge-label":(0,l.w5)((({edge:e,...t})=>[(0,l.Wm)(d,(0,l.dG)({text:e.label,align:"center","vertical-align":"above"},t),null,16,["text"])])),_:1},8,["nodes","edges","style","configs","selected-edges","selected-nodes"])}R()(Ae,"components",{QTable:Ze.Z,QInput:Me.Z,QIcon:T.Z,QBtn:De.Z,QTooltip:ze.Z,QTr:Qe.Z,QTh:We.Z,QTd:$e.Z,QCheckbox:Ve.Z,QSelect:Oe.Z});var Pe=a(5111);const Te=Pe.Ye();Te.edge.selectable=!0,Te.node.selectable=!0,Te.node.label.directionAutoAdjustment=!0,Te.edge.marker.target.type="arrow";const Ie=(0,l.aZ)({name:"ugraph",data(){return{configs:Te,selectedEdges:[],selectedNodes:[],alreadySelectedNodes:null,alreadySelectedEdges:null}},methods:{log(){console.log(Object.keys(screenBlocks).length,this.name,this.$el.getBoundingClientRect())},sendMessage(e,t){q([this.pdata["name"],this.data["name"],e,t])},sendValue(){this.sendMessage("=",this.value)}},computed:{name(){return this.data.name},nodes(){return this.data.nodes},edges(){return this.data.edges},expanding(){return this.data.scroll},expanding_width(){return this.expanding},expanding_height(){return!this.data.height&&this.expanding}},props:{data:Object,pdata:Object,styleSize:String},beforeMount(){this.data.value&&(void 0!==this.data.value.nodes&&(this.selectedNodes=this.data.value.nodes,this.alreadySelectedNodes=this.selectedNodes,console.log("nodes m",this.alreadySelectedNodes)),void 0!==this.data.value.edges&&(this.selectedEdges=this.data.value.edges,this.alreadySelectedEdges=this.selectedEdges,console.log("edges m",this.alreadySelectedEdges)))},watch:{data:{handler(e){if(console.log("wa gr"),e.value){let t=e.value;void 0!==t.nodes&&this.selectedNodes!=t.nodes&&(this.selectedNodes=t.nodes,this.alreadySelectedNodes=this.selectedNodes,console.log("nodes",this.alreadySelectedNodes)),void 0!==t.edges&&this.selectedEdges!==t.edges&&(this.selectedEdges=t.edges,this.alreadySelectedEdges=this.selectedEdges,console.log("edges",this.alreadySelectedEdges))}},deep:!0},selectedEdges(e){e!==this.alreadySelectedEdges&&(this.sendMessage("=",{edges:this.selectedEdges}),this.alreadySelectedEdges=this.selectedEdges)},selectedNodes(e){e!==this.alreadySelectedNodes&&(this.sendMessage("=",{nodes:this.selectedNodes}),this.alreadySelectedNodes=this.selectedNodes)}}}),Ne=(0,H.Z)(Ie,[["render",Ue]]),Re=Ne;function Ke(e){let t=new FormData;t.append("image",e);let a=new XMLHttpRequest;a.open("POST","http://localhost:8000",!0),a.onload=function(){200===this.status?console.log(this.response):console.error(a)},a.send(t)}const Le=(0,l.aZ)({name:"element",components:{utable:He,ugraph:Re},methods:{log(e){console.log(e)},onAdded(e){0!==e.length&&(0!==this.fileArr.length?(this.$refs.uploaderRef.removeFile(this.fileArr[0]),this.fileArr.splice(0,1,e[0])):this.fileArr.push(e[0]))},sendMessage(e,t){q([this.pdata["name"],this.data["name"],e,t])},pressedEnter(){"update"in this.data&&this.sendMessage("->",this.value)},updateDom(e){let t=e.files.length;t&&(this.sendMessage("=",e.files[t-1].name),z())},sendValue(){this.sendMessage("=",this.value)},switchValue(){this.value=!this.value},setValue(e){console.log(e),this.value=e},complete(e,t,a){this.value=e,S(this,e,(e=>t((()=>{this.options=e}))))},lens(){u.lens(this.data)},toggleCamera(){this.isCameraOpen?(this.isCameraOpen=!1,this.isPhotoTaken=!1,this.isShotPhoto=!1,this.stopCameraStream()):(this.isCameraOpen=!0,this.createCameraElement())},createCameraElement(){this.isLoading=!0;const e=window.constraints={audio:!1,video:!0};navigator.mediaDevices.getUserMedia(e).then((e=>{this.isLoading=!1,this.$refs.camera.srcObject=e})).catch((e=>{this.isLoading=!1,alert("May the browser didn't support or there is some errors.")}))},stopCameraStream(){let e=this.$refs.camera.srcObject.getTracks();e.forEach((e=>{e.stop()}))},takePhoto(){if(!this.isPhotoTaken){this.isShotPhoto=!0;const e=50;setTimeout((()=>{this.isShotPhoto=!1}),e)}this.isPhotoTaken=!this.isPhotoTaken;const e=this.$refs.canvas.getContext("2d");e.drawImage(this.$refs.camera,0,0,450,337.5)},downloadImage(){document.getElementById("downloadPhoto"),document.getElementById("photoTaken").toBlob(Ke,"image/jpeg")},geom(){const e="clientHeight"in this.$el?this.$el:this.$el.nextElementSibling,t="docviewer"==this.type?e:e.querySelector("table"==this.type?".scroll":".q-tree"),a=e.getBoundingClientRect();return{el:e,inner:t,left:a.left,right:a.right,top:a.top,scrollHeight:t.scrollHeight,scrollWidth:t.scrollWidth}}},mounted(){b[this.fullname]=this,g&&console.log("mounted",this.fullname)},data(){return{value:this.data.value,styleSize:w,options:[],thumbStyle:{right:"4px",borderRadius:"7px",backgroundColor:"#027be3",width:"4px",opacity:.75},barStyle:{right:"2px",borderRadius:"9px",backgroundColor:"#027be3",width:"8px",opacity:.2},updated:"#027be3sds",isCameraOpen:!1,isPhotoTaken:!1,isShotPhoto:!1,isLoading:!1,link:"#",fileArr:[]}},computed:{elemSize(){let e="";return this.data.width&&(e=`width:${this.data.width}px`),this.data.height&&(""!=e&&(e+="; "),e+=`height:${this.data.height}px`),""==e?this.styleSize:e},name(){return this.data.name},fullname(){return`${this.data.name}@${this.pdata.name}`},showname(){return"_"!=this.data.name[0]},nameLabel(){return this.data.label?this.data.label:"_"!=this.data.name[0]?this.data.name:""},text(){return this.data.text},expanding(){let e=this.type;return"tree"==e||"table"==e||"list"==e||"docviewer"==e},expanding_width(){return!this.data.width&&this.expanding},expanding_height(){return!this.data.height&&this.expanding},selection(){return this.data.selection},icon(){return this.data.icon},type(){var e=this.data.type;if(e)return e;const t=this.data,a=t.options;return a?a.length>3?"select":"radio":t.headers?"table":(e=typeof this.value,"number"==e||"string"==e?void 0!==t.complete?"autoedit":"edit":"boolean"==e?"switch":"button")},treeNodes(){var e=[];if("list"==this.type)return this.data.options.map((e=>({label:e,children:[]})));var t={};for(const[s,o]of Object.entries(this.data.options)){var a=t[s];if(a||(a={label:s,children:[]},t[s]=a),o){var l=t[o];l||(l={label:o,children:[]},t[o]=l),l.children.push(a)}else e.push(a)}return e}},props:{data:{type:Object,required:!0},pdata:{type:Object,required:!0}},watch:{value(e,t){e!==this.updated&&(g&&console.log("value changed",e,t),this.sendValue(),this.updated=e)},selection(e){g&&console.log("selection changed",e,this.$refs.inputRef),Array.isArray(e)||(e=[0,0]);let t=this.$refs.inputRef.$el;t.focus();let a=t.getElementsByTagName("textarea");0==a.length&&(a=t.getElementsByTagName("input")),a[0].setSelectionRange(e[0],e[1])},data(e,t){g&&console.log("data update",this.fullname,t.name),this.expanding&&(this.styleSize=w,console.log(`${this.name} size changed`)),this.value=this.data.value,this.updated=this.value,b[this.fullname]=this}}});var Be=a(4027),Ye=a(9721),Fe=a(8886),Je=a(8761),Ge=a(1232),Xe=a(5551),et=a(5869),tt=a(1745);const at=(0,H.Z)(Le,[["render",qe],["__scopeId","data-v-424a81a0"]]),lt=at;R()(Le,"components",{QImg:Be.Z,QIcon:T.Z,QSelect:Oe.Z,QBadge:Ye.Z,QCheckbox:Ve.Z,QToggle:Fe.Z,QBtnToggle:Je.Z,QInput:Me.Z,QScrollArea:Ge.Z,QTree:Xe.Z,QSeparator:et.Z,QUploader:tt.Z,QBtn:De.Z});const st=(0,l.aZ)({name:"block",components:{element:lt},data(){return{styleSize:w,thumbStyle:{right:"4px",borderRadius:"7px",backgroundColor:"#027be3",width:"4px",opacity:.75},barStyle:{right:"2px",borderRadius:"9px",backgroundColor:"#027be3",width:"8px",opacity:.2}}},methods:{log(){console.log(Object.keys(y).length,this.name,this.$el.getBoundingClientRect())},geom(){let e="clientHeight"in this.$el?this.$el:this.$el.nextElementSibling;const t=e.querySelector(".q-scrollarea"),a=e.getBoundingClientRect();return{el:e,inner:t,left:a.left,right:a.right,top:a.top,scrollHeight:window.innerHeight,scrollWidth:window.innerWidth}}},mounted(){y[this.name]=this,this.expanding&&(b[this.fullname]=this)},computed:{name(){return this.data.name},fullname(){return`_scroll@${this.name}`},icon(){return this.data.icon},expanding(){return this.data.scroll},expanding_width(){return this.expanding},expanding_height(){return!this.data.height&&this.expanding}},props:{data:{type:Object,required:!0}},watch:{data(e){g&&console.log("data update",this.name),this.styleSize=w,y[this.name]=this,this.expanding&&(b[this.fullname]=this)}}});var ot=a(151);const nt=(0,H.Z)(st,[["render",se]]),it=nt;R()(st,"components",{QCard:ot.Z,QIcon:T.Z,QScrollArea:Ge.Z});const dt=(0,l.aZ)({name:"zone",components:{block:it},props:{data:Object}}),rt=(0,H.Z)(dt,[["render",J]]),ct=rt,ht={class:"row q-gutter-sm row-md"};function ut(e,t,a,o,n,i){const d=(0,l.up)("block"),r=(0,l.up)("q-item-label"),c=(0,l.up)("q-space"),h=(0,l.up)("q-btn"),u=(0,l.up)("q-card"),p=(0,l.up)("q-dialog");return(0,l.wg)(),(0,l.j4)(p,{ref:"dialog",onHide:i.onDialogHide},{default:(0,l.w5)((()=>[(0,l.Wm)(u,{class:"q-dialog-plugin q-pa-md items-start q-gutter-md",bordered:"",style:(0,s.j5)(a.data.internal?"width: 800px; max-width: 80vw;":"")},{default:(0,l.w5)((()=>[a.data?((0,l.wg)(),(0,l.j4)(d,{key:0,data:a.data},null,8,["data"])):(0,l.kq)("",!0),(0,l.Wm)(r,{class:"text-h6"},{default:(0,l.w5)((()=>[(0,l.Uk)((0,s.zw)(a.data.text?a.data.text:""),1)])),_:1}),(0,l._)("div",ht,[(0,l.Wm)(c),((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(a.buttons,(e=>((0,l.wg)(),(0,l.j4)(h,{class:"col-md-3",label:e,color:a.buttons[0]==e?"primary":"secondary",onClick:t=>i.sendMessage(e)},null,8,["label","color","onClick"])))),256))])])),_:1},8,["style"])])),_:1},8,["onHide"])}const pt={props:{data:Object,buttons:Array},components:{block:it},emits:["ok","hide"],methods:{show(){this.$refs.dialog.show()},sendMessage(e){this.data.internal||q([this.data["name"],e]),this.hide()},hide(){this.$refs.dialog.hide()},onDialogHide(){this.$emit("hide")},onOKClick(){this.$emit("ok"),this.hide()},onCancelClick(){this.hide()}}};var gt=a(5926),mt=a(2025);const ft=(0,H.Z)(pt,[["render",ut]]),wt=ft;R()(pt,"components",{QDialog:gt.Z,QCard:ot.Z,QItemLabel:I.Z,QSpace:mt.Z,QBtn:De.Z});var yt=!0;let bt=null;const kt=(0,l.aZ)({name:"MainLayout",data(){return{leftDrawerOpen:!1,menu:[],tab:"",localServer:!0,statusConnect:!1,screen:{blocks:[]},prevHeight:0}},components:{menubar:L,zone:ct},created(){v(this)},unmounted(){window.removeEventListener("resize",this.onResize)},methods:{toggleLeftDrawer(){this.leftDrawerOpen=!this.leftDrawerOpen},tabclick(e){q(["root",e])},onResize(e){const t=e.currentTarget.innerHeight;this.prevHeight!=t&&(g&&console.log("window has been resized",t,window.innerHeight),this.prevHeight=t,z())},lens(e){let t={title:"Photo lens",message:e.text,cancel:!0,persistent:!0,component:wt},{height:a,...l}=e;l.width=750;let s={name:`Picture lens of ${e.name}`,top_childs:[],childs:[l],internal:!0};t.componentProps={data:s,buttons:["Close"]},this.$q.dialog(t)},notify(e,t){let a=t,l={message:e,type:t,position:"top",icon:a};"progress"==t?null==bt?(l={group:!1,timeout:0,spinner:!0,type:"info",message:e||"Progress..",position:"top",color:"secondary"},bt=this.$q.notify(l)):null==e?(bt(),bt=null):(l={caption:e},bt(l)):("error"==t&&l.type,this.$q.notify(l))},error(e){this.notify(e,"error")},info(e){this.notify(e,"info")},processMessage(e){if(yt)yt=!1,this.menu=e[0].map((e=>({name:e[0],icon:e[1],order:e[2]}))),W(),this.screen=e[1],this.tab=this.screen.name,g&&console.log("init loading..");else if("screen"==e.type)j(),W(),this.screen=e;else if("dialog"==e.type){let t={title:e.name,message:e.text,cancel:!0,persistent:!0};t.component=wt,t.componentProps={data:e.content?e.content:e,buttons:e.buttons},this.$q.dialog(t)}else if(e.hasOwnProperty("answer"))M(e);else{e.update&&Z(e);let t=!1;for(let a of k)a in e&&(this.notify(e[a],a),t=!0);t||e.update||(this.error("Invalid data came from the server! Look the console."),console.log(`Invalid data came from the server! ${e}`))}bt&&!e.progress&&this.notify(null,"progress")}},mounted(){W(),window.addEventListener("resize",this.onResize)},updated(){g&&console.log("before updated")}});var vt=a(9214),qt=a(3812),Ct=a(9570),_t=a(7547),xt=a(3269),St=a(2652),jt=a(4379);const At=(0,H.Z)(kt,[["render",n]]),Zt=At;R()(kt,"components",{QLayout:vt.Z,QHeader:qt.Z,QToolbar:Ct.Z,QBtn:De.Z,QItemLabel:I.Z,QTabs:_t.Z,QTab:xt.Z,QPageContainer:St.Z,QPage:jt.Z})}}]);