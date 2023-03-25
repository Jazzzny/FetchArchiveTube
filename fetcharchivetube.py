import requests, tqdm, bs4, argparse

parser = argparse.ArgumentParser(
    usage='%(prog)s --download-video [Video ID]',
    description='Download a YouTube video from the Internet Archive.')

parser.add_argument('-d','--download-video', type=str, required=True,
                    help='The ID of the video to download.')

args = parser.parse_args()

vidid = args.download_video

metadata = requests.get(f"https://web.archive.org/cdx/search/cdx?url=http://youtu.be/{vidid}&output=json&filter=statuscode:302&limit=1&from=2013") #earlier versions of the youtube website did not have the same metadata format. TODO: imeplement support

if metadata.json()[1:]:
    metaurl = f"https://web.archive.org/web/{metadata.json()[1:][0][1]}/{metadata.json()[1:][0][2]}"
    print(f"Downloading video metadata from {metaurl}")
    response = requests.get(metaurl,allow_redirects=True)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    if soup.title.string.strip() != "Wayback Machine":
        title = soup.find('meta', attrs={'itemprop': 'name'})['content']
        thumbnailurl = soup.find('link', attrs={'itemprop': 'thumbnailUrl'})['href']
    else:
        print("Unable to download metadata! Continuing...")
        title = vidid
else:
    print("Unable to download metadata! Continuing...")
    title = vidid

response = requests.get(f"https://web.archive.org/web/2oe_/http://wayback-fakeurl.archive.org/yt/{vidid}", stream=True)

if response.status_code == 200:
    print(f"Downloading {title}...")
    total_size = int(response.headers.get('Content-Length', 0))
    block_size = 1024
    progress_bar = tqdm.tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(f"{title}.mp4", "wb") as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)

    progress_bar.close()
    print("Video downloaded successfully!")
else:
    print(f"Failed to locate video: {title} - This means that the Internet Archive does not have a copy of the requested video.")