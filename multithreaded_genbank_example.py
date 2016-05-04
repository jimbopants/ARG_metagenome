from Bio import SeqIO
from Bio import Entrez
from multiprocessing.dummy import Pool

Entrez.email = "gao.han.lisa@gmail.com"

# Generate a large list of acccession numbers (or use your own):
handle = Entrez.esearch(db="protein", term ="Amidase[Protein] AND bacteria[Organism]", retmax=100000)
record = Entrez.read(handle)
handle.close()
recordList=record["IdList"]

# Example function that takes a record and returns some components of the genbank accessions
def get_record(record):
    try:
        handle = Entrez.efetch(db="protein",id=record, retmode="xml")
        record = Entrez.read(handle)
        organism = record[0]["GBSeq_source"]
        taxon =  record[0]["GBSeq_taxonomy"]
    except:
        return record,'error'
    return organism, taxon


# For counting iterations
z=0
total = len(recordList)

# Pool(n) will return n separate threads.
pool = Pool(20) # at most 20 concurrent downloads

# Open a file for writing:
with open("/Users/jimbo/Desktop/example.txt", "wb") as f:
    # Call imap_unordered on the pool of processors you opened, and pass a function(x) and a list of x's
    for org,tax in pool.imap_unordered(get_record, recordList):
        # Write output line by line as results come in from pool.
        f.write(org+"\t"+tax+"\n")
        
        # Interactive output to check status
        if z%1000==0:
            print '{0} down, {1} to go'.format(z, total-z) 
