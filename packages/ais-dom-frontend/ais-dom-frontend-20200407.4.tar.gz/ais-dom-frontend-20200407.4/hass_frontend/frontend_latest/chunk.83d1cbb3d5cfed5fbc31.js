(self.webpackJsonp=self.webpackJsonp||[]).push([[121],{187:function(e,t,r){"use strict";var i=r(0);function o(e){var t,r=l(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function n(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function a(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function l(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}!function(e,t,r,i){var d=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!s(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=l(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=c(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=c(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var p=0;p<i.length;p++)d=i[p](d);var u=t(function(e){d.initializeInstanceElements(e,h.elements)},r),h=d.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===c.key&&e.placement===c.placement},i=0;i<e.length;i++){var o,c=e[i];if("method"===c.kind&&(o=t.find(r)))if(a(c.descriptor)||a(o.descriptor)){if(s(c)||s(o))throw new ReferenceError("Duplicated methods ("+c.key+") can't be decorated.");o.descriptor=c.descriptor}else{if(s(c)){if(s(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+c.key+").");o.decorators=c.decorators}n(c,o)}else t.push(c)}return t}(u.d.map(o)),e);d.initializeClassElements(u.F,h.elements),d.runClassFinishers(u.F,h.finishers)}([Object(i.d)("ha-card")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.g)()],key:"header",value:void 0},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      :host {
        background: var(
          --ha-card-background,
          var(--paper-card-background-color, white)
        );
        border-radius: var(--ha-card-border-radius, 2px);
        box-shadow: var(
          --ha-card-box-shadow,
          0 2px 2px 0 rgba(0, 0, 0, 0.14),
          0 1px 5px 0 rgba(0, 0, 0, 0.12),
          0 3px 1px -2px rgba(0, 0, 0, 0.2)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 32px;
        padding: 24px 16px 16px;
        display: block;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid #e8e8e8;
        padding: 5px 16px;
      }
    `}},{kind:"method",key:"render",value:function(){return i.f`
      ${this.header?i.f`
            <div class="card-header">${this.header}</div>
          `:i.f``}
      <slot></slot>
    `}}]}},i.a)},188:function(e,t,r){"use strict";r.d(t,"a",function(){return n});r(120);const i=customElements.get("iron-icon");let o=!1;class n extends i{constructor(...e){var t,r,i;super(...e),i=void 0,(r="_iconsetName")in(t=this)?Object.defineProperty(t,r,{value:i,enumerable:!0,configurable:!0,writable:!0}):t[r]=i}listen(e,t,i){super.listen(e,t,i),o||"mdi"!==this._iconsetName||(o=!0,r.e(98).then(r.bind(null,240)))}}customElements.define("ha-icon",n)},191:function(e,t,r){"use strict";var i=r(8);t.a=Object(i.a)(e=>(class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}}))},196:function(e,t,r){"use strict";r.d(t,"a",function(){return n});var i=r(8),o=r(11);const n=Object(i.a)(e=>(class extends e{fire(e,t,r){return r=r||{},Object(o.a)(r.node||this,e,t,r)}}))},205:function(e,t,r){"use strict";var i=r(0),o=(r(244),r(211)),n=r(110),s=r(78);function a(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t,r){return(h="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=f(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function f(e){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const m=customElements.get("mwc-switch");!function(e,t,r,i){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!l(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=p(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=p(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t(function(e){o.initializeInstanceElements(e,h.elements)},r),h=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(d(n.descriptor)||d(o.descriptor)){if(l(n)||l(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(l(n)){if(l(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}c(n,o)}else t.push(n)}return t}(s.d.map(a)),e);o.initializeClassElements(s.F,h.elements),o.runClassFinishers(s.F,h.finishers)}([Object(i.d)("ha-switch")],function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[Object(i.g)({type:Boolean})],key:"haptic",value:()=>!1},{kind:"field",decorators:[Object(i.h)("slot")],key:"_slot",value:void 0},{kind:"method",key:"firstUpdated",value:function(){h(f(r.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--switch-checked-color)"),this.classList.toggle("slotted",Boolean(this._slot.assignedNodes().length)),this.addEventListener("change",()=>{this.haptic&&Object(n.a)("light")})}},{kind:"method",key:"render",value:function(){return i.f`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div
          class="mdc-switch__thumb-underlay"
          .ripple="${Object(s.a)({interactionNode:this})}"
        >
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              @change="${this._haChangeHandler}"
            />
          </div>
        </div>
      </div>
      <label for="basic-switch"><slot></slot></label>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[o.a,i.c`
        :host {
          display: flex;
          flex-direction: row;
          align-items: center;
        }
        .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
          background-color: var(--switch-checked-button-color);
          border-color: var(--switch-checked-button-color);
        }
        .mdc-switch.mdc-switch--checked .mdc-switch__track {
          background-color: var(--switch-checked-track-color);
          border-color: var(--switch-checked-track-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
          background-color: var(--switch-unchecked-button-color);
          border-color: var(--switch-unchecked-button-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
          background-color: var(--switch-unchecked-track-color);
          border-color: var(--switch-unchecked-track-color);
        }
        :host(.slotted) .mdc-switch {
          margin-right: 24px;
        }
      `]}},{kind:"method",key:"_haChangeHandler",value:function(e){this.mdcFoundation.handleChange(e),this.checked=this.formElement.checked}}]}},m)},208:function(e,t,r){"use strict";var i=r(0),o=r(70);function n(e){var t,r=d(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function a(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function l(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function d(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}!function(e,t,r,i){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!a(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=d(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=l(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=l(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var p=0;p<i.length;p++)o=i[p](o);var u=t(function(e){o.initializeInstanceElements(e,h.elements)},r),h=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(c(n.descriptor)||c(o.descriptor)){if(a(n)||a(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(a(n)){if(a(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}s(n,o)}else t.push(n)}return t}(u.d.map(n)),e);o.initializeClassElements(u.F,h.elements),o.runClassFinishers(u.F,h.finishers)}([Object(i.d)("ha-config-section")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.g)()],key:"isWide",value:()=>!1},{kind:"method",key:"render",value:function(){return i.f`
      <div
        class="content ${Object(o.a)({narrow:!this.isWide})}"
      >
        <div class="header"><slot name="header"></slot></div>
        <div
          class="together layout ${Object(o.a)({narrow:!this.isWide,vertical:!this.isWide,horizontal:this.isWide})}"
        >
          <div class="intro"><slot name="introduction"></slot></div>
          <div class="panel flex-auto"><slot></slot></div>
        </div>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      :host {
        display: block;
      }
      .content {
        padding: 28px 20px 0;
        max-width: 1040px;
        margin: 0 auto;
      }

      .layout {
        display: flex;
      }

      .horizontal {
        flex-direction: row;
      }

      .vertical {
        flex-direction: column;
      }

      .flex-auto {
        flex: 1 1 auto;
      }

      .header {
        font-family: var(--paper-font-headline_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-headline_-_-webkit-font-smoothing
        );
        font-size: var(--paper-font-headline_-_font-size);
        font-weight: var(--paper-font-headline_-_font-weight);
        letter-spacing: var(--paper-font-headline_-_letter-spacing);
        line-height: var(--paper-font-headline_-_line-height);
        opacity: var(--dark-primary-opacity);
      }

      .together {
        margin-top: 32px;
      }

      .intro {
        font-family: var(--paper-font-subhead_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-subhead_-_-webkit-font-smoothing
        );
        font-weight: var(--paper-font-subhead_-_font-weight);
        line-height: var(--paper-font-subhead_-_line-height);
        width: 100%;
        max-width: 400px;
        margin-right: 40px;
        opacity: var(--dark-primary-opacity);
        font-size: 14px;
        padding-bottom: 20px;
      }

      .panel {
        margin-top: -24px;
      }

      .panel ::slotted(*) {
        margin-top: 24px;
        display: block;
      }

      .narrow.content {
        max-width: 640px;
      }
      .narrow .together {
        margin-top: 20px;
      }
      .narrow .intro {
        padding-bottom: 20px;
        margin-right: 0;
        max-width: 500px;
      }
    `}}]}},i.a)},226:function(e,t,r){"use strict";r.d(t,"a",function(){return i}),r.d(t,"c",function(){return o}),r.d(t,"b",function(){return n});const i=function(){try{(new Date).toLocaleDateString("i")}catch(e){return"RangeError"===e.name}return!1}(),o=function(){try{(new Date).toLocaleTimeString("i")}catch(e){return"RangeError"===e.name}return!1}(),n=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()},234:function(e,t,r){"use strict";r.d(t,"a",function(){return n}),r.d(t,"b",function(){return s});var i=r(225),o=r(226);const n=o.b?(e,t)=>e.toLocaleString(t,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):e=>i.a.format(e,`${i.a.masks.longDate}, ${i.a.masks.shortTime}`),s=o.b?(e,t)=>e.toLocaleString(t,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",second:"2-digit"}):e=>i.a.format(e,`${i.a.masks.longDate}, ${i.a.masks.mediumTime}`)},238:function(e,t,r){"use strict";r(120);var i=r(188);customElements.define("ha-icon-next",class extends i.a{connectedCallback(){super.connectedCallback(),setTimeout(()=>{this.icon="ltr"===window.getComputedStyle(this).direction?"hass:chevron-right":"hass:chevron-left"},100)}})},256:function(e,t,r){"use strict";r(95),r(201);var i=r(4),o=r(32);customElements.define("ha-progress-button",class extends o.a{static get template(){return i.a`
      <style>
        .container {
          position: relative;
          display: inline-block;
        }

        mwc-button {
          transition: all 1s;
        }

        .success mwc-button {
          --mdc-theme-primary: white;
          background-color: var(--google-green-500);
          transition: none;
        }

        .error mwc-button {
          --mdc-theme-primary: white;
          background-color: var(--google-red-500);
          transition: none;
        }

        .progress {
          @apply --layout;
          @apply --layout-center-center;
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
        }
      </style>
      <div class="container" id="container">
        <mwc-button
          id="button"
          disabled="[[computeDisabled(disabled, progress)]]"
          on-click="buttonTapped"
        >
          <slot></slot>
        </mwc-button>
        <template is="dom-if" if="[[progress]]">
          <div class="progress"><paper-spinner active=""></paper-spinner></div>
        </template>
      </div>
    `}static get properties(){return{hass:{type:Object},progress:{type:Boolean,value:!1},disabled:{type:Boolean,value:!1}}}tempClass(e){var t=this.$.container.classList;t.add(e),setTimeout(()=>{t.remove(e)},1e3)}ready(){super.ready(),this.addEventListener("click",e=>this.buttonTapped(e))}buttonTapped(e){this.progress&&e.stopPropagation()}actionSuccess(){this.tempClass("success")}actionError(){this.tempClass("error")}computeDisabled(e,t){return e||t}})},438:function(e,t,r){"use strict";var i=r(0),o=(r(256),r(11));customElements.define("ha-call-api-button",class extends i.a{render(){return i.f`
      <ha-progress-button
        .progress="${this.progress}"
        @click="${this._buttonTapped}"
        ?disabled="${this.disabled}"
        ><slot></slot
      ></ha-progress-button>
    `}constructor(){super(),this.method="POST",this.data={},this.disabled=!1,this.progress=!1}static get properties(){return{hass:{},progress:Boolean,path:String,method:String,data:{},disabled:Boolean}}get progressButton(){return this.renderRoot.querySelector("ha-progress-button")}async _buttonTapped(){this.progress=!0;const e={method:this.method,path:this.path,data:this.data};try{const r=await this.hass.callApi(this.method,this.path,this.data);this.progress=!1,this.progressButton.actionSuccess(),e.success=!0,e.response=r}catch(t){this.progress=!1,this.progressButton.actionError(),e.success=!1,e.response=t}Object(o.a)(this,"hass-api-called",e)}})},439:function(e,t,r){"use strict";r.d(t,"a",function(){return o});var i=r(55);const o=(e,t)=>Object(i.a)(e,{message:t.localize("ui.common.successfully_saved")})},511:function(e,t,r){"use strict";r.d(t,"a",function(){return i});const i=e=>e.callWS({type:"webhook/list"})},574:function(e,t,r){"use strict";r.d(t,"a",function(){return i}),r.d(t,"b",function(){return o});const i=e=>e.callWS({type:"cloud/alexa/entities"}),o=e=>e.callWS({type:"cloud/alexa/sync"})},921:function(e,t,r){"use strict";r.r(t);r(95),r(193);var i=r(4),o=r(32),n=(r(187),r(438),r(165),r(108),r(208),r(0)),s=(r(157),r(201),r(205),r(511)),a=r(346),c=r(11);function l(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t,r){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function g(e){return(g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let v=function(e,t,r,i){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=h(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t(function(e){o.initializeInstanceElements(e,a.elements)},r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(u(n.descriptor)||u(o.descriptor)){if(p(n)||p(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(p(n)){if(p(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}d(n,o)}else t.push(n)}return t}(s.d.map(l)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}(null,function(e,t){class i extends t{constructor(){super(),e(this),this._progress=[]}}return{F:i,d:[{kind:"field",decorators:[Object(n.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"_cloudHooks",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"_localHooks",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"_progress",value:void 0},{kind:"method",key:"connectedCallback",value:function(){m(g(i.prototype),"connectedCallback",this).call(this),this._fetchData()}},{kind:"method",key:"render",value:function(){return n.f`
      ${this.renderStyle()}
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.webhooks.title")}
      >
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.webhooks.info")}
          ${this._renderBody()}

          <div class="footer">
            <a
              href="https://www.nabucasa.com/config/webhooks"
              target="_blank"
              rel="noreferrer"
            >
              ${this.hass.localize("ui.panel.config.cloud.account.webhooks.link_learn_more")}
            </a>
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"updated",value:function(e){m(g(i.prototype),"updated",this).call(this,e),e.has("cloudStatus")&&this.cloudStatus&&(this._cloudHooks=this.cloudStatus.prefs.cloudhooks||{})}},{kind:"method",key:"_renderBody",value:function(){return this.cloudStatus&&this._localHooks&&this._cloudHooks?0===this._localHooks.length?n.f`
        <div class="body-text">
          ${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet")}
          <a href="/config/integrations"
            >${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet_link_integration")}</a
          >
          ${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet2")}
          <a href="/config/automation/new"
            >${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet_link_automation")}</a
          >.
        </div>
      `:this._localHooks.map(e=>n.f`
        <div class="webhook" .entry="${e}">
          <paper-item-body two-line>
            <div>
              ${e.name}
              ${e.domain===e.name.toLowerCase()?"":` (${e.domain})`}
            </div>
            <div secondary>${e.webhook_id}</div>
          </paper-item-body>
          ${this._progress.includes(e.webhook_id)?n.f`
                <div class="progress">
                  <paper-spinner active></paper-spinner>
                </div>
              `:this._cloudHooks[e.webhook_id]?n.f`
                <mwc-button @click="${this._handleManageButton}">
                  ${this.hass.localize("ui.panel.config.cloud.account.webhooks.manage")}
                </mwc-button>
              `:n.f`
                <ha-switch @click="${this._enableWebhook}"></ha-switch>
              `}
        </div>
      `):n.f`
        <div class="body-text">
          ${this.hass.localize("ui.panel.config.cloud.account.webhooks.loading")}
        </div>
      `}},{kind:"method",key:"_showDialog",value:function(e){const t=this._localHooks.find(t=>t.webhook_id===e),i=this._cloudHooks[e];var o,n;o=this,n={webhook:t,cloudhook:i,disableHook:()=>this._disableWebhook(e)},Object(c.a)(o,"show-dialog",{dialogTag:"dialog-manage-cloudhook",dialogImport:()=>Promise.all([r.e(2),r.e(35)]).then(r.bind(null,898)),dialogParams:n})}},{kind:"method",key:"_handleManageButton",value:function(e){const t=e.currentTarget.parentElement.entry;this._showDialog(t.webhook_id)}},{kind:"method",key:"_enableWebhook",value:async function(e){const t=e.currentTarget.parentElement.entry;let r;this._progress=[...this._progress,t.webhook_id];try{r=await Object(a.d)(this.hass,t.webhook_id)}catch(i){return void alert(i.message)}finally{this._progress=this._progress.filter(e=>e!==t.webhook_id)}this._cloudHooks=Object.assign({},this._cloudHooks,{[t.webhook_id]:r}),0===this._progress.length&&this._showDialog(t.webhook_id)}},{kind:"method",key:"_disableWebhook",value:async function(e){this._progress=[...this._progress,e];try{await Object(a.e)(this.hass,e)}catch(r){return void alert(`${this.hass.localize("ui.panel.config.cloud.account.webhooks.disable_hook_error_msg")} ${r.message}`)}finally{this._progress=this._progress.filter(t=>t!==e)}const t=function(e,t){if(null==e)return{};var r,i,o={},n=Object.keys(e);for(i=0;i<n.length;i++)r=n[i],t.indexOf(r)>=0||(o[r]=e[r]);return o}(this._cloudHooks,[e].map(f));this._cloudHooks=t}},{kind:"method",key:"_fetchData",value:async function(){this._localHooks=this.hass.config.components.includes("webhook")?await Object(s.a)(this.hass):[]}},{kind:"method",key:"renderStyle",value:function(){return n.f`
      <style>
        .body-text {
          padding: 8px 0;
        }
        .webhook {
          display: flex;
          padding: 4px 0;
        }
        .progress {
          margin-right: 16px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .footer {
          padding-top: 16px;
        }
        .body-text a,
        .footer a {
          color: var(--primary-color);
        }
      </style>
    `}}]}},n.a);customElements.define("cloud-webhooks",v);var y=r(574);function b(e){var t,r=x(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function w(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function k(e){return e.decorators&&e.decorators.length}function E(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function _(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function x(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}let P=function(e,t,r,i){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!k(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=x(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=_(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=_(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t(function(e){o.initializeInstanceElements(e,a.elements)},r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(E(n.descriptor)||E(o.descriptor)){if(k(n)||k(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(k(n)){if(k(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}w(n,o)}else t.push(n)}return t}(s.d.map(b)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}(null,function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(n.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"_syncing",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return n.f``;const{alexa_enabled:e,alexa_report_state:t}=this.cloudStatus.prefs;return n.f`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.alexa.title")}
      >
        <div class="switch">
          <ha-switch
            .checked=${e}
            @change=${this._enabledToggleChanged}
          ></ha-switch>
        </div>
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.alexa.info")}
          <ul>
            <li>
              <a
                href="https://skills-store.amazon.com/deeplink/dp/B0772J1QKB?deviceType=app"
                target="_blank"
                rel="noreferrer"
              >
                ${this.hass.localize("ui.panel.config.cloud.account.alexa.enable_ha_skill")}
              </a>
            </li>
            <li>
              <a
                href="https://www.nabucasa.com/config/amazon_alexa/"
                target="_blank"
                rel="noreferrer"
              >
                ${this.hass.localize("ui.panel.config.cloud.account.alexa.config_documentation")}
              </a>
            </li>
          </ul>
          ${e?n.f`
                <div class="state-reporting">
                  <h3>
                    ${this.hass.localize("ui.panel.config.cloud.account.alexa.enable_state_reporting")}
                  </h3>
                  <div class="state-reporting-switch">
                    <ha-switch
                      .checked=${t}
                      @change=${this._reportToggleChanged}
                    ></ha-switch>
                  </div>
                </div>
                <p>
                  ${this.hass.localize("ui.panel.config.cloud.account.alexa.info_state_reporting")}
                </p>
              `:""}
        </div>
        <div class="card-actions">
          <mwc-button @click=${this._handleSync} .disabled=${this._syncing}>
            ${this.hass.localize("ui.panel.config.cloud.account.alexa.sync_entities")}
          </mwc-button>
          <div class="spacer"></div>
          <a href="/config/cloud/alexa">
            <mwc-button
              >${this.hass.localize("ui.panel.config.cloud.account.alexa.manage_entities")}</mwc-button
            >
          </a>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_handleSync",value:async function(){this._syncing=!0;try{await Object(y.b)(this.hass)}catch(e){alert(`${this.hass.localize("ui.panel.config.cloud.account.alexa.sync_entities_error")} ${e.body.message}`)}finally{this._syncing=!1}}},{kind:"method",key:"_enabledToggleChanged",value:async function(e){const t=e.target;try{await Object(a.k)(this.hass,{alexa_enabled:t.checked}),Object(c.a)(this,"ha-refresh-cloud-status")}catch(r){t.checked=!t.checked}}},{kind:"method",key:"_reportToggleChanged",value:async function(e){const t=e.target;try{await Object(a.k)(this.hass,{alexa_report_state:t.checked}),Object(c.a)(this,"ha-refresh-cloud-status")}catch(r){alert(`${this.hass.localize("ui.panel.config.cloud.account.alexa.state_reporting_error","enable_disable",this.hass.localize(t.checked?"ui.panel.config.cloud.account.alexa.enable":"ui.panel.config.cloud.account.alexa.disable"))} ${r.message}`),t.checked=!t.checked}}},{kind:"get",static:!0,key:"styles",value:function(){return n.c`
      a {
        color: var(--primary-color);
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 32px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
      .state-reporting {
        display: flex;
        margin-top: 1.5em;
      }
      .state-reporting + p {
        margin-top: 0.5em;
      }
      .state-reporting h3 {
        flex-grow: 1;
        margin: 0;
      }
      .state-reporting-switch {
        margin-top: 0.25em;
        margin-right: 7px;
        margin-left: 0.5em;
      }
    `}}]}},n.a);customElements.define("cloud-alexa-pref",P);var z=r(439);function D(e){var t,r=T(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function O(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function j(e){return e.decorators&&e.decorators.length}function S(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function C(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function T(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}let A=function(e,t,r,i){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!j(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=T(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=C(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=C(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t(function(e){o.initializeInstanceElements(e,a.elements)},r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(S(n.descriptor)||S(o.descriptor)){if(j(n)||j(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(j(n)){if(j(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}O(n,o)}else t.push(n)}return t}(s.d.map(D)),e);return o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}(null,function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(n.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"cloudStatus",value:void 0},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return n.f``;const{google_enabled:e,google_report_state:t,google_secure_devices_pin:r}=this.cloudStatus.prefs;return n.f`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.google.title")}
      >
        <div class="switch">
          <ha-switch
            id="google_enabled"
            .checked="${e}"
            @change="${this._enableToggleChanged}"
          ></ha-switch>
        </div>
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.google.info")}
          <ul>
            <li>
              <a
                href="https://assistant.google.com/services/a/uid/00000091fd5fb875?hl=en-US"
                target="_blank"
                rel="noreferrer"
              >
                ${this.hass.localize("ui.panel.config.cloud.account.google.enable_ha_skill")}
              </a>
            </li>
            <li>
              <a
                href="https://www.nabucasa.com/config/google_assistant/"
                target="_blank"
                rel="noreferrer"
              >
                ${this.hass.localize("ui.panel.config.cloud.account.google.config_documentation")}
              </a>
            </li>
          </ul>
          ${e?n.f`
                <div class="state-reporting">
                  <h3>
                    ${this.hass.localize("ui.panel.config.cloud.account.google.enable_state_reporting")}
                  </h3>
                  <div class="state-reporting-switch">
                    <ha-switch
                      .checked=${t}
                      @change=${this._reportToggleChanged}
                    ></ha-switch>
                  </div>
                </div>
                <p>
                  ${this.hass.localize("ui.panel.config.cloud.account.google.info_state_reporting")}
                </p>
                <div class="secure_devices">
                  <h3>
                    ${this.hass.localize("ui.panel.config.cloud.account.google.security_devices")}
                  </h3>
                  ${this.hass.localize("ui.panel.config.cloud.account.google.enter_pin_info")}
                  <paper-input
                    label="${this.hass.localize("ui.panel.config.cloud.account.google.devices_pin")}"
                    id="google_secure_devices_pin"
                    placeholder="${this.hass.localize("ui.panel.config.cloud.account.google.enter_pin_hint")}"
                    .value=${r||""}
                    @change="${this._pinChanged}"
                  ></paper-input>
                </div>
              `:""}
        </div>
        <div class="card-actions">
          <ha-call-api-button
            .hass=${this.hass}
            .disabled="${!e}"
            @hass-api-called=${this._syncEntitiesCalled}
            path="cloud/google_actions/sync"
          >
            ${this.hass.localize("ui.panel.config.cloud.account.google.sync_entities")}
          </ha-call-api-button>
          <div class="spacer"></div>
          <a href="/config/cloud/google-assistant">
            <mwc-button
              >${this.hass.localize("ui.panel.config.cloud.account.google.manage_entities")}</mwc-button
            >
          </a>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_syncEntitiesCalled",value:function(e){e.detail.success||404!==e.detail.response.status_code||alert(this.hass.localize("ui.panel.config.cloud.account.google.sync_entities_404_message"))}},{kind:"method",key:"_enableToggleChanged",value:async function(e){const t=e.target;try{await Object(a.k)(this.hass,{[t.id]:t.checked}),Object(c.a)(this,"ha-refresh-cloud-status")}catch(r){t.checked=!t.checked}}},{kind:"method",key:"_reportToggleChanged",value:async function(e){const t=e.target;try{await Object(a.k)(this.hass,{google_report_state:t.checked}),Object(c.a)(this,"ha-refresh-cloud-status")}catch(r){alert(`Unable to ${t.checked?"enable":"disable"} report state. ${r.message}`),t.checked=!t.checked}}},{kind:"method",key:"_pinChanged",value:async function(e){const t=e.target;try{await Object(a.k)(this.hass,{[t.id]:t.value||null}),Object(z.a)(this,this.hass),Object(c.a)(this,"ha-refresh-cloud-status")}catch(r){alert(`${this.hass.localize("ui.panel.config.cloud.account.google.enter_pin_error")} ${r.message}`),t.value=this.cloudStatus.prefs.google_secure_devices_pin}}},{kind:"get",static:!0,key:"styles",value:function(){return n.c`
      a {
        color: var(--primary-color);
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 32px;
      }
      ha-call-api-button {
        color: var(--primary-color);
        font-weight: 500;
      }
      .secure_devices {
        padding-top: 8px;
      }
      paper-input {
        width: 250px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
      .state-reporting {
        display: flex;
        margin-top: 1.5em;
      }
      .state-reporting + p {
        margin-top: 0.5em;
      }
      h3 {
        margin: 0 0 8px 0;
      }
      .state-reporting h3 {
        flex-grow: 1;
        margin: 0;
      }
      .state-reporting-switch {
        margin-top: 0.25em;
        margin-right: 7px;
        margin-left: 0.5em;
      }
    `}}]}},n.a);customElements.define("cloud-google-pref",A);function $(e){var t,r=W(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function F(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function I(e){return e.decorators&&e.decorators.length}function R(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function L(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function W(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}!function(e,t,r,i){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!I(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=W(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=L(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=L(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t(function(e){o.initializeInstanceElements(e,a.elements)},r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(R(n.descriptor)||R(o.descriptor)){if(I(n)||I(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(I(n)){if(I(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}F(n,o)}else t.push(n)}return t}(s.d.map($)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([Object(n.d)("cloud-remote-pref")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(n.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"cloudStatus",value:void 0},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return n.f``;const{remote_connected:e,remote_domain:t,remote_certificate:r}=this.cloudStatus;return r?n.f`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.remote.title")}
      >
        <div class="switch">
          <ha-switch
            .checked="${e}"
            @change="${this._toggleChanged}"
          ></ha-switch>
        </div>
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.remote.info")}
          ${e?this.hass.localize("ui.panel.config.cloud.account.remote.instance_is_available"):this.hass.localize("ui.panel.config.cloud.account.remote.instance_will_be_available")}
          <a
            href="https://${t}"
            target="_blank"
            class="break-word"
            rel="noreferrer"
          >
            https://${t}</a
          >.
        </div>
        <div class="card-actions">
          <a
            href="https://www.nabucasa.com/config/remote/"
            target="_blank"
            rel="noreferrer"
          >
            <mwc-button
              >${this.hass.localize("ui.panel.config.cloud.account.remote.link_learn_how_it_works")}</mwc-button
            >
          </a>
          ${r?n.f`
                <div class="spacer"></div>
                <mwc-button @click=${this._openCertInfo}>
                  ${this.hass.localize("ui.panel.config.cloud.account.remote.certificate_info")}
                </mwc-button>
              `:""}
        </div>
      </ha-card>
    `:n.f`
        <ha-card
          header=${this.hass.localize("ui.panel.config.cloud.account.remote.title")}
        >
          <div class="preparing">
            ${this.hass.localize("ui.panel.config.cloud.account.remote.access_is_being_prepared")}
          </div>
        </ha-card>
      `}},{kind:"method",key:"_openCertInfo",value:function(){var e,t;e=this,t={certificateInfo:this.cloudStatus.remote_certificate},Object(c.a)(e,"show-dialog",{dialogTag:"dialog-cloud-certificate",dialogImport:()=>Promise.all([r.e(2),r.e(46)]).then(r.bind(null,899)),dialogParams:t})}},{kind:"method",key:"_toggleChanged",value:async function(e){const t=e.target;try{t.checked?await Object(a.b)(this.hass):await Object(a.f)(this.hass),Object(c.a)(this,"ha-refresh-cloud-status")}catch(r){alert(r.message),t.checked=!t.checked}}},{kind:"get",static:!0,key:"styles",value:function(){return n.c`
      .preparing {
        padding: 0 16px 16px;
      }
      a {
        color: var(--primary-color);
      }
      .break-word {
        overflow-wrap: break-word;
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 32px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
    `}}]}},n.a);var B=r(196),H=r(234),M=r(191);customElements.define("cloud-account",class extends(Object(B.a)(Object(M.a)(o.a))){static get template(){return i.a`
      <style include="iron-flex ha-style">
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        .account-row {
          display: flex;
          padding: 0 16px;
        }
        mwc-button {
          align-self: center;
        }
        .soon {
          font-style: italic;
          margin-top: 24px;
          text-align: center;
        }
        .nowrap {
          white-space: nowrap;
        }
        .wrap {
          white-space: normal;
        }
        .status {
          text-transform: capitalize;
          padding: 16px;
        }
        a {
          color: var(--primary-color);
        }
      </style>
      <hass-subpage header="[[localize('ui.panel.config.cloud.caption')]]">
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header"
              >[[localize('ui.panel.config.cloud.caption')]]</span
            >
            <div slot="introduction">
              <p>
                [[localize('ui.panel.config.cloud.account.thank_you_note')]]
              </p>
            </div>

            <ha-card
              header="[[localize('ui.panel.config.cloud.account.nabu_casa_account')]]"
            >
              <div class="account-row">
                <paper-item-body two-line="">
                  [[cloudStatus.email]]
                  <div secondary class="wrap">
                    [[_formatSubscription(_subscription)]]
                  </div>
                </paper-item-body>
              </div>

              <div class="account-row">
                <paper-item-body
                  >[[localize('ui.panel.config.cloud.account.connection_status')]]</paper-item-body
                >
                <div class="status">[[cloudStatus.cloud]]</div>
              </div>

              <div class="card-actions">
                <a
                  href="https://account.nabucasa.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  <mwc-button
                    >[[localize('ui.panel.config.cloud.account.manage_account')]]</mwc-button
                  >
                </a>
                <mwc-button style="float: right" on-click="handleLogout"
                  >[[localize('ui.panel.config.cloud.account.sign_out')]]</mwc-button
                >
              </div>
            </ha-card>
          </ha-config-section>

          <ha-config-section is-wide="[[isWide]]">
            <span slot="header"
              >[[localize('ui.panel.config.cloud.account.integrations')]]</span
            >
            <div slot="introduction">
              <p>
                [[localize('ui.panel.config.cloud.account.integrations_introduction')]]
              </p>
              <p>
                [[localize('ui.panel.config.cloud.account.integrations_introduction2')]]
                <a
                  href="https://www.nabucasa.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  [[localize('ui.panel.config.cloud.account.integrations_link_all_features')]] </a
                >.
              </p>
            </div>

            <cloud-remote-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-remote-pref>

            <cloud-alexa-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-alexa-pref>

            <cloud-google-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-google-pref>

            <cloud-webhooks
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-webhooks>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,cloudStatus:Object,_subscription:{type:Object,value:null}}}ready(){super.ready(),this._fetchSubscriptionInfo()}_computeRemoteConnected(e){return e?this.hass.localize("ui.panel.config.cloud.account.connected"):this.hass.localize("ui.panel.config.cloud.account.not_connected")}async _fetchSubscriptionInfo(){this._subscription=await Object(a.h)(this.hass),this._subscription.provider&&this.cloudStatus&&"connected"!==this.cloudStatus.cloud&&this.fire("ha-refresh-cloud-status")}handleLogout(){this.hass.callApi("post","cloud/logout").then(()=>this.fire("ha-refresh-cloud-status"))}_formatSubscription(e){if(null===e)return this.hass.localize("ui.panel.config.cloud.account.fetching_subscription");let t=e.human_description;return e.plan_renewal_date&&(t=t.replace("{periodEnd}",Object(H.a)(new Date(1e3*e.plan_renewal_date),this.hass.language))),t}});r(119),r(77),r(107),r(256);var N=r(8),q=r(105),U=Object(N.a)(e=>(class extends e{navigate(...e){Object(q.a)(this,...e)}}));r(238);customElements.define("cloud-login",class extends(Object(M.a)(U(Object(B.a)(o.a)))){static get template(){return i.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        paper-item {
          cursor: pointer;
        }
        ha-card {
          overflow: hidden;
        }
        ha-card .card-header {
          margin-bottom: -8px;
        }
        h1 {
          @apply --paper-font-headline;
          margin: 0;
        }
        .error {
          color: var(--google-red-500);
        }
        .card-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        [hidden] {
          display: none;
        }
        .flash-msg {
          padding-right: 44px;
        }
        .flash-msg paper-icon-button {
          position: absolute;
          top: 8px;
          right: 8px;
          color: var(--secondary-text-color);
        }
      </style>
      <hass-subpage header="[[localize('ui.panel.config.cloud.caption')]]">
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header"
              >[[localize('ui.panel.config.cloud.caption')]]</span
            >
            <div slot="introduction">
              <p>
                [[localize('ui.panel.config.cloud.login.introduction')]]
              </p>
              <p>
                [[localize('ui.panel.config.cloud.login.introduction2')]]
                <a
                  href="https://www.nabucasa.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  Nabu&nbsp;Casa,&nbsp;Inc
                </a>
                [[localize('ui.panel.config.cloud.login.introduction2a')]]
              </p>
              <p>
                [[localize('ui.panel.config.cloud.login.introduction3')]]
              </p>
              <p>
                <a
                  href="https://www.nabucasa.com"
                  target="_blank"
                  rel="noreferrer"
                >
                  [[localize('ui.panel.config.cloud.login.learn_more_link')]]
                </a>
              </p>
            </div>

            <ha-card hidden$="[[!flashMessage]]">
              <div class="card-content flash-msg">
                [[flashMessage]]
                <paper-icon-button icon="hass:close" on-click="_dismissFlash"
                  >[[localize('ui.panel.config.cloud.login.dismiss')]]</paper-icon-button
                >
                <paper-ripple id="flashRipple" noink=""></paper-ripple>
              </div>
            </ha-card>

            <ha-card
              header="[[localize('ui.panel.config.cloud.login.sign_in')]]"
            >
              <div class="card-content">
                <div class="error" hidden$="[[!_error]]">[[_error]]</div>
                <paper-input
                  label="[[localize('ui.panel.config.cloud.login.email')]]"
                  id="email"
                  type="email"
                  value="{{email}}"
                  on-keydown="_keyDown"
                  error-message="[[localize('ui.panel.config.cloud.login.email_error_msg')]]"
                ></paper-input>
                <paper-input
                  id="password"
                  label="[[localize('ui.panel.config.cloud.login.password')]]"
                  value="{{_password}}"
                  type="password"
                  on-keydown="_keyDown"
                  error-message="[[localize('ui.panel.config.cloud.login.password_error_msg')]]"
                ></paper-input>
              </div>
              <div class="card-actions">
                <ha-progress-button
                  on-click="_handleLogin"
                  progress="[[_requestInProgress]]"
                  >[[localize('ui.panel.config.cloud.login.sign_in')]]</ha-progress-button
                >
                <button
                  class="link"
                  hidden="[[_requestInProgress]]"
                  on-click="_handleForgotPassword"
                >
                  [[localize('ui.panel.config.cloud.login.forgot_password')]]
                </button>
              </div>
            </ha-card>

            <ha-card>
              <paper-item on-click="_handleRegister">
                <paper-item-body two-line="">
                  [[localize('ui.panel.config.cloud.login.start_trial')]]
                  <div secondary="">
                    [[localize('ui.panel.config.cloud.login.trial_info')]]
                  </div>
                </paper-item-body>
                <ha-icon-next></ha-icon-next>
              </paper-item>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,email:{type:String,notify:!0},_password:{type:String,value:""},_requestInProgress:{type:Boolean,value:!1},flashMessage:{type:String,notify:!0},_error:String}}static get observers(){return["_inputChanged(email, _password)"]}connectedCallback(){super.connectedCallback(),this.flashMessage&&requestAnimationFrame(()=>requestAnimationFrame(()=>this.$.flashRipple.simulatedRipple()))}_inputChanged(){this.$.email.invalid=!1,this.$.password.invalid=!1,this._error=!1}_keyDown(e){13===e.keyCode&&(this._handleLogin(),e.preventDefault())}_handleLogin(){let e=!1;this.email&&this.email.includes("@")||(this.$.email.invalid=!0,this.$.email.focus(),e=!0),this._password.length<8&&(this.$.password.invalid=!0,e||(e=!0,this.$.password.focus())),e||(this._requestInProgress=!0,this.hass.callApi("post","cloud/login",{email:this.email,password:this._password}).then(()=>{this.fire("ha-refresh-cloud-status"),this.setProperties({email:"",_password:""})},e=>{this._password="";const t=e&&e.body&&e.body.code;if("PasswordChangeRequired"===t)return alert("[[localize('ui.panel.config.cloud.login.alert_password_change_required')]]"),void this.navigate("/config/cloud/forgot-password");const r={_requestInProgress:!1,_error:e&&e.body&&e.body.message?e.body.message:"Unknown error"};"UserNotConfirmed"===t&&(r._error="[[localize('ui.panel.config.cloud.login.alert_email_confirm_necessary')]]"),this.setProperties(r),this.$.email.focus()}))}_handleRegister(){this.flashMessage="",this.navigate("/config/cloud/register")}_handleForgotPassword(){this.flashMessage="",this.navigate("/config/cloud/forgot-password")}_dismissFlash(){setTimeout(()=>{this.flashMessage=""},200)}});var J=r(146);function K(e){var t,r=Y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function Q(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function G(e){return e.decorators&&e.decorators.length}function V(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function X(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function Y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function Z(e,t,r){return(Z="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=ee(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function ee(e){return(ee=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const te=["account","google-assistant","alexa"],re=["login","register","forgot-password"];!function(e,t,r,i){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!G(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=Y(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=X(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=X(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t(function(e){o.initializeInstanceElements(e,a.elements)},r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(V(n.descriptor)||V(o.descriptor)){if(G(n)||G(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(G(n)){if(G(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}Q(n,o)}else t.push(n)}return t}(s.d.map(K)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([Object(n.d)("ha-config-cloud")],function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[Object(n.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"isWide",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"narrow",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"route",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"cloudStatus",value:void 0},{kind:"field",key:"routerOptions",value(){return{defaultPage:"login",showLoading:!0,initialLoad:()=>this._cloudStatusLoaded,beforeRender:e=>{if(this.cloudStatus.logged_in){if(!te.includes(e))return"account"}else if(!re.includes(e))return"login"},routes:{login:{tag:"cloud-login"},register:{tag:"cloud-register",load:()=>r.e(34).then(r.bind(null,895))},"forgot-password":{tag:"cloud-forgot-password",load:()=>r.e(32).then(r.bind(null,896))},account:{tag:"cloud-account"},"google-assistant":{tag:"cloud-google-assistant",load:()=>Promise.all([r.e(15),r.e(33)]).then(r.bind(null,956))},alexa:{tag:"cloud-alexa",load:()=>Promise.all([r.e(15),r.e(31)]).then(r.bind(null,897))}}}}},{kind:"field",decorators:[Object(n.g)()],key:"_flashMessage",value:()=>""},{kind:"field",decorators:[Object(n.g)()],key:"_loginEmail",value:()=>""},{kind:"field",key:"_resolveCloudStatusLoaded",value:void 0},{kind:"field",key:"_cloudStatusLoaded",value(){return new Promise(e=>{this._resolveCloudStatusLoaded=e})}},{kind:"method",key:"firstUpdated",value:function(e){Z(ee(i.prototype),"firstUpdated",this).call(this,e),this.addEventListener("cloud-done",e=>{this._flashMessage=e.detail.flashMessage,Object(q.a)(this,"/config/cloud/login")})}},{kind:"method",key:"updated",value:function(e){if(Z(ee(i.prototype),"updated",this).call(this,e),e.has("cloudStatus")){const t=e.get("cloudStatus");void 0===t?this._resolveCloudStatusLoaded():t.logged_in!==this.cloudStatus.logged_in&&Object(q.a)(this,this.route.prefix,!0)}}},{kind:"method",key:"createElement",value:function(e){const t=Z(ee(i.prototype),"createElement",this).call(this,e);return t.addEventListener("email-changed",e=>{this._loginEmail=e.detail.value}),t.addEventListener("flash-message-changed",e=>{this._flashMessage=e.detail.value}),t}},{kind:"method",key:"updatePageEl",value:function(e){this.cloudStatus&&!this.cloudStatus.logged_in&&te.includes(this._currentPage)||("setProperties"in e?e.setProperties({hass:this.hass,email:this._loginEmail,isWide:this.isWide,cloudStatus:this.cloudStatus,flashMessage:this._flashMessage}):(e.hass=this.hass,e.email=this._loginEmail,e.isWide=this.isWide,e.narrow=this.narrow,e.cloudStatus=this.cloudStatus,e.flashMessage=this._flashMessage))}}]}},J.a)}}]);
//# sourceMappingURL=chunk.83d1cbb3d5cfed5fbc31.js.map