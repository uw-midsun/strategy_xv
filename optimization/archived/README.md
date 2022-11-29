# Optimization
This directory contains code for race-time optimization.

New Regulations
-  FSGP 2023: https://www.americansolarchallenge.org/regulations/2023-formula-sun-grand-prix-regulations/
- ASC 2024: https://www.americansolarchallenge.org/regulations/2024-american-solar-challenge-regulations/

Optimization guides our understanding of how we should race. It should be a fairly high-level model, in that it will feed off of other models.

Open Questions / Milestones 
[Last edited: W22]
- Technical implementation of evaluating discrete (0, 1, 2, ... loops, etc.) possibilities
  - Identify what our overall evaluation table might look like
- What inputs and outputs do we want? 
  - Does this reflect models that existed in the MSXIV code? (Not that it should/has to, but it's worth referencing)
- How can we consider different-sized loops?
  - Mentioned above that we coudl have 0, 1, 2, ... loops, but really this could be (0, 1, 2, ... loops from Loop A) + (0, 1, 2, ... loops from Loop B) + (0, 1, 2, ...) loops from Loop C
- Do we want to consider our optimizations on a daily basis? Overall race? 
- Compare ASC and FSGP optimization plans


# Loops
Loops add distance to our total, increasing our score. This comes with a trade-off of power expended that we will have to evaluate (in order to still finish the race). 

Open Question / Milestones 
[Last edited: W22]
- What data does the routebook provide us on loops? (eg. location, distance, etc.)
  - Sample routebook (2021): https://www.americansolarchallenge.org/ASC/wp-content/uploads/2021/07/ASC-2021-Route-Book.pdf
- What does our model like?
  - fields of interest
  - inputs/outputs
  - passive (member variables, getters/setters) + active (mutations on itself) components
  - interactions with other models (eg. route model)
