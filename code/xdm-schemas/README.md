# XDM examples

| File | What it is | Chapter |
| --- | --- | --- |
| `fieldgroup-loyalty.json` | Custom field group (Profile class) under the tenant namespace | 3 |
| `schema-loyalty-members.json` | Profile schema template: standard + custom field groups | 3 |
| `descriptor-identity-loyaltyid.json` | Identity descriptor making `loyaltyId` the primary identity | 3, 4 |
| `sample-profile-record.json` | One record that fits the loyalty schema | 3, 5 |
| `sample-web-event.json` | One ExperienceEvent as sent by the Web SDK (with identityMap) | 3, 6 |

Replace `<TENANT_ID>` with your tenant ID as returned by the Schema Registry `stats` call (e.g. `acmeretail`), so `_<TENANT_ID>` becomes `_acmeretail`.
`code/api/create_loyalty_schema.py` fills the placeholders automatically.
