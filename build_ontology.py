from utils import KnowledgeGraph, human_name, name_to_snake_case
from ontologies import PATH as PATH_ONTOLOGY
from results import PATH as PATH_RESULTS
import json
import os


PATH_RESULTS = PATH_RESULTS / "nutrition" / "100tuples_top20prompts" / "roberta-large"
PATH_BASE_ONTOLOGY = PATH_ONTOLOGY / "base_ontology.owl"
PATH_POPULATED_ONTOLOGY = PATH_ONTOLOGY / "populated_ontology.owl"
THRESHOLD = 10E-3


if __name__ == "__main__":
    processed_classes = set()
    os.system("cp {} {}".format(str(PATH_BASE_ONTOLOGY), str(PATH_POPULATED_ONTOLOGY)))
    with KnowledgeGraph(PATH_POPULATED_ONTOLOGY) as kg:
        Recipe = kg.onto.Recipe
        for cls in kg.visit_classes_depth_first():
            if human_name(cls) in processed_classes:
                continue
            processed_classes.add(human_name(cls))
            # Read the results file for the specific class
            results_file = PATH_RESULTS / "is_instance_of_{}".format(name_to_snake_case(human_name(cls))) / "ent_tuples.json"
            # Iterate over the results file
            with open(results_file, "r") as f:
                results = json.load(f)
            # Add each entity to the class
            processed_entities = set()
            for entity in results:
                for ent in entity:
                    if isinstance(ent, float):
                        continue
                    if ent[0] not in processed_entities:
                        if entity[1] > THRESHOLD:
                            kg.add_instance(cls, ent[0])
                            processed_entities.add(ent[0])
        # Save the populated ontology
        kg.save()
