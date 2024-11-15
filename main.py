from selenium import webdriver
from selenium.webdriver.common.by import By
from csv import writer

def setDriver():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


def setTable(driver):

    playlist_name = driver.find_element(
        By.XPATH,
        '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/span[2]/h1',
    ).get_attribute("innerHTML")

    print("--", playlist_name, "--")
    table = driver.find_element(
        By.XPATH,
        '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div[1]/div[2]/div[2]',
    )
    return table

def writeToCSV(track):
    with open('playlist.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(track)
        f_object.close()


def getTracks(table):
    index = 2

    while 1:
        try:
            track = table.find_element(By.XPATH, "./div[@aria-rowindex='" + str(index) + "']") 
        except: 
            print("\nAll songs have been scanned") 
            break
        driver.execute_script("arguments[0].scrollIntoView();", track)

        track_info = []
        current_track = track.get_attribute("aria-rowindex")
        track_data = track.find_element(
            By.CSS_SELECTOR, 'div > div[aria-colindex="2"] > div '
        )
        track_name = track_data.find_element(By.CSS_SELECTOR, "a > div").get_attribute(
            "innerHTML"
        )
        track_artist = track_data.find_elements(
            By.CSS_SELECTOR, "span.standalone-ellipsis-one-line > div > a"
        )

        track_info.append(int(current_track) -1)
        track_info.append(track_name)
        output_artists =""
        for artist in track_artist:
            output_artists += artist.get_attribute("innerHTML") + ", "
        output_artists = output_artists[:-2]
        track_info.append(output_artists)

        writeToCSV(track_info)

        index = index + 1

if __name__ == "__main__":

    driver = setDriver()

    print("Link catre playlist: ")
    driver.get(
        "https://open.spotify.com/playlist/78xhpWhXna83q0CCkyouaJ?si=f386fcd88018486c"
    )

    table = setTable(driver)
    getTracks(table)

    driver.quit()
    exit(1)
