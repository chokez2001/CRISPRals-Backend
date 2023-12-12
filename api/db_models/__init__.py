from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class RalstoniaTbl(db.Model):
    strain = db.Column(db.String, nullable=False)
    phylotype = db.Column(db.String)
    specie = db.Column(db.String, nullable=False)
    assembly = db.Column(db.String, primary_key=True, nullable=False)
    level = db.Column(db.String, nullable=False)
    accession_number_rf = db.Column(db.String)
    accession_number_genbank = db.Column(db.String)
    wgs = db.Column(db.String)
    scaffolds = db.Column(db.Integer)
    crispr_array = db.Column(db.Boolean, nullable=True)
    number_of_crispr_arrays = db.Column(db.Integer)
    consensus = db.Column(db.String)
    type_of_crispr = db.Column(db.String)
    observation = db.Column(db.String)
    score_crispr_identify = db.Column(db.Double, nullable=True)

    def to_dict(self):
        return {
            "strain": self.strain,
            "phylotype": self.phylotype,
            "specie": self.specie,
            "assembly": self.assembly,
            "level": self.level,
            "accession_number_rf": self.accession_number_rf,
            "accession_number_genbank": self.accession_number_genbank,
            "wgs": self.wgs,
            "scaffolds": self.scaffolds,
            "crispr_array": self.crispr_array,
            "number_of_crispr_arrays": self.number_of_crispr_arrays,
            "consensus": self.consensus,
            "type_of_crispr": self.type_of_crispr,
            "observation" : self.observation,
            "score_crispr_identify": self.score_crispr_identify,
        }


class PhagesTbl(db.Model):
    id_phage = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phage_name = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id_phage": self.id_phage,
            "phage_name": self.phage_name,
        }


class CrisprTbl(db.Model):
    id_crispr = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assembly_fk = db.Column(db.String, db.ForeignKey(RalstoniaTbl.assembly), nullable=False)
    id_phage_fk = db.Column(db.Integer, db.ForeignKey(PhagesTbl.id_phage), nullable=False)
    position_phage_genome = db.Column(db.String, nullable=False)
    locus = db.Column(db.String)
    cluster_spacer = db.Column(db.String)
    position_bacterial_genome = db.Column(db.String)
    spacer_rna = db.Column(db.String, nullable=False)
    protospacer_sequence = db.Column(db.String)
    score = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id_crispr": self.id_crispr,
            "assembly_fk": self.assembly_fk,
            "id_phage_fk": self.id_phage_fk,
            "position_phage_genome": self.position_phage_genome,
            "locus": self.locus,
            "cluster_spacer": self.cluster_spacer,
            "position_bacterial_genome": self.position_bacterial_genome,
            "spacer_rna": self.spacer_rna,
            "protospacer_sequence": self.protospacer_sequence,
            "score": self.score
        }
