# ASVS 4.1.1 Attack Analysis

## Why incorrect Content-Type is dangerous

When a response contains the wrong `Content-Type`, the browser may render or execute the payload incorrectly. This can allow attackers to exploit how the browser interprets data.

## Browser behaviour

Browsers use `Content-Type` and `charset` to parse responses. If the header is wrong, the browser may:

- render HTML as plain text
- execute script-like content unexpectedly
- apply different security policies than intended

## MIME sniffing

MIME sniffing occurs when the browser examines the response body to determine its actual type. It is a fallback mechanism that can introduce security issues when the declared header does not match the content.

## Incorrect rendering

If HTML is returned with `text/plain`, a browser may not execute embedded scripts. If HTML is returned with `text/html` but actual content is JSON, the browser may display invalid markup or expose structured data.

## XSS possibilities

A mismatched header can make it easier for an attacker to deliver payloads that execute in the wrong context. For example, if JSON is labeled `text/html`, a browser could treat data as markup and expand any embedded tags.

## Information disclosure

Incorrect MIME types can also expose data in the wrong format. A purely textual response with sensitive information may be interpreted as HTML or JSON, which can change how the client exposes or logs the data.

## Developer mistakes

Common mistakes include:

- forgetting to set `Content-Type`
- using a generic type such as `text/plain` or `application/octet-stream`
- omitting `charset=UTF-8` for text content
- sending JSON via a text or HTML content type

This lab shows secure headers and a vulnerable implementation so learners can compare how the same payload can behave differently depending on the response metadata.
