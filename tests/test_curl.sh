curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "tomoyuki-nohara",
 "recipient": "someone-other-address",
 "amount": 523
}' "http://localhost:5001/transactions/new"


curl -X GET "http://localhost:5001/mine"
curl -X GET "http://localhost:5001/chain"
curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://localhost:5001"]
}' "http://localhost:5001/nodes/register"
curl -X POST -H "Content-Type: application/json" -d '{
    "nodes": ["http://localhost:5000"]
}' "http://localhost:5001/nodes/register"


curl "http://localhost:5001/mine"
$ curl "http://localhost:5000/nodes/resolve"