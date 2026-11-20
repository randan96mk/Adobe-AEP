/*
 * Consent handling (Chapter 6, section 7).
 * Configure the SDK with defaultConsent: "pending", then call one of these
 * when the consent banner (CMP) returns the visitor's choice.
 */
function grantConsent() {
  return alloy("setConsent", {
    consent: [{
      standard: "Adobe",
      version: "2.0",
      value: {
        collect: { val: "y" },
        marketing: { preferred: "email", any: { val: "y" } }
      }
    }]
  });
}

function denyConsent() {
  return alloy("setConsent", {
    consent: [{
      standard: "Adobe",
      version: "2.0",
      value: { collect: { val: "n" } }
    }]
  });
}
