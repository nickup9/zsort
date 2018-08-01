#!/usr/bin/env python3
import zkillsort

organizationID = int(input("\nEnter the ID of the organization, must be corp or alliance \n"))
typeID = int(input("\nEnter 1 if the organization is a corp, 2 if alliance \n"))
file_name = input("\nEnter in the name of the output file, no extensions please. \n")
file_name = file_name + ".txt"

zkillsort.sort(organizationID, typeID, file_name)