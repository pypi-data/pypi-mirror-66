this.workbox=this.workbox||{},this.workbox.googleAnalytics=function(e,t,o,n,a,c,w){"use strict";try{self["workbox:google-analytics:4.1.1"]&&_()}catch(e){}const r=/^\/(\w+\/)?collect/,s=e=>async({queue:t})=>{let o;for(;o=await t.shiftRequest();){const{request:n,timestamp:a}=o,c=new URL(n.url);try{const w="POST"===n.method?new URLSearchParams(await n.clone().text()):c.searchParams,r=a-(Number(w.get("qt"))||0),s=Date.now()-r;if(w.set("qt",s),e.parameterOverrides)for(const t of Object.keys(e.parameterOverrides)){const o=e.parameterOverrides[t];w.set(t,o)}"function"==typeof e.hitFilter&&e.hitFilter.call(null,w),await fetch(new Request(c.origin+c.pathname,{body:w.toString(),method:"POST",mode:"cors",credentials:"omit",headers:{"Content-Type":"text/plain"}}))}catch(e){throw await t.unshiftRequest(o),e}}},i=e=>{const t=({url:e})=>"www.google-analytics.com"===e.hostname&&r.test(e.pathname),o=new w.NetworkOnly({plugins:[e]});return[new n.Route(t,o,"GET"),new n.Route(t,o,"POST")]},l=e=>{const t=new c.NetworkFirst({cacheName:e});return new n.Route(({url:e})=>"www.google-analytics.com"===e.hostname&&"/analytics.js"===e.pathname,t,"GET")},m=e=>{const t=new c.NetworkFirst({cacheName:e});return new n.Route(({url:e})=>"www.googletagmanager.com"===e.hostname&&"/gtag/js"===e.pathname,t,"GET")},u=e=>{const t=new c.NetworkFirst({cacheName:e});return new n.Route(({url:e})=>"www.googletagmanager.com"===e.hostname&&"/gtm.js"===e.pathname,t,"GET")};return e.initialize=((e={})=>{const n=o.cacheNames.getGoogleAnalyticsName(e.cacheName),c=new t.Plugin("workbox-google-analytics",{maxRetentionTime:2880,onSync:s(e)}),w=[u(n),l(n),m(n),...i(c)],r=new a.Router;for(const e of w)r.registerRoute(e);r.addFetchListener()}),e}({},workbox.backgroundSync,workbox.core._private,workbox.routing,workbox.routing,workbox.strategies,workbox.strategies);
//# sourceMappingURL=workbox-offline-ga.prod.js.map
