setTimeout(fade_out, 3000);

function fade_out() {
  $("#banner").hide();
}

/**
 * lc_select.js - Superlight Javascript dropdowns
 * Version: 1.1.3
 * Author: Luca Montanari aka LCweb
 * Website: https://lcweb.it
 * Licensed under the MIT license
 */

 var $jscomp=$jscomp||{};$jscomp.scope={};$jscomp.createTemplateTagFirstArg=function(n){return n.raw=n};$jscomp.createTemplateTagFirstArgWithRaw=function(n,t){n.raw=t;return n};$jscomp.arrayIteratorImpl=function(n){var t=0;return function(){return t<n.length?{done:!1,value:n[t++]}:{done:!0}}};$jscomp.arrayIterator=function(n){return{next:$jscomp.arrayIteratorImpl(n)}};$jscomp.makeIterator=function(n){var t="undefined"!=typeof Symbol&&Symbol.iterator&&n[Symbol.iterator];return t?t.call(n):$jscomp.arrayIterator(n)};
 (function(){if("undefined"!=typeof window.lc_select)return!1;var n=[],t=null,l=null,z={enable_search:!0,min_for_search:7,autofocus_search:!1,wrap_width:"auto",addit_classes:[],pre_placeh_opt:!1,max_opts:!1,on_change:null,labels:["search options","add options","Select options ..",".. no matching options .."]};document.addEventListener("click",function(g){var e=document.querySelector("#lc-select-dd.lcslt-shown");if(!e)return!0;for(var a=$jscomp.makeIterator(document.getElementsByClassName("lcslt-wrap")),
 c=a.next();!c.done;c=a.next())if(c.value.contains(g.target))return!0;e.contains(g.target)||g.target.classList.contains("lcslt-shown")||(e.remove(),l&&(l.classList.remove("lcslt_dd-open"),l=null));return!0});window.addEventListener("resize",function(g){g=document.querySelector("#lc-select-dd.lcslt-shown");if(!g||document.activeElement.hasAttribute("type")&&"text"===document.activeElement.getAttribute("type"))return!0;g.classList.remove("lcslt-shown");l.classList.remove("lcslt_dd-open");l=null;return!0});
 document.addEventListener("keydown",function(g){if(-1===[38,40,13,27,9].indexOf(g.keyCode)||!document.querySelector("#lc-select-dd.lcslt-shown"))return!0;g.preventDefault();var e=document.querySelector(".lcslt-dd-opt.lcslt-dd-opt-hlight"),a=document.querySelectorAll(".lcslt-dd-opt:not(.lcslt-disabled)"),c=new Event("mouseenter",{bubbles:!0});switch(g.keyCode){case 27:l.click();break;case 9:document.activeElement.classList&&document.activeElement.classList.contains("lcslt-tabindex-trick")||l.click();
 break;case 13:e&&(e.classList.remove("lcslt-dd-opt-hlight"),e.click());break;case 38:case 40:var b=38==g.keyCode?0:a.length-1;e&&a.forEach(function(d,h){d==e&&(b=h)});a[38==g.keyCode?b?b-1:a.length-1:b==a.length-1?0:b+1].dispatchEvent(c);x()}return!0});var x=function(){var g=document.querySelector(".lcslt-dd-opt-hlight");if(!g)return!1;var e=parseInt(getComputedStyle(g).borderTopWidth,10);document.querySelector(".lc-select-dd-scroll").scrollTop=g.offsetTop-2*(g.offsetHeight+e)-10};window.lc_select=
 function(g,e){e=void 0===e?{}:e;if(!g)return console.error("You must provide a valid selector or DOM object as first argument");if("object"!=typeof e)return console.error("Options must be an object");e=Object.assign({},z,e);this.init=function(){var a=this;t||(this.generate_style(),t=!0);A(g).forEach(function(c){"SELECT"!=c.tagName||c.parentNode.classList.length&&c.parentNode.classList.contains("lcslt-wrap")||(a.wrap_element(c),c.removeEventListener("lc-select-refresh",function(){}),c.addEventListener("lc-select-refresh",
 function(b){l&&l.click();var d=b.target.parentNode.querySelector(".lcslt");a.set_sel_content(d);if(!b.target.parentNode.classList.length||b.target.parentNode.classList.length&&!b.target.parentNode.classList.contains("lcslt-wrap"))return!1;b.target.disabled?d.classList.add("lcslt-disabled"):d.classList.remove("lcslt-disabled");return!0}),c.removeEventListener("lc-select-destroy",function(){}),c.addEventListener("lc-select-destroy",function(b){l&&l.click();var d=b.target;b=b.target.parentNode;var h=
 d.querySelector('option[data-lcslt-placeh="1"]');if(!b.classList.length||b.classList.length&&!b.classList.contains("lcslt-wrap"))return!1;h&&h.remove();b.parentNode.insertBefore(d,b);b.remove();return!0}))})};this.wrap_element=function(a){var c=this,b=document.createElement("div"),d="lcslt-f-"+a.getAttribute("name").replace(/\[\]/g,""),h=a.disabled?"lcslt-disabled":"",p=a.multiple?"lcslt-multiple":"",q=a.getAttribute("tabindex")?parseInt(a.getAttribute("tabindex"),10):"",r=a.hasAttribute("data-placeholder")?
 a.getAttribute("data-placeholder").trim():"";!r&&p&&(r=e.labels[2]);"object"==typeof e.addit_classes&&e.addit_classes.some(function(m){b.classList.add(m)});"auto"!=e.wrap_width&&(b.style.width="inherit"==e.wrap_width?Math.round(a.getBoundingClientRect().width)+"px":e.wrap_width);b.classList.add("lcslt-wrap",d);b.innerHTML='<input type="text" name="'+d+'-tit" tabindex="'+q+'" class="lcslt-tabindex-trick" /><div class="lcslt '+d+" "+p+" "+h+'" data-placeh="'+r+'"></div>';a.parentNode.insertBefore(b,
 a);b.appendChild(a);var k=b.querySelector(".lcslt");if(e.pre_placeh_opt&&!p&&r){var f=!0;a.querySelectorAll("option").forEach(function(m){if(m.hasAttribute("selected"))return f=!1});f&&(d=document.createElement("option"),d.setAttribute("data-lcslt-placeh",1),d.setAttribute("value",""),d.style.display="none",d.innerHTML=r,d.selected=!0,a.insertBefore(d,a.firstChild))}this.set_sel_content(k);k.addEventListener("click",function(m){k.classList.contains("lcslt-disabled")||m.target.classList.contains("lcslt-multi-selected")||
 m.target.classList.contains("lcslt-max-opts")||m.target.parentNode.classList.contains("lcslt-multi-selected")||c.show_dd(k)});b.querySelector(".lcslt-tabindex-trick").onfocus=function(m){k.click()}};this.set_sel_content=function(a){(a=void 0===a?!1:a)||(a=l);var c=this,b=a.nextSibling,d=a.classList.contains("lcslt-multiple"),h="",p=0,q=0;b.querySelectorAll("option").forEach(function(k){if(k.selected){var f=k.hasAttribute("data-image")?'<i class="lcslt-img" style="background-image: url(\''+k.getAttribute("data-image").trim()+
 "')\"></i>":"";h=d?h+('<div class="lcslt-multi-selected" data-val="'+k.getAttribute("value")+'" title="'+k.innerHTML+'"><span>'+f+k.innerHTML+"</span></div>"):"<span "+(e.pre_placeh_opt&&k.hasAttribute("data-lcslt-placeh")?'class="lcslt-placeholder"':"")+' title="'+k.innerHTML+'">'+f+k.innerHTML+"</span>";q++}p++});var r=!1;"number"==typeof e.max_opts&&1<e.max_opts&&(q>=e.max_opts?(a.classList.add("lcslt-max-opts"),r=!0):a.classList.remove("lcslt-max-opts"));h?d&&p>q&&!b.disabled&&!r&&(h+='<span class="lcslt-multi-callout" title="'+
 e.labels[1]+'">+</span>'):h='<span class="lcslt-placeholder">'+a.getAttribute("data-placeh")+"</span>";a.innerHTML=h;d&&a.querySelectorAll(".lcslt-multi-selected").forEach(function(k){k.addEventListener("click",function(f){for(var m=f.target;null!=m.parentNode&&!m.matches(".lcslt");)m=m.parentNode;m.classList.contains("lcslt-disabled")||c.deselect_option(f,a,k)})})};this.show_dd=function(a){document.querySelector("#lc-select-dd")&&(document.querySelector("#lc-select-dd").remove(),l.classList.remove("lcslt_dd-open"));
 if(a==l)return l=null,!1;l=a;this.append_dd();this.set_dd_position();x();var c=this,b=document.querySelector("#lc-select-dd");b.classList.add("lcslt-shown");a.classList.add("lcslt_dd-open");setTimeout(function(){a.getBoundingClientRect().x!=b.getBoundingClientRect().x&&c.set_dd_position()},10)};this.set_dd_position=function(){var a=document.querySelector("#lc-select-dd"),c=l.getBoundingClientRect(),b=c.width.toFixed(2),d=parseInt(l.clientHeight,10)+parseInt(getComputedStyle(l).borderTopWidth,10);
 d=parseInt(c.y,10)+parseInt(window.pageYOffset,10)+d;c=c.left.toFixed(2);0>c&&(c=0);a.setAttribute("style","width:"+b+"px; top:"+d+"px; left: "+c+"px;")};this.append_dd=function(){var a=this,c=this,b=l.parentNode.querySelector("select"),d=[],h=!1,p=[];b.querySelectorAll("optgroup").length?b.querySelectorAll("optgroup").forEach(function(f){d[f.getAttribute("label")]={};f.disabled&&p.push(f.getAttribute("label"))}):(h=!0,d["%%lcslt%%"]={});b.querySelectorAll("option").forEach(function(f){var m={img:f.hasAttribute("data-image")?
 f.getAttribute("data-image").trim():"",name:f.innerHTML,selected:f.selected,disabled:f.disabled},u=h?"%%lcslt%%":f.parentNode.getAttribute("label");if(h||u)d[u][f.getAttribute("value")]=m});var q=l.classList.contains("lcslt-multiple")?"lcslt-multiple-dd":"",r="object"==typeof e.addit_classes?e.addit_classes.join(" "):"",k='<div id="lc-select-dd" class="'+q+" "+r+'">';(r=e.enable_search&&b.querySelectorAll("option").length>=parseInt(e.min_for_search,10)?!0:!1)&&(k+='<ul><li class="lcslt-search-li"><input type="text" name="lcslt-search" value="" placeholder="'+
 e.labels[0]+' .." autocomplete="off" /></li></ul>');k+='<ul class="lc-select-dd-scroll">';Object.keys(d).some(function(f){if(!h){var m=-1!==p.indexOf(f)?"lcslt-disabled":"",u=b.querySelector('optgroup[label="'+f+'"]');u=u.hasAttribute("data-image")&&u.getAttribute("data-image")?'<i class="lcslt-img" style="background-image: url(\''+u.getAttribute("data-image").trim()+"')\"></i>":"";k+='<li class="lcslt-group '+m+'"><span class="lcslt-group-name">'+u+f+'</span><ul class="lcslt-group-opts">'}Object.keys(d[f]).some(function(w){var v=
 d[f][w],B=v.img?'<i class="lcslt-img" style="background-image: url(\''+v.img+"')\"></i>":"",y=v.selected?"lcslt-selected":"",C=v.disabled||-1!==p.indexOf(f)?"lcslt-disabled":"",D=y?"lcslt-dd-opt-hlight":"";if(q||!b.querySelector('option[value="'+w+'"]').hasAttribute("data-lcslt-placeh"))k+='<li class="lcslt-dd-opt '+y+" "+C+" "+D+'" data-val="'+w+'"><span>'+B+v.name+"</span></li>"});h||(k+="</ul></li>")});document.body.insertAdjacentHTML("beforeend",k+"</ul></div>");document.querySelectorAll(".lcslt-dd-opt").forEach(function(f){f.addEventListener("click",
 function(m){c.clicked_dd_option(m,f)});f.addEventListener("mouseenter",function(m){document.querySelector(".lcslt-dd-opt-hlight")&&document.querySelector(".lcslt-dd-opt-hlight").classList.remove("lcslt-dd-opt-hlight");f.classList.contains("lcslt-disabled")||f.classList.add("lcslt-dd-opt-hlight")});f.addEventListener("mouseleave",function(m){f.classList.remove("lcslt-dd-opt-hlight")})});r&&(1024<window.innerWidth&&e.autofocus_search&&setTimeout(function(){return document.querySelector("input[name=lcslt-search]").focus()},
 50),document.querySelector("input[name=lcslt-search]").addEventListener("keyup",function(f){a.debounce("opts_search",500,"search_options")}))};this.on_val_change=function(a){a=a.nextSibling;var c=Array.from(a.selectedOptions).map(function(d){return d.value}),b=new Event("change",{bubbles:!0});a.dispatchEvent(b);"function"==typeof e.on_change&&e.on_change.call(this,c,a)};this.deselect_option=function(a,c,b){c.nextSibling.querySelector('option[value="'+b.getAttribute("data-val")+'"]').selected=!1;this.set_sel_content(c);
 this.on_val_change(c)};this.clicked_dd_option=function(a,c){var b=l.classList.contains("lcslt-multiple"),d=c.getAttribute("data-val"),h=l.nextSibling;if(c.classList.contains("lcslt-disabled")||!b&&c.classList.contains("lcslt-selected")||!c.classList.contains("lcslt-selected")&&l.classList.contains("lcslt-max-opts"))return!1;b||(document.querySelectorAll(".lcslt-dd-opt").forEach(function(p){p.getAttribute("data-val")!=d&&p.classList.remove("lcslt-selected")}),h.querySelectorAll("option").forEach(function(p){p.getAttribute("value")!=
 d&&(p.selected=!1)}));c.classList.toggle("lcslt-selected");c.classList.remove("lcslt-dd-opt-hlight");h.querySelector('option[value="'+d+'"]').selected=!h.querySelector('option[value="'+d+'"]').selected;this.set_sel_content();this.on_val_change(l);b?this.set_dd_position():l.click()};this.search_options=function(){if(!document.querySelector("input[name=lcslt-search]"))return!1;var a=document.querySelector("input[name=lcslt-search]").value.trim(),c=document.querySelectorAll(".lcslt-group-name"),b=document.querySelectorAll(".lcslt-dd-opt"),
 d=document.querySelector(".lcslt-no-results");if(2>a.length)document.getElementById("lc-select-dd").classList.remove("lcslt-is-searching"),c.forEach(function(q){q.style.removeProperty("display")}),b.forEach(function(q){q.style.removeProperty("display")}),d&&d.remove();else{document.getElementById("lc-select-dd").classList.add("lcslt-is-searching");c.forEach(function(q){q.style.display="none"});var h=a.split(" "),p=!0;b.forEach(function(q){var r=!1;h.some(function(k){-1!==q.querySelector("span").innerHTML.toLowerCase().indexOf(k.toLowerCase())&&
 (r=!0,p=!1)});r?q.style.removeProperty("display"):q.style.display="none"});p?d||document.querySelector(".lc-select-dd-scroll").insertAdjacentHTML("beforeend",'<li class="lcslt-no-results"><span>'+e.labels[3]+"</span></li>"):d.remove()}};this.debounce=function(a,c,b,d){"undefined"!=typeof n[a]&&n[a]&&clearTimeout(n[a]);var h=this;n[a]=setTimeout(function(){h[b].call(h,d)},c)};this.generate_style=function(){document.head.insertAdjacentHTML("beforeend",'<style>\n.lcslt-wrap {\n    position: relative;\n    display: inline-block;\n}\n.lcslt-wrap select {\n    display: none !important;\n}\n.lcslt {\n    display: flex;\n\talign-items: center;\n\tflex-direction: row;\n\tflex-wrap: wrap;\n    width: 100%;\n    min-height: 15px;\n    padding: 5px 30px 5px 5px;\n    position: relative;\n    overflow: hidden;\n    font-size: 1rem;\n}\n.lcslt:not(.lcslt-disabled):not(.lcslt-max-opts) {\n    cursor: pointer;\n}\n.lcslt:not(.lcslt-multiple):after {\n\tcontent: "";\n\twidth: 0;\n\theight: 0;\n\tborder-left: 5px solid transparent;\n\tborder-right: 5px solid transparent;\n\tborder-top: 6px solid #444;\n\tdisplay: inline-block;\n    position: absolute;\n    right: 6px;\n    transition: transform .3s ease;\n}\n.lcslt.lcslt_dd-open:after {\n    transform: rotate(180deg);\n}\n.lcslt:not(.lcslt-multiple) > span {\n    line-height: normal;\n}\n.lcslt span,\n.lcslt-multi-selected {\n    max-width: 100%;\n\toverflow: hidden;\n\twhite-space: nowrap;\n\ttext-overflow: ellipsis;\n}\n.lcslt-multiple {\n\tpadding: 5px 5px 0 5px;\n\theight: auto;\n\tline-height: 0;\n}\n.lcslt span:not(.lcslt-placeholder):not(.lcslt-multi-callout) {\n\tline-height: 1.1em;\n\tfont-size: 0.95em;\n}\n.lcslt-opt {\n    display: inline-block;\n    margin: 0 0 5px 5px;\n}\n.lcslt-multi-selected {\n\tdisplay: flex;\n\tposition: relative;\n\tline-height: normal;\n\talign-items: center;\n}\n.lcslt:not(.lcslt-disabled) .lcslt-multi-selected {\n    cursor: pointer;\n}\n.lcslt-multi-selected:before {\n    content: "\u00d7";\n    font-family: arial;\n}\n.lcslt-multi-callout {\n\tdisplay: inline-block;\n    line-height: 0;\n}\n.lcslt-placeholder {\n\tline-height: normal;\n\tpadding-bottom: 5px;\n}\n.lcslt-tabindex-trick {\n    position: fixed;\n    top: -99999px;\n}\n\n\n.lcslt-wrap,\n.lcslt-wrap *,\n#lc-select-dd,\n#lc-select-dd * {\n    box-sizing: border-box;\n}\n#lc-select-dd {\n\tvisibility: hidden;\n\tz-index: -100;\n\tposition: absolute;\n\ttop: -9999px;\n\tz-index: 999;\n\toverflow: hidden;\n\tborder-top: none;\n\tfont-size: 1rem;\n\tfont-family: sans-serif;\n}\n#lc-select-dd.lcslt-shown {\n    visibility: visible;\n    z-index: 99999999;\n}\n#lc-select-dd ul {\n\tmargin: 0;\n\tlist-style: none;\n}\n.lc-select-dd-scroll {\n    max-height: 200px;\n    overflow: auto;\n}\n.lcslt-search-li {\n    padding: 0 !important;\n    margin: 0 !important;\n    position: relative;\n}\n.lcslt-search-li input {\n    width: 100%;\n    padding-right: 36px;\n    line-height: normal;\n}\n.lcslt-search-li input[type=text] { /* for iOS safari */\n    border: none;\n    outline: none;\n    -webkit-appearance: none;\n    -webkit-border-radius: 0;\n}\n.lcslt-search-li input[type=text],\n.lcslt-search-li input[type=text]:hover,\n.lcslt-search-li input[type=text]:active,\n.lcslt-search-li input[type=text]:focus,\n.lcslt-search-li input[type=text]:focus-visible {\n    border: none;\n    outline: none;\n}\n.lcslt-search-li:before {\n    content: "";\n    position: absolute;\n    z-index: 10;\n    width: 25px;\n    height: 50%;\n    right: 8px;\n    top: 50%;\n    -webkit-mask:     url(\'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IiB3aWR0aD0iNTg3LjQ3MXB4IiBoZWlnaHQ9IjU4Ny40NzFweCIgdmlld0JveD0iMCAwIDU4Ny40NzEgNTg3LjQ3MSIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgNTg3LjQ3MSA1ODcuNDcxOyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+PGc+PGc+PHBhdGggZD0iTTIyMC4zMDIsNDQwLjYwNGMxMjEuNDc2LDAsMjIwLjMwMi05OC44MjYsMjIwLjMwMi0yMjAuMzAyQzQ0MC42MDQsOTguODI2LDM0MS43NzcsMCwyMjAuMzAyLDBDOTguODI2LDAsMCw5OC44MjYsMCwyMjAuMzAyQzAsMzQxLjc3Nyw5OC44MjYsNDQwLjYwNCwyMjAuMzAyLDQ0MC42MDR6IE0yMjAuMzAyLDcxLjE0MmM4Mi4yNDcsMCwxNDkuMTU5LDY2LjkxMywxNDkuMTU5LDE0OS4xNTljMCw4Mi4yNDgtNjYuOTEyLDE0OS4xNi0xNDkuMTU5LDE0OS4xNnMtMTQ5LjE2LTY2LjkxMi0xNDkuMTYtMTQ5LjE2QzcxLjE0MiwxMzguMDU1LDEzOC4wNTUsNzEuMTQyLDIyMC4zMDIsNzEuMTQyeiIvPjxwYXRoIGQ9Ik01MjUuNTIzLDU4Ny40NzFjMTYuNTU1LDAsMzIuMTEzLTYuNDQ3LDQzLjgwMS0xOC4xNThjMTEuNjk5LTExLjY4LDE4LjE0Ni0yNy4yMzQsMTguMTQ2LTQzLjc5MWMwLTE2LjU1My02LjQ0Ny0zMi4xMTUtMTguMTUyLTQzLjgyMkw0NDYuNjQzLDM1OS4wMjNjLTMuMjYyLTMuMjYyLTcuNDc1LTUuMDYxLTExLjg1OS01LjA2MWMtNS40NDksMC0xMC40NjUsMi43MTEtMTMuNzYyLDcuNDM4Yy0xNi4yMzgsMjMuMzE4LTM2LjI5Nyw0My4zNzctNTkuNjEzLDU5LjYxNWMtNC4yNTgsMi45NjUtNi45NDcsNy40NjctNy4zNzksMTIuMzUyYy0wLjQyOCw0LjgyOCwxLjM5Myw5LjY2Niw0Ljk5OCwxMy4yN2wxMjIuNjc0LDEyMi42NzZDNDkzLjQwNiw1ODEuMDIzLDUwOC45NjksNTg3LjQ3MSw1MjUuNTIzLDU4Ny40NzF6Ii8+PC9nPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48L3N2Zz4=\') no-repeat right center;\n    mask:     url(\'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IiB3aWR0aD0iNTg3LjQ3MXB4IiBoZWlnaHQ9IjU4Ny40NzFweCIgdmlld0JveD0iMCAwIDU4Ny40NzEgNTg3LjQ3MSIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgNTg3LjQ3MSA1ODcuNDcxOyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+PGc+PGc+PHBhdGggZD0iTTIyMC4zMDIsNDQwLjYwNGMxMjEuNDc2LDAsMjIwLjMwMi05OC44MjYsMjIwLjMwMi0yMjAuMzAyQzQ0MC42MDQsOTguODI2LDM0MS43NzcsMCwyMjAuMzAyLDBDOTguODI2LDAsMCw5OC44MjYsMCwyMjAuMzAyQzAsMzQxLjc3Nyw5OC44MjYsNDQwLjYwNCwyMjAuMzAyLDQ0MC42MDR6IE0yMjAuMzAyLDcxLjE0MmM4Mi4yNDcsMCwxNDkuMTU5LDY2LjkxMywxNDkuMTU5LDE0OS4xNTljMCw4Mi4yNDgtNjYuOTEyLDE0OS4xNi0xNDkuMTU5LDE0OS4xNnMtMTQ5LjE2LTY2LjkxMi0xNDkuMTYtMTQ5LjE2QzcxLjE0MiwxMzguMDU1LDEzOC4wNTUsNzEuMTQyLDIyMC4zMDIsNzEuMTQyeiIvPjxwYXRoIGQ9Ik01MjUuNTIzLDU4Ny40NzFjMTYuNTU1LDAsMzIuMTEzLTYuNDQ3LDQzLjgwMS0xOC4xNThjMTEuNjk5LTExLjY4LDE4LjE0Ni0yNy4yMzQsMTguMTQ2LTQzLjc5MWMwLTE2LjU1My02LjQ0Ny0zMi4xMTUtMTguMTUyLTQzLjgyMkw0NDYuNjQzLDM1OS4wMjNjLTMuMjYyLTMuMjYyLTcuNDc1LTUuMDYxLTExLjg1OS01LjA2MWMtNS40NDksMC0xMC40NjUsMi43MTEtMTMuNzYyLDcuNDM4Yy0xNi4yMzgsMjMuMzE4LTM2LjI5Nyw0My4zNzctNTkuNjEzLDU5LjYxNWMtNC4yNTgsMi45NjUtNi45NDcsNy40NjctNy4zNzksMTIuMzUyYy0wLjQyOCw0LjgyOCwxLjM5Myw5LjY2Niw0Ljk5OCwxMy4yN2wxMjIuNjc0LDEyMi42NzZDNDkzLjQwNiw1ODEuMDIzLDUwOC45NjksNTg3LjQ3MSw1MjUuNTIzLDU4Ny40NzF6Ii8+PC9nPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48L3N2Zz4=\') no-repeat right center;\n    -webkit-mask-size: contain;\n    mask-size: contain;\n    transform: translate3d(0, -53%, 0);\n}\n#lc-select-dd li {\n    width: 100%;\n    margin: 0;\n}\n#lc-select-dd li > div {\n    display: flex;\n    align-items: center;\n}\n#lc-select-dd li span {\n    word-break: break-all;\n}\n#lc-select-dd li span {\n    display: inline-block;\n    line-height: normal;\n}\n.lcslt-dd-opt:not(.lcslt-disabled):not(.lcslt-selected),\n.lcslt-multiple-dd .lcslt-dd-opt:not(.lcslt-disabled) {\n    cursor: pointer;\n}\n.lcslt-img {\n    background-position: center center;\n    background-repeat: no-repeat;\n    background-size: contain;\n    background-color: transparent;\n    vertical-align: top;\n    line-height: 0;\n    font-size: 0;\n}\n</style>')};
 this.init()};var A=function(g){if("string"!=typeof g)return g instanceof Element?[g]:Object.values(g);(g.match(/(#[0-9][^\s:,]*)/g)||[]).forEach(function(e){g=g.replace(e,'[id="'+e.replace("#","")+'"]')});return document.querySelectorAll(g)}})();