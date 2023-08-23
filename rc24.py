import os
import requests
from pick import pick
from tqdm import tqdm

banner = """
  _   ___  ___   _   _                _   _  ___  _        
 |_)   |    |   /   / \  |\ |  |\ |  |_  /    |    )  |_|_ 
 | \  _|_  _|_  \_  \_/  | \|  | \|  |_  \_   |   /_    |

  _    _                      _          _    _   _
 | \  / \  \    /  |\ |  |   / \   /\   | \  |_  |_)       
 |_/  \_/   \/\/   | \|  |_  \_/  /--\  |_/  |_  | \       
                                                               
\n\n
"""

def main():
    regions = ['USA', 'Europe', 'Korea', 'Japan']
    region, _ = pick(regions, banner+'Select your Wiis region: ')

    choices = ['Channels', 'IOS']
    choice, _ = pick(choices, banner+'Select Channels or IOS: ')

    if choice == 'Channels':
        channels = [
            'Check Mii Out Channel', 'Everybody Votes Channel', 'Forecast Channel',
            'News Channel', 'Nintendo Channel', 'Mii Contest Channel'
        ]
        selected_channels = pick_channels(channels)
        download_channels(region, list(selected_channels))
    elif choice == 'IOS':
        ios_wads = ['IOS31', 'IOS80']
        selected_ios = pick_ios_wads(ios_wads)
        download_ios(region, list(selected_ios))
        
def pick_channels(channels):
    selected_channels_tuples = pick(channels, banner+'Use Spacebar to select your channels and hit Enter (Some channels may not exist for some regions yet): ', multiselect=True)
    selected_channels = [channel_tuple[0] for channel_tuple in selected_channels_tuples]
    return selected_channels

def pick_ios_wads(ios_wads):
    selected_ios_tuples = pick(ios_wads, banner+'Use Spacebar to select your IOS and hit Enter: ', multiselect=True)
    selected_ios = [ios_tuple[0] for ios_tuple in selected_ios_tuples]
    return selected_ios

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    if response.status_code == 404:
        print("Not available yet. Pick a different option.")
        return

    with open(dest_path, 'wb') as file, tqdm(
            desc=dest_path,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)

def download_channels(region, selected_channels):
    base_url = "https://localhost.com/WADs/RiiConnect24"
    region_path = os.path.join("rc24", region)
    os.makedirs(region_path, exist_ok=True)

    for channel in selected_channels:
        formatted_channel = channel.replace(" ", "%20")
        download_url = f"{base_url}/{region}/{formatted_channel}%20({region})%20(Channel)%20(RiiConnect24).wad"
        dest_path = os.path.join(region_path, f"{channel}.wad")
        download_file(download_url, dest_path)

    print("Download completed!")

def download_ios(region, selected_ios):
    base_url = "https://localhost.com/WADs/RiiConnect24"
    region_path = os.path.join("rc24", region)
    os.makedirs(region_path, exist_ok=True)

    for ios_version in selected_ios:
        download_url = f"{base_url}/{region}/{ios_version}%20Wii%20Only%20(IOS)%20(RiiConnect24).wad"
        dest_path = os.path.join(region_path, f"{ios_version}.wad")
        download_file(download_url, dest_path)

    print("Download completed!")

if __name__ == "__main__":
    main()
