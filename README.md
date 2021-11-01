## Fake-API Web App

This repo is created for the blog post:
cURL: Hands-on Interacting with APIs

Website: http://fake-api-webapp.herokuapp.com/


<b>GET request: retrieve data from a specified resource</b>

- Retrieve all the players in the table as json format.
```
curl -X GET https://fake-api-webapp.herokuapp.com/players
```
- Return only response headers with -I option

```
curl -X GET -I https://fake-api-webapp.herokuapp.com
```
- Retrieve details of a specific player in the table
```
curl -X GET https://fake-api-webapp.herokuapp.com/players/1
```
<hr>

<b>POST request: performs resource-specific processing on the payload</b>

- Create a new player
```
curl -X POST https://fake-api-webapp.herokuapp.com/players \
                    -H "Content-Type: application/json" \
                    -d '{"name" : "Ibrahimovic","team": "AC Milan"}'
```
- Reset player's table

```
curl -X POST https://fake-api-webapp.herokuapp.com/reset

```
<hr>
<b>PUT request: replace the target resource with the request payload</b>

- Update the existing player's information

```
curl -X PUT https://fake-api-webapp.herokuapp.com/players/3 \
                    -H "Content-Type: application/json" \
                    -d '{"player_id": 3, "name" : "Lionel Messi","team": "PSG"}'
```
<hr>
<b>DELETE request: deletes the specified resources</b>

- Delete a player from the list
```
curl -X DELETE https://fake-api-webapp.herokuapp.com/players/1
```