import os, sys, shutil
import xml.etree.ElementTree as ET

# TODO: iterate through images and corresponding .xml files
# TODO: check that there is a corresponding image - decide what to do when check fails
# TODO: check integrity of the annotation matrix
# TODO: need to check for corresponding .png/.jpg file

'''
Annotation format:
<x> <y> <width> <height>
'''
### Run-time testing
'''
print(get_coords(tree))
print(get_width_height(x_min, x_max, y_min, y_max))
print(get_centre_coords(x_min, x_max, y_min, y_max))
print(get_class(tree))
'''

# Knowledge base
def find_class(name):
    if(name == 'alex'): return 0
    elif (name == 'alexandra'): return 1
    elif (name == 'annett'): return 2
    elif (name == 'bangolo'): return 3
    elif (name == 'corrie'): return 4
    elif (name == 'dorien'): return 5
    elif (name == 'fifi'): return 6
    elif (name == 'fraukje'): return 7
    elif (name == 'frodo'): return 8
    elif (name == 'gertrudia'): return 9
    elif (name == 'jahaga'): return 10
    elif (name == 'kofi'): return 11
    elif (name == 'lobo'): return 12
    elif (name == 'lome'): return 13
    elif (name == 'natascha'): return 14
    elif (name == 'patrick'): return 15
    elif (name == 'pia'): return 16
    elif (name == 'riet'): return 17
    elif (name == 'robert'): return 18
    elif (name == 'sandra'): return 19
    elif (name == 'kara'): return 20
    elif (name == 'swela'): return 21
    elif (name == 'tai'): return 22
    elif (name == 'ulla'): return 23
    else: print('Error: the class "' + name + '" does not exist')

def get_name(tree, user_id):

    root = tree.getroot()
    for label in root.iter('label'):
        if(label.get('uid') == str(user_id)):
            name = label.get('name').lower()
    return name

def get_class(tree, user_id):

    name = get_name(tree, user_id)
    ape_class = find_class(name)
    return ape_class

def count_apes(tree):

    apes = 0
    root = tree.getroot()

    for label in root.iter('label'):
        apes += 1
    return apes

def generate_matrix(label_number):
    dimensions = 4
    data_points = label_number
    M = [[0 for x in range(dimensions)] for y in range(data_points)]
    return M

def get_coords(tree):

    x_min, x_max = 0, 2
    y_min, y_max = 1, 3

    label_number = 0
    ape_number = count_apes(tree)
    label_matrix = generate_matrix(ape_number)

    root = tree.getroot()

    for point in root.iter('point'):
        if(point.get('orderIdx') is "0"):
            label_matrix[label_number][x_min] = point.get('posX')
            label_matrix[label_number][y_min] = point.get('posY')
        if(point.get('orderIdx') is "2"):
            label_matrix[label_number][x_max] = point.get('posX')
            label_matrix[label_number][y_max] = point.get('posY')

            '''
            label_matrix[label_number].insert(0, get_class(tree, label_number))
            '''
            # increase label once we have all 4 coords

            if(ape_number > 1):
                label_number += 1

    return label_matrix

def get_annotation(label_matrix, tree):

    for i in range(len(label_matrix)):
        x_min, y_min, x_max, y_max = label_matrix[i]

        x_min = float(x_min)
        x_max = float(x_max)
        y_min = float(y_min)
        y_max = float(y_max)

        # calculate centre coords
        x_c = 0.5 * (x_max + x_min)

        y_c = 0.5 * (y_max + y_min)

        # calculate width, height
        w = x_max - x_min
        h = y_max - y_min

        label_matrix[i][0] = round(x_c, 6)
        label_matrix[i][1] = round(y_c, 6)
        label_matrix[i][2] = round(w, 6)
        label_matrix[i][3] = round(h, 6)

        label_matrix[i].insert(0, get_class(tree, i))

    return label_matrix

def generate_annotation(tree):
    coord_matrix = get_coords(tree)
    annotation_matrix = get_annotation(coord_matrix, tree)
    return annotation_matrix


def get_centre_coords(x_min, x_max, y_min, y_max):

    x_min = float(x_min)
    x_max = float(x_max)
    y_min = float(y_min)
    y_max = float(y_max)

    x_centre = 0.5 * (x_max + x_min)
    y_centre = 0.5 * (y_max + y_min)
    return x_centre, y_centre

def generate_multiclass_label(annotation_matrix, file):
    for j in range(len(annotation_matrix)):
        annotation_str = ' '.join([str(elem) for elem in annotation_matrix[j]])
        file.write("{}\n".format(annotation_str))

def generate_uniclass_label(annotation_matrix, file):
    datapoint = 0
    annotation_str = ' '.join([str(elem) for elem in annotation_matrix[datapoint]])
    file.write(annotation_str)

'''
def check_datapoint(annotation_matrix):
    for i in range(len(annotation_matrix)):
        for j in range(len(annotation_matrix[i])):
            if(annotation_matrix[i][0] not in range(0, 23)):
                return False
'''

# TODO: move copy image and .txt annotation into class-based directory structure

# not really working... not in use either

def make_directory(tree):

    user_id = 0
    dir_name = get_name(tree, user_id)
    if not(os.path.exists(dir_name)):
        os.mkdir(dir_name)

def label_data():

    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir('.') if isfile(f)]

    for i in range(len(onlyfiles)):
        if(onlyfiles[i].lower().endswith('.xml')):

            # make an empty .txt file with same name as .xml file

            file = onlyfiles[i].split('.')[0] + '.txt'
            file = open(file, "w+")

            tree = ET.parse(onlyfiles[i])
            annotation_matrix = generate_annotation(tree)

            datapoint_count = len(annotation_matrix)

            if(datapoint_count > 1):
                generate_multiclass_label(annotation_matrix, file)
            elif(datapoint_count is 1):
                generate_uniclass_label(annotation_matrix, file)

            make_directory(tree)

def validate_xml_txt():

    from os import listdir
    from os.path import isfile, join

    onlyfiles = [f for f in listdir('.') if isfile(f)]

    xml_count = 0
    txt_count = 0

    for i in range(len(onlyfiles)):
        if(onlyfiles[i].lower().endswith('.xml')):
            xml_count += 1
        elif(onlyfiles[i].lower().endswith('.txt')):
            txt_count += 1

    print(".xml file count: " + str(xml_count))
    print(".txt file count: " + str(txt_count))

    if(xml_count == txt_count):
        return True
    return False


# Main
def main():
    label_data()
    if not(validate_xml_txt()):
        print("Error: Labels & XML do not match")

if __name__ == "__main__":
    main()
