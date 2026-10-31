# Genuine cURL execution output

Captured from the running local Django server at 2026-10-31 20:35:24 +05:30 using curl.exe 8.22.0. Test credentials and auth tokens are intentionally omitted.

## loginuser (HTTP 200)
```json
{"token":"[redacted]","username":"curl_demo_f3a176fa"}
```

## getalldealers (HTTP 200)
```json
[{"id":5,"name":"Desert Sky Motors","city":"Phoenix","state":"AZ","address":"4100 N Central Ave","phone":"602-555-0191","description":"Explore a carefully selected range of vehicles at Desert Sky Motors."},{"id":4,"name":"Rocky Mountain Cars","city":"Denver","state":"CO","address":"6700 Leetsdale Dr","phone":"303-555-0164","description":"Explore a carefully selected range of vehicles at Rocky Mountain Cars."},{"id":3,"name":"Lakeside Automotive","city":"Chicago","state":"IL","address":"225 N Michigan Ave","phone":"312-555-0127","description":"Explore a carefully selected range of vehicles at Lakeside Automotive."},{"id":2,"name":"Prairie Auto Center","city":"Overland Park","state":"KS","address":"8400 W 135th St","phone":"913-555-0188","description":"Explore a carefully selected range of vehicles at Prairie Auto Center."},{"id":1,"name":"Heartland Motors","city":"Wichita","state":"KS","address":"1200 E Douglas Ave","phone":"316-555-0142","description":"Explore a carefully selected range of vehicles at Heartland Motors."}]
```

## getdealerbyid (HTTP 200)
```json
{"id":5,"name":"Desert Sky Motors","city":"Phoenix","state":"AZ","address":"4100 N Central Ave","phone":"602-555-0191","description":"Explore a carefully selected range of vehicles at Desert Sky Motors."}
```

## getdealerreviews (HTTP 200)
```json
[{"id":8,"dealership":5,"reviewer":"curl_demo_f3a176fa","text":"A genuinely helpful local dealership.","created_at":"2026-10-31T15:05:23.880171Z"},{"id":6,"dealership":5,"reviewer":"curl_demo_0fc30cee","text":"A genuinely helpful local dealership.","created_at":"2026-10-31T14:56:48.795154Z"},{"id":5,"dealership":5,"reviewer":"curl_demo_72aa65ba","text":"A genuinely helpful local dealership.","created_at":"2026-10-31T14:56:10.141222Z"},{"id":4,"dealership":5,"reviewer":"evidence_f725c64e","text":"A genuinely helpful local dealership.","created_at":"2026-10-31T14:54:57.629551Z"}]
```

## getdealersbyState (HTTP 200)
```json
[{"id":2,"name":"Prairie Auto Center","city":"Overland Park","state":"KS","address":"8400 W 135th St","phone":"913-555-0188","description":"Explore a carefully selected range of vehicles at Prairie Auto Center."},{"id":1,"name":"Heartland Motors","city":"Wichita","state":"KS","address":"1200 E Douglas Ave","phone":"316-555-0142","description":"Explore a carefully selected range of vehicles at Heartland Motors."}]
```

## getallcarmakes (HTTP 200)
```json
[{"id":3,"name":"Ford","models":["Escape","F-150","Mustang"]},{"id":2,"name":"Honda","models":["Accord","CR-V","Civic"]},{"id":4,"name":"Subaru","models":["Forester","Outback"]},{"id":1,"name":"Toyota","models":["Camry","Corolla","RAV4"]}]
```

## analyzereview (HTTP 200)
```json
{"sentiment":"positive","score":1}
```

## review_submission (HTTP 201)
```json
{"id":8,"dealership":5,"reviewer":"curl_demo_f3a176fa","text":"A genuinely helpful local dealership.","created_at":"2026-10-31T15:05:23.880171Z"}
```

## logoutuser (HTTP 200)
```json
{"message":"Logged out successfully."}
```
