(self.webpackJsonp=self.webpackJsonp||[]).push([[35],{897:function(e,n,o){"use strict";o.r(n);o(77);var t=o(4),r=o(32),i=(o(189),o(255),o(165),o(108),o(197)),a=o(192);function s(e){return(s="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function l(){var e=function(e,n){n||(n=e.slice(0));return Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(n)}}))}(['\n      <style include="iron-flex ha-style">\n        .content {\n          padding-bottom: 24px;\n          direction: ltr;\n        }\n\n        ha-card {\n          max-width: 600px;\n          margin: 0 auto;\n          margin-top: 24px;\n        }\n        h1 {\n          @apply --paper-font-headline;\n          margin: 0;\n        }\n        .error {\n          color: var(--google-red-500);\n        }\n        .card-actions {\n          display: flex;\n          justify-content: space-between;\n          align-items: center;\n        }\n        .card-actions a {\n          color: var(--primary-text-color);\n        }\n        [hidden] {\n          display: none;\n        }\n      </style>\n      <hass-subpage header=[[localize(\'ui.panel.config.cloud.forgot_password.title\')]]>\n        <div class="content">\n          <ha-card header=[[localize(\'ui.panel.config.cloud.forgot_password.subtitle\')]]>\n            <div class="card-content">\n              <p>\n                [[localize(\'ui.panel.config.cloud.forgot_password.instructions\')]]\n              </p>\n              <div class="error" hidden$="[[!_error]]">[[_error]]</div>\n              <paper-input\n                autofocus=""\n                id="email"\n                label="[[localize(\'ui.panel.config.cloud.forgot_password.email\')]]"\n                value="{{email}}"\n                type="email"\n                on-keydown="_keyDown"\n                error-message="[[localize(\'ui.panel.config.cloud.forgot_password.email_error_msg\')]]"\n              ></paper-input>\n            </div>\n            <div class="card-actions">\n              <ha-progress-button\n                on-click="_handleEmailPasswordReset"\n                progress="[[_requestInProgress]]"\n                >[[localize(\'ui.panel.config.cloud.forgot_password.send_reset_email\')]]</ha-progress-button\n              >\n            </div>\n          </ha-card>\n        </div>\n      </hass-subpage>\n    ']);return l=function(){return e},e}function c(e,n){for(var o=0;o<n.length;o++){var t=n[o];t.enumerable=t.enumerable||!1,t.configurable=!0,"value"in t&&(t.writable=!0),Object.defineProperty(e,t.key,t)}}function u(e,n){return!n||"object"!==s(n)&&"function"!=typeof n?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):n}function p(e){return(p=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function f(e,n){return(f=Object.setPrototypeOf||function(e,n){return e.__proto__=n,e})(e,n)}var d=function(e){function n(){return function(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}(this,n),u(this,p(n).apply(this,arguments))}var o,s,d;return function(e,n){if("function"!=typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(n&&n.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),n&&f(e,n)}(n,Object(a["a"])(Object(i["a"])(r["a"]))),o=n,d=[{key:"template",get:function(){return Object(t.a)(l())}},{key:"properties",get:function(){return{hass:Object,email:{type:String,notify:!0,observer:"_emailChanged"},_requestInProgress:{type:Boolean,value:!1},_error:{type:String,value:""}}}}],(s=[{key:"_emailChanged",value:function(){this._error="",this.$.email.invalid=!1}},{key:"_keyDown",value:function(e){13===e.keyCode&&(this._handleEmailPasswordReset(),e.preventDefault())}},{key:"_handleEmailPasswordReset",value:function(){var e=this;this.email&&this.email.includes("@")||(this.$.email.invalid=!0),this.$.email.invalid||(this._requestInProgress=!0,this.hass.callApi("post","cloud/forgot_password",{email:this.email}).then(function(){e._requestInProgress=!1,e.fire("cloud-done",{flashMessage:"[[localize('ui.panel.config.cloud.forgot_password.check_your_email')]]"})},function(n){return e.setProperties({_requestInProgress:!1,_error:n&&n.body&&n.body.message?n.body.message:"Unknown error"})}))}}])&&c(o.prototype,s),d&&c(o,d),n}();customElements.define("cloud-forgot-password",d)}}]);
//# sourceMappingURL=chunk.f2e71fae2bf684b12378.js.map