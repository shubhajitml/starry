# starry
Finding the most starred repos of an organisation

#### 0. Run locally

```console
python3 main.py
```
### 1. Test
make POST requests to https://starry.appspot.com/repos with data as the specifed format `{"org": "google"}`

```console
curl --header "Content-Type: application/json" --request POST \
  --data '{"org": "nvidia"}' https://web-dep.appspot.com/repos
```
### 2. Measure Response Time:
measure resonse time : `starry/response_time.py`

### 3. Logs
Find the logs in `starry/starry.log`

### 4. Solution to Bottlenecks:
Latency in Response time for organisations having large no.s of repos
- [Solved] using Redis

### TODO
- [x] Handle Pagination
- [ ] Endpoint Errors Handling
