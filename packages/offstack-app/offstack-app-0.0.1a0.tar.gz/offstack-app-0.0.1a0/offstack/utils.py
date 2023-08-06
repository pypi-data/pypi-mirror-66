import os
import sys
import subprocess
import json

from getpass import getuser

from offstack.logger import logger

from .constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    FAVORITES,
    USERDATA
)

# Check if favorites exist
def check_favorites():
    if os.path.isfile(FAVORITES) and not os.stat(FAVORITES).st_size == 0:
        logger.debug("Favorites are locally stored.")
        return True
    logger.debug("[!] Favorites are not locally stored.")
    return False

# Check if user credentials exist
def check_user_credentials():
    if os.path.isfile(USERDATA):
        with open(USERDATA, 'r') as f:
            arr_len = f.readlines()
            if len(arr_len) > 1 and len(arr_len) < 4:
                logger.debug("User credentials are stored.")
                return True
            logger.debug("[!] User credentials are not stored, though file with user data exists.")
            return False
    logger.debug("[!] User credentials are not stored and neither does the user_data file exist.")
    return False

# Check if access token exists
def check_access_token():
    if os.path.isfile(USERDATA):
        with open(USERDATA, 'r') as f:
            arr_len = f.readlines()
            if len(arr_len) == 3:
                logger.debug("Access token is stored.")
                return True
            logger.debug("Access token is not stored.")
            return False
    logger.debug("[!] Access token is not stored and neither does the user_data file exist.")
    return False

def get_user_credentials():
    with open(USERDATA, 'r') as f:
        user_data = f.readlines()
        logger.debug("Retrieving user credentials.")
        return [data.strip("\n") for data in user_data]

# Request access token
def request_access_token(driver, oauth_manager, user_data):

    oauth_manager.get_authorization_state_url()

    driver._go_to(oauth_manager.authorization_url)

    with open(USERDATA, 'r') as f:
        user_data = f.readlines()

        print()
        print("Entering user data...")

        user_list_dict = [{'value': user_data[0], "xpath":'//*[@id="email"]'}, {'value': user_data[1], "xpath":'//*[@id="password"]'}]
        driver._type(*user_list_dict)

        driver._click('//*[@id="submit-button"]')
        
        print()
        print("Searching for access token...")

        url = driver._get_current_url()
        print(url)
        driver._quit()

        print()
        print("Extracting access token...")
        logger.debug("Extracting access token.")

        try:
            access_token, state = oauth_manager.extract_state_token(url)
            with open(USERDATA, 'a') as f:
                f.write("\n{0}".format(access_token))
                print()
                print("Access token saved to file.")
                logger.debug("Access token saved to file.")
                return True
        except TypeError:
            print("Unable to extract token! (It could be related to incorrect credentials)")
            logger.debug("[!] Unable to extract token! (It could be related to incorrect credentials or captcha)")
            # sys.exit(1)
            return False

# Get favorites
def request_favorites(oauth_manager):
    stored_access_token = False
    if not check_access_token():
        if not check_user_credentials():
            print("[!] Unable to request for favorites.")
            logger.debug("[!] Unable to send request favorites.")
            return False
            # prompt_user_credentials(bypass_check=True)

        access_token = request_access_token()
        with open(USERDATA, 'a') as f:
            f.write("\n{0}".format(access_token))
            print()
            print("Access token saved to file.")
            logger.debug("Access token saved to file.")
        
        stored_access_token = access_token

    if not stored_access_token:
        logger.debug("Access token exist, retrieving favorites from file.")
        with open(USERDATA, 'r') as f:
            user_data = f.readlines()
            stored_access_token = user_data[2]

    with open(FAVORITES, 'w') as f:
            json.dump(oauth_manager.fetch_from_api(stored_access_token).json(), f, indent=4)
            print()
            print("Favorites are locally stored!")
            logger.debug("Favorites are locally stored.")
            return True
        
def get_questions():
    if check_favorites():
        response_list = []
        with open(FAVORITES, 'r') as f:
            for el in json.load(f)['items']:
                for x in el:
                    # print("""
                    # Title:      {title}
                    # Text:       {text}
                    # Answered:   {is_answered}
                    # Views:      {views}
                    # Answers:    {answers}
                    # Score:      {score}
                    # Link:       {link}
                    # """.format(
                    #     title=el['title'], 
                    #     text=el['body_markdown'], 
                    #     is_answered=el['is_answered'], 
                    #     views=el['view_count'],
                    #     answers=el['answer_count'],
                    #     score=el['score'],
                    #     link=el['link'],))
                    response_dict = {
                        "question_id": el['question_id'],
                        "tags": el['tags'],
                        "title": el['title'],
                        # "text": el['body_markdown'],
                        "answered": el['is_answered'],
                        # "views": el['view_count'],
                        # "answers": el['answer_count'],
                        "score": el['score'],
                        # "link": el['link'],
                    }
                response_list.append(response_dict)
        logger.debug("Questions were collected.")
        return response_list                    
    return False

def display_favorite_question(favorite_id):
    """Return favorite related quesion, answers and other data."""
    if check_favorites():
        answers = ''
        with open(FAVORITES, "r") as f:
            for el in json.load(f)['items']:
                if el["question_id"] == favorite_id:
                    question = """
                    <h3>{title}</h3>
                    <br>
                    {body}
                    <br><br>
                    """.format(title=el["title"], body=el["body_markdown"])
                    resp_count = 1
                    for answer in el["answers"]:
                        answers = answers + """
                        <u>Accepted: {accepted}</u>
                        <br>
                        <a href="{link}">Link</a>
                        <br>
                        Response number: {number}
                        <br>
                        {response}
                        <br><br>
                        """.format(
                            accepted=answer["is_accepted"], 
                            link=answer["share_link"], 
                            number=str(resp_count), 
                            response=answer["body"])
                        resp_count += 1
                    logger.debug("Return favorite related quesion, answers and other data. Favorite Id: {}".format(favorite_id))
                    return (question, resp_count, answers)
            logger.debug("[!] Unable to find any favorite related quesion, answers and other data.")
            return False    

def check_root():
    """Check if the program was executed as root and prompt the user."""
    if os.geteuid() != 0:
        print(
            "[!] The program was not executed as root.\n"
            "[!] Please run as root."
        )
        sys.exit(1)

def get_user():
    try:
        user = os.environ["SUDO_USER"]
    except KeyError:
        user = getuser()

    return user

def change_owner(path):
    """Change the owner of specific files to the sudo user."""
    user = get_user()

    uid = int(subprocess.run(["id", "-u", user], stdout=subprocess.PIPE).stdout) # nosec
    gid = int(subprocess.run(["id", "-u", user], stdout=subprocess.PIPE).stdout) # nosec

    current_owner = subprocess.run(["id", "-nu", str(os.stat(path).st_uid)], stdout=subprocess.PIPE).stdout # nosec
    current_owner = current_owner.decode().rstrip("\n")

    # Only change file owner if it wasn't owned by current running user.
    if current_owner != user:
        os.chown(path, uid, gid)
