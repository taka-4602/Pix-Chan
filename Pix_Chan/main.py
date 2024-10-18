import requests
from time import sleep

def captcha(proxy:dict):
    responce=requests.get("https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Ld_hskiAAAAADfg9HredZvZx8Z_C8FrNJ519Rc6&co=aHR0cHM6Ly9waXhhaS5hcnQ6NDQz&hl=ja&v=aR-zv8WjtWx4lAw-tRCA-zca&size=invisible&cb=u2wj0bvs99s6",proxies=proxy).text
    recaptcha_token=responce.split('recaptcha-token" value="')[1].split('">')[0]
    payload={
        "v":"aR-zv8WjtWx4lAw-tRCA-zca",
        "reason":"q",
        "c":recaptcha_token,
        "k":"6Ld_hskiAAAAADfg9HredZvZx8Z_C8FrNJ519Rc6",
        "co":"aHR0cHM6Ly9waXhhaS5hcnQ6NDQz",
        "hl":"en",
        "size":"invisible",
        "chr":"",
        "vh":"",
        "bg":""
    }

    responce=requests.post(f"https://www.google.com/recaptcha/api2/reload?k=6Ld_hskiAAAAADfg9HredZvZx8Z_C8FrNJ519Rc6",data=payload,proxies=proxy).text
    try:
        token=responce.split('"rresp","')[1].split('"')[0]
    except:
        return False
    
    return token

class PixError(Exception):
    pass
