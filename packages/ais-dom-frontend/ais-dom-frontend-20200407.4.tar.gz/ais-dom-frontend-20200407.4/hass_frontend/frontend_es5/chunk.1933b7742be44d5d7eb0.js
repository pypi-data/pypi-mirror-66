(self.webpackJsonp=self.webpackJsonp||[]).push([[226],{522:function(t,e,n){"use strict";n.d(e,"a",function(){return i});var i=function(t,e){var n=e.operator||"==",i=e.value||e,r=e.attribute?t.attributes[e.attribute]:t.state;switch(n){case"==":return r===i;case"<=":return r<=i;case"<":return r<i;case">=":return r>=i;case">":return r>i;case"!=":return r!==i;case"regex":return r.match(i);default:return!1}}},840:function(t,e,n){"use strict";n.r(e);var i=n(323),r=n(301),o=n(522);function s(t){return(s="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}function a(t,e){for(var n=0;n<e.length;n++){var i=e[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}function f(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}function u(t){var e="function"==typeof Map?new Map:void 0;return(u=function(t){if(null===t||(n=t,-1===Function.toString.call(n).indexOf("[native code]")))return t;var n;if("function"!=typeof t)throw new TypeError("Super expression must either be null or a function");if(void 0!==e){if(e.has(t))return e.get(t);e.set(t,i)}function i(){return c(t,arguments,h(this).constructor)}return i.prototype=Object.create(t.prototype,{constructor:{value:i,enumerable:!1,writable:!0,configurable:!0}}),l(i,t)})(t)}function c(t,e,n){return(c=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],function(){})),!0}catch(t){return!1}}()?Reflect.construct:function(t,e,n){var i=[null];i.push.apply(i,e);var r=new(Function.bind.apply(t,i));return n&&l(r,n.prototype),r}).apply(null,arguments)}function l(t,e){return(l=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t})(t,e)}function h(t){return(h=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}function y(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}var d=function(t){function e(){var t,n,i,r;!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,e);for(var o=arguments.length,a=new Array(o),u=0;u<o;u++)a[u]=arguments[u];return i=this,n=!(r=(t=h(e)).call.apply(t,[this].concat(a)))||"object"!==s(r)&&"function"!=typeof r?f(i):r,y(f(n),"isPanel",void 0),y(f(n),"_editMode",!1),y(f(n),"_element",void 0),y(f(n),"_config",void 0),y(f(n),"_configEntities",void 0),y(f(n),"_baseCardConfig",void 0),y(f(n),"_hass",void 0),y(f(n),"_oldEntities",void 0),n}var n,c,d;return function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&l(t,e)}(e,u(HTMLElement)),n=e,(c=[{key:"getCardSize",value:function(){return this._element?this._element.getCardSize():1}},{key:"setConfig",value:function(t){if(!t.entities||!Array.isArray(t.entities))throw new Error("entities must be specified.");if(!(t.state_filter&&Array.isArray(t.state_filter)||t.entities.every(function(t){return"object"===s(t)&&t.state_filter&&Array.isArray(t.state_filter)})))throw new Error("Incorrect filter config.");this._config=t,this._configEntities=void 0,this._baseCardConfig=Object.assign({type:"entities",entities:[]},this._config.card),this.lastChild&&(this.removeChild(this.lastChild),this._element=void 0)}},{key:"haveEntitiesChanged",value:function(t){if(!this._hass)return!0;if(!this._configEntities)return!0;var e=!0,n=!1,i=void 0;try{for(var r,o=this._configEntities[Symbol.iterator]();!(e=(r=o.next()).done);e=!0){var s=r.value;if(this._hass.states[s.entity]!==t.states[s.entity]||this._hass.localize!==t.localize)return!0}}catch(a){n=!0,i=a}finally{try{e||null==o.return||o.return()}finally{if(n)throw i}}return!1}},{key:"_cardElement",value:function(){if(!this._element&&this._config){var t=Object(i.a)(this._baseCardConfig);this._element=t}return this._element}},{key:"editMode",set:function(t){this._editMode=t,this._element&&(this._element.editMode=t)}},{key:"hass",set:function(t){var e=this;if(t&&this._config)if(this.haveEntitiesChanged(t)){this._hass=t,this._configEntities||(this._configEntities=Object(r.a)(this._config.entities));var n=this._configEntities.filter(function(n){var i=t.states[n.entity];if(!i)return!1;if(n.state_filter){var r=!0,s=!1,a=void 0;try{for(var f,u=n.state_filter[Symbol.iterator]();!(r=(f=u.next()).done);r=!0){var c=f.value;if(Object(o.a)(i,c))return!0}}catch(_){s=!0,a=_}finally{try{r||null==u.return||u.return()}finally{if(s)throw a}}}else{var l=!0,h=!1,y=void 0;try{for(var d,p=e._config.state_filter[Symbol.iterator]();!(l=(d=p.next()).done);l=!0){var v=d.value;if(Object(o.a)(i,v))return!0}}catch(_){h=!0,y=_}finally{try{l||null==p.return||p.return()}finally{if(h)throw y}}}return!1});if(0!==n.length||!1!==this._config.show_empty){var i=this._cardElement();if(i){if("HUI-ERROR-CARD"!==i.tagName)this._oldEntities&&n.length===this._oldEntities.length&&n.every(function(t,n){return t===e._oldEntities[n]})||(this._oldEntities=n,i.setConfig(Object.assign({},this._baseCardConfig,{entities:n}))),i.isPanel=this.isPanel,i.editMode=this._editMode,i.hass=t;this.lastChild||this.appendChild(i),this.style.display="block"}}else this.style.display="none"}else this._hass=t}}])&&a(n.prototype,c),d&&a(n,d),e}();customElements.define("hui-entity-filter-card",d)}}]);
//# sourceMappingURL=chunk.1933b7742be44d5d7eb0.js.map