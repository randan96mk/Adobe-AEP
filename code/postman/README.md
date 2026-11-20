# Postman (Chapter 15)

Adobe maintains official Postman collections for the Experience Platform APIs. Use them for exploration and support; use the Python scripts in `code/api` for repeatable automation.

## Set up

1. Follow Adobe's guide: [Postman in Experience Platform](https://experienceleague.adobe.com/en/docs/experience-platform/landing/platform-apis/postman)
   (it links to the official Postman samples repository and to the collection in each API reference).
2. Create a Postman **environment** for each sandbox, e.g. `acme-dev`, with variables such as:

| Variable | Value |
| --- | --- |
| `CLIENT_ID` | OAuth Server-to-Server client ID |
| `CLIENT_SECRET` | client secret (mark as *secret* type) |
| `IMS_ORG` | `<ORG_ID>@AdobeOrg` |
| `SANDBOX_NAME` | e.g. `dev` |
| `SCOPES` | scopes from the Developer Console credential |
| `ACCESS_TOKEN` | filled by the token request |

3. Run the token request first, then any API request. Tokens expire after about 24 hours.

## Safety rules

- One environment per sandbox; colour-code or prefix the production environment.
- Never share exported environments that contain secrets.
- Double-check `SANDBOX_NAME` before sending write requests.

Hands-on lesson: [Set up Developer Console and Postman](https://experienceleague.adobe.com/en/docs/platform-learn/getting-started-for-data-architects-and-data-engineers/set-up-developer-console-and-postman)
