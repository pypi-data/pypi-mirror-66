#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 17:31:05 2020

@author: juan
"""

import unittest
from unittest.mock import patch
from unittest.mock import mock_open

from cctop.gff2bedFiles import readGFF

"""
GFF v3 specification at
https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md
"""
class TestGff2bedFiles(unittest.TestCase):
    
    def setUp(self):
        self.gffEnsembl = """##gff-version 3
##sequence-region V 1 20924180

V	Ensembl	gene	19174806	19187899	.	+	.	ID=WBGene00001987.1;Name=WBGene00001987.1;biotype=protein_coding
V	Ensembl	gene	19189246	19190035	.	-	.	ID=WBGene00012666.1;Name=WBGene00012666.1;biotype=protein_coding
V	Ensembl	transcript	19174806	19187899	.	+	.	ID=Y39B6A.48a.1;Name=Y39B6A.48a.1;Parent=WBGene00001987.1;biotype=protein_coding
V	Ensembl	transcript	19185155	19187899	.	+	.	ID=Y39B6A.48b.1;Name=Y39B6A.48b.1;Parent=WBGene00001987.1;biotype=protein_coding
V	Ensembl	transcript	19189246	19190035	.	-	.	ID=Y39B6A.3a.1;Name=Y39B6A.3a.1;Parent=WBGene00012666.1;biotype=protein_coding
V	Ensembl	transcript	19189246	19190001	.	-	.	ID=Y39B6A.3b.1;Name=Y39B6A.3b.1;Parent=WBGene00012666.1;biotype=protein_coding
V	Ensembl	CDS	19174806	19175178	.	+	0	Name=Y39B6A.48a.1;Parent=Y39B6A.48a.1
V	Ensembl	CDS	19185594	19185697	.	+	2	Name=Y39B6A.48a.1;Parent=Y39B6A.48a.1
V	Ensembl	CDS	19186541	19186643	.	+	0	Name=Y39B6A.48a.1;Parent=Y39B6A.48a.1
V	Ensembl	CDS	19186799	19186899	.	+	2	Name=Y39B6A.48a.1;Parent=Y39B6A.48a.1
V	Ensembl	CDS	19187471	19187653	.	+	0	Name=Y39B6A.48a.1;Parent=Y39B6A.48a.1
V	Ensembl	CDS	19185178	19185286	.	+	0	Name=Y39B6A.48b.1;Parent=Y39B6A.48b.1
V	Ensembl	CDS	19185594	19185697	.	+	2	Name=Y39B6A.48b.1;Parent=Y39B6A.48b.1
V	Ensembl	CDS	19186541	19186643	.	+	0	Name=Y39B6A.48b.1;Parent=Y39B6A.48b.1
V	Ensembl	CDS	19186799	19186899	.	+	2	Name=Y39B6A.48b.1;Parent=Y39B6A.48b.1
V	Ensembl	CDS	19187471	19187653	.	+	0	Name=Y39B6A.48b.1;Parent=Y39B6A.48b.1
V	Ensembl	CDS	19189900	19189964	.	-	.	Name=Y39B6A.3a.1;Parent=Y39B6A.3a.1
V	Ensembl	CDS	19189764	19189845	.	-	.	Name=Y39B6A.3a.1;Parent=Y39B6A.3a.1
V	Ensembl	CDS	19189598	19189687	.	-	.	Name=Y39B6A.3a.1;Parent=Y39B6A.3a.1
V	Ensembl	CDS	19189340	19189492	.	-	.	Name=Y39B6A.3a.1;Parent=Y39B6A.3a.1
V	Ensembl	CDS	19189900	19189964	.	-	.	Name=Y39B6A.3b.1;Parent=Y39B6A.3b.1
V	Ensembl	CDS	19189764	19189851	.	-	.	Name=Y39B6A.3b.1;Parent=Y39B6A.3b.1
V	Ensembl	CDS	19189598	19189687	.	-	.	Name=Y39B6A.3b.1;Parent=Y39B6A.3b.1
V	Ensembl	CDS	19189340	19189492	.	-	.	Name=Y39B6A.3b.1;Parent=Y39B6A.3b.1
V	Ensembl	exon	19174806	19175178	.	+	.	Name=Y39B6A.48a.1.e1;Parent=Y39B6A.48a.1
V	Ensembl	exon	19185594	19185697	.	+	.	Name=Y39B6A.48a.1.e2;Parent=Y39B6A.48a.1
V	Ensembl	exon	19186541	19186643	.	+	.	Name=Y39B6A.48a.1.e3;Parent=Y39B6A.48a.1
V	Ensembl	exon	19186799	19186899	.	+	.	Name=Y39B6A.48a.1.e4;Parent=Y39B6A.48a.1
V	Ensembl	exon	19187471	19187899	.	+	.	Name=Y39B6A.48a.1.e5;Parent=Y39B6A.48a.1
V	Ensembl	exon	19185155	19185286	.	+	.	Name=Y39B6A.48b.1.e1;Parent=Y39B6A.48b.1
V	Ensembl	exon	19185594	19185697	.	+	.	Name=Y39B6A.48a.1.e2;Parent=Y39B6A.48b.1
V	Ensembl	exon	19186541	19186643	.	+	.	Name=Y39B6A.48a.1.e3;Parent=Y39B6A.48b.1
V	Ensembl	exon	19186799	19186899	.	+	.	Name=Y39B6A.48a.1.e4;Parent=Y39B6A.48b.1
V	Ensembl	exon	19187471	19187899	.	+	.	Name=Y39B6A.48a.1.e5;Parent=Y39B6A.48b.1
V	Ensembl	exon	19189900	19190035	.	-	.	Name=Y39B6A.3a.1.e1;Parent=Y39B6A.3a.1
V	Ensembl	exon	19189764	19189845	.	-	.	Name=Y39B6A.3a.1.e2;Parent=Y39B6A.3a.1
V	Ensembl	exon	19189598	19189687	.	-	.	Name=Y39B6A.3a.1.e3;Parent=Y39B6A.3a.1
V	Ensembl	exon	19189246	19189492	.	-	.	Name=Y39B6A.3a.1.e4;Parent=Y39B6A.3a.1
V	Ensembl	exon	19189900	19190001	.	-	.	Name=Y39B6A.3b.1.e1;Parent=Y39B6A.3b.1
V	Ensembl	exon	19189764	19189851	.	-	.	Name=Y39B6A.3b.1.e2;Parent=Y39B6A.3b.1
V	Ensembl	exon	19189598	19189687	.	-	.	Name=Y39B6A.3a.1.e3;Parent=Y39B6A.3b.1
V	Ensembl	exon	19189246	19189492	.	-	.	Name=Y39B6A.3a.1.e4;Parent=Y39B6A.3b.1
"""
        self.gffRefSeq = """##gff-version 3
