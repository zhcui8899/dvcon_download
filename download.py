import urllib3
import os

#"http://events.dvcon.org/Europe/2018/proceedings/papers/01_3.pdf"
temp_str = "http://events.dvcon.org/{location}/{year:0d}/proceedings/{type_s}/{chapter:02d}_{item:0d}.pdf"

MAX_CHAPTER = 30
MAX_ITEM = 30

def download_file(connection, type_s, download_url):
    ##try to connect to the website, if not success, skip the writing file step.
    rsp = connection.request("GET", download_url)
    if (rsp.status != 200):
        return  False

    print("Downloading from {}".format(download_url))

    ##write to file, the name is the basename, such as 10_1.pdf
    file_name = type_s + "_" + os.path.basename(download_url)
    fd = open(file_name, "wb")
    fd.write(rsp.data)
    fd.close()

    rsp.close()

    return True

def main(connection):
    locations = ["USA", "Europe"]
    years = [2018, 2017, 2016]
    cur_dir = os.path.abspath(os.path.curdir)

    ##TODO: split this function into smaller ones.
    for location in locations:
        for year in years:
            rel_path = location + "_{year:0d}".format(year = year)
            ##create a subfolder, format: Europe_2018, US
            dir_name = os.path.join(cur_dir, rel_path)
            os.mkdir(dir_name)
            ##
            os.chdir(dir_name)

            ##if USA, url for location should be empty
            if(location == "USA"):
                location = ""

            for chapter in range(1, MAX_CHAPTER):
                for type_s in ["papers", "slides", "posters"]:
                        for item in range(1, MAX_ITEM):
                            s = temp_str.format(year = year,
                                                location = location,
                                                chapter = chapter,
                                                item = item,
                                                type_s  = type_s
                                                )
                            ret = download_file(connection, type_s, s)
                            if(not ret):
                                break

            ##change back.
            os.chdir(cur_dir)
            ##

if __name__ == "__main__":
    connection = urllib3.PoolManager()
    main(connection)
    connection.clear()