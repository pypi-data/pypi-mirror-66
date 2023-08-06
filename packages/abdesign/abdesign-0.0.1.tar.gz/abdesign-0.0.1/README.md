# ABDesign

## API

The ABDesign API includes IgObject which provides different methods to annotate and analyze an Immunoglobulin sequence.

> **Note:** A local installation of ANARCI is needed for this tool. You can downlod ANARCI [here.](http://opig.stats.ox.ac.uk/webapps/newsabdab/sabpred/anarci/#download "ANARCI Download")

**Initialize IgObject( *params* )**

* seq *required*
* chain_type [ =None ]
* species [ =None ]
* humaness_score [ =None ]
* annotation [ =None ]
* regions [ =None ]


**current methods:**
* create_annotation()
* export_to_json()
* replace_cdr()