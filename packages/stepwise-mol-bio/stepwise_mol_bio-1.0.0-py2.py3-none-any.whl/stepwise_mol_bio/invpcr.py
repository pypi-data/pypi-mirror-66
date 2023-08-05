#!/usr/bin/env python3

"""\
Clone a plasmid by inverse PCR.
"""

import docopt
import autoprop
from stepwise_mol_bio import Main, pcr, kld

@autoprop
class InversePcr(Main):

    def __init__(self):
        self.pcr = pcr.Pcr()
        self.kld = kld.Kld()

    @classmethod
    def from_docopt(cls, args):
        inv = cls()
        inv.pcr = pcr.Pcr.from_docopt(args)
        return inv

    def get_protocol(self):
        self.kld.num_reactions = self.pcr.num_reactions
        return self.pcr.protocol + self.kld.protocol

def copy_pcr_usage():
    i = pcr.__doc__.find('Usage:')
    return __doc__ + pcr.__doc__[i:].replace('pcr', 'invpcr', 1)

if __name__ == '__main__':
    usage = copy_pcr_usage()
    InversePcr.main(usage)




