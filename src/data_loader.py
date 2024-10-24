import csv
from typing import List, Type, Union
from models import Territory, AgeGender
from constants import *

def read_csv(
        path: str, 
        entity_class: Type[Union[Territory, AgeGender]]
    ) -> List[Union[Territory, AgeGender]]:

    """
    Reads a CSV file and creates a list of objects of the specified class: 
    either Territory or AgeGender.

    Args:
        path (str): File path.
        entity_class (Type[Union[Territory, AgeGender]]): Type selector.

    Returns:
        List[Union[Territory, AgeGender]]: List with either Territory or AgeGender objects.
    """

    # Initialize an appropriate collection: dict for Territory, list for AgeGender
    entities = {} if entity_class is Territory else []

    # Open the CSV file with the specified encoding
    with open(path, newline='', encoding=ENCODING) as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Determine the attributes based on the class type
            if entity_class is Territory:
                name = row.get('TERRITORIO#es')
                purpose = row['TASA_TURISTICA_FINALIDAD_CODE']
                value = row['OBS_VALUE']

                # Get existing Territory or create a new one
                entity = entities.get(name) or Territory(name)
                entities[name] = entity

            elif entity_class is AgeGender:
                name = AgeStruct.AGE_GROUPS[row.get('EDAD_CODE')]
                gender = GenderStruct.GENDERS[row.get('SEXO_CODE')]
                purpose = row['TASA_TURISTICA_FINALIDAD_CODE']
                value = row['OBS_VALUE']

                # Find existing AgeGender or create a new one if not found
                entity = next((e for e in entities if e.age == name and e.gender == gender), None)
                if not entity:
                    entity = AgeGender(name, gender)
                    entities.append(entity)

            # Convert the value to int or float and update the entity's purpose
            try:
                value_int = int(value)
                entity.update_purpose(purpose=purpose, population=value_int)
            except ValueError:
                entity.update_purpose(purpose=purpose, percentage=float(value))

    # Return the appropriate collection: list of values if Territory, or the list itself if AgeGender
    return list(entities.values()) if entity_class is Territory else entities
