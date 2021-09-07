from constants import *
import requests
import json
import yaml
import warnings


def getProcessedInfo(parsedJson, isLeaf):
    parsedJson = parsedJson["items"]
    ans = {}
    for item in parsedJson:
        assert item["kind"] == "drive#file"
        assert len(item["parents"]) == 1
        item["parent"] = item["parents"][0]["id"]
        if not isLeaf and item["mimeType"] != "application/vnd.google-apps.folder":
            print('Warning: ' + item['mimeType'] + 'is not folder')
            print('    parent folder:')
            print('    ' + DRIVE_FOLDER_URL + item["parent"])
        itemId = item["id"]
        del item["parents"]
        del item["id"]
        ans[itemId] = item 
    return ans

def getRequest(folderId, isLeaf=False):
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
    processedInfo = getProcessedInfo(parsed, isLeaf)
    
    return processedInfo
def getFancyRequestSrting(request):
    return json.dumps(request, indent=4, sort_keys=True)

def buildDriveTree(rootId):
    tree = getRequest(rootId)
    for folderId, folderInfo in tree.items():
        childFolder = getRequest(folderId)
        folderInfo["children"] = childFolder
        for folderId, folderInfo in folderInfo["children"].items():
            childFolder = getRequest(folderId, isLeaf=True)
            folderInfo["children"] = childFolder
        
    with open(DRIVE_OUTPUT, "w") as f:
        yaml.dump(tree, f, default_flow_style=False)

def main():
    folderId = DRIVE_ROOT_ID
    buildDriveTree(folderId)

if __name__ == "__main__":
    main()


