# curl Testing

## Valid signature

curl -i http://localhost:5000/transfer \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: <valid-signature>' \
  -d '{"amount":100,"recipient":"recipient-123","message":"Confirm transfer"}'

Expected secure response: 200 OK, verification passed.
Expected vulnerable response: 200 OK, verification skipped.

## Missing signature

curl -i http://localhost:5000/transfer \
  -H 'Content-Type: application/json' \
  -d '{"amount":100,"recipient":"recipient-123","message":"Confirm transfer"}'

Expected secure response: 401 Unauthorized.
Expected vulnerable response: 200 OK.

## Invalid signature

curl -i http://localhost:5000/transfer \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: invalidsignature' \
  -d '{"amount":100,"recipient":"recipient-123","message":"Confirm transfer"}'

Expected secure response: 403 Forbidden.
Expected vulnerable response: 200 OK.

## Modified request body

curl -i http://localhost:5000/transfer \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: <signature-for-original-body>' \
  -d '{"amount":200,"recipient":"recipient-456","message":"Tampered"}'

Expected secure response: 403 Forbidden.
Expected vulnerable response: 200 OK.
