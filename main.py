#####################################################################################################
# An API server that handles the requests for getting the top-3 starred repo(s) 
# of a github organisation
# 
# Author: Shubhajit Das
# Email: shubhajitdas121@gmail.com
# Creation Date: 03 Sept 2019
# Last Modified: 05 Sept 2019
# reference: https://developer.github.com/v3/
#####################################################################################################

import os
import requests
import json 
import time
import logging
from sanic import Sanic
from sanic.response import json as jsn
from sanic_redis import SanicRedis

logging.basicConfig(filename="starry.log", level=logging.INFO,\
    format="%(asctime)s:%(levelname)s:%(message)s")

class GitHub(object):
    """Operations on github repos using github's REST API v3"""
    def __init__(self, org_name):
        # generate the api token from https://github.com/settings/tokens
        self.GITHUB_TOKEN = "fb882ebb789863a2b6a6766d38421ec8ba9b5ff0"
        # github url of the org
        self.ORG_URL = f"https://api.github.com/orgs/{org_name}/repos?type=sources&per_page=100&page=1"

    def count_stars(self) -> (str,int):
        """
        Fetches repositories data (name, stars) of a github organisation
        
        - Args:
            - org_name (string) : name of the organisation \n
            
        - Returns:
            - result_list (list) : list containing top-3 repo name and number of stars
            - int : an integer containing the length of the repos_list
        """
        res=requests.get(self.ORG_URL,headers={"Authorization": self.GITHUB_TOKEN})
        repos_list=res.json()
        # results for all pages (as github provides 100 pages at max)    
        while 'next' in res.links.keys():
            res=requests.get(res.links['next']['url'],headers={"Authorization": self.GITHUB_TOKEN})
            repos_list.extend(res.json())
        
        # sort the repo by stars and return top-3 results in desired format
        result_list = []
        repos_list = sorted(repos_list, key=lambda x: x['stargazers_count'], reverse=True)
        for repo in repos_list[:3]:
            result_list.append({"name":repo["name"], "stars":repo["stargazers_count"]})
        
        return result_list, len(repos_list)

#  API Server
app = Sanic()

app.config.update( { 'REDIS': { 'address': ('localhost', int(os.environ.get('REDIS_PORT', 6379)))} } )
redis = SanicRedis(app)

@app.route("/repos", methods=["POST",])
async def repos(request):
    start = time.time()
    org_name = request.json["org"]
    
    # establish a connection pool
    with await redis.conn as rd:
        results = await rd.get(org_name)

        # if result can't be found in redis
        if(not results):
            results, num_repos = GitHub(org_name).count_stars()
            await rd.set(org_name, str(results)) # set string value in redis
            logging.info(f"{results},\nres_time:{time.time()-start:.3f}sec,\
                 num_repos:{num_repos}, added to redis\n")
            return jsn({"results":results})

        # if result found in redis
        else: 
            logging.info(f"{results},\nres_time:{time.time()-start:.3f}sec, found in redis\n")
            return jsn({"results":results})
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
    # org_name = ["pytorch", "verloop", "nvidia", "openai", "tensorflow", "huggingface", "google", "facebook", "microsoft", "apache", "boostorg"]    