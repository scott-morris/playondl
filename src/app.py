import requests
from tqdm import tqdm
from timestamp import getTimestamp

class PlayOn:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-mmt-app': 'cloud-web',
            'x-mmt-version': '1.0',
            'Origin': 'https://www.playonrecorder.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.playonrecorder.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site', 
            'TE': 'trailers'
        }
        self.session = requests.Session()
    
    def login(self, username, password):
        formdata = { 'email': username, 'password': password }
        resp = requests.post(url='https://api.playonrecorder.com/v3/login', headers=self.headers, data=formdata)
        self.cookies = self.session.cookies

        if resp.json()['success'] == False:
            print('There was a problem with logging in')
            for key in resp.json():{ 
                print(key,":", resp.json()[key]) 
            }
            exit(1)

        self.data = resp.json()['data']
        self.headers['Authorization'] = self.data['token']


    def getDownloadList(self):
        timestamp = getTimestamp()
        resp = requests.get(url=f'https://api.playonrecorder.com/v3/library/all?_={timestamp}', headers=self.headers)
        
        if resp.json()['success'] == False:
            print(f'There was a problem retrieving the download list')
            for key in resp.json():{ 
                print(key,":", resp.json()[key]) 
            }
            exit(1)

        return resp.json()['data']['entries']

    def getDownloadInfo(self, id: str):
        timestamp = getTimestamp()
        url = f'https://api.playonrecorder.com/v3/library/{id}/download?_={timestamp}'

        resp = requests.get(url, headers=self.headers)
        
        if resp.json()['success'] == False:
            print(f'There was a problem retrieving the download info')
            for key in resp.json():{ 
                print(key,":", resp.json()[key]) 
            }
            exit(1)

        return resp.json()['data']

    def download(self, id: str, title: str) -> str:
        filename = f'{title}.mp4'

        downloadInfo = self.getDownloadInfo(id)
        url = downloadInfo['url']
        data = downloadInfo['data']
        cookies = []
        for key in data:
            cookies.append(f'{key}={data[key]}')

        headers = self.headers.copy()
        headers['Cookie'] = '; '.join(cookies)

        with requests.get(url, stream=True, headers=headers) as response:
            response.raise_for_status()
            
            # sizes in bytes
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024

            with tqdm(desc=title, total=total_size, unit="B", unit_scale=True) as progress_bar:
                with open(filename, "wb") as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)


            if total_size != 0 and progress_bar.n != total_size:
                raise RuntimeError("Could not download file")

            progress_bar.close()
            
        return filename
    
