# starry
Finding the most starred repos of an organisation

### 1. Test
make POST requests to https://web-dep.appspot.com/repos with data as the specifed format `{"org": "verloop"}`

```
curl --header "Content-Type: application/json" --request POST \
  --data '{"org": "nvidia"}' https://web-dep.appspot.com/repos
```
### 2. Measure Response Time:
measure resonse time : `starry/response_time.py`

### 3. Logs
Find the logs in `starry/starry.log`

### 4. Solution to Bottlenecks:
Latency in Response time for organisations having large no.s of repos
- [Solved (partial)] using Redis