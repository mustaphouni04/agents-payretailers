import json
import numpy as np
from api_tools import get_embedding

def main():
	with open("cepalstat_data.json", "r") as file:
		data = json.load(file)
	subjects = data["body"]["children"]

	subjects_children = [subject["children"] for subject in subjects]
	subjects_children_flatten = [item for sublist in subjects_children for item in sublist]

	subjects_children_children = [subjects_child["children"] for subjects_child in subjects_children_flatten]
	subjects_children_children_flatten = [item for sublist in subjects_children_children for item in sublist]

	subjects_children_children_children = [subjects_children_child["children"] for subjects_children_child in subjects_children_children_flatten]
	subjects_children_children_children_flatten = [item for sublist in subjects_children_children_children for item in sublist]
	subjects_children_children_children_flatten = [subjects_children_children_children_flatten[i] for i in range(len(subjects_children_children_children_flatten)) if "indicator_id" in subjects_children_children_children_flatten[i]]
	subjects_children_children_children_names = [subjects_children_children_child["name"] for subjects_children_children_child in subjects_children_children_children_flatten]
	subjects_children_children_children_ids = [subjects_children_children_child["indicator_id"] for subjects_children_children_child in subjects_children_children_children_flatten]

	# make embeddings of subjects_children_children_children_names (list of strings)
	embeddings = get_embedding(subjects_children_children_children_names)
	# convert embeddings to numpy array
	embeddings = np.array([np.array(embedding) for embedding in embeddings])

	# save embeddings to file
	np.save("cepalstat_stats.npy", embeddings)
	# save ids and names to file
	with open("cepalstat_names.json", "w") as file:
		json.dump({"ids": subjects_children_children_children_ids, "names": subjects_children_children_children_names}, file)


if __name__ == "__main__":
	main()
