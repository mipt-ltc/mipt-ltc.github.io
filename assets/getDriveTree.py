# py script that does this:
# 1. send get request in google drive for list of files in Notes folder
# 2. process info from request
# 3. Then goes in each subfolder and fill info for them in similar way
# 4. At the end it writes in the file "DriveTree" info that it has gathered 

import requests
import json
import warnings

def getProcessedInfo(parsedJson):
    parsedJson = parsedJson["items"]
    ans = {}
    for item in parsedJson:
        assert item["kind"] == "drive#file"
        assert len(item["parents"]) == 1
        if item["mimeType"] != "application/vnd.google-apps.folder":
            warnings.warn(item["mimeType"] + " it is not folder")
        item["parent"] = item["parents"][0]["id"]
        itemId = item["id"]
        del item["parents"]
        del item["id"]
        ans[itemId] = item 
    return ans

def getRequest(folderId):
    with open("apiKey.txt", "r") as f:
        apiKey = f.read()[:-1]  # last char is end of line
        
    url = 'https://www.googleapis.com/drive/v2/files?q="' + folderId + \
            '"+in+parents&key=' + apiKey + \
            '&fields=items/kind,items/id,items/title,items/mimeType,'\
            'items/parents/id'
    r = requests.get(url)
    parsed = json.loads(r.content)
    if(r.status_code != 200):
        print(getFancyRequestSrting(parsed))
        raise ValueError('Request problem')
    processedInfo = getProcessedInfo(parsed)
    
    return processedInfo
def getFancyRequestSrting(request):
    return json.dumps(request, indent=4, sort_keys=True)

def buildDriveTree(rootId):
    tree = getRequest(rootId)
    for folderId, folderInfo in tree.items():
        childFolder = getRequest(folderId)
        folderInfo["children"] = childFolder
        for folderId, folderInfo in folderInfo["children"].items():
            childFolder = getRequest(folderId)
            folderInfo["children"] = childFolder
        
    processedResponce = json.dumps(tree, indent=4, sort_keys=True)

    with open("driveInfo.json", "w") as f:
        f.write(processedResponce)

def main():
    folderId = "17tvogD2WnmudB-MqnAdxnNCC7CtZS-Gm"
    buildDriveTree(folderId)

#   print(getFancyRequestSrting(getRequest('19i5lNftoc3STk7rutBLBBLVoWEVhI5WQ')))
#   print(getFancyRequestSrting(getRequest('1l4HFzPH3OLaZTwZokkUhseEhb3q0ethw')))

if __name__ == "__main__":
    main()


