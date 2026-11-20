/*
 * Loading the Web SDK on an AEM Edge Delivery Services site (Chapter 6, architect tips).
 * EDS pages load in three phases (eager, lazy, delayed). Put martech in scripts/delayed.js
 * so it never slows the Largest Contentful Paint. Adapt names to your project's boilerplate.
 */
function loadScript(src) {
  return new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src;
    s.async = true;
    s.onload = resolve;
    s.onerror = reject;
    document.head.append(s);
  });
}

(async function initMartech() {
  // base code
  !function(n,o){o.forEach(function(o){n[o]||((n.__alloyNS=n.__alloyNS||[]).push(o),n[o]=
  function(){var u=arguments;return new Promise(function(i,l){n.setTimeout(function(){n[o].q.push([i,l,u])})})},
  n[o].q=[])})}(window,["alloy"]);

  await loadScript("https://cdn1.adoberesources.net/alloy/2.37.1/alloy.min.js");

  window.alloy("configure", {
    datastreamId: "<DATASTREAM_ID>",
    orgId: "<ORG_ID>@AdobeOrg",
    defaultConsent: "pending"
  });

  window.alloy("sendEvent", {
    xdm: {
      eventType: "web.webpagedetails.pageViews",
      web: { webPageDetails: { name: document.title, URL: window.location.href, pageViews: { value: 1 } } }
    }
  });
}());
