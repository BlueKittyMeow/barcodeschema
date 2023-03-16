A tool to generate unique barcodes including a check digit. 

Barcodes are checked against a spreadsheet and, so long as they do not match a repeat, are entered into that spreadsheet. 

The schema I used breaks the barcode up into three regions of four digits each. The first two regions are set to have the first digit correspond to a schema. For the first block, first digit signifies the type of item (person, physical item, etc) and defaults to 3 for equipment. 
In the second block, the first digit is selectable from the dropdown menu. It defaults to 1. Options I used are Equipment; Media; Books; Theses; Infrastructure, but this can be changed. 
