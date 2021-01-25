#!/usr/bin/env python

import argparse

from sqlalchemy.orm import joinedload
from tabulate import tabulate

import muninn.models as models
import muninn.log as log
import muninn.config as config

logger = log.get_logger("pets")


def create_genus(conf: config.Config, args):
    session = conf.database.Session()

    genus = models.Genus(name=args.name)

    session.add(genus)
    session.commit()
    return


def create_species(conf: config.Config, args):
    session = conf.database.Session()

    genus = session.query(models.Genus).filter(models.Genus.name == args.genus).one()

    species = models.Species(name=args.name, genus_id=genus.id)
    session.add(species)
    session.commit()
    return


def create_enclosure(conf: config.Config, args):
    session = conf.database.Session()

    enclosure = models.Enclosure(name=args.name)
    session.add(enclosure)
    session.commit()

    logger.info("successfully created enclosure", name=args.name)


def create_creature(conf: config.Config, args):
    session = conf.database.Session()

    genus = session.query(models.Genus).filter(models.Genus.name == args.genus).one()
    species = (
        session.query(models.Species).filter(models.Species.name == args.species).one()
    )

    if species.genus_id != genus.id:
        raise Exception("genus IDs do not match")

    creature = models.Creature(name=args.name, species_id=species.id)
    session.add(creature)
    session.commit()


def list_genuses(conf: config.Config, args):
    session = conf.database.Session()

    genuses = session.query(models.Genus).all()

    for genus in genuses:
        print("%d %s" % (genus.id, genus.name))

    session.close()

    return


def list_creatures(conf: config.Config, args):
    session = conf.database.Session()

    creatures = (
        session.query(models.Creature)
        .options(joinedload("species"), joinedload("species.genus"))
        .all()
    )

    table_data = [
        [x.id, x.name, x.species.genus.name, x.species.name] for x in creatures
    ]

    print(
        tabulate(
            table_data,
            headers=["ID", "Name", "Genus", "Species"],
            tablefmt="github",
        )
    )

    session.close()


def list_species(conf: config.Config, args):
    session = conf.database.Session()

    species = session.query(models.Species).options(joinedload("genus")).all()

    session.close()

    for s in species:
        print("%d %s %s" % (s.id, s.genus.name, s.name))


def build_command():
    parser = argparse.ArgumentParser(description="Manage pet records")

    subparsers = parser.add_subparsers()
    create_parser = subparsers.add_parser("create", help="Create a resource")

    create_subparser = create_parser.add_subparsers()

    create_genus_parser = create_subparser.add_parser(
        "genus",
        help="Create a Genus.",
    )
    create_genus_parser.add_argument("name", help="The name of the genus.")
    create_genus_parser.set_defaults(func=create_genus)

    create_species_parser = create_subparser.add_parser(
        "species", help="Create a Species."
    )
    create_species_parser.add_argument("genus", help="The name of the genus.")
    create_species_parser.add_argument("name", help="The name of the species.")
    create_species_parser.set_defaults(func=create_species)

    create_creature_parser = create_subparser.add_parser("creature")
    create_creature_parser.add_argument("name")
    create_creature_parser.add_argument("genus")
    create_creature_parser.add_argument("species")
    create_creature_parser.set_defaults(func=create_creature)

    create_enclosure_parser = create_subparser.add_parser("enclosure")
    create_enclosure_parser.add_argument("name")
    create_enclosure_parser.set_defaults(func=create_enclosure)

    list_parser = subparsers.add_parser("list", help="List resources")
    list_subparser = list_parser.add_subparsers()

    list_genus_parser = list_subparser.add_parser(
        "genus",
        help="List genuses.",
    )
    list_genus_parser.set_defaults(func=list_genuses)

    list_species_parser = list_subparser.add_parser(
        "species",
        help="List species.",
    )
    list_species_parser.set_defaults(func=list_species)

    list_creatures_parser = list_subparser.add_parser(
        "creatures",
        help="List species.",
    )
    list_creatures_parser.set_defaults(func=list_creatures)

    return parser


def main():
    parser = build_command()

    args = parser.parse_args()

    conf = config.load_default()
    conf.database.connect()
    args.func(conf, args)
    return


if __name__ == "__main__":
    main()