from selenium import webdriver
from selenium.webdriver.common.by import By
from csv import writer


def setDriver():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


def getPlaylistInfo(driver):
    playlist_name = driver.find_element(
        By.XPATH,
        '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/span[2]/h1',
    ).get_attribute("innerHTML")
    playlist_name = str(playlist_name).replace(" ", "_")
    return playlist_name


def setTable(driver):
    table = driver.find_element(
        By.XPATH,
        '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div[1]/div[2]/div[2]',
    )
    return table


def writeToCSV(track):
    name = getPlaylistInfo(driver)
    name = name + ".csv"

    with open(name, mode="a", newline="", encoding="utf-8") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(track)
        f_object.close()


def resetCSV():
    name = getPlaylistInfo(driver)
    name = name + ".csv"

    header = ["Number", "Title", "Artists"]

    with open(name, mode="w", newline="") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(header)
        f_object.close()


def getTracks(table):
    index = 2

    while 1:
        try:
            track = table.find_element(
                By.XPATH, "./div[@aria-rowindex='" + str(index) + "']"
            )
        except:
            print("\nAll songs have been scanned")
            break
        driver.execute_script("arguments[0].scrollIntoView();", track)

        track_info = []
        current_track = track.get_attribute("aria-rowindex")

        try:
            track_data = track.find_element(
                By.CSS_SELECTOR, 'div > div[aria-colindex="2"] > div '
            )
            track_name = track_data.find_element(
                By.CSS_SELECTOR, "a > div"
            ).get_attribute("innerHTML")
            track_artist = track_data.find_elements(
                By.CSS_SELECTOR, "span.standalone-ellipsis-one-line > div > a"
            )
        except:
            track_name = "Unavalable song"
            track_artist = []

        track_info.append(int(current_track) - 1)
        track_info.append(track_name)
        output_artists = ""
        for artist in track_artist:
            output_artists += artist.get_attribute("innerHTML") + ", "
        
        if(len(output_artists)): output_artists = output_artists[:-2]
        track_info.append(str(output_artists))

        writeToCSV(track_info)

        index = index + 1


def writeTxtFile(driver, link):
    name = getPlaylistInfo(driver)
    name = name + ".txt"

    file = open(name, mode="w")

    playlist_name = driver.find_element(
        By.XPATH,
        '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/span[2]/h1',
    ).get_attribute("innerHTML")

    file.write("Title: ")
    file.write(playlist_name)
    file.write("\n\nAuthored by: ")

    playlist_author = driver.find_element(
        By.XPATH,
        '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/div/div[1]/span/a',
    ).get_attribute("innerHTML")
    file.write(playlist_author)

    song_counter = driver.find_element(
        By.XPATH,
        '//*[@id="main"]/div/div[2]/div[4]/div/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/div/div[2]/span[1]',
    ).get_attribute("innerHTML")
    file.write("\n\nContains ")
    file.write(song_counter)

    file.write("\n\nLink to playlist: ")
    file.write(link)

    file.write(
        '\n\n You can find a spreadsheet of the scraped songs at "song name".csv'
    )

    file.write("\n\n\nApp designed by Stresna George")

    file.close()


if __name__ == "__main__":

    driver = setDriver()

    print("Link to playlist: ")
    link = input()
    driver.get(link)

    resetCSV()

    table = setTable(driver)
    getTracks(table)

    writeTxtFile(driver, link)

    driver.quit()
    exit(1)
