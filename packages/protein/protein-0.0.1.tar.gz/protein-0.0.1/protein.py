#!/usr/bin/env python
import urllib.request
import xmltodict
import argparse

parser = argparse.ArgumentParser(description="Quick command line Uniprot protein search.")

parser.add_argument("protein", metavar = "p", type = str, help = "Uniprot ID for protein")
parser.add_argument("-s", "--sequence", help = "Output only the amino acid sequence", action = "store_true")
parser.add_argument("-n", "--name", help = "Output only the protein name", action = "store_true")
parser.add_argument("-f", "--function", help = "Output only the protein function", action = "store_true")

args = parser.parse_args()
id = args.protein

url = urllib.request.urlopen("https://www.uniprot.org/uniprot/" + id + ".xml")
data = url.read()

mydict = xmltodict.parse(data)
name = mydict["uniprot"]["entry"]["protein"]["recommendedName"]["fullName"]["#text"]
function = mydict["uniprot"]["entry"]["comment"][0]["text"]["#text"]
sequence = mydict["uniprot"]["entry"]["sequence"]["#text"]

check = True

if args.name:
    print(name)
    check = False
if args.function:
    print(function)
    check = False
if args.sequence:
    print(sequence)
    check = False

if check:
    print("NAME: " + name)
    print("FUNCTION: " + function)
    print("AMINO ACID SEQUENCE: " + sequence)


