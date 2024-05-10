import os
import shutil
import random

def split_data(directory):
    gt_file = os.path.join(directory, "gt.txt")
    if not os.path.exists(gt_file):
        print(f"No 'gt.txt' found in {directory}")
        return

    with open(gt_file, "r") as f:
        lines = f.readlines()
    
    random.shuffle(lines)
    
    num_samples = len(lines)
    train_size = int(0.75 * num_samples)
    
    train_data = lines[:train_size]
    val_data = lines[train_size:]
    
    with open(os.path.join(directory, "train.txt"), "w") as f:
        f.writelines(train_data)
    
    with open(os.path.join(directory, "val.txt"), "w") as f:
        f.writelines(val_data)


def main(root_directory):
    for subdir in os.listdir(root_directory):
        split_data(os.path.join(root_directory, subdir))

def move_files(root_directory):
    train_entries = []
    val_entries = []
    for subdir in os.listdir(root_directory):
        train_file = os.path.join(root_directory, subdir, "train.txt")
        val_file = os.path.join(root_directory, subdir, "val.txt")
        if os.path.exists(train_file) and os.path.exists(val_file):
            tf_obj = open(train_file, "r")
            vf_obj = open(val_file, "r")
            for line in tf_obj.readlines():
                train_entries.append(line)
            for line in vf_obj.readlines():
                val_entries.append(line)
            tf_obj.close()
            vf_obj.close()
        else:
            print(f"Either {train_file} or {val_file} doesn't exist!")            
    
    random.shuffle(train_entries)
    random.shuffle(val_entries)

    with open(os.path.join(root_directory, "train.txt"), "w") as f:
        for ent in train_entries:
            # print(ent)
            f.write(ent)
    with open(os.path.join(root_directory, "val.txt"), "w") as f:
        for ent in val_entries:
            f.writelines(ent)


root_directory = "./extracted_frames"
main(root_directory)
move_files(root_directory)
