import json

def get():
    with open('test.json', 'r') as json_file:
        data = json.load(json_file)
    return data

def find_delta(delta_ori, delta_vans):
    # Combine the two lists and get unique values as potential thresholds
    combined = sorted(set(delta_ori + delta_vans))

    best_threshold = None
    best_score = -1

    for threshold in combined:
        # Calculate the score for the current threshold
        delta_ori_over = sum(1 for x in delta_ori if x > threshold)
        delta_vans_below = sum(1 for x in delta_vans if x < threshold)

        score = delta_ori_over + delta_vans_below  # The goal is to maximize this score

        # Update the best score and threshold if this one is better
        if score > best_score:
            best_score = score
            best_threshold = threshold

    grade = best_score / (len(delta_ori)+len(delta_vans))

    return best_threshold, best_score, grade

def find_ratio(ratio_ori, ratio_vans):
    # Combine the two lists and get unique values as potential thresholds
    combined = sorted(set(ratio_ori + ratio_vans))

    best_threshold = None
    best_score = -1

    for threshold in combined:
        # Calculate the score for the current threshold
        ratio_ori_over = sum(1 for x in ratio_ori if x > threshold)
        ratio_vans_below = sum(1 for x in ratio_vans if x < threshold)

        score = ratio_ori_over + ratio_vans_below  # The goal is to maximize this score

        # Update the best score and threshold if this one is better
        if score > best_score:
            best_score = score
            best_threshold = threshold

    grade = best_score / (len(ratio_ori)+len(ratio_vans))

    return best_threshold, best_score, grade

# ! Value
length = 124
def prep():
    with open('test.json', 'r') as json_file:
        data = json.load(json_file)
    lcars = len(data["cars_confs_yolo"])
    l_trucks = len(data["trucks_confs_yolo"])
    l_vans = len(data["vans_confs_yolo"])
    data["cars_confs_deltas"] = [data["cars_confs_yolo"][i] - data["cars_confs_vans"][i] for i in range(lcars)]
    data["trucks_confs_deltas"] = [data["trucks_confs_yolo"][i] - data["trucks_confs_vans"][i] for i in range(l_trucks)]
    data["vans_confs_deltas"] = [data["vans_confs_yolo"][i] - data["vans_confs_vans"][i] for i in range(l_vans)]

    data["cars_confs_ratio"] = [data["cars_confs_yolo"][i] / data["cars_confs_vans"][i] if data["cars_confs_vans"][i]>0 else 10e9 for i in range(lcars)]
    data["trucks_confs_ratio"] = [data["trucks_confs_yolo"][i] / data["trucks_confs_vans"][i] if data["trucks_confs_vans"][i]>0 else 10e9 for i in range(l_trucks)]
    data["vans_confs_ratio"] = [data["vans_confs_yolo"][i] / data["vans_confs_vans"][i] if data["vans_confs_vans"][i]>0 else 10e9 for i in range(l_vans)]
    with open('test.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

prep()
data = get()

threshold, score, grade = find_delta(data["cars_confs_deltas"], data["vans_confs_deltas"])
print(f"Best threshold delta cars vs vans : {threshold}, Best score: {score}, Grade: {100*grade:.2f}%")
threshold, score, grade = find_ratio(data["cars_confs_ratio"], data["vans_confs_ratio"])
print(f"Best threshold ratio cars vs vans : {threshold}, Best score: {score}, Grade: {100*grade:.2f}%")
threshold, score, grade = find_delta(data["trucks_confs_deltas"], data["vans_confs_deltas"])
print(f"Best threshold delta trucks vs vans : {threshold}, Best score: {score}, Grade: {100*grade:.2f}%")
threshold, score, grade = find_ratio(data["trucks_confs_ratio"], data["vans_confs_ratio"])
print(f"Best threshold ratio trucks vs vans : {threshold}, Best score: {score}, Grade: {100*grade:.2f}%")
