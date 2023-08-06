from cocktail_shaker import PeptideBuilder
from cocktail_shaker import Cocktail
from cocktail_shaker import FileWriter
import pandas as pd

if __name__ == '__main__':


    natural_amino_acids = ["C", "CCCNC(N)=N", "CCC(N)=O", "CC(O)=O", "CS", "CCC(O)=O", "CCC(O)=O", "CCC(N)=O", "[H]",
                           "CC1=CNC=N1", "C(CC)([H])C", "CC(C)C", "CCCCN", "CCSC", "CC1=CC=CC=C1", "CO", "C(C)([H])O",
                           "CCC1=CNC2=C1C=CC=C2", "CC1=CC=C(O)C=C1", "C(C)C"]
    number = 1


    root_dataframe = pd.DataFrame(columns=["smiles", "amino_acid"])

    peptide_molecule = PeptideBuilder(length_of_peptide=1)
    cocktail = Cocktail(peptide_backbone=peptide_molecule,
                        ligand_library=[natural_amino_acids[0]],
                        enable_isomers=False)
    molecules = cocktail.shake()
    FileWriter('new_compounds', molecules, 'sdf')
    molecules = cocktail.enumerate(dimensionality='1D', enumeration_complexity='high')

    dataframe = pd.DataFrame(molecules, columns=["smiles"])