class PixAI():
    def __init__(self,email:str,password:str,login:bool=True,token:str=None,proxy:dict=None) -> None:
        self.proxy=proxy
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://pixai.art",
            "Priority": "u=1, i",
            "Referer": "https://pixai.art/",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0  Safari/537.36"
        }

        if token:
            self.token=token
            self.headers["authorization"]=f"Bearer {self.token}"
            self.user_id=None
        else:
            payload={
                "query":"\n    mutation register($input: RegisterOrLoginInput!) {\n  register(input: $input) {\n    ...UserBase\n  }\n}\n    \n    fragment UserBase on User {\n  id\n  email\n  emailVerified\n  username\n  displayName\n  createdAt\n  updatedAt\n  avatarMedia {\n    ...MediaBase\n  }\n  membership {\n    membershipId\n    tier\n  }\n  isAdmin\n}\n    \n\n    fragment MediaBase on Media {\n  id\n  type\n  width\n  height\n  urls {\n    variant\n    url\n  }\n  imageType\n  fileUrl\n  duration\n  thumbnailUrl\n  hlsUrl\n  size\n  flag {\n    ...ModerationFlagBase\n  }\n}\n    \n\n    fragment ModerationFlagBase on ModerationFlag {\n  status\n  isSensitive\n  isMinors\n  isRealistic\n  isFlagged\n  isSexyPic\n  isSexyText\n  shouldBlur\n  isWarned\n}\n    ",
                "variables":{
                        "input":{
                            "email":email,
                            "password":password,
                            "recaptchaToken":captcha(self.proxy)
                            }
                        }
                    }

            if not payload["variables"]["input"]["recaptchaToken"]:
                raise PixError("キャプチャー失敗")
            
            if login:
                payload["query"]="\n    mutation login($input: RegisterOrLoginInput!) {\n  login(input: $input) {\n    ...UserDetail\n  }\n}\n    \n    fragment UserDetail on User {\n  ...UserBase\n  coverMedia {\n    ...MediaBase\n  }\n  followedByMe\n  followingMe\n  followerCount\n  followingCount\n  inspiredCount\n}\n    \n\n    fragment UserBase on User {\n  id\n  email\n  emailVerified\n  username\n  displayName\n  createdAt\n  updatedAt\n  avatarMedia {\n    ...MediaBase\n  }\n  membership {\n    membershipId\n    tier\n  }\n  isAdmin\n}\n    \n\n    fragment MediaBase on Media {\n  id\n  type\n  width\n  height\n  urls {\n    variant\n    url\n  }\n  imageType\n  fileUrl\n  duration\n  thumbnailUrl\n  hlsUrl\n  size\n  flag {\n    ...ModerationFlagBase\n  }\n}\n    \n\n    fragment ModerationFlagBase on ModerationFlag {\n  status\n  isSensitive\n  isMinors\n  isRealistic\n  isFlagged\n  isSexyPic\n  isSexyText\n  shouldBlur\n  isWarned\n}\n    "
            
            responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
            if "errors" in responce.json():
                raise PixError(responce.json())
            
            self.token=responce.headers["Token"]
            self.headers["authorization"]=f"Bearer {self.token}"

            if not login:
                self.user_id=responce.json()["data"]["register"]["id"]
                age_payload={
                    "query":"\n    mutation setPreferences($value: JSONObject!) {\n  setPreferences(value: $value)\n}\n    ",
                    "variables":{
                        "value":{
                            "experienceLevel":"beginner",
                            "ageVerificationStatus":"OVER18"
                            }
                        }
                    }
                responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=age_payload,proxies=self.proxy)
            else:
                self.user_id=responce.json()["data"]["login"]["id"]
        

    def get_quota(self):
        payload={"query":"\n    query getMyQuota {\n  me {\n    quotaAmount\n  }\n}\n    ","variables":{}}
        responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
        if "errors" in responce.json():
            raise PixError(responce.json())
        
        return int(responce.json()["data"]["me"]["quotaAmount"])

    def get_media(self,media_id:str):
        payload={
            "query":"\n    query getMedia($id: String!) {\n  media(id: $id) {\n    ...MediaBase\n  }\n}\n    \n    fragment MediaBase on Media {\n  id\n  type\n  width\n  height\n  urls {\n    variant\n    url\n  }\n  imageType\n  fileUrl\n  duration\n  thumbnailUrl\n  hlsUrl\n  size\n  flag {\n    ...ModerationFlagBase\n  }\n}\n    \n\n    fragment ModerationFlagBase on ModerationFlag {\n  status\n  isSensitive\n  isMinors\n  isRealistic\n  isFlagged\n  isSexyPic\n  isSexyText\n  shouldBlur\n  isWarned\n}\n    ",
            "variables":{"id":media_id}
            }
        
        responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
        if "errors" in responce.json():
            raise PixError(responce.json())
        
        return responce.json()["data"]["media"]["urls"][0]["url"]

    def claim_daily_quota(self):
        payload={"query":"\n    mutation dailyClaimQuota {\n  dailyClaimQuota\n}\n    "}
        responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
        if "errors" in responce.json():
            raise PixError(responce.json())
        
        return responce.json()
    
    def claim_questionnaire_quota(self,wait:int=3):
        form_data={
            'entry.64278853': self.user_id, 
            'entry.2090837715': '趣味に身を投じる人', 
            'entry.238512000': '18-25', 
            'entry.1451582794': '日本', 
            'entry.571931610': 'AI生成ツールをほとんど使ったことがない', 
            'entry.1078511207': 'Twitter', 
            'entry.1446121912': '好きなキャラクター', 
            'entry.2087342135': 'カートゥーン', 
            'entry.1264482712': '壁紙・プロフィール画像用', 
            'entry.1293236062': '7', 
        }
        requests.post("https://docs.google.com/forms/u/0/d/e/1FAIpQLSdYvAY6PDOVBl3Bd2FgnkCoz-G0KXk8OV_63gG96FIVYm0mEw/formResponse",data=form_data,proxies=self.proxy)
        payload={
            "query":"\n    mutation claimQuestReward($id: ID!) {\n  rewardQuest(id: $id) {\n    count\n  }\n}\n    ",
            "variables":{"id":"1723830082652557313"}
        }
        if wait>0:
            sleep(wait)

        responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
        if "errors" in responce.json():
            raise PixError(responce.json())
            
        return responce.json()

    def get_all_tasks(self):
        payload={
            "query":"\n    query listMyTasks($status: String, $before: String, $after: String, $first: Int, $last: Int) {\n  me {\n    tasks(\n      status: $status\n      before: $before\n      after: $after\n      first: $first\n      last: $last\n    ) {\n      pageInfo {\n        hasNextPage\n        hasPreviousPage\n        endCursor\n        startCursor\n      }\n      edges {\n        node {\n          ...TaskWithMedia\n        }\n      }\n    }\n  }\n}\n    \n    fragment TaskWithMedia on Task {\n  ...TaskBase\n  favoritedAt\n  artworkIds\n  media {\n    ...MediaBase\n  }\n}\n    \n\n    fragment TaskBase on Task {\n  id\n  userId\n  parameters\n  outputs\n  status\n  priority\n  runnerId\n  startedAt\n  endAt\n  createdAt\n  updatedAt\n  retryCount\n  paidCredit\n  moderationAction {\n    promptsModerationAction\n  }\n}\n    \n\n    fragment MediaBase on Media {\n  id\n  type\n  width\n  height\n  urls {\n    variant\n    url\n  }\n  imageType\n  fileUrl\n  duration\n  thumbnailUrl\n  hlsUrl\n  size\n  flag {\n    ...ModerationFlagBase\n  }\n}\n    \n\n    fragment ModerationFlagBase on ModerationFlag {\n  status\n  isSensitive\n  isMinors\n  isRealistic\n  isFlagged\n  isSexyPic\n  isSexyText\n  shouldBlur\n  isWarned\n}\n    ",
            "variables":{
                "last":30
                }
            }
        responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
        edges=responce.json()["data"]["me"]["tasks"]["edges"]
        mediaids_all=[]
        for edge in edges:
            mediaids=[]
            payload={
                "query":"\n    query getTaskById($id: ID!) {\n  task(id: $id) {\n    ...TaskDetail\n  }\n}\n    \n    fragment TaskDetail on Task {\n  ...TaskBase\n  favoritedAt\n  artworkId\n  artworkIds\n  artworks {\n    createdAt\n    hidePrompts\n    id\n    isNsfw\n    isSensitive\n    mediaId\n    title\n    updatedAt\n    flag {\n      ...ModerationFlagBase\n    }\n  }\n  media {\n    ...MediaBase\n  }\n  type {\n    type\n    model\n  }\n}\n    \n\n    fragment TaskBase on Task {\n  id\n  userId\n  parameters\n  outputs\n  status\n  priority\n  runnerId\n  startedAt\n  endAt\n  createdAt\n  updatedAt\n  retryCount\n  paidCredit\n  moderationAction {\n    promptsModerationAction\n  }\n}\n    \n\n    fragment ModerationFlagBase on ModerationFlag {\n  status\n  isSensitive\n  isMinors\n  isRealistic\n  isFlagged\n  isSexyPic\n  isSexyText\n  shouldBlur\n  isWarned\n}\n    \n\n    fragment MediaBase on Media {\n  id\n  type\n  width\n  height\n  urls {\n    variant\n    url\n  }\n  imageType\n  fileUrl\n  duration\n  thumbnailUrl\n  hlsUrl\n  size\n  flag {\n    ...ModerationFlagBase\n  }\n}\n    ",
                "variables":{
                    "id":edge["node"]["id"]
                    }
                }
            
            responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
            if "errors" in responce.json():
                raise PixError(responce.json())

            if responce.json()["data"]["task"]["status"]!="completed":
                mediaids.append(None)
                continue

            try:
                for batch in responce.json()["data"]["task"]["outputs"]["batch"]:
                    mediaids.append(batch["mediaId"])
            except:
                mediaids.append(responce.json()["data"]["task"]["outputs"]["mediaId"])

            mediaids_all.append(mediaids)

        return mediaids_all

    def get_latest_task(self):
        payload={
            "query":"\n    query listMyTasks($status: String, $before: String, $after: String, $first: Int, $last: Int) {\n  me {\n    tasks(\n      status: $status\n      before: $before\n      after: $after\n      first: $first\n      last: $last\n    ) {\n      pageInfo {\n        hasNextPage\n        hasPreviousPage\n        endCursor\n        startCursor\n      }\n      edges {\n        node {\n          ...TaskWithMedia\n        }\n      }\n    }\n  }\n}\n    \n    fragment TaskWithMedia on Task {\n  ...TaskBase\n  favoritedAt\n  artworkIds\n  media {\n    ...MediaBase\n  }\n}\n    \n\n    fragment TaskBase on Task {\n  id\n  userId\n  parameters\n  outputs\n  status\n  priority\n  runnerId\n  startedAt\n  endAt\n  createdAt\n  updatedAt\n  retryCount\n  paidCredit\n  moderationAction {\n    promptsModerationAction\n  }\n}\n    \n\n    fragment MediaBase on Media {\n  id\n  type\n  width\n  height\n  urls {\n    variant\n    url\n  }\n  imageType\n  fileUrl\n  duration\n  thumbnailUrl\n  hlsUrl\n  size\n  flag {\n    ...ModerationFlagBase\n  }\n}\n    \n\n    fragment ModerationFlagBase on ModerationFlag {\n  status\n  isSensitive\n  isMinors\n  isRealistic\n  isFlagged\n  isSexyPic\n  isSexyText\n  shouldBlur\n  isWarned\n}\n    ",
            "variables":{
                "last":30
                }
            }
        
        responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
        if "errors" in responce.json():
            raise PixError(responce.json())
        
        tasks=len(responce.json()["data"]["me"]["tasks"]["edges"])
        query_id=responce.json()["data"]["me"]["tasks"]["edges"][tasks-1]["node"]["id"]
        payload={
            "query":"\n    query getTaskById($id: ID!) {\n  task(id: $id) {\n    ...TaskDetail\n  }\n}\n    \n    fragment TaskDetail on Task {\n  ...TaskBase\n  favoritedAt\n  artworkId\n  artworkIds\n  artworks {\n    createdAt\n    hidePrompts\n    id\n    isNsfw\n    isSensitive\n    mediaId\n    title\n    updatedAt\n    flag {\n      ...ModerationFlagBase\n    }\n  }\n  media {\n    ...MediaBase\n  }\n  type {\n    type\n    model\n  }\n}\n    \n\n    fragment TaskBase on Task {\n  id\n  userId\n  parameters\n  outputs\n  status\n  priority\n  runnerId\n  startedAt\n  endAt\n  createdAt\n  updatedAt\n  retryCount\n  paidCredit\n  moderationAction {\n    promptsModerationAction\n  }\n}\n    \n\n    fragment ModerationFlagBase on ModerationFlag {\n  status\n  isSensitive\n  isMinors\n  isRealistic\n  isFlagged\n  isSexyPic\n  isSexyText\n  shouldBlur\n  isWarned\n}\n    \n\n    fragment MediaBase on Media {\n  id\n  type\n  width\n  height\n  urls {\n    variant\n    url\n  }\n  imageType\n  fileUrl\n  duration\n  thumbnailUrl\n  hlsUrl\n  size\n  flag {\n    ...ModerationFlagBase\n  }\n}\n    ",
            "variables":{
                "id":query_id
                }
            }
        
        try:
            if responce.json()["data"]["me"]["tasks"]["edges"][0]["node"]["status"]!="completed":
                return None
        except:
            return None
        
        mediaids=[]
        responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
        
        try:
            for batch in responce.json()["data"]["task"]["outputs"]["batch"]:
                mediaids.append(batch["mediaId"])
        except:
            mediaids.append(responce.json()["data"]["task"]["outputs"]["mediaId"])

        return mediaids

    def get_task_by_id(self,query_id:str):
        payload={
            "query":"\n    query getTaskById($id: ID!) {\n  task(id: $id) {\n    ...TaskDetail\n  }\n}\n    \n    fragment TaskDetail on Task {\n  ...TaskBase\n  favoritedAt\n  artworkId\n  artworkIds\n  artworks {\n    createdAt\n    hidePrompts\n    id\n    isNsfw\n    isSensitive\n    mediaId\n    title\n    updatedAt\n    flag {\n      ...ModerationFlagBase\n    }\n  }\n  media {\n    ...MediaBase\n  }\n  type {\n    type\n    model\n  }\n}\n    \n\n    fragment TaskBase on Task {\n  id\n  userId\n  parameters\n  outputs\n  status\n  priority\n  runnerId\n  startedAt\n  endAt\n  createdAt\n  updatedAt\n  retryCount\n  paidCredit\n  moderationAction {\n    promptsModerationAction\n  }\n}\n    \n\n    fragment ModerationFlagBase on ModerationFlag {\n  status\n  isSensitive\n  isMinors\n  isRealistic\n  isFlagged\n  isSexyPic\n  isSexyText\n  shouldBlur\n  isWarned\n}\n    \n\n    fragment MediaBase on Media {\n  id\n  type\n  width\n  height\n  urls {\n    variant\n    url\n  }\n  imageType\n  fileUrl\n  duration\n  thumbnailUrl\n  hlsUrl\n  size\n  flag {\n    ...ModerationFlagBase\n  }\n}\n    ",
            "variables":{
                "id":query_id
                }
            }
        responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
        if "errors" in responce.json():
            raise PixError(responce.json())
        
        try:
            if responce.json()["data"]["task"]["status"]!="completed":
                return None
        except:
            return None
        
        mediaids=[]
        try:
            for batch in responce.json()["data"]["task"]["outputs"]["batch"]:
                mediaids.append(batch["mediaId"])
        except:
            mediaids.append(responce.json()["data"]["task"]["outputs"]["mediaId"])

        return mediaids

    def generate_image(self,prompts:str,width:int=768,height:int=1280,x4:bool=False):
        payload={
            "query":"\n    mutation createGenerationTask($parameters: JSONObject!) {\n  createGenerationTask(parameters: $parameters) {\n    ...TaskBase\n  }\n}\n    \n    fragment TaskBase on Task {\n  id\n  userId\n  parameters\n  outputs\n  status\n  priority\n  runnerId\n  startedAt\n  endAt\n  createdAt\n  updatedAt\n  retryCount\n  paidCredit\n  moderationAction {\n    promptsModerationAction\n  }\n}\n    ",
            "variables":{
                "parameters":{
                    "prompts":prompts,
                    "extra":{},
                    "negativePrompts":"lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, quality bad, hands bad, eyes bad, face bad, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name\n",
                    "samplingSteps":25,#↑nsfwは消した、みんないらないよね？
                    "samplingMethod":"Euler a",
                    "cfgScale":6,
                    "seed":"",
                    "priority":1000,
                    "width":width,
                    "height":height,
                    "clipSkip":1,
                    "modelId":"1709400693561386681",
                    "controlNets":[]
                    }
                }
            }
        if x4:
            payload["batchSize"]=4

        responce=requests.post("https://api.pixai.art/graphql",headers=self.headers,json=payload,proxies=self.proxy)
        if "errors" in responce.json():
            raise PixError(responce.json())
        
        return responce.json()["data"]["createGenerationTask"]["id"]