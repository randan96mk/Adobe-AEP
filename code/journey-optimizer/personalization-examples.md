# AJO personalization examples (Chapter 12)

Syntax is based on Handlebars. Paths below assume the tenant namespace `_acmeretail`;
check field paths with the personalization editor's attribute browser.

## Profile attributes

```text
Hi {{profile.person.name.firstName}},
Your points balance is {{profile._acmeretail.loyalty.points}}.
```

## Default value when a field is empty

Use the editor's **default fallback text** option on the attribute, or a condition:

```text
Hi {%#if profile.person.name.firstName%}{{profile.person.name.firstName}}{%else%}there{%/if%},
```

## Conditions

```text
{%#if profile._acmeretail.loyalty.tier = "gold"%}
  Free express delivery for Gold members.
{%elseif profile._acmeretail.loyalty.tier = "silver"%}
  Free standard delivery for Silver members.
{%else%}
  Free delivery on orders over £50.
{%/if%}
```

## Loop over items from the journey event

```text
{{#each context.journey.events.<EVENT_ID>.productListItems as |product|}}
  {{product.name}} - £{{product.priceTotal}}
{{/each}}
```

## Audience membership

```text
{%#if inAudience("<AUDIENCE_NAME>")%}
  Special message for this audience.
{%/if%}
```

Always preview with **test profiles** and the **simulate content** option before activating.
Docs: [Personalization in Journey Optimizer](https://experienceleague.adobe.com/en/docs/journey-optimizer/using/personalization/personalize)