#!gff-spec-version 1.21
#!processor NCBI annotwriter
#!genome-build WBcel235
#!genome-build-accession NCBI_Assembly:GCF_000002985.6
#!annotation-source WormBase WS275
##sequence-region NC_003279.8 1 15072434
##species https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=6239
NC_003283.11	RefSeq	gene	19174759	19187908	.	+	.	ID=gene-CELE_Y39B6A.48;Dbxref=WormBase:WBGene00001987,GeneID:180261;Name=hot-2;gbkey=Gene;gene=hot-2;gene_biotype=protein_coding;locus_tag=CELE_Y39B6A.48
NC_003283.11	RefSeq	mRNA	19174759	19187908	.	+	.	ID=rna-NM_001269917.2;Parent=gene-CELE_Y39B6A.48;Dbxref=GeneID:180261,Genbank:NM_001269917.2,WormBase:WBGene00001987;Name=NM_001269917.2;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48a.1;transcript_id=NM_001269917.2
NC_003283.11	RefSeq	exon	19174759	19175178	.	+	.	ID=exon-NM_001269917.2-1;Parent=rna-NM_001269917.2;Dbxref=GeneID:180261,Genbank:NM_001269917.2,WormBase:WBGene00001987;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48a.1;transcript_id=NM_001269917.2
NC_003283.11	RefSeq	exon	19185594	19185697	.	+	.	ID=exon-NM_001269917.2-2;Parent=rna-NM_001269917.2;Dbxref=GeneID:180261,Genbank:NM_001269917.2,WormBase:WBGene00001987;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48a.1;transcript_id=NM_001269917.2
NC_003283.11	RefSeq	exon	19186541	19186643	.	+	.	ID=exon-NM_001269917.2-3;Parent=rna-NM_001269917.2;Dbxref=GeneID:180261,Genbank:NM_001269917.2,WormBase:WBGene00001987;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48a.1;transcript_id=NM_001269917.2
NC_003283.11	RefSeq	exon	19186799	19186899	.	+	.	ID=exon-NM_001269917.2-4;Parent=rna-NM_001269917.2;Dbxref=GeneID:180261,Genbank:NM_001269917.2,WormBase:WBGene00001987;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48a.1;transcript_id=NM_001269917.2
NC_003283.11	RefSeq	exon	19187471	19187908	.	+	.	ID=exon-NM_001269917.2-5;Parent=rna-NM_001269917.2;Dbxref=GeneID:180261,Genbank:NM_001269917.2,WormBase:WBGene00001987;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48a.1;transcript_id=NM_001269917.2
NC_003283.11	RefSeq	CDS	19174806	19175178	.	+	0	ID=cds-NP_001256846.1;Parent=rna-NM_001269917.2;Dbxref=EnsemblGenomes-Gn:WBGene00001987,EnsemblGenomes-Tr:Y39B6A.48a,GOA:D5SH00,InterPro:IPR010558,UniProtKB/TrEMBL:D5SH00,GeneID:180261,Genbank:NP_001256846.1,WormBase:WBGene00001987;Name=NP_001256846.1;Note=Product from WormBase gene class hot%3B~Confirmed by transcript evidence;gbkey=CDS;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);protein_id=NP_001256846.1;standard_name=Y39B6A.48a
NC_003283.11	RefSeq	CDS	19185594	19185697	.	+	2	ID=cds-NP_001256846.1;Parent=rna-NM_001269917.2;Dbxref=EnsemblGenomes-Gn:WBGene00001987,EnsemblGenomes-Tr:Y39B6A.48a,GOA:D5SH00,InterPro:IPR010558,UniProtKB/TrEMBL:D5SH00,GeneID:180261,Genbank:NP_001256846.1,WormBase:WBGene00001987;Name=NP_001256846.1;Note=Product from WormBase gene class hot%3B~Confirmed by transcript evidence;gbkey=CDS;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);protein_id=NP_001256846.1;standard_name=Y39B6A.48a
NC_003283.11	RefSeq	CDS	19186541	19186643	.	+	0	ID=cds-NP_001256846.1;Parent=rna-NM_001269917.2;Dbxref=EnsemblGenomes-Gn:WBGene00001987,EnsemblGenomes-Tr:Y39B6A.48a,GOA:D5SH00,InterPro:IPR010558,UniProtKB/TrEMBL:D5SH00,GeneID:180261,Genbank:NP_001256846.1,WormBase:WBGene00001987;Name=NP_001256846.1;Note=Product from WormBase gene class hot%3B~Confirmed by transcript evidence;gbkey=CDS;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);protein_id=NP_001256846.1;standard_name=Y39B6A.48a
NC_003283.11	RefSeq	CDS	19186799	19186899	.	+	2	ID=cds-NP_001256846.1;Parent=rna-NM_001269917.2;Dbxref=EnsemblGenomes-Gn:WBGene00001987,EnsemblGenomes-Tr:Y39B6A.48a,GOA:D5SH00,InterPro:IPR010558,UniProtKB/TrEMBL:D5SH00,GeneID:180261,Genbank:NP_001256846.1,WormBase:WBGene00001987;Name=NP_001256846.1;Note=Product from WormBase gene class hot%3B~Confirmed by transcript evidence;gbkey=CDS;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);protein_id=NP_001256846.1;standard_name=Y39B6A.48a
NC_003283.11	RefSeq	CDS	19187471	19187653	.	+	0	ID=cds-NP_001256846.1;Parent=rna-NM_001269917.2;Dbxref=EnsemblGenomes-Gn:WBGene00001987,EnsemblGenomes-Tr:Y39B6A.48a,GOA:D5SH00,InterPro:IPR010558,UniProtKB/TrEMBL:D5SH00,GeneID:180261,Genbank:NP_001256846.1,WormBase:WBGene00001987;Name=NP_001256846.1;Note=Product from WormBase gene class hot%3B~Confirmed by transcript evidence;gbkey=CDS;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);protein_id=NP_001256846.1;standard_name=Y39B6A.48a
NC_003283.11	RefSeq	mRNA	19185173	19187899	.	+	.	ID=rna-NM_001269919.2;Parent=gene-CELE_Y39B6A.48;Dbxref=GeneID:180261,Genbank:NM_001269919.2,WormBase:WBGene00001987;Name=NM_001269919.2;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48b.1;transcript_id=NM_001269919.2
NC_003283.11	RefSeq	exon	19185173	19185286	.	+	.	ID=exon-NM_001269919.2-1;Parent=rna-NM_001269919.2;Dbxref=GeneID:180261,Genbank:NM_001269919.2,WormBase:WBGene00001987;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48b.1;transcript_id=NM_001269919.2
NC_003283.11	RefSeq	exon	19185594	19185697	.	+	.	ID=exon-NM_001269919.2-2;Parent=rna-NM_001269919.2;Dbxref=GeneID:180261,Genbank:NM_001269919.2,WormBase:WBGene00001987;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48b.1;transcript_id=NM_001269919.2
NC_003283.11	RefSeq	exon	19186541	19186643	.	+	.	ID=exon-NM_001269919.2-3;Parent=rna-NM_001269919.2;Dbxref=GeneID:180261,Genbank:NM_001269919.2,WormBase:WBGene00001987;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48b.1;transcript_id=NM_001269919.2
NC_003283.11	RefSeq	exon	19186799	19186899	.	+	.	ID=exon-NM_001269919.2-4;Parent=rna-NM_001269919.2;Dbxref=GeneID:180261,Genbank:NM_001269919.2,WormBase:WBGene00001987;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48b.1;transcript_id=NM_001269919.2
NC_003283.11	RefSeq	exon	19187471	19187899	.	+	.	ID=exon-NM_001269919.2-5;Parent=rna-NM_001269919.2;Dbxref=GeneID:180261,Genbank:NM_001269919.2,WormBase:WBGene00001987;Note=Product from WormBase gene class hot;gbkey=mRNA;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);standard_name=Y39B6A.48b.1;transcript_id=NM_001269919.2
NC_003283.11	RefSeq	CDS	19185178	19185286	.	+	0	ID=cds-NP_001256848.1;Parent=rna-NM_001269919.2;Dbxref=EnsemblGenomes-Gn:WBGene00001987,EnsemblGenomes-Tr:Y39B6A.48b,GOA:D5SH01,InterPro:IPR010558,UniProtKB/TrEMBL:D5SH01,GeneID:180261,Genbank:NP_001256848.1,WormBase:WBGene00001987;Name=NP_001256848.1;Note=Product from WormBase gene class hot%3B~Confirmed by transcript evidence;gbkey=CDS;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);protein_id=NP_001256848.1;standard_name=Y39B6A.48b
NC_003283.11	RefSeq	CDS	19185594	19185697	.	+	2	ID=cds-NP_001256848.1;Parent=rna-NM_001269919.2;Dbxref=EnsemblGenomes-Gn:WBGene00001987,EnsemblGenomes-Tr:Y39B6A.48b,GOA:D5SH01,InterPro:IPR010558,UniProtKB/TrEMBL:D5SH01,GeneID:180261,Genbank:NP_001256848.1,WormBase:WBGene00001987;Name=NP_001256848.1;Note=Product from WormBase gene class hot%3B~Confirmed by transcript evidence;gbkey=CDS;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);protein_id=NP_001256848.1;standard_name=Y39B6A.48b
NC_003283.11	RefSeq	CDS	19186541	19186643	.	+	0	ID=cds-NP_001256848.1;Parent=rna-NM_001269919.2;Dbxref=EnsemblGenomes-Gn:WBGene00001987,EnsemblGenomes-Tr:Y39B6A.48b,GOA:D5SH01,InterPro:IPR010558,UniProtKB/TrEMBL:D5SH01,GeneID:180261,Genbank:NP_001256848.1,WormBase:WBGene00001987;Name=NP_001256848.1;Note=Product from WormBase gene class hot%3B~Confirmed by transcript evidence;gbkey=CDS;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);protein_id=NP_001256848.1;standard_name=Y39B6A.48b
NC_003283.11	RefSeq	CDS	19186799	19186899	.	+	2	ID=cds-NP_001256848.1;Parent=rna-NM_001269919.2;Dbxref=EnsemblGenomes-Gn:WBGene00001987,EnsemblGenomes-Tr:Y39B6A.48b,GOA:D5SH01,InterPro:IPR010558,UniProtKB/TrEMBL:D5SH01,GeneID:180261,Genbank:NP_001256848.1,WormBase:WBGene00001987;Name=NP_001256848.1;Note=Product from WormBase gene class hot%3B~Confirmed by transcript evidence;gbkey=CDS;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);protein_id=NP_001256848.1;standard_name=Y39B6A.48b
NC_003283.11	RefSeq	CDS	19187471	19187653	.	+	0	ID=cds-NP_001256848.1;Parent=rna-NM_001269919.2;Dbxref=EnsemblGenomes-Gn:WBGene00001987,EnsemblGenomes-Tr:Y39B6A.48b,GOA:D5SH01,InterPro:IPR010558,UniProtKB/TrEMBL:D5SH01,GeneID:180261,Genbank:NP_001256848.1,WormBase:WBGene00001987;Name=NP_001256848.1;Note=Product from WormBase gene class hot%3B~Confirmed by transcript evidence;gbkey=CDS;gene=hot-2;locus_tag=CELE_Y39B6A.48;product=Homolog of Odr-2 (Two);protein_id=NP_001256848.1;standard_name=Y39B6A.48b
NC_003283.11	RefSeq	gene	19189241	19190035	.	-	.	ID=gene-CELE_Y39B6A.3;Dbxref=WormBase:WBGene00012666,GeneID:180262;Name=Y39B6A.3;gbkey=Gene;gene=Y39B6A.3;gene_biotype=protein_coding;locus_tag=CELE_Y39B6A.3
NC_003283.11	RefSeq	mRNA	19189241	19190013	.	-	.	ID=rna-NM_001129566.3;Parent=gene-CELE_Y39B6A.3;Dbxref=GeneID:180262,Genbank:NM_001129566.3,WormBase:WBGene00012666;Name=NM_001129566.3;gbkey=mRNA;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;standard_name=Y39B6A.3b.1;transcript_id=NM_001129566.3
NC_003283.11	RefSeq	exon	19189900	19190013	.	-	.	ID=exon-NM_001129566.3-1;Parent=rna-NM_001129566.3;Dbxref=GeneID:180262,Genbank:NM_001129566.3,WormBase:WBGene00012666;gbkey=mRNA;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;standard_name=Y39B6A.3b.1;transcript_id=NM_001129566.3
NC_003283.11	RefSeq	exon	19189764	19189851	.	-	.	ID=exon-NM_001129566.3-2;Parent=rna-NM_001129566.3;Dbxref=GeneID:180262,Genbank:NM_001129566.3,WormBase:WBGene00012666;gbkey=mRNA;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;standard_name=Y39B6A.3b.1;transcript_id=NM_001129566.3
NC_003283.11	RefSeq	exon	19189598	19189687	.	-	.	ID=exon-NM_001129566.3-3;Parent=rna-NM_001129566.3;Dbxref=GeneID:180262,Genbank:NM_001129566.3,WormBase:WBGene00012666;gbkey=mRNA;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;standard_name=Y39B6A.3b.1;transcript_id=NM_001129566.3
NC_003283.11	RefSeq	exon	19189241	19189492	.	-	.	ID=exon-NM_001129566.3-4;Parent=rna-NM_001129566.3;Dbxref=GeneID:180262,Genbank:NM_001129566.3,WormBase:WBGene00012666;gbkey=mRNA;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;standard_name=Y39B6A.3b.1;transcript_id=NM_001129566.3
NC_003283.11	RefSeq	CDS	19189900	19189964	.	-	0	ID=cds-NP_001123038.1;Parent=rna-NM_001129566.3;Dbxref=EnsemblGenomes-Gn:WBGene00012666,EnsemblGenomes-Tr:Y39B6A.3b,GOA:A5HWB2,InterPro:IPR000361,InterPro:IPR016092,InterPro:IPR017870,InterPro:IPR035903,UniProtKB/TrEMBL:A5HWB2,GeneID:180262,Genbank:NP_001123038.1,WormBase:WBGene00012666;Name=NP_001123038.1;Note=Partially confirmed by transcript evidence;gbkey=CDS;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;protein_id=NP_001123038.1;standard_name=Y39B6A.3b
NC_003283.11	RefSeq	CDS	19189764	19189851	.	-	1	ID=cds-NP_001123038.1;Parent=rna-NM_001129566.3;Dbxref=EnsemblGenomes-Gn:WBGene00012666,EnsemblGenomes-Tr:Y39B6A.3b,GOA:A5HWB2,InterPro:IPR000361,InterPro:IPR016092,InterPro:IPR017870,InterPro:IPR035903,UniProtKB/TrEMBL:A5HWB2,GeneID:180262,Genbank:NP_001123038.1,WormBase:WBGene00012666;Name=NP_001123038.1;Note=Partially confirmed by transcript evidence;gbkey=CDS;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;protein_id=NP_001123038.1;standard_name=Y39B6A.3b
NC_003283.11	RefSeq	CDS	19189598	19189687	.	-	0	ID=cds-NP_001123038.1;Parent=rna-NM_001129566.3;Dbxref=EnsemblGenomes-Gn:WBGene00012666,EnsemblGenomes-Tr:Y39B6A.3b,GOA:A5HWB2,InterPro:IPR000361,InterPro:IPR016092,InterPro:IPR017870,InterPro:IPR035903,UniProtKB/TrEMBL:A5HWB2,GeneID:180262,Genbank:NP_001123038.1,WormBase:WBGene00012666;Name=NP_001123038.1;Note=Partially confirmed by transcript evidence;gbkey=CDS;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;protein_id=NP_001123038.1;standard_name=Y39B6A.3b
NC_003283.11	RefSeq	CDS	19189340	19189492	.	-	0	ID=cds-NP_001123038.1;Parent=rna-NM_001129566.3;Dbxref=EnsemblGenomes-Gn:WBGene00012666,EnsemblGenomes-Tr:Y39B6A.3b,GOA:A5HWB2,InterPro:IPR000361,InterPro:IPR016092,InterPro:IPR017870,InterPro:IPR035903,UniProtKB/TrEMBL:A5HWB2,GeneID:180262,Genbank:NP_001123038.1,WormBase:WBGene00012666;Name=NP_001123038.1;Note=Partially confirmed by transcript evidence;gbkey=CDS;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;protein_id=NP_001123038.1;standard_name=Y39B6A.3b
NC_003283.11	RefSeq	mRNA	19189246	19190035	.	-	.	ID=rna-NM_171606.5;Parent=gene-CELE_Y39B6A.3;Dbxref=GeneID:180262,Genbank:NM_171606.5,WormBase:WBGene00012666;Name=NM_171606.5;gbkey=mRNA;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;standard_name=Y39B6A.3a.1;transcript_id=NM_171606.5
NC_003283.11	RefSeq	exon	19189900	19190035	.	-	.	ID=exon-NM_171606.5-1;Parent=rna-NM_171606.5;Dbxref=GeneID:180262,Genbank:NM_171606.5,WormBase:WBGene00012666;gbkey=mRNA;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;standard_name=Y39B6A.3a.1;transcript_id=NM_171606.5
NC_003283.11	RefSeq	exon	19189764	19189845	.	-	.	ID=exon-NM_171606.5-2;Parent=rna-NM_171606.5;Dbxref=GeneID:180262,Genbank:NM_171606.5,WormBase:WBGene00012666;gbkey=mRNA;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;standard_name=Y39B6A.3a.1;transcript_id=NM_171606.5
NC_003283.11	RefSeq	exon	19189598	19189687	.	-	.	ID=exon-NM_171606.5-3;Parent=rna-NM_171606.5;Dbxref=GeneID:180262,Genbank:NM_171606.5,WormBase:WBGene00012666;gbkey=mRNA;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;standard_name=Y39B6A.3a.1;transcript_id=NM_171606.5
NC_003283.11	RefSeq	exon	19189246	19189492	.	-	.	ID=exon-NM_171606.5-4;Parent=rna-NM_171606.5;Dbxref=GeneID:180262,Genbank:NM_171606.5,WormBase:WBGene00012666;gbkey=mRNA;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;standard_name=Y39B6A.3a.1;transcript_id=NM_171606.5
NC_003283.11	RefSeq	CDS	19189900	19189964	.	-	0	ID=cds-NP_741696.1;Parent=rna-NM_171606.5;Dbxref=EnsemblGenomes-Gn:WBGene00012666,EnsemblGenomes-Tr:Y39B6A.3a,GOA:Q9NES9,InterPro:IPR000361,InterPro:IPR016092,InterPro:IPR017870,InterPro:IPR035903,UniProtKB/TrEMBL:Q9NES9,GeneID:180262,Genbank:NP_741696.1,WormBase:WBGene00012666;Name=NP_741696.1;Note=Partially confirmed by transcript evidence;gbkey=CDS;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;protein_id=NP_741696.1;standard_name=Y39B6A.3a
NC_003283.11	RefSeq	CDS	19189764	19189845	.	-	1	ID=cds-NP_741696.1;Parent=rna-NM_171606.5;Dbxref=EnsemblGenomes-Gn:WBGene00012666,EnsemblGenomes-Tr:Y39B6A.3a,GOA:Q9NES9,InterPro:IPR000361,InterPro:IPR016092,InterPro:IPR017870,InterPro:IPR035903,UniProtKB/TrEMBL:Q9NES9,GeneID:180262,Genbank:NP_741696.1,WormBase:WBGene00012666;Name=NP_741696.1;Note=Partially confirmed by transcript evidence;gbkey=CDS;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;protein_id=NP_741696.1;standard_name=Y39B6A.3a
NC_003283.11	RefSeq	CDS	19189598	19189687	.	-	0	ID=cds-NP_741696.1;Parent=rna-NM_171606.5;Dbxref=EnsemblGenomes-Gn:WBGene00012666,EnsemblGenomes-Tr:Y39B6A.3a,GOA:Q9NES9,InterPro:IPR000361,InterPro:IPR016092,InterPro:IPR017870,InterPro:IPR035903,UniProtKB/TrEMBL:Q9NES9,GeneID:180262,Genbank:NP_741696.1,WormBase:WBGene00012666;Name=NP_741696.1;Note=Partially confirmed by transcript evidence;gbkey=CDS;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;protein_id=NP_741696.1;standard_name=Y39B6A.3a
NC_003283.11	RefSeq	CDS	19189340	19189492	.	-	0	ID=cds-NP_741696.1;Parent=rna-NM_171606.5;Dbxref=EnsemblGenomes-Gn:WBGene00012666,EnsemblGenomes-Tr:Y39B6A.3a,GOA:Q9NES9,InterPro:IPR000361,InterPro:IPR016092,InterPro:IPR017870,InterPro:IPR035903,UniProtKB/TrEMBL:Q9NES9,GeneID:180262,Genbank:NP_741696.1,WormBase:WBGene00012666;Name=NP_741696.1;Note=Partially confirmed by transcript evidence;gbkey=CDS;gene=Y39B6A.3;locus_tag=CELE_Y39B6A.3;product=Fe-S_biosyn domain-containing protein;protein_id=NP_741696.1;standard_name=Y39B6A.3a
"""
        
    def test_readGFFEnsembl(self):
        mock_o = mock_open(read_data=self.gffEnsembl)
        
        with patch('builtins.open', mock_o):
            with open('foo') as h:
                genes = readGFF(h)
                
        self.assertEqual(2,len(genes.genes))
        self.assertTrue('WBGene00001987.1' in genes.genes)
        self.assertTrue('WBGene00012666.1' in genes.genes)
        
        genesBed = genes.getGeneContent()
        self.assertEqual(2,len(genesBed))
        exonsBed = genes.getExonContent()
        # Expected 12 exons (6+6) in total plus 1 empty line
        self.assertEqual(13,len(exonsBed.split('\n')))
        
        
    def test_readGFFRefSeq(self):
        mock_o = mock_open(read_data=self.gffRefSeq)
        
        with patch('builtins.open', mock_o):
            with open('foo') as h:
                genes = readGFF(h)
                
        self.assertEqual(2,len(genes.genes))
        self.assertTrue('gene-CELE_Y39B6A.48' in genes.genes)
        self.assertTrue('gene-CELE_Y39B6A.3' in genes.genes)
        
        genesBed = genes.getGeneContent()
        self.assertEqual(2,len(genesBed))
        exonsBed = genes.getExonContent()
        # Expected 14 exons (7+7) in total plus 1 empty line
        self.assertEqual(15,len(exonsBed.split('\n')))
    
if __name__ == "__main__":
    unittest.main()