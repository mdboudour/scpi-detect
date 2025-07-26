from datetime import date
import os

class Person:
    def __init__(self, full_name, role):
        self.full_name = full_name
        self.role = role

    def __str__(self):
        return f"{self.full_name} - {self.role}"

    def serialize(self):
        return f"{self.full_name}|{self.role}"

    @staticmethod
    def deserialize(data):
        full_name, role = data.strip().split('|')
        return Person(full_name, role)


class Personnes:
    def __init__(self):
        self.person_list = []

    def add_person(self, person):
        self.person_list.append(person)

    def __str__(self):
        return "\n".join(str(p) for p in self.person_list)

    def serialize(self):
        return "\n".join([p.serialize() for p in self.person_list])

    @staticmethod
    def deserialize(lines):
        personnes = Personnes()
        for line in lines:
            if line.strip():
                personnes.add_person(Person.deserialize(line))
        return personnes


class Instrument:
    def __init__(self, name, alias, address):
        self.name = name
        self.alias = alias
        self.address = address

    def __str__(self):
        return f"{self.alias}: {self.name} @ {self.address}"

    def serialize(self):
        return f"{self.name}|{self.alias}|{self.address}"

    @staticmethod
    def deserialize(data):
        name, alias, address = data.strip().split('|')
        return Instrument(name, alias, address)


class Instruments:
    def __init__(self):
        self.instrument_list = []

    def add_instrument(self, instrument):
        self.instrument_list.append(instrument)

    def __str__(self):
        return "\n".join(str(i) for i in self.instrument_list)

    def serialize(self):
        return "\n".join([i.serialize() for i in self.instrument_list])

    @staticmethod
    def deserialize(lines):
        instruments = Instruments()
        for line in lines:
            if line.strip():
                instruments.add_instrument(Instrument.deserialize(line))
        return instruments


class Rack:
    def __init__(self, rack_id, construction_date, personnes, instruments):
        self.rack_id = rack_id
        self.construction_date = construction_date
        self.personnes = personnes
        self.instruments = instruments

    def __str__(self):
        return (f"Rack ID: {self.rack_id}\n"
                f"Construction Date: {self.construction_date}\n\n"
                f"Personnes:\n{self.personnes}\n\n"
                f"Instruments:\n{self.instruments}")

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(f"{self.rack_id}\n")
            f.write(f"{self.construction_date}\n")
            f.write("==PERSONS==\n")
            f.write(self.personnes.serialize() + "\n")
            f.write("==INSTRUMENTS==\n")
            f.write(self.instruments.serialize() + "\n")

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        rack_id = lines[0].strip()
        construction_date = lines[1].strip()

        index_persons = lines.index("==PERSONS==\n")
        index_instruments = lines.index("==INSTRUMENTS==\n")

        person_lines = lines[index_persons + 1:index_instruments]
        instrument_lines = lines[index_instruments + 1:]

        personnes = Personnes.deserialize(person_lines)
        instruments = Instruments.deserialize(instrument_lines)

        return Rack(rack_id, construction_date, personnes, instruments)

# ------------------------------------------
# INTERACTIVE MAIN
# ------------------------------------------

def ask_personnes():
    personnes = Personnes()
    while True:
        full_name = input("Full name of person: ")
        role = input("Role of person: ")
        personnes.add_person(Person(full_name, role))
        again = input("Add another person? (Y/N): ").strip().upper()
        if again != 'Y':
            break
    return personnes

def ask_instruments():
    instruments = Instruments()
    while True:
        name = input("Instrument name: ")
        alias = input("Alias: ")
        address = input("Address: ")
        instruments.add_instrument(Instrument(name, alias, address))
        again = input("Add another instrument? (Y/N): ").strip().upper()
        if again != 'Y':
            break
    return instruments

if __name__ == "__main__":
    print(">> ENTER PERSONS")
    personnes = ask_personnes()

    print("\n>> ENTER INSTRUMENTS")
    instruments = ask_instruments()

    print("\n>> RACK INFO")
    rack_id = input("Rack ID: ")
    construction_date = input("Construction date (YYYY-MM-DD) [Enter to use today]: ")
    if construction_date.strip() == "":
        construction_date = date.today().isoformat()

    rack = Rack(rack_id, construction_date, personnes, instruments)

    print("\nSaving to 'rack.txt'...")
    rack.save_to_file("rack.txt")

    print("\nLoading from 'rack.txt' and displaying:")
    loaded_rack = Rack.load_from_file("rack.txt")
    print("\n--- RACK LOADED ---")
    print(loaded_rack)
