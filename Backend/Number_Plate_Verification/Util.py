import string
import easyocr
import random
from pymongo import MongoClient

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['test_database']
collection = db['data_lists']

# Code to access all lists
all_data = collection.find_one()

# accessing verified number plates
verified_num_plates = all_data['num_plates']


#Function to find top k number according to score
def top_k_scores(num_score, k):
    """
    The function `top_k_scores` takes a list of scores and an integer `k` as input, and returns the top
    `k` scores in descending order.
    
    :param num_score: The `num_score` parameter is a list of tuples, where each tuple contains a score
    and its corresponding index. The scores are used to determine the order of the tuples, and the
    indices are used to identify the scores
    :param k: The parameter `k` represents the number of top scores you want to retrieve from the list
    of scores
    :return: the top k scores from the given list of scores.
    """
    #Helper function for partition
    def partition(num_score, left, right):
        pivot_index = random.randint(left, right)
        pivot = num_score[pivot_index][1]
        num_score[right], num_score[pivot_index] = num_score[pivot_index], num_score[right]
        i = left
        for j in range(left, right):
            if num_score[j][1] > pivot:
                num_score[i], num_score[j] = num_score[j], num_score[i]
                i += 1
        num_score[i], num_score[right] = num_score[right], num_score[i]
        return i
    
    left = 0
    right = len(num_score) - 1
    while left <= right:
        pivot_index = partition(num_score, left, right)
        if pivot_index == k - 1:
            return num_score[:k]
        elif pivot_index < k - 1:
            left = pivot_index + 1
        else:
            right = pivot_index - 1
    return num_score[:k]


#search function to detect if detected number matches the database or not...
def search(detected, from_database):
    """
    The function "search" checks if there are any common elements between two sets.
    
    :param detected: A list of values that have been detected
    :param from_database: A list of numbers from a database
    :return: a boolean value. If there is at least one common element between the "detected" list and
    the "from_database" list, it will return True. Otherwise, it will return False.
    """
    hashset1 = set()
    hashset2 = set()

    for values in detected:
        hashset1.add(values[0])

    for num in from_database:
        hashset2.add(num)

    hashset3 = hashset1.intersection(hashset2)

    if len(hashset3)==0:
        return False
    else:
        return True


def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """
    if (len(text)==13):
        text=text[3::]
        
    if len(text) != 10:
        return False

    if (text[0].isalpha() and text[1].isalpha() and text[2].isdigit() and text[3].isdigit() and text[4].isalpha() and text[5].isalpha() and text[6].isdigit() and text[7].isdigit() and text[8].isdigit() and text[9].isdigit()):
        return True
    else:
        return False


def read_license_plate(license_plate_crop):
    """
    Read the license plate text from the given cropped image.

    Args:
        license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

    Returns:
        tuple: Tuple containing the formatted license plate text and its confidence score.
    """

    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '')
        text = text.upper().replace('-', '')

        if license_complies_format(text):
            return text, score

    return None, None