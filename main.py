from selenium import webdriver
from selenium.webdriver.common.by import By


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


def getTracks(table):
    index = 2

    while 1:
        try:
            track = table.find_element(By.XPATH, "./div[@aria-rowindex='" + str(index) + "']") #sa ii pun dupa elementu ala din atribut si ar trb sa mearga
        except: 
            print("\nAll songs have been scanned") 
            break
        driver.execute_script("arguments[0].scrollIntoView();", track)

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

        output = current_track + " " + track_name + " by "
        for artist in track_artist:
            output += artist.get_attribute("innerHTML") + ", "
        output = output[:-2]
        print(output)

        index = index + 1


# file = open("test.html", "w")
# file.write(tracks[1].get_attribute("outerHTML"))
# file.close()

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
