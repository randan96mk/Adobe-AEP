/*
 * Reusable Web SDK event helpers (Chapter 6).
 * Field names follow the standard XDM field groups:
 *   - Web Details (web.webPageDetails)
 *   - Commerce Details (commerce.*, productListItems[])
 *   - AEP Web SDK ExperienceEvent (added to the schema for Web SDK data)
 */

// Page view + personalization in the same call
function sendPageView(pageName) {
  return alloy("sendEvent", {
    renderDecisions: true,
    xdm: {
      eventType: "web.webpagedetails.pageViews",
      web: { webPageDetails: { name: pageName, URL: window.location.href, pageViews: { value: 1 } } }
    }
  });
}

// Add the person ID after login so web history joins the CRM profile (Chapter 4)
function sendLogin(crmId) {
  sessionStorage.setItem("crmId", crmId);
  return alloy("sendEvent", {
    xdm: {
      eventType: "userAccount.login",
      identityMap: identityMapForLoggedInUser()
    }
  });
}

function identityMapForLoggedInUser() {
  const crmId = sessionStorage.getItem("crmId");
  return crmId
    ? { crmId: [{ id: crmId, authenticatedState: "authenticated", primary: false }] }
    : undefined;
}

function sendProductView(item) {
  return alloy("sendEvent", {
    xdm: {
      eventType: "commerce.productViews",
      identityMap: identityMapForLoggedInUser(),
      commerce: { productViews: { value: 1 } },
      productListItems: [item]
    }
  });
}

function sendAddToCart(item) {
  return alloy("sendEvent", {
    xdm: {
      eventType: "commerce.productListAdds",
      identityMap: identityMapForLoggedInUser(),
      commerce: { productListAdds: { value: 1 } },
      productListItems: [item]
    }
  });
}

function sendPurchase(orderId, items, currencyCode) {
  const total = items.reduce((sum, i) => sum + i.priceTotal, 0);
  return alloy("sendEvent", {
    xdm: {
      eventType: "commerce.purchases",
      identityMap: identityMapForLoggedInUser(),
      commerce: {
        purchases: { value: 1 },
        order: { purchaseID: orderId, priceTotal: total, currencyCode: currencyCode }
      },
      productListItems: items
    }
  });
}
