import string
import easyocr
import random
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['test_database']
collection = db['data_lists']

# Insert the lists into the collection
'''
!code to save the data of verified number plates

!!! NOTE :: key for number plates in database should be 'num_plates' only!!!
if not then change the key name for verified_num_plates from all_data

'''

# Code to access all lists
all_data = collection.find_one()

# accessing verified number plates
verified_num_plates = all_data['num_plates']


#Function to find top k number according to score
def top_k_scores(num_score, k):
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

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                print(results[frame_nmr][car_id])
                if 'car' in results[frame_nmr][car_id].keys() and \
                   'license_plate' in results[frame_nmr][car_id].keys() and \
                   'text' in results[frame_nmr][car_id]['license_plate'].keys():
                    f.write('{},{},{},{},{},{},{}\n'.format(frame_nmr,
                                                            car_id,
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['car']['bbox'][0],
                                                                results[frame_nmr][car_id]['car']['bbox'][1],
                                                                results[frame_nmr][car_id]['car']['bbox'][2],
                                                                results[frame_nmr][car_id]['car']['bbox'][3]),
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][0],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][1],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][2],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][3]),
                                                            results[frame_nmr][car_id]['license_plate']['bbox_score'],
                                                            results[frame_nmr][car_id]['license_plate']['text'],
                                                            results[frame_nmr][car_id]['license_plate']['text_score'])
                            )
        f.close()


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