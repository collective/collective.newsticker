!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?exports["collective.newsticker"]=t():e["collective.newsticker"]=t()}(this,function(){return function(e){function t(n){if(o[n])return o[n].exports;var i=o[n]={i:n,l:!1,exports:{}};return e[n].call(i.exports,i,i.exports,t),i.l=!0,i.exports}var o={};return t.m=e,t.c=o,t.i=function(e){return e},t.d=function(e,o,n){t.o(e,o)||Object.defineProperty(e,o,{configurable:!1,enumerable:!0,get:n})},t.n=function(e){var o=e&&e.__esModule?function(){return e.default}:function(){return e};return t.d(o,"a",o),o},t.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},t.p="++resource++collective.newsticker/",t(t.s=2)}([function(e,t){},function(e,t,o){e.exports=o.p+"newsticker-icon.png"},function(e,t,o){"use strict";o(0),o(1),$.fn.ticker=function(e){var t=$.extend({},$.fn.ticker.defaults,e);if(0==$(this).length)return window.console&&window.console.log?window.console.log("Element does not exist in DOM!"):alert("Element does not exist in DOM!"),!1;var o="#"+$(this).attr("id"),n=$(this).get(0).tagName;return this.each(function(){function e(e){var t=0,o=void 0;for(o in e)e.hasOwnProperty(o)&&t++;return t}function i(){var e=new Date;return e.getTime()}function d(e){t.debugMode&&(window.console&&window.console.log?window.console.log(e):alert(e))}function r(){s(),$(o).wrap('<div id="'+h.dom.wrapperID.replace("#","")+'"></div>'),$(h.dom.wrapperID).children().remove(),$(h.dom.wrapperID).append('<div id="'+h.dom.tickerID.replace("#","")+'" class="ticker">\n           <div id="'+h.dom.titleID.replace("#","")+'" class="ticker-title">\n             <span><!-- --></span>\n           </div>\n           <p id="'+h.dom.contentID.replace("#","")+'" class="ticker-content"></p>\n           <div id="'+h.dom.revealID.replace("#","")+'" class="ticker-swipe">\n             <span><!-- --></span>\n           </div>\n        </div>'),$(h.dom.wrapperID).removeClass("no-js").addClass("ticker-wrapper has-js "+t.direction),$(h.dom.tickerElem+","+h.dom.contentID).hide(),t.controls&&($(h.dom.controlsID).live("click mouseover mousedown mouseout mouseup",function(e){var t=e.target.id;if("click"==e.type)switch(t){case h.dom.prevID.replace("#",""):h.paused=!0,$(h.dom.playPauseID).addClass("paused"),u("prev");break;case h.dom.nextID.replace("#",""):h.paused=!0,$(h.dom.playPauseID).addClass("paused"),u("next");break;case h.dom.playPauseID.replace("#",""):1==h.play?(h.paused=!0,$(h.dom.playPauseID).addClass("paused"),p()):(h.paused=!1,$(h.dom.playPauseID).removeClass("paused"),m())}else"mouseover"==e.type&&$("#"+t).hasClass("controls")?$("#"+t).addClass("over"):"mousedown"==e.type&&$("#"+t).hasClass("controls")?$("#"+t).addClass("down"):"mouseup"==e.type&&$("#"+t).hasClass("controls")?$("#"+t).removeClass("down"):"mouseout"==e.type&&$("#"+t).hasClass("controls")&&$("#"+t).removeClass("over")}),$(h.dom.wrapperID).append('<ul id="'+h.dom.controlsID.replace("#","")+'" class="ticker-controls">\n             <li id="'+h.dom.playPauseID.replace("#","")+'" class="jnt-play-pause controls"><a href=""><!-- --></a></li>\n             <li id="'+h.dom.prevID.replace("#","")+'" class="jnt-prev controls"><a href=""><!-- --></a></li>\n             <li id="'+h.dom.nextID.replace("#","")+'" class="jnt-next controls"><a href=""><!-- --></a></li>\n          </ul>')),"fade"!=t.displayType&&$(h.dom.contentID).mouseover(function(){0==h.paused&&p()}).mouseout(function(){0==h.paused&&m()}),t.ajaxFeed||l()}function s(){if(0==h.contentLoaded)if(t.ajaxFeed)"xml"==t.feedType?$.ajax({url:t.feedUrl,cache:!1,dataType:t.feedType,async:!0,success:function(o){count=0;for(var n=0;n<o.childNodes.length;n++)"rss"==o.childNodes[n].nodeName&&(xmlContent=o.childNodes[n]);for(var i=0;i<xmlContent.childNodes.length;i++)"channel"==xmlContent.childNodes[i].nodeName&&(xmlChannel=xmlContent.childNodes[i]);for(var r=0;r<xmlChannel.childNodes.length;r++)if("item"==xmlChannel.childNodes[r].nodeName){xmlItems=xmlChannel.childNodes[r];for(var s=void 0,a=!1,c=0;c<xmlItems.childNodes.length;c++)"title"==xmlItems.childNodes[c].nodeName?s=xmlItems.childNodes[c].lastChild.nodeValue:"link"==xmlItems.childNodes[c].nodeName&&(a=xmlItems.childNodes[c].lastChild.nodeValue),s!==!1&&""!=s&&a!==!1&&(h.newsArr["item-"+count]={type:t.titleText,content:'<a href="'+a+'">'+s+"</a>"},count++,s=!1,a=!1)}return e(h.newsArr<1)?(d("Couldn't find any content from the XML feed for the ticker to use!"),!1):(h.contentLoaded=!0,void l())}}):d("Code Me!");else{if(!t.htmlFeed)return d("The ticker is set to not use any types of content! Check the settings for the ticker."),!1;if(!($(o+" LI").length>0))return d("Couldn't find HTML any content for the ticker to use!"),!1;$(o+" LI").each(function(e){h.newsArr["item-"+e]={type:t.titleText,content:$(this).html()}})}}function l(){h.contentLoaded=!0,$(h.dom.titleElem).html(h.newsArr["item-"+h.position].type),$(h.dom.contentID).html(h.newsArr["item-"+h.position].content),h.position==e(h.newsArr)-1?h.position=0:h.position++,a()}function a(){var e=$(h.dom.contentID).width(),o=e/t.speed;if($(h.dom.contentID).css("opacity","1"),!h.play)return!1;var n=$(h.dom.titleID).width()+20;$(h.dom.revealID).css(t.direction,n+"px"),"fade"==t.displayType?$(h.dom.revealID).hide(0,function(){$(h.dom.contentID).css(t.direction,n+"px").fadeIn(t.fadeInSpeed,c)}):"scroll"==t.displayType||$(h.dom.revealElem).show(0,function(){$(h.dom.contentID).css(t.direction,n+"px").show();var i="right"==t.direction?{marginRight:e+"px"}:{marginLeft:e+"px"};$(h.dom.revealID).css("margin-"+t.direction,"0px").delay(20).animate(i,o,"linear",c)})}function c(){h.play?($(h.dom.contentID).delay(t.pauseOnItems).fadeOut(t.fadeOutSpeed),"fade"==t.displayType?$(h.dom.contentID).fadeOut(t.fadeOutSpeed,function(){$(h.dom.wrapperID).find(h.dom.revealElem+","+h.dom.contentID).hide().end().find(h.dom.tickerID+","+h.dom.revealID).show().end().find(h.dom.tickerID+","+h.dom.revealID).removeAttr("style"),l()}):$(h.dom.revealID).hide(0,function(){$(h.dom.contentID).fadeOut(t.fadeOutSpeed,function(){$(h.dom.wrapperID).find(h.dom.revealElem+","+h.dom.contentID).hide().end().find(h.dom.tickerID+","+h.dom.revealID).show().end().find(h.dom.tickerID+","+h.dom.revealID).removeAttr("style"),l()})})):$(h.dom.revealElem).hide()}function p(){h.play=!1,$(h.dom.tickerID+","+h.dom.revealID+","+h.dom.titleID+","+h.dom.titleElem+","+h.dom.revealElem+","+h.dom.contentID).stop(!0,!0),$(h.dom.revealID+","+h.dom.revealElem).hide(),$(h.dom.wrapperID).find(h.dom.titleID+","+h.dom.titleElem).show().end().find(h.dom.contentID).show()}function m(){h.play=!0,h.paused=!1,c()}function u(t){switch(p(),t){case"prev":0==h.position?h.position=e(h.newsArr)-2:1==h.position?h.position=e(h.newsArr)-1:h.position=h.position-2,$(h.dom.titleElem).html(h.newsArr["item-"+h.position].type),$(h.dom.contentID).html(h.newsArr["item-"+h.position].content);break;case"next":$(h.dom.titleElem).html(h.newsArr["item-"+h.position].type),$(h.dom.contentID).html(h.newsArr["item-"+h.position].content)}h.position==e(h.newsArr)-1?h.position=0:h.position++}var f=i(),h={position:0,time:0,distance:0,newsArr:{},play:!0,paused:!1,contentLoaded:!1,dom:{contentID:"#ticker-content-"+f,titleID:"#ticker-title-"+f,titleElem:"#ticker-title-"+f+" SPAN",tickerID:"#ticker-"+f,wrapperID:"#ticker-wrapper-"+f,revealID:"#ticker-swipe-"+f,revealElem:"#ticker-swipe-"+f+" SPAN",controlsID:"#ticker-controls-"+f,prevID:"#prev-"+f,nextID:"#next-"+f,playPauseID:"#play-pause-"+f}};return"UL"!=n&&"OL"!=n&&t.htmlFeed===!0?(d("Cannot use <"+n.toLowerCase()+"> type of element for this plugin - must of type <ul> or <ol>"),!1):("rtl"==t.direction?t.direction="right":t.direction="left",void r())})},$.fn.ticker.defaults={speed:.1,ajaxFeed:!1,feedUrl:"",feedType:"xml",displayType:"reveal",htmlFeed:!0,debugMode:!0,controls:!0,titleText:"Latest",direction:"ltr",pauseOnItems:3e3,fadeInSpeed:600,fadeOutSpeed:300}}])});
//# sourceMappingURL=newsticker.js.map