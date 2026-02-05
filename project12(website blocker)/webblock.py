import datetime
import time

end_time = datetime.datetime.now() + datetime.timedelta(seconds=10)

site_block = "www.facebook.com"
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect_ip = "127.0.0.1"

print("Blocking website...")

while True:
    if datetime.datetime.now() < end_time:
        with open(hosts_path, "r+") as file:
            content = file.read()
            if site_block not in content:
                file.write(f"\n{redirect_ip} {site_block}")
    else:
        with open(hosts_path, "r+") as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                if site_block not in line:
                    file.write(line)
            file.truncate()

        print("Website unblocked.")
        break  

    time.sleep(2) 